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
    # curl and wget for downloading
    curl \
    wget \
    # Azure CLI dependencies
    gnupg \
    lsb-release \
    ca-certificates \
    # Network tools
    net-tools \
    iputils-ping \
    # Text processing
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install Azure CLI
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

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
    mypy

# Create a working directory
WORKDIR /workspace

# Set the default command
CMD ["/bin/bash"]
