# Azure Function App - Enrollment Deployment Pipeline

This is an Azure DevOps CI/CD pipeline for deploying a Python Azure Function application across multiple environments (dev, test, prod). The pipeline checks out code from a separate repository, runs pytest tests, and deploys to an existing Azure Function App based on user-selected environment.

## Project Structure

```
function-app-sample/
├── HttpTrigger/              # Sample HTTP trigger function
│   ├── __init__.py          # Function implementation
│   └── function.json        # Function bindings configuration
├── tests/                   # Test directory
│   ├── __init__.py         # Tests package init
│   └── test_http_trigger.py # Unit tests for HTTP trigger
├── host.json                # Function app host configuration
├── requirements.txt         # Python dependencies (includes pytest)
├── pytest.ini              # Pytest configuration
├── local.settings.json      # Local development settings
├── .funcignore             # Files to ignore during deployment
├── azure-pipelines.yml     # Azure DevOps CI/CD pipeline (multi-environment)
└── README.md               # This file
```

## Pipeline Architecture

This setup uses a **separate repository pattern with multi-environment support**:
- **Pipeline repository**: This repository (`azure-devops`) contains the pipeline YAML
- **Code repository**: `enrollment-app` contains the actual function app code in the `enrollment-function-app` folder
- **Environment Selection**: User selects deployment environment (dev/test/prod) when running the pipeline
- **Environment-Specific Connections**: Each environment uses its own Azure service connection

This is useful when you want to centralize pipeline definitions while keeping application code separate and supporting multiple deployment environments.

## Function Details

### HttpTrigger

A simple HTTP trigger function that:
- Accepts GET and POST requests
- Takes an optional `name` parameter from query string or request body
- Returns a JSON response with a greeting message

**Example Usage:**
```bash
# GET request
curl "https://your-function-app.azurewebsites.net/api/HttpTrigger?name=John"

# POST request
curl -X POST "https://your-function-app.azurewebsites.net/api/HttpTrigger" \
  -H "Content-Type: application/json" \
  -d '{"name": "John"}'
```

## Local Development

### Prerequisites
- Python 3.11 or later
- Azure Functions Core Tools
- Azure CLI (for deployment)

### Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   pytest tests/ -v
   ```

3. Run tests with coverage:
   ```bash
   pytest tests/ -v --cov=. --cov-report=html
   ```

4. Start the function locally:
   ```bash
   func start
   ```

5. Test the function:
   ```bash
   curl "http://localhost:7071/api/HttpTrigger?name=Test"
   ```

## Testing

The project includes comprehensive unit tests using pytest.

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=. --cov-report=html

# Run specific test file
pytest tests/test_http_trigger.py -v

# Run tests matching a pattern
pytest tests/ -k "test_http_trigger_with_name"
```

### Test Coverage

Tests include:
- Testing with name parameter in query string
- Testing with name parameter in request body
- Testing without name parameter (error handling)
- Testing with empty name parameter
- Testing with special characters
- Testing GET and POST methods
- Testing invalid JSON handling

View coverage report: Open `htmlcov/index.html` after running tests with coverage.

## Azure DevOps Pipeline Setup

### Prerequisites
1. An existing Azure Function App: `azfn-test` (Linux-based for Python)
2. An Azure DevOps project with two repositories:
   - `azure-devops`: Contains the pipeline YAML (this repository)
   - `enrollment-app`: Contains the function app code in `enrollment-function-app` folder
3. Azure Resource Manager service connections for each environment:
   - **Dev**: `azure-rm-connection-dev`
   - **Test**: `azure-rm-connection-test`
   - **Prod**: `azure-rm-connection-prod`

### Current Configuration

The pipeline is configured with:
- **Function App Name**: `azfn-test` (same for all environments)
- **Code Repository**: `enrollment-app`
- **Code Folder**: `enrollment-function-app`
- **Python Version**: 3.11
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
   - Create repository named `enrollment-app` in your Azure DevOps project
   - Create folder `enrollment-function-app` in the repository
   - Push the function app code (HttpTrigger, host.json, requirements.txt, tests, etc.) to the `enrollment-function-app` folder

2. **Verify Service Connections**:
   - Go to Project Settings → Service connections
   - Verify all three service connections exist:
     - `azure-rm-connection-dev`
     - `azure-rm-connection-test`
     - `azure-rm-connection-prod`
   - Ensure each has permissions to deploy to `azfn-test` in their respective Azure environments
   - If not, create new Azure Resource Manager service connections for each environment

3. **Create Azure DevOps Environments** (optional but recommended):
   - Go to Pipelines → Environments
   - Create three environments:
     - `development` (for dev deployments)
     - `testing` (for test deployments)
     - `production` (for prod deployments, can add approval gates)
   - Add approval gates to production environment for safety

4. **Create Pipeline**:
   - Go to Pipelines → New Pipeline
   - Select this repository (`azure-devops`)
   - Choose "Existing Azure Pipelines YAML file"
   - Select `function-app-sample/azure-pipelines.yml`
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

#### Build and Test Stage
1. **Checkout Code**: Checks out code from `enrollment-app` repository
2. **Set Working Directory**: Changes to `enrollment-function-app` folder
3. **Setup Python**: Installs Python 3.11
4. **Install Dependencies**: Installs requirements including pytest
5. **Run Tests**: Executes pytest with coverage reporting
   - Tests must pass for deployment to proceed
   - Publishes test results to Azure DevOps
   - Publishes code coverage report
