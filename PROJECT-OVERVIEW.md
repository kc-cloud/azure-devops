# Azure DevOps Deployment Pipelines - Project Overview

This repository contains Azure DevOps CI/CD pipelines for deploying Azure Function Apps and Logic Apps across multiple environments.

## Repository Structure

```
azure-devops/
├── function-app-sample/              # Azure Function App Pipeline
│   ├── azure-pipelines.yml          # Multi-environment deployment pipeline
│   ├── README.md                    # Comprehensive documentation
│   └── QUICK-REFERENCE.md           # Quick reference guide
│
├── logic-app-sample/                 # Azure Logic App Pipeline
│   ├── azure-pipelines.yml          # Multi-environment deployment pipeline
│   ├── README.md                    # Comprehensive documentation
│   └── QUICK-REFERENCE.md           # Quick reference guide
│
├── enrollment-app/               # Simulated code repository
│   ├── enrollment-function-app/     # Function app code
│   │   ├── HttpTrigger/            # Sample HTTP trigger
│   │   ├── tests/                  # Pytest tests
│   │   ├── host.json
│   │   ├── requirements.txt
│   │   └── pytest.ini
│   ├── enrollment-logic-app/        # Logic app code
│   │   ├── 001/                    # Workflow 1
│   │   ├── 002/                    # Workflow 2
│   │   ├── 003/                    # Workflow 3
│   │   ├── host.json
│   │   └── connections.json
│   └── README.md                    # Repository documentation
│
└── PROJECT-OVERVIEW.md               # This file
```

## Quick Summary

| Component | Pipeline Location | Code Location | Deploys To | Environments |
|-----------|------------------|---------------|------------|--------------|
| **Function App** | `function-app-sample/` | `enrollment-app/enrollment-function-app/` | `azfn-test` | dev, test, prod |
| **Logic App** | `logic-app-sample/` | `enrollment-app/enrollment-logic-app/` | `logic-enrollment-app` | dev, test, prod |

## Architecture Overview

### Separate Repository Pattern

This setup uses a **separate repository pattern**:
- **azure-devops** (this repo): Contains pipeline definitions
- **enrollment-app** (separate repo): Contains application code

Benefits:
- Centralized pipeline management
- Reusable pipeline templates
- Clear separation of concerns
- Easy to manage multiple applications

### Multi-Environment Support

Both pipelines support three environments with user selection:
- **dev** (default) - Development environment
- **test** - Testing environment
- **prod** - Production environment (with optional approval gates)

Each environment uses its own Azure service connection:
- `azure-rm-connection-dev`
- `azure-rm-connection-test`
- `azure-rm-connection-prod`

## Pipelines

### 1. Function App Pipeline

**Location:** `function-app-sample/azure-pipelines.yml`

**What it does:**
1. Checks out code from `enrollment-app/enrollment-function-app`
2. Installs Python dependencies
3. Runs pytest tests (deployment stops if tests fail)
4. Builds deployment package
5. Deploys to `azfn-test` using environment-specific service connection

**Key Features:**
- ✅ Automated pytest testing
- ✅ Code coverage reporting
- ✅ Test-gated deployment
- ✅ Multi-environment support
- ✅ Environment-specific service connections

**Triggers:**
- Push to `main` or `develop` branch (deploys to dev)
- Manual run with environment selection

### 2. Logic App Pipeline

**Location:** `logic-app-sample/azure-pipelines.yml`

**What it does:**
1. Checks out code from `enrollment-app/enrollment-logic-app`
2. Validates structure (host.json, connections.json, workflows)
3. Lists all workflows
4. Builds deployment package
5. Deploys to `logic-enrollment-app` using environment-specific service connection

**Key Features:**
- ✅ Structure validation
- ✅ Workflow discovery
- ✅ Multi-workflow support
- ✅ Multi-environment support
- ✅ Environment-specific service connections

**Triggers:**
- Push to `main` or `develop` branch (deploys to dev)
- Manual run with environment selection

## Service Connections

Both pipelines use environment-specific Azure Resource Manager service connections:

| Environment | Service Connection | Purpose |
|-------------|-------------------|---------|
| **dev** | `azure-rm-connection-dev` | Development deployments |
| **test** | `azure-rm-connection-test` | Testing deployments |
| **prod** | `azure-rm-connection-prod` | Production deployments (with approvals) |

**Setup Required:**
1. Create three service connections in Azure DevOps (Project Settings → Service connections)
2. Name them exactly as shown above
3. Grant appropriate Azure permissions to each

## Azure Resources

### Required Azure Resources

| Resource | Name | Type | Purpose |
|----------|------|------|---------|
| Function App | `azfn-test` | Azure Function App (Linux, Python) | Hosts enrollment function app |
| Logic App | `logic-enrollment-app` | Azure Logic App (Standard) | Hosts enrollment workflows |

