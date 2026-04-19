FROM ubuntu:22.04

ARG AGENT_VERSION=3.248.0

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    git \
    jq \
    libicu70 \
    libssl3 \
    ca-certificates \
    unzip \
    zip \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI (for pipelines that build images)
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker.gpg] \
    https://download.docker.com/linux/ubuntu jammy stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && apt-get install -y docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && \
    rm kubectl

RUN useradd -m -s /bin/bash agent
WORKDIR /home/agent

RUN curl -fsSL \
    "https://vstsagentpackage.azureedge.net/agent/${AGENT_VERSION}/vsts-agent-linux-x64-${AGENT_VERSION}.tar.gz" \
    -o agent.tar.gz && \
    tar -xzf agent.tar.gz && \
    rm agent.tar.gz && \
    chown -R agent:agent /home/agent

COPY entrypoint.sh /home/agent/entrypoint.sh
RUN chmod +x /home/agent/entrypoint.sh && chown agent:agent /home/agent/entrypoint.sh

USER agent
ENTRYPOINT ["/home/agent/entrypoint.sh"]