6. **Install Deployment Dependencies**: Prepares Python packages for deployment
7. **Archive Files**: Creates deployment package from `enrollment-function-app` folder
8. **Publish Artifact**: Uploads package for deployment stage

#### Deploy Stage (Environment-Specific)
1. **Environment Selection**: Uses the environment selected by the user (dev/test/prod)
2. **Service Connection**: Uses environment-specific service connection
   - dev → `azure-rm-connection-dev`
   - test → `azure-rm-connection-test`
   - prod → `azure-rm-connection-prod`
3. **Download Artifact**: Retrieves build artifact
4. **Deploy to Azure**: Deploys to `azfn-test` function app
   - Uses environment-specific Azure DevOps environment
   - Deploys to Linux-based Function App
   - Uses automatic deployment method
   - May require approval if configured on the environment

### Pipeline Features

- **Multi-Environment Support**: Deploy to dev, test, or prod with a single click
- **Environment-Specific Service Connections**: Each environment uses its own Azure credentials
- **Automated Testing**: Tests run automatically on every build
- **Test Failure Prevention**: Deployment only proceeds if all tests pass
- **Code Coverage**: Tracks test coverage and publishes reports
- **Multi-Repository**: Separates pipeline config from application code
- **Environment Gates**: Can require approval before production deployment
- **Flexible Folder Structure**: Supports code in subdirectories (`enrollment-function-app`)

### Customization

#### Change Python Version
Update the `pythonVersion` variable in the pipeline:
```yaml
variables:
  pythonVersion: '3.11'  # Change to 3.9, 3.10, 3.11, etc.
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

#### Change Function App Names Per Environment
If you have different function app names per environment:
```yaml
${{ if eq(parameters.environment, 'dev') }}:
  functionAppName: 'azfn-enrollment-dev'
${{ if eq(parameters.environment, 'test') }}:
  functionAppName: 'azfn-enrollment-test'
${{ if eq(parameters.environment, 'prod') }}:
  functionAppName: 'azfn-enrollment-prod'
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
    - repository: functionAppCode
      name: your-repo-name  # Change repository name

variables:
  workingDirectory: '$(System.DefaultWorkingDirectory)/your-folder'  # Change folder
```

## Deployment

### Manual Deployment (using Azure CLI)
```bash
# Login to Azure
az login

# Deploy function app
func azure functionapp publish YOUR_FUNCTION_APP_NAME
```

### Pipeline Deployment

#### Automated Trigger
Push your changes to the `main` or `develop` branch in the `azure-devops` repository to trigger the pipeline automatically (defaults to dev environment).

#### Manual Run (Recommended for Environment Selection)
1. Go to Pipelines in Azure DevOps
2. Select the pipeline
3. Click "Run pipeline"
4. Select the **environment** parameter (dev, test, or prod)
5. Click "Run"

The pipeline will:
1. Checkout code from `enrollment-app` repository (`enrollment-function-app` folder)
2. Install dependencies
3. Run pytest tests (deployment stops if tests fail)
4. Build the function app
5. Create a deployment package
6. Deploy to `azfn-test` using the selected environment's service connection

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

**Note**: The pipeline is in the `azure-devops` repository, but deploys code from the `enrollment-app` repository's `enrollment-function-app` folder.

## Monitoring

After deployment, monitor your function:
- Azure Portal → Your Function App → Monitor
- Application Insights (if configured)
- Log Stream for real-time logs

## Troubleshooting

### Common Issues

1. **Tests failing in pipeline**
   - Run tests locally first: `pytest tests/ -v`
   - Check test error messages in Azure DevOps test results
   - Ensure all dependencies are in `requirements.txt`
   - Verify Python version matches (3.11)

2. **Repository checkout failing**
   - Verify `enrollment-app` repository exists
   - Check that `enrollment-function-app` folder exists in the repository
   - Ensure pipeline has permissions to access the repository
   - Verify the branch reference is correct (default: main)
   - Check that the repository name matches exactly in the pipeline YAML

3. **Dependencies not installed**
   - Ensure `requirements.txt` is present and correct
   - Check Python version compatibility
   - Verify pytest and pytest-cov are included

4. **Function not responding**
   - Check Application Insights logs
   - Verify function app settings
   - Ensure authentication level is correct

5. **Pipeline failing at deployment**
   - Verify the environment-specific service connection exists and has permissions:
     - Dev: `azure-rm-connection-dev`
     - Test: `azure-rm-connection-test`
     - Prod: `azure-rm-connection-prod`
   - Check function app name `azfn-test` is correct
   - Ensure Python version matches
   - Verify function app exists and is Linux-based
   - Check that the service connection has access to the correct Azure subscription

7. **Wrong environment being used**
   - Verify you selected the correct environment parameter when running the pipeline
   - Check the pipeline run details to see which service connection was used
   - Review the Azure DevOps environment being deployed to

8. **Working directory issues**
   - Ensure `enrollment-function-app` folder exists in the `enrollment-app` repository
   - Check that all required files (host.json, requirements.txt, etc.) are in the `enrollment-function-app` folder
   - Verify the working directory path in the pipeline YAML is correct

6. **Code coverage not showing**
   - Ensure pytest-cov is installed
   - Check coverage.xml is generated in build
   - Verify PublishCodeCoverageResults task is running

## Additional Resources

- [Azure Functions Python Developer Guide](https://docs.microsoft.com/azure/azure-functions/functions-reference-python)
- [Azure DevOps Pipeline Documentation](https://docs.microsoft.com/azure/devops/pipelines/)
- [Azure Functions Best Practices](https://docs.microsoft.com/azure/azure-functions/functions-best-practices)