**Note:** Currently configured with the same function app name for all environments. You can customize to use different names per environment.

## Azure DevOps Environments

Optional but recommended for approval gates:

| Environment Name | Used For | Approval Gate |
|-----------------|----------|---------------|
| `development` | dev deployments | No |
| `testing` | test deployments | Optional |
| `production` | prod deployments | **Recommended** |

**Setup:**
1. Go to Pipelines → Environments
2. Create the three environments
3. Add approval gates to production for safety

## Getting Started

### Prerequisites

1. **Azure DevOps Project** with this repository
2. **Azure Subscription** with resources created:
   - Azure Function App: `azfn-test`
   - Azure Logic App: `logic-enrollment-app`
3. **Service Connections** created:
   - azure-rm-connection-dev
   - azure-rm-connection-test
   - azure-rm-connection-prod

### Step 1: Create the Code Repository

The `enrollment-app` folder in this repo is a simulation. Create a real separate repository:

```bash
# In Azure DevOps, create new repository named: enrollment-app

# Clone it
git clone <enrollment-app-repo-url>
cd enrollment-app

# Copy code from this repo's enrollment-app folder
cp -r /path/to/azure-devops/enrollment-app/* .

# Commit and push
git add .
git commit -m "Initial commit: Add enrollment apps"
git push origin main
```

### Step 2: Create the Pipelines

#### Function App Pipeline

1. Go to Pipelines → New Pipeline
2. Select `azure-devops` repository
3. Choose "Existing Azure Pipelines YAML file"
4. Select `/function-app-sample/azure-pipelines.yml`
5. Save and run
6. Select `dev` environment for first test

#### Logic App Pipeline

1. Go to Pipelines → New Pipeline
2. Select `azure-devops` repository
3. Choose "Existing Azure Pipelines YAML file"
4. Select `/logic-app-sample/azure-pipelines.yml`
5. Save and run
6. Select `dev` environment for first test

### Step 3: Test Deployments

1. **Deploy Function App to dev:**
   - Run function app pipeline
   - Select `dev` environment
   - Verify tests pass
   - Check deployment succeeded

2. **Deploy Logic App to dev:**
   - Run logic app pipeline
   - Select `dev` environment
   - Verify workflows deployed
   - Check deployment succeeded

3. **Test deployed resources:**
   - Function App: `curl https://azfn-test.azurewebsites.net/api/HttpTrigger?name=Test`
   - Logic Apps: Get workflow URLs from Azure Portal

### Step 4: Set Up Production

1. **Add Approval Gates:**
   - Go to Environments → production
   - Add approvers (yourself or team leads)
   - Configure approval settings

2. **Test production deployment:**
   - Run pipeline with `prod` environment
   - Approve the deployment
   - Verify deployment succeeded

## Running Pipelines

### Manual Run (Recommended)

1. Go to Pipelines in Azure DevOps
2. Select the pipeline (Function or Logic App)
3. Click "Run pipeline"
4. **Select environment** from dropdown (dev/test/prod)
5. Click "Run"

### Automatic Trigger

- Push to `main` or `develop` branch in `azure-devops` repository
- Automatically deploys to **dev** environment
- No environment selection (always dev)

## Workflow

### Development Workflow

```
Developer
    ↓
Edits code in enrollment-app repo
    ↓
Commits and pushes to feature branch
    ↓
Creates PR to main
    ↓
PR triggers pipeline (optional)
    ↓
After merge, manually run pipeline
    ↓
Select dev environment
    ↓
Code deployed to dev
    ↓
Test in dev
    ↓
If good, run pipeline again with test environment
    ↓
Test in test environment
    ↓
If good, run pipeline with prod environment
    ↓
Approve production deployment
    ↓
Code deployed to production
```

### Environment Promotion

```
┌─────────────────┐
│  azure-devops   │  (Pipeline definitions)
│   repository    │
└────────┬────────┘
         │ checks out code from
         ↓
┌─────────────────┐
│azure-function-  │  (Application code)
│   app repo      │
└────────┬────────┘
         │ pipeline deploys to
         ↓
┌─────────────────────────────────┐
│  Azure Environments             │
│  ┌─────┐  ┌──────┐  ┌────────┐ │
│  │ dev │→ │ test │→ │  prod  │ │
│  └─────┘  └──────┘  └────────┘ │
│     ↓         ↓          ↓      │
│  azfn-test (all environments)  │
│  logic-enrollment-app (all)    │
└─────────────────────────────────┘
```

## Customization

### Use Different Resource Names Per Environment

Edit the pipeline YAML files to use environment-specific resource names:

