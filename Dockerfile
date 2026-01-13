FROM mcr.microsoft.com/devcontainers/base:ubuntu

# ------------------------------------------------------------
# Outils système et C
# ------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    clang \
    clang-tools \
    lldb \
    valgrind \
    make \
    curl \
    git-lfs \
    sudo \
    jq \
    python3 \
    python3-pip \
    python3-venv \
    ca-certificates \
    cowsay \
    && curl -s https://packagecloud.io/install/repositories/cs50/repo/script.deb.sh | bash \
    && apt-get update \
    && apt-get install -y libcs50 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Environnement virtuel CS50 (PEP 668 safe)
# ------------------------------------------------------------
RUN python3 -m venv /opt/cs50-venv \
    && /opt/cs50-venv/bin/pip install --upgrade pip \
    && /opt/cs50-venv/bin/pip install --no-cache-dir \
        check50 \
        submit50 \
        style50 \
        help50

# ------------------------------------------------------------
# PATH global
# ------------------------------------------------------------
ENV PATH="/opt/cs50-venv/bin:${PATH}"

# ------------------------------------------------------------
# Prompt simple
# ------------------------------------------------------------
RUN echo "export PS1='\\W $ '" >> /home/vscode/.bashrc

# ------------------------------------------------------------
# Workspace
# ------------------------------------------------------------
WORKDIR /workspaces/programming-in-C