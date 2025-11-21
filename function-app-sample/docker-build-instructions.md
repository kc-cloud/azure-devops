# Build and Push Custom Docker Image to ACR

## Prerequisites
- Azure CLI installed
- Docker installed
- Access to Azure Container Registry (ACR)

## Step 1: Login to Azure and ACR

```bash
# Login to Azure
az login

# Login to ACR (replace <acr-name> with your ACR name)
az acr login --name <acr-name>
```

## Step 2: Build the Docker Image

```bash
# Navigate to the directory containing the Dockerfile
cd /path/to/function-app-sample

# Build the image
docker build -t python-azure-builder:3.12 .

# Or with a specific tag
docker build -t python-azure-builder:3.12-$(date +%Y%m%d) .
```

## Step 3: Tag the Image for ACR

```bash
# Tag the image (replace <acr-name> with your ACR name)
docker tag python-azure-builder:3.12 <acr-name>.azurecr.io/python-azure-builder:3.12

# Tag with specific version
docker tag python-azure-builder:3.12 <acr-name>.azurecr.io/python-azure-builder:3.12-latest
```

## Step 4: Push to ACR

```bash
# Push the image to ACR
docker push <acr-name>.azurecr.io/python-azure-builder:3.12

# Push with version tag
docker push <acr-name>.azurecr.io/python-azure-builder:3.12-latest
```

## Step 5: Verify the Image in ACR

```bash
# List repositories in ACR
az acr repository list --name <acr-name> --output table

# Show tags for the image
az acr repository show-tags --name <acr-name> --repository python-azure-builder --output table
```

## Example: Complete Commands

Replace `myacr` with your actual ACR name:

```bash
# Login
az login
az acr login --name myacr

# Build
docker build -t python-azure-builder:3.12 .

# Tag
docker tag python-azure-builder:3.12 myacr.azurecr.io/python-azure-builder:3.12
docker tag python-azure-builder:3.12 myacr.azurecr.io/python-azure-builder:latest

# Push
docker push myacr.azurecr.io/python-azure-builder:3.12
docker push myacr.azurecr.io/python-azure-builder:latest
```

## Optional: Test the Image Locally

```bash
# Run the container
docker run -it --rm python-azure-builder:3.12 /bin/bash

# Inside the container, verify installations
python --version
pip --version
zip --version
git --version
pytest --version
```
