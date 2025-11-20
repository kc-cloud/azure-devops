# Enrollment App Repository (Simulated)

This folder simulates the `enrollment-app` repository that contains the actual application code for both Azure Functions and Logic Apps.

## Purpose

This folder is included in the `azure-devops` repository to:
1. **Demonstrate the repository structure** that the pipelines expect
2. **Provide sample code** for testing pipelines locally
3. **Serve as a template** for creating the actual `enrollment-app` repository

## Important Note

In a real deployment scenario, this code should be in a **separate repository** named `enrollment-app` in your Azure DevOps project. The pipelines in this repository (`azure-devops`) will check out code from that separate repository.

## Repository Structure

```
enrollment-app/
├── enrollment-function-app/          # Azure Function App code
│   ├── HttpTrigger/                  # Sample HTTP trigger function
│   │   ├── __init__.py
│   │   └── function.json
│   ├── tests/                        # Unit tests
│   │   ├── __init__.py
│   │   └── test_http_trigger.py
│   ├── host.json
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── local.settings.json
│   └── .funcignore
│
├── enrollment-logic-app/             # Azure Logic App code
│   ├── 001/                          # Workflow 1: Enrollment Initiation
│   │   └── workflow.json
│   ├── 002/                          # Workflow 2: Enrollment Verification
│   │   └── workflow.json
│   ├── 003/                          # Workflow 3: Enrollment Notification
│   │   └── workflow.json
│   ├── host.json
│   ├── connections.json
│   ├── local.settings.json
│   └── .logicappignore
│
└── README.md                         # This file
```

## Folders Explained

### enrollment-function-app/
Contains Azure Function App code deployed by the pipeline in `function-app-sample/azure-pipelines.yml`

**Key files:**
- `HttpTrigger/__init__.py` - Sample Python HTTP trigger function
- `tests/` - Pytest unit tests (run before deployment)
- `host.json` - Function app configuration
- `requirements.txt` - Python dependencies

**Deployed to:** `azfn-test` (Azure Function App)

### enrollment-logic-app/
Contains Azure Logic App (Standard) workflows deployed by the pipeline in `logic-app-sample/azure-pipelines.yml`

**Key files:**
- `001/`, `002/`, `003/` - Individual workflow folders
- `workflow.json` - Workflow definition in each folder
- `host.json` - Logic App configuration
- `connections.json` - API connections

**Deployed to:** `logic-enrollment-app` (Azure Logic App)

## How Pipelines Use This Structure

### Function App Pipeline
```yaml
# In function-app-sample/azure-pipelines.yml
resources:
  repositories:
    - repository: functionAppCode
      name: enrollment-app          # References this repo

variables:
  workingDirectory: '$(System.DefaultWorkingDirectory)/enrollment-function-app'
```

### Logic App Pipeline
```yaml
# In logic-app-sample/azure-pipelines.yml
resources:
  repositories:
    - repository: logicAppCode
      name: enrollment-app          # Same repo, different folder

variables:
  workingDirectory: '$(System.DefaultWorkingDirectory)/enrollment-logic-app'
```

## Setting Up the Actual Repository

When you're ready to create the real `enrollment-app` repository:

### Step 1: Create Repository in Azure DevOps
1. Go to Azure DevOps → Repos
2. Click "New repository"
3. Name it: `enrollment-app`
4. Click "Create"

### Step 2: Copy Code from This Folder
```bash
# Clone the new repository
git clone <enrollment-app-repo-url>
cd enrollment-app

# Copy the enrollment folders from this simulated repo
cp -r /path/to/azure-devops/enrollment-app/enrollment-function-app .
cp -r /path/to/azure-devops/enrollment-app/enrollment-logic-app .
cp /path/to/azure-devops/enrollment-app/README.md .

# Commit and push
git add .
git commit -m "Initial commit: Add enrollment function and logic app code"
git push origin main
```

### Step 3: Verify Structure
Ensure the repository has this structure:
```
enrollment-app/
├── enrollment-function-app/
│   ├── HttpTrigger/
│   ├── tests/
│   ├── host.json
│   └── requirements.txt
├── enrollment-logic-app/
│   ├── 001/
│   ├── 002/
│   ├── 003/
│   ├── host.json
│   └── connections.json
└── README.md
```

### Step 4: Update Pipelines (if needed)
The pipelines are already configured to use `enrollment-app` repository, so no changes needed unless you used a different repository name.

## Testing Locally

### Test Function App Locally
```bash
cd enrollment-function-app

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Start function
func start
```

### Test Logic App Locally
```bash
cd enrollment-logic-app

# Start Azurite
azurite --silent --location ./azurite

# Open in VS Code with Logic Apps extension
code .

# Press F5 to run
```

## Adding More Applications

You can add more applications to this repository structure:

```
enrollment-app/
├── enrollment-function-app/       # Existing
├── enrollment-logic-app/          # Existing
├── notifications-function-app/    # New function app
├── reporting-logic-app/           # New logic app
└── common/                        # Shared code/configurations
```

Then create separate pipelines in the `azure-devops` repository that reference the appropriate folders.

## Best Practices

1. **Separate Concerns**: Keep function apps and logic apps in separate folders
2. **Clear Naming**: Use descriptive folder names that indicate the application purpose
3. **Shared Code**: Create a `common` folder for shared utilities
4. **Documentation**: Maintain a README in each application folder
5. **Version Control**: Use Git tags/branches for releases
6. **Environment Config**: Keep environment-specific settings out of code (use pipeline variables)

## Deployment Workflow

```
Developer
    ↓
Commits to enrollment-app repo
    ↓
Pipeline in azure-devops repo triggered
    ↓
Pipeline checks out code from enrollment-app
    ↓
Pipeline builds and deploys to Azure
```

## Repository Permissions

Ensure the pipeline has permissions to access the `enrollment-app` repository:
1. Azure DevOps → Project Settings → Repositories
2. Select `enrollment-app`
3. Security → Add pipeline service account
4. Grant "Read" permission

## Troubleshooting

### Pipeline can't find repository
- Verify repository name is exactly `enrollment-app`
- Check pipeline has read access to the repository
- Ensure the repository is in the same Azure DevOps project

### Pipeline can't find folder
- Verify folder names match exactly:
  - `enrollment-function-app`
  - `enrollment-logic-app`
- Check folder structure is correct
- Ensure required files exist (host.json, etc.)

### Local development not working
- For functions: Ensure Azure Functions Core Tools installed
- For logic apps: Ensure VS Code with Logic Apps extension
- Check `local.settings.json` is configured correctly
- Verify Azurite is running (for logic apps)

## Migration Checklist

When moving from this simulated structure to real repository:

- [ ] Create `enrollment-app` repository in Azure DevOps
- [ ] Copy `enrollment-function-app` folder
- [ ] Copy `enrollment-logic-app` folder
- [ ] Copy or create README.md
- [ ] Commit and push to main branch
- [ ] Verify pipeline access to repository
- [ ] Test function app pipeline deployment
- [ ] Test logic app pipeline deployment
- [ ] Remove this simulated folder from `azure-devops` repo (optional)

## Additional Notes

- This simulated folder is useful for local testing and development
- Keep this folder in sync with the actual repository structure
- Use this as a reference when creating new applications
- Update this README when adding new application folders
