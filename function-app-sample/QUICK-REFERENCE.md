# Quick Reference - Enrollment Function App Pipeline

## Pipeline Configuration Summary

### Multi-Environment Setup

| Component | Value |
|-----------|-------|
| **Pipeline Repository** | `azure-devops` |
| **Code Repository** | `enrollment-app` |
| **Code Folder** | `enrollment-function-app` |
| **Function App Name** | `azfn-test` (all environments) |
| **Python Version** | 3.11 |

### Environments & Service Connections

| Environment | Service Connection | Azure DevOps Env | Default |
|-------------|-------------------|------------------|---------|
| dev | azure-rm-connection-dev | development | ✓ |
| test | azure-rm-connection-test | testing | |
| prod | azure-rm-connection-prod | production | |

## How to Run the Pipeline

### Option 1: Manual Run (Recommended)
1. Navigate to Pipelines in Azure DevOps
2. Select the enrollment function app pipeline
3. Click "Run pipeline"
4. Select environment from dropdown:
   - `dev` (default)
   - `test`
   - `prod`
5. Click "Run"

### Option 2: Automatic Trigger
- Push to `main` or `develop` branch in `azure-devops` repository
- Automatically deploys to **dev** environment

## Repository Structure Required

```
enrollment-app/
└── enrollment-function-app/
    ├── HttpTrigger/
    │   ├── __init__.py
    │   └── function.json
    ├── tests/
    │   ├── __init__.py
    │   └── test_http_trigger.py
    ├── host.json
    ├── requirements.txt
    ├── pytest.ini
    ├── local.settings.json
    └── .funcignore
```

## Pipeline Flow

```
User Selects Environment (dev/test/prod)
    ↓
Checkout enrollment-app repo
    ↓
Navigate to enrollment-function-app folder
    ↓
Install dependencies
    ↓
Run pytest tests ← [GATE: Must pass to continue]
    ↓
Publish test results & coverage
    ↓
Build deployment package
    ↓
Deploy to azfn-test using environment-specific service connection
    ↓
Complete (may require approval for prod)
```

## Pre-Deployment Checklist

- [ ] `enrollment-app` repository exists
- [ ] `enrollment-function-app` folder exists in the repository
- [ ] Function app code is in `enrollment-function-app` folder
- [ ] All three service connections exist:
  - [ ] azure-rm-connection-dev
  - [ ] azure-rm-connection-test
  - [ ] azure-rm-connection-prod
- [ ] Service connections have permissions to deploy to `azfn-test`
- [ ] Azure DevOps environments created (optional):
  - [ ] development
  - [ ] testing
  - [ ] production (with approval gate recommended)
- [ ] Pipeline created from `function-app-sample/azure-pipelines.yml`

## Common Commands

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=. --cov-report=html

# Start function locally
func start
```

### Verify Service Connections
```bash
# In Azure DevOps
Project Settings → Service connections

# Verify each connection:
1. azure-rm-connection-dev
2. azure-rm-connection-test
3. azure-rm-connection-prod
```

## Troubleshooting Quick Tips

| Issue | Quick Fix |
|-------|-----------|
| Tests failing | Run `pytest tests/ -v` locally first |
| Checkout fails | Verify `enrollment-app` repo and `enrollment-function-app` folder exist |
| Wrong environment | Check which environment parameter was selected in pipeline run |
| Service connection error | Verify correct service connection exists and has permissions |
| Working directory error | Ensure code is in `enrollment-function-app` folder, not root |

## Key Features

✓ Multi-environment deployment (dev/test/prod)
✓ Environment-specific service connections
✓ Automated testing with pytest
✓ Code coverage reporting
✓ Test-gated deployment (tests must pass)
✓ Support for environment approval gates
✓ Separate pipeline and code repositories
✓ Subdirectory support for code organization

## Next Steps After Setup

1. **First Deployment**: Run pipeline manually, select `dev` environment
2. **Verify Deployment**: Check Azure Function App portal
3. **Test Function**: Use the function URL to test
4. **Set Up Approvals**: Add approval gates to production environment
5. **Monitor**: Set up Application Insights for monitoring