**Function App Pipeline:**
```yaml
${{ if eq(parameters.environment, 'dev') }}:
  functionAppName: 'azfn-enrollment-dev'
${{ if eq(parameters.environment, 'test') }}:
  functionAppName: 'azfn-enrollment-test'
${{ if eq(parameters.environment, 'prod') }}:
  functionAppName: 'azfn-enrollment-prod'
```

**Logic App Pipeline:**
```yaml
${{ if eq(parameters.environment, 'dev') }}:
  logicAppName: 'logic-enrollment-dev'
${{ if eq(parameters.environment, 'test') }}:
  logicAppName: 'logic-enrollment-test'
${{ if eq(parameters.environment, 'prod') }}:
  logicAppName: 'logic-enrollment-prod'
```

### Add More Environments

Add staging, QA, or other environments:

```yaml
parameters:
  - name: environment
    values:
      - dev
      - qa        # New
      - staging   # New
      - test
      - prod

# Add service connection mapping
${{ if eq(parameters.environment, 'qa') }}:
  azureSubscription: 'azure-rm-connection-qa'
  environmentName: 'qa'
```

### Add More Applications

Create new folders in `enrollment-app` repo and new pipeline YAML files:

```
azure-devops/
├── function-app-sample/      # Existing
├── logic-app-sample/         # Existing
├── notifications-app/        # New pipeline for notifications
└── reporting-app/            # New pipeline for reporting

enrollment-app/
├── enrollment-function-app/  # Existing
├── enrollment-logic-app/     # Existing
├── notifications-app/        # New app
└── reporting-app/            # New app
```

## Monitoring

### Function App
- Azure Portal → Function App → Monitor
- Application Insights for detailed metrics
- Log Stream for real-time logs

### Logic App
- Azure Portal → Logic App → Workflows → Run History
- Application Insights for detailed metrics
- Monitor workflow execution

## Troubleshooting

### Common Issues

1. **Pipeline can't find repository**
   - Verify `enrollment-app` repository exists
   - Check pipeline has read access to repository

2. **Service connection not found**
   - Verify service connection names match exactly
   - Check service connections exist in Project Settings

3. **Tests failing (Function App)**
   - Run tests locally: `pytest tests/ -v`
   - Check test output in Azure DevOps test results

4. **Structure validation failing (Logic App)**
   - Ensure host.json and connections.json exist
   - Verify workflow folders contain workflow.json

5. **Wrong environment deployed**
   - Check which environment was selected in pipeline run
   - Review pipeline run logs

### Getting Help

- **Function App Docs:** `function-app-sample/README.md`
- **Logic App Docs:** `logic-app-sample/README.md`
- **Quick References:** See QUICK-REFERENCE.md in each folder
- **Azure Docs:** Links in individual README files

## Security Best Practices

1. **Service Connections:** Use Workload Identity Federation instead of service principals
2. **Approval Gates:** Always require approval for production deployments
3. **Secrets:** Store sensitive values in Azure Key Vault, not in code
4. **Managed Identities:** Use managed identities for Azure resource access
5. **Least Privilege:** Grant minimum required permissions to service connections
6. **Audit Logs:** Enable and monitor deployment audit logs

## Maintenance

### Regular Tasks

- **Update Dependencies:** Keep Python packages and extensions up to date
- **Review Logs:** Check Application Insights regularly
- **Test Pipelines:** Periodically test deployment to all environments
- **Update Documentation:** Keep README files current
- **Backup:** Ensure workflows and functions are in source control

### Versioning

Consider using Git tags for releases:

```bash
# Tag a release
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Reference in pipeline (optional)
ref: refs/tags/v1.0.0
```

## Additional Resources

### Documentation
- [Function App README](function-app-sample/README.md)
- [Logic App README](logic-app-sample/README.md)
- [Code Repository README](enrollment-app/README.md)

### Quick References
- [Function App Quick Reference](function-app-sample/QUICK-REFERENCE.md)
- [Logic App Quick Reference](logic-app-sample/QUICK-REFERENCE.md)

### External Links
- [Azure Functions Documentation](https://docs.microsoft.com/azure/azure-functions/)
- [Azure Logic Apps Documentation](https://docs.microsoft.com/azure/logic-apps/)
- [Azure DevOps Pipelines Documentation](https://docs.microsoft.com/azure/devops/pipelines/)

## Support

For issues or questions:
1. Check the relevant README and QUICK-REFERENCE files
2. Review pipeline logs in Azure DevOps
3. Check Azure resource logs in Azure Portal
4. Consult Azure and Azure DevOps documentation

---

**Version:** 1.0
**Last Updated:** 2025-11-20
**Maintained By:** DevOps Team
