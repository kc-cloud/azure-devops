# Azure Logic App - Enrollment Deployment Pipeline

This is an Azure DevOps CI/CD pipeline for deploying Azure Logic App (Standard) workflows across multiple environments (dev, test, prod). The pipeline checks out code from a separate repository and deploys to an existing Azure Logic App based on user-selected environment.

## Project Structure

```
enrollment-logic-app/
├── 001/                        # Workflow 1: Student Enrollment Initiation
│   └── workflow.json          # Workflow definition
├── 002/                        # Workflow 2: Enrollment Verification
│   └── workflow.json          # Workflow definition
├── 003/                        # Workflow 3: Enrollment Notification
│   └── workflow.json          # Workflow definition
├── host.json                   # Logic App host configuration
├── connections.json            # API connections configuration
├── local.settings.json         # Local development settings
└── .logicappignore            # Files to ignore during deployment
```

## Pipeline Architecture

This setup uses a **separate repository pattern with multi-environment support**:
- **Pipeline repository**: This repository (`azure-devops`) contains the pipeline YAML in `logic-app-sample` folder
- **Code repository**: `enrollment-app` contains the actual logic app code in the `enrollment-logic-app` folder
- **Environment Selection**: User selects deployment environment (dev/test/prod) when running the pipeline
- **Environment-Specific Connections**: Each environment uses its own Azure service connection

This is useful when you want to centralize pipeline definitions while keeping application code separate and supporting multiple deployment environments.

## Workflow Details

### Workflow 001 - Student Enrollment Initiation
- **Trigger**: HTTP Request
- **Purpose**: Initiates student enrollment process
- **Input**: studentId, courseName
- **Output**: Enrollment confirmation with timestamp

### Workflow 002 - Enrollment Verification
- **Trigger**: HTTP Request
- **Purpose**: Verifies enrollment details
- **Input**: studentId, enrollmentId
- **Output**: Verification status and data

### Workflow 003 - Enrollment Notification
- **Trigger**: HTTP Request
- **Purpose**: Sends enrollment confirmation notifications
- **Input**: studentId, email, enrollmentId
- **Output**: Notification confirmation

## Local Development

### Prerequisites
- Visual Studio Code
- Azure Logic Apps (Standard) extension
- Azurite (for local storage emulation)
- Node.js 14.x or later

### Setup
1. Open the `enrollment-logic-app` folder in VS Code

2. Install Azure Logic Apps extension

3. Start Azurite for local storage:
   ```bash
   azurite --silent --location ./azurite --debug ./azurite/debug.log
   ```

4. Configure `local.settings.json` with your Azure subscription details

5. Press F5 to run locally

6. Test workflows using the provided callback URLs

## Azure DevOps Pipeline Setup

### Prerequisites
1. An existing Azure Logic App (Standard): `logic-enrollment-app`
2. An Azure DevOps project with the repository:
   - `enrollment-app`: Contains the logic app code in `enrollment-logic-app` folder
3. Azure Resource Manager service connections for each environment:
   - **Dev**: `azure-rm-connection-dev`
   - **Test**: `azure-rm-connection-test`
   - **Prod**: `azure-rm-connection-prod`

### Current Configuration

The pipeline is configured with:
- **Logic App Name**: `logic-enrollment-app` (same for all environments)
- **Code Repository**: `enrollment-app`
- **Code Folder**: `enrollment-logic-app`
- **Supported Environments**: dev, test, prod
- **Default Environment**: dev

### Environment-Specific Service Connections

| Environment | Service Connection | Azure DevOps Environment |
|-------------|-------------------|--------------------------|
| dev | azure-rm-connection-dev | development |
| test | azure-rm-connection-test | testing |
| prod | azure-rm-connection-prod | production |

### Setup Steps

1. **Ensure Code Repository Exists**:
   - Create or use existing repository named `enrollment-app` in your Azure DevOps project
   - Ensure folder `enrollment-logic-app` exists in the repository
   - Push the logic app code (workflows, host.json, connections.json, etc.) to the `enrollment-logic-app` folder

2. **Verify Service Connections**:
   - Go to Project Settings → Service connections
   - Verify all three service connections exist:
     - `azure-rm-connection-dev`
     - `azure-rm-connection-test`
     - `azure-rm-connection-prod`
   - Ensure each has permissions to deploy to `logic-enrollment-app` in their respective Azure environments

3. **Create Azure DevOps Environments** (optional but recommended):
   - Go to Pipelines → Environments
   - Create three environments:
     - `development` (for dev deployments)
     - `testing` (for test deployments)
     - `production` (for prod deployments, can add approval gates)
   - Add approval gates to production environment for safety

4. **Create Logic App in Azure** (if not exists):
   ```bash
   # Using Azure CLI
   az logicapp create \
     --resource-group <resource-group> \
     --name logic-enrollment-app \
     --storage-account <storage-account> \
     --plan <app-service-plan>
   ```

5. **Create Pipeline**:
   - Go to Pipelines → New Pipeline
   - Select this repository (`azure-devops`)
   - Choose "Existing Azure Pipelines YAML file"
   - Select `logic-app-sample/azure-pipelines.yml`
   - Save

