#!/usr/bin/env bash

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[*]${NC} $1"; }
log_success() { echo -e "${GREEN}[+]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[!]${NC} $1"; }

if [[ "$(uname -s)" != "Linux" ]]; then
    log_warn "install-wsl.sh is intended for Linux environments (WSL2)."
    exit 1
fi

if ! grep -qiE "microsoft|wsl" /proc/version 2>/dev/null; then
    log_warn "This environment does not appear to be WSL. Running anyway."
fi

if command -v apt-get &>/dev/null; then
    log_info "Updating apt package index..."
    sudo apt-get update -y
    log_info "Installing base dependencies..."
    sudo apt-get install -y git curl wget python3 python3-pip build-essential unzip
else
    log_warn "apt-get not found. Install base dependencies manually, then run ./setup/install.sh"
fi

log_info "Ensuring setup scripts are executable..."
chmod +x ./setup/*.sh

log_info "Running full installer..."
./setup/install.sh --all

log_success "WSL bootstrap completed"
