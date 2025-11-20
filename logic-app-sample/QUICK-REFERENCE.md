# Quick Reference - Enrollment Logic App Pipeline

## Pipeline Configuration Summary

### Multi-Environment Setup

| Component | Value |
|-----------|-------|
| **Pipeline Repository** | `azure-devops` |
| **Code Repository** | `enrollment-app` |
| **Code Folder** | `enrollment-logic-app` |
| **Logic App Name** | `logic-enrollment-app` (all environments) |
| **Workflows** | 001, 002, 003 |

### Environments & Service Connections

| Environment | Service Connection | Azure DevOps Env | Default |
|-------------|-------------------|------------------|---------|
| dev | azure-rm-connection-dev | development | ✓ |
| test | azure-rm-connection-test | testing | |
| prod | azure-rm-connection-prod | production | |

## How to Run the Pipeline

### Option 1: Manual Run (Recommended)
1. Navigate to Pipelines in Azure DevOps
2. Select the enrollment logic app pipeline
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
└── enrollment-logic-app/
    ├── 001/
    │   └── workflow.json
    ├── 002/
    │   └── workflow.json
    ├── 003/
    │   └── workflow.json
    ├── host.json
    ├── connections.json
    ├── local.settings.json
    └── .logicappignore
```

## Workflow Summary

| ID | Name | Purpose | Inputs |
|----|------|---------|--------|
| 001 | Enrollment Initiation | Start enrollment process | studentId, courseName |
| 002 | Enrollment Verification | Verify enrollment | studentId, enrollmentId |
| 003 | Enrollment Notification | Send notifications | studentId, email, enrollmentId |

## Pipeline Flow

```
User Selects Environment (dev/test/prod)
    ↓
Checkout enrollment-app repo
    ↓
Navigate to enrollment-logic-app folder
    ↓
Validate structure (host.json, connections.json)
    ↓
List and count workflows
    ↓
Build deployment package (ZIP)
    ↓
Deploy to logic-enrollment-app using environment-specific service connection
    ↓
Complete (may require approval for prod)
```

## Pre-Deployment Checklist

- [ ] `enrollment-app` repository exists
- [ ] `enrollment-logic-app` folder exists in the repository
- [ ] Logic app code is in `enrollment-logic-app` folder
- [ ] All workflow folders exist (001, 002, 003)
- [ ] Each workflow has `workflow.json` file
- [ ] `host.json` exists in root of enrollment-logic-app
- [ ] `connections.json` exists in root of enrollment-logic-app
- [ ] All three service connections exist:
  - [ ] azure-rm-connection-dev
  - [ ] azure-rm-connection-test
  - [ ] azure-rm-connection-prod
- [ ] Service connections have permissions to deploy to `logic-enrollment-app`
- [ ] Azure Logic App exists in Azure
- [ ] Azure DevOps environments created (optional):
  - [ ] development
  - [ ] testing
  - [ ] production (with approval gate recommended)
- [ ] Pipeline created from `logic-app-sample/azure-pipelines.yml`

## Common Commands

### Local Development
```bash
# Start Azurite for local storage
azurite --silent --location ./azurite

# Open in VS Code with Logic Apps extension
code enrollment-logic-app/

# Press F5 to run locally
```

### Get Workflow URLs
```bash
# After deployment, get workflow callback URL from Azure Portal:
# Logic App → Workflows → Select workflow → Overview → Workflow URL
```

### Test Workflows
```bash
# Test Workflow 001
curl -X POST "<workflow-url>" \
  -H "Content-Type: application/json" \
  -d '{"studentId": "S12345", "courseName": "CS101"}'

# Test Workflow 002
curl -X POST "<workflow-url>" \
  -H "Content-Type: application/json" \
  -d '{"studentId": "S12345", "enrollmentId": "E67890"}'

# Test Workflow 003
curl -X POST "<workflow-url>" \
  -H "Content-Type: application/json" \
  -d '{"studentId": "S12345", "email": "student@example.com", "enrollmentId": "E67890"}'
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
| Structure validation fails | Ensure host.json and connections.json exist in enrollment-logic-app root |
| No workflows found | Check that folders 001, 002, 003 contain workflow.json files |
| Checkout fails | Verify `enrollment-app` repo and `enrollment-logic-app` folder exist |
| Wrong environment | Check which environment parameter was selected in pipeline run |
| Service connection error | Verify correct service connection exists and has permissions |
| Working directory error | Ensure code is in `enrollment-logic-app` folder, not root |
| Workflow not triggering | Check workflow is enabled in Azure Portal and get correct callback URL |

## Key Features

✓ Multi-environment deployment (dev/test/prod)
✓ Environment-specific service connections
✓ Automated structure validation
✓ Workflow discovery and listing
✓ Support for environment approval gates
✓ Separate pipeline and code repositories
✓ Subdirectory support for code organization
✓ Multiple workflows in single logic app

## Adding New Workflows

1. Create new folder: `enrollment-logic-app/004`
2. Add `workflow.json` in the folder
3. Commit and push changes
4. Run pipeline - new workflow will be automatically deployed

## Next Steps After Setup

1. **First Deployment**: Run pipeline manually, select `dev` environment
2. **Verify Deployment**: Check Azure Logic App portal → Workflows
3. **Get Workflow URLs**: Navigate to each workflow and copy callback URL
4. **Test Workflows**: Use curl or Postman to test each workflow
5. **Set Up Approvals**: Add approval gates to production environment
6. **Monitor**: Set up Application Insights for monitoring
7. **Document**: Update workflow documentation as you add new workflows

## Monitoring & Logs

```bash
# View in Azure Portal
Logic App → Workflows → Select workflow → Run history

# Check Application Insights
Logic App → Application Insights → Logs

# Stream logs
Logic App → Log stream
```

## Best Practices

✓ Test in dev before promoting to test/prod
✓ Use numbered folders for workflows (001, 002, etc.)
✓ Document each workflow's purpose
✓ Configure approval gates for production
✓ Monitor workflows using Application Insights
✓ Use managed identities for connections
✓ Keep connections.json updated
✓ Version control all workflow definitions