### Running the Pipeline

When you run the pipeline, you'll be prompted to select the deployment environment:

1. Click "Run pipeline"
2. Select the **Deployment Environment** parameter:
   - `dev` (default) - Deploys using azure-rm-connection-dev
   - `test` - Deploys using azure-rm-connection-test
   - `prod` - Deploys using azure-rm-connection-prod
3. Click "Run"

The pipeline will automatically use the correct service connection based on your selection.

### Pipeline Stages

#### Build and Package Stage
1. **Checkout Code**: Checks out code from `enrollment-app` repository
2. **Set Working Directory**: Changes to `enrollment-logic-app` folder
3. **Validate Structure**: Validates that host.json, connections.json exist
4. **Count Workflows**: Lists all workflows found
5. **List Contents**: Shows all files to be packaged
6. **Archive Files**: Creates deployment package from `enrollment-logic-app` folder
7. **Publish Artifact**: Uploads package for deployment stage

#### Deploy Stage (Environment-Specific)
1. **Environment Selection**: Uses the environment selected by the user (dev/test/prod)
2. **Service Connection**: Uses environment-specific service connection
   - dev → `azure-rm-connection-dev`
   - test → `azure-rm-connection-test`
   - prod → `azure-rm-connection-prod`
3. **Download Artifact**: Retrieves build artifact
4. **Deploy to Azure**: Deploys to `logic-enrollment-app`
   - Uses environment-specific Azure DevOps environment
   - Uses ZIP deployment method
   - May require approval if configured on the environment

### Pipeline Features

- **Multi-Environment Support**: Deploy to dev, test, or prod with a single click
- **Environment-Specific Service Connections**: Each environment uses its own Azure credentials
- **Structure Validation**: Validates logic app structure before deployment
- **Workflow Discovery**: Automatically detects and lists all workflows
- **Multi-Repository**: Separates pipeline config from application code
- **Environment Gates**: Can require approval before production deployment
- **Flexible Folder Structure**: Supports code in subdirectories (`enrollment-logic-app`)

### Customization

#### Change Logic App Name
Update the `logicAppName` variable in the pipeline:
```yaml
variables:
  logicAppName: 'your-logic-app-name'
```

#### Add More Environments
To add new environments (e.g., staging, qa):
1. Add to the parameters section:
   ```yaml
   parameters:
     - name: environment
       values:
         - dev
         - test
         - staging  # New environment
         - prod
   ```

2. Add service connection mapping:
   ```yaml
   ${{ if eq(parameters.environment, 'staging') }}:
     azureSubscription: 'azure-rm-connection-staging'
     environmentName: 'staging'
   ```

3. Create the corresponding service connection in Azure DevOps

#### Use Different Logic App Names Per Environment
If you have different logic app names per environment:
```yaml
${{ if eq(parameters.environment, 'dev') }}:
  logicAppName: 'logic-enrollment-dev'
${{ if eq(parameters.environment, 'test') }}:
  logicAppName: 'logic-enrollment-test'
${{ if eq(parameters.environment, 'prod') }}:
  logicAppName: 'logic-enrollment-prod'
```

#### Add Environment-Specific Variables
Use variable groups for environment-specific configuration:
```yaml
variables:
  ${{ if eq(parameters.environment, 'prod') }}:
    - group: 'production-variables'
  ${{ if eq(parameters.environment, 'dev') }}:
    - group: 'development-variables'
```

#### Change Code Repository or Folder
Update the repository reference and working directory:
```yaml
resources:
  repositories:
    - repository: logicAppCode
      name: your-repo-name  # Change repository name

variables:
  workingDirectory: '$(System.DefaultWorkingDirectory)/your-folder'  # Change folder
```

## Deployment

### Manual Deployment (using Azure CLI)
```bash
# Login to Azure
az login

# Deploy logic app
az logicapp deployment source config-zip \
  --resource-group <resource-group> \
  --name logic-enrollment-app \
  --src <path-to-zip-file>
```

### Pipeline Deployment

#### Automated Trigger
Push your changes to the `main` or `develop` branch in the `azure-devops` repository to trigger the pipeline automatically (defaults to dev environment).

#### Manual Run (Recommended for Environment Selection)
1. Go to Pipelines in Azure DevOps
2. Select the logic app pipeline
3. Click "Run pipeline"
4. Select the **environment** parameter (dev, test, or prod)
5. Click "Run"

The pipeline will:
1. Checkout code from `enrollment-app` repository (`enrollment-logic-app` folder)
2. Validate logic app structure
3. List all workflows
4. Create a deployment package
5. Deploy to `logic-enrollment-app` using the selected environment's service connection

#### Environment-Based Deployment Flow

```
┌─────────────┐
│ Select Env  │
│ dev/test/prod│
└──────┬──────┘
       │
       ├─ dev  → azure-rm-connection-dev  → development environment
       ├─ test → azure-rm-connection-test → testing environment
       └─ prod → azure-rm-connection-prod → production environment
                                             (may require approval)
```

**Note**: The pipeline is in the `azure-devops` repository, but deploys code from the `enrollment-app` repository's `enrollment-logic-app` folder.

