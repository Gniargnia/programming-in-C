FROM mcr.microsoft.com/devcontainers/base:ubuntu

RUN apt-get update && apt-get install -y \
    build-essential \
    clang \
    curl \
    sudo \
    && curl -s https://packagecloud.io/install/repositories/cs50/repo/script.deb.sh | sudo bash \
    && apt-get install -y libcs50