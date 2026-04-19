# ADO Agents on Kubernetes

Self-hosted Azure DevOps agents running as a fixed-size Kubernetes Deployment. Each pod stays registered in the agent pool and continuously picks up queued pipeline jobs. The replica count matches your parallel job license.

## Architecture

```
Azure DevOps job queue
        │
        │  routes to available agent
        ▼
  Deployment  (12 replicas = 12 licensed parallel jobs)
  ┌──────────────────────────────┐
  │  Pod 1  — ado-agent-xxxxx   │  ── idle or running a job
  │  Pod 2  — ado-agent-yyyyy   │  ── idle or running a job
  │  ...                        │
  │  Pod 12 — ado-agent-zzzzz   │  ── idle or running a job
  └──────────────────────────────┘
        │
        └─ each pod registers once on startup,
           runs jobs continuously, deregisters on shutdown
```

## Prerequisites

| Tool | Minimum version |
|------|----------------|
| Kubernetes | 1.27+ |
| Docker | any (to build the image) |
| kubectl | any |

No KEDA or other controllers needed.

## File layout

```
ado-agents-on-k8s/
├── docker/
│   ├── Dockerfile        — Ubuntu 22.04 image (agent + Docker CLI + kubectl)
│   └── entrypoint.sh     — Registers on startup, runs jobs, deregisters on shutdown
└── k8s/
    ├── namespace.yaml
    ├── serviceaccount.yaml
    ├── secret.yaml        — PAT + org URL (fill in before applying)
    ├── configmap.yaml     — Pool name
    ├── deployment.yaml    — Fixed 12-replica agent pool
    └── kustomization.yaml
```

## Step 1 — Build and push the agent image

```bash
docker build -t <YOUR_REGISTRY>/ado-agent:latest docker/
docker push <YOUR_REGISTRY>/ado-agent:latest
```

Replace `<YOUR_REGISTRY>` with your container registry (e.g. `myacr.azurecr.io`).

## Step 2 — Create the ADO agent pool

1. In Azure DevOps go to **Organization Settings → Agent pools → Add pool**
2. Choose **Self-hosted**, name it (e.g. `k8s-pool`)
3. Note the pool name — you'll use it in the next step

## Step 3 — Create a Personal Access Token (PAT)

1. In Azure DevOps go to **User Settings → Personal access tokens → New token**
2. Set scope: **Agent Pools → Read & Manage**
3. Copy the token — it is shown only once

## Step 4 — Fill in your values

### secret.yaml

Use `kubectl` to generate the secret (handles base64 encoding for you):

```bash
kubectl create secret generic ado-agent-secret \
  --namespace ado-agents \
  --from-literal=AZP_URL="https://dev.azure.com/YOUR_ORG" \
  --from-literal=AZP_TOKEN="YOUR_PAT_TOKEN" \
  --dry-run=client -o yaml > k8s/secret.yaml
```

### configmap.yaml

Set `AZP_POOL` to the pool name from Step 2.

### deployment.yaml

Update these two fields:

| Field | Example |
|-------|---------|
| `image` | `myacr.azurecr.io/ado-agent:latest` |
| `replicas` | `12` (or however many parallel jobs your license allows) |

## Step 5 — Apply the manifests

```bash
kubectl apply -k ado-agents-on-k8s/k8s/
```

Verify all pods come up:

```bash
kubectl get pods -n ado-agents
# All 12 pods should reach Running state within ~60s
```

Check that agents appear in your ADO pool:

**Azure DevOps → Organization Settings → Agent pools → k8s-pool → Agents**

You should see 12 agents with status **Online**.

## Updating the agent image

A rolling update keeps agents available during the rollout. `maxUnavailable: 0` in the Deployment ensures the pool never drops below 12 running agents.

```bash
docker build -t <YOUR_REGISTRY>/ado-agent:latest docker/
docker push <YOUR_REGISTRY>/ado-agent:latest
kubectl rollout restart deployment/ado-agent -n ado-agents
kubectl rollout status  deployment/ado-agent -n ado-agents
```

## Tuning

| Parameter | File | Default | What it controls |
|-----------|------|---------|-----------------|
| `replicas` | deployment.yaml | 12 | Number of always-on agents |
| `terminationGracePeriodSeconds` | deployment.yaml | 300s | Time a pod waits for a running job to finish before shutdown |
| `AZP_POOL` | configmap.yaml | Default | Agent pool name |
| CPU / memory requests | deployment.yaml | 500m / 512Mi | Per-pod resource floor |
| CPU / memory limits | deployment.yaml | 2 / 2Gi | Per-pod resource ceiling |

## Removing Docker socket access

The pod spec mounts `/var/run/docker.sock` so pipelines can run `docker build`. If your pipelines don't need Docker, remove the `volumeMounts` and `volumes` blocks from `deployment.yaml`.

## Troubleshooting

**Pods are Running but agents show Offline in ADO**
- Check logs: `kubectl logs -n ado-agents <pod-name>`
- Verify the PAT has not expired and has `Agent Pools: Read & Manage` scope
- Confirm `AZP_URL` has no trailing slash

**Agents register but jobs never route to them**
- Confirm the pipeline's `pool.name` matches `AZP_POOL` in the ConfigMap exactly
- Check that the pool is not set to **Grant access permission to all pipelines: off** without an explicit authorization

**Pod restarts mid-job**
- The pod's `terminationGracePeriodSeconds` (default 300s) gives in-flight jobs time to finish
- Increase this value if your jobs regularly exceed 5 minutes
- Kubernetes will send SIGTERM first; the entrypoint's `trap` catches it and deregisters cleanly
