#!/bin/bash
set -e

# Required env vars (injected via Secret/ConfigMap):
#   AZP_URL        - https://dev.azure.com/<your-org>
#   AZP_TOKEN      - Personal Access Token
#   AZP_POOL       - Agent pool name (default: Default)
#   AZP_AGENT_NAME - Agent name (default: hostname)

AZP_POOL="${AZP_POOL:-Default}"
AZP_AGENT_NAME="${AZP_AGENT_NAME:-$(hostname)}"

if [[ -z "$AZP_URL" ]]; then
  echo "ERROR: AZP_URL is not set" >&2
  exit 1
fi

if [[ -z "$AZP_TOKEN" ]]; then
  echo "ERROR: AZP_TOKEN is not set" >&2
  exit 1
fi

cleanup() {
  echo "Deregistering agent..."
  ./config.sh remove --unattended --auth pat --token "$AZP_TOKEN" || true
}
trap cleanup EXIT SIGTERM SIGINT

echo "Configuring agent: $AZP_AGENT_NAME in pool: $AZP_POOL"

./config.sh \
  --unattended \
  --url "$AZP_URL" \
  --auth pat \
  --token "$AZP_TOKEN" \
  --pool "$AZP_POOL" \
  --agent "$AZP_AGENT_NAME" \
  --replace \
  --acceptTeeEula

echo "Starting agent..."
./run.sh
