FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
       git \
       curl \
       wget \
       build-essential \
       software-properties-common \
       openssh-client \
       gnupg2 \
       lsb-release \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Install Node.js for documentation tools
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Create vscode user
RUN groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid vscode --shell /bin/bash --create-home vscode

# Install Python tools globally
RUN python -m pip install --upgrade pip \
    && pip install \
       black \
       isort \
       ruff \
       mypy \
       pre-commit \
       pytest \
       pytest-cov \
       bandit \
       safety

# Install documentation tools
RUN npm install -g markdownlint-cli markdown-link-check prettier

# Set up command history persistence
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && mkdir /commandhistory \
    && touch /commandhistory/.bash_history \
    && chown -R vscode /commandhistory \
    && echo "$SNIPPET" >> "/home/vscode/.bashrc"

# Set up git configuration template
RUN echo '[user]' > /home/vscode/.gitconfig.template \
    && echo '    name = Your Name' >> /home/vscode/.gitconfig.template \
    && echo '    email = your.email@example.com' >> /home/vscode/.gitconfig.template \
    && chown vscode:vscode /home/vscode/.gitconfig.template

USER vscode

WORKDIR /workspace