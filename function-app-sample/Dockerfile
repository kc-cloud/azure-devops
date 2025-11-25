# Base image with Python 3.12
FROM python:3.12-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Archive and compression tools
    zip \
    unzip \
    tar \
    gzip \
    # Build essentials
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    # Python development headers
    python3-dev \
    # Common libraries for Python packages
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    # Git for version control
    git \
    git-lfs \
    # curl and wget for downloading
    curl \
    wget \
    # Azure CLI dependencies
    gnupg \
    lsb-release \
    ca-certificates \
    apt-transport-https \
    software-properties-common \
    # Network and SSH tools
    net-tools \
    iputils-ping \
    openssh-client \
    rsync \
    # Text processing
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install Azure CLI
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

# Install Azure DevOps CLI extension
RUN az extension add --name azure-devops

# Install Node.js 20.x (LTS) and npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Azure Functions Core Tools v4
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg \
    && mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg \
    && sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/debian/$(lsb_release -rs | cut -d'.' -f 1)/prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list' \
    && apt-get update \
    && apt-get install -y azure-functions-core-tools-4 \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y docker-ce-cli docker-compose-plugin \
    && rm -rf /var/lib/apt/lists/*

# Install kubectl
RUN curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /" > /etc/apt/sources.list.d/kubernetes.list \
    && apt-get update \
    && apt-get install -y kubectl \
    && rm -rf /var/lib/apt/lists/*

# Install Helm
RUN curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install Terraform
RUN wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" > /etc/apt/sources.list.d/hashicorp.list \
    && apt-get update \
    && apt-get install -y terraform \
    && rm -rf /var/lib/apt/lists/*

# Install Bicep CLI
RUN curl -Lo bicep https://github.com/Azure/bicep/releases/latest/download/bicep-linux-x64 \
    && chmod +x ./bicep \
    && mv ./bicep /usr/local/bin/bicep

# Install PowerShell Core
RUN wget -q https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && rm packages-microsoft-prod.deb \
    && apt-get update \
    && apt-get install -y powershell \
    && rm -rf /var/lib/apt/lists/*

# Install .NET SDK 8.0 (for C# Azure Functions and build tasks)
RUN wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh \
    && chmod +x dotnet-install.sh \
    && ./dotnet-install.sh --channel 8.0 --install-dir /usr/share/dotnet \
    && ln -s /usr/share/dotnet/dotnet /usr/local/bin/dotnet \
    && rm dotnet-install.sh

# Install Azure Resource Manager (ARM) template tools
RUN npm install -g azure-arm-validator

# Install Azure Storage tools (for artifact uploads, logic app deployments)
RUN pip install azure-storage-blob azure-storage-file-share

# Install zip deployment utilities (used by AzureFunctionApp task)
RUN npm install -g azure-functions-core-tools@4 --unsafe-perm true

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Install common Python packages for testing and development
RUN pip install \
    pytest \
    pytest-cov \
    pytest-mock \
    pytest-asyncio \
    coverage \
    black \
    flake8 \
    pylint \
    mypy \
    # Azure SDK packages for deployments
    azure-functions \
    azure-identity \
    azure-mgmt-resource \
    azure-mgmt-web \
    azure-mgmt-logicapp \
    azure-mgmt-containerservice \
    azure-mgmt-storage \
    azure-mgmt-keyvault \
    azure-mgmt-monitor \
    azure-mgmt-authorization \
    # Azure deployment tools
    azure-cli-core \
    knack

# Create a working directory
WORKDIR /workspace

# Set the default command
CMD ["/bin/bash"]