## Monitoring

After deployment, monitor your logic app:
- Azure Portal → Your Logic App → Workflows
- Run History for each workflow
- Application Insights (if configured)
- Log Stream for real-time logs

### Testing Workflows

After deployment, get the callback URLs for each workflow:
```bash
# Get workflow callback URL
az rest --method post \
  --uri "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Web/sites/logic-enrollment-app/hostruntime/runtime/webhooks/workflow/api/management/workflows/<workflow-name>/triggers/manual/listCallbackUrl?api-version=2020-05-01-preview"
```

Or get them from Azure Portal:
1. Navigate to your Logic App
2. Select a workflow (001, 002, or 003)
3. Click "Overview"
4. Copy the "Workflow URL"

### Sample Test Request

```bash
# Test Workflow 001
curl -X POST "https://logic-enrollment-app.azurewebsites.net:443/api/001/triggers/manual/invoke?..." \
  -H "Content-Type: application/json" \
  -d '{
    "studentId": "S12345",
    "courseName": "Introduction to Computer Science"
  }'
```

## Troubleshooting

### Common Issues

1. **Structure validation failing**
   - Ensure `host.json` exists in the root of `enrollment-logic-app` folder
   - Ensure `connections.json` exists in the root of `enrollment-logic-app` folder
   - Verify workflow folders contain `workflow.json` files

2. **No workflows found**
   - Check that workflow folders (001, 002, 003) exist
   - Verify each folder contains a `workflow.json` file
   - Ensure the folder structure is correct (workflows in subdirectories)

3. **Repository checkout failing**
   - Verify `enrollment-app` repository exists
   - Check that `enrollment-logic-app` folder exists in the repository
   - Ensure pipeline has permissions to access the repository
   - Verify the branch reference is correct (default: main)

4. **Logic App not responding after deployment**
   - Check Azure Portal → Logic App → Configuration
   - Verify Application Settings are correct
   - Check that workflows are enabled
   - Review run history for errors

5. **Pipeline failing at deployment**
   - Verify the environment-specific service connection exists and has permissions:
     - Dev: `azure-rm-connection-dev`
     - Test: `azure-rm-connection-test`
     - Prod: `azure-rm-connection-prod`
   - Check logic app name `logic-enrollment-app` is correct
   - Verify logic app exists in Azure
   - Check that the service connection has access to the correct Azure subscription

6. **Wrong environment being used**
   - Verify you selected the correct environment parameter when running the pipeline
   - Check the pipeline run details to see which service connection was used
   - Review the Azure DevOps environment being deployed to

7. **Working directory issues**
   - Ensure `enrollment-logic-app` folder exists in the `enrollment-app` repository
   - Check that all required files (host.json, connections.json, workflows) are in the `enrollment-logic-app` folder
   - Verify the working directory path in the pipeline YAML is correct

8. **Workflow not triggering**
   - Check that the workflow is enabled in Azure Portal
   - Verify the callback URL is correct
   - Check Application Insights for errors
   - Review the workflow run history

## Adding New Workflows

To add a new workflow:

1. **Create a new folder** in `enrollment-logic-app`:
   ```bash
   mkdir enrollment-logic-app/004
   ```

2. **Create workflow.json** in the new folder:
   ```json
   {
     "definition": {
       "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
       "actions": {
         "Response": {
           "type": "Response",
           "kind": "http",
           "inputs": {
             "statusCode": 200,
             "body": {
               "message": "Workflow 004"
             }
           }
         }
       },
       "triggers": {
         "manual": {
           "type": "Request",
           "kind": "Http"
         }
       },
       "contentVersion": "1.0.0.0",
       "outputs": {}
     },
     "kind": "Stateful"
   }
   ```

3. **Commit and push** the changes

4. **Run the pipeline** to deploy the new workflow

## Best Practices

1. **Use Approval Gates**: Configure approval gates for production environment deployments
2. **Version Control**: Keep all workflow definitions in version control
3. **Naming Convention**: Use clear, numbered folder names for workflows (001, 002, etc.)
4. **Testing**: Test workflows in dev environment before promoting to test/prod
5. **Monitoring**: Set up Application Insights for production monitoring
6. **Connections**: Manage API connections separately using `connections.json`
7. **Documentation**: Document each workflow's purpose and inputs/outputs
8. **Error Handling**: Implement proper error handling in workflows
9. **Retry Policies**: Configure appropriate retry policies for actions
10. **Security**: Use managed identities where possible instead of connection strings

## Additional Resources

- [Azure Logic Apps Standard Documentation](https://docs.microsoft.com/azure/logic-apps/logic-apps-overview)
- [Logic Apps Workflow Definition Language](https://docs.microsoft.com/azure/logic-apps/logic-apps-workflow-definition-language)
- [Azure DevOps Pipeline Documentation](https://docs.microsoft.com/azure/devops/pipelines/)
- [Logic Apps Best Practices](https://docs.microsoft.com/azure/logic-apps/logic-apps-best-practices-guide)
- [Logic Apps Monitoring](https://docs.microsoft.com/azure/logic-apps/monitor-logic-apps)
