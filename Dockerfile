FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Installer les outils de base
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    clang \
    curl \
    git-lfs \
    sudo \
    gdb \
    valgrind \
    make \
    jq \
    python3 \
    python3-pip \
    python3-venv \
    ca-certificates \
    cowsay

RUN curl -s https://packagecloud.io/install/repositories/cs50/repo/script.deb.sh | bash \
    && apt-get install -y libcs50 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# Créer un environnement virtuel pour contourner PEP 668
RUN python3 -m venv /opt/cs50-venv \
    && /opt/cs50-venv/bin/pip install --no-cache-dir \
    check50 \
    submit50 \
    style50 \
    help50

# Ajouter l'environnement virtuel au PATH
ENV PATH="/opt/cs50-venv/bin:${PATH}"

# Prompt simple
RUN echo "export PS1='\W $ '" >> /home/vscode/.bashrc

WORKDIR /workspaces/programming-in-C