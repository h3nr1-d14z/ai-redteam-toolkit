#!/usr/bin/env bash

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[*]${NC} $1"; }
log_success() { echo -e "${GREEN}[+]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[!]${NC} $1"; }

install_pip() {
    local pkg="$1"
    local cmd="${2:-$1}"
    if command -v "${cmd}" &>/dev/null; then
        log_info "${cmd} is already installed"
        return
    fi
    pip3 install "${pkg}" 2>/dev/null && log_success "${pkg} installed via pip" || log_warn "Failed pip install: ${pkg}"
}

install_npm() {
    local pkg="$1"
    local cmd="$2"
    if command -v "${cmd}" &>/dev/null; then
        log_info "${cmd} is already installed"
        return
    fi
    if command -v npm &>/dev/null; then
        npm install -g "${pkg}" 2>/dev/null && log_success "${pkg} installed via npm" || log_warn "Failed npm install: ${pkg}"
    else
        log_warn "npm not found; skipping ${pkg}"
    fi
}

main() {
    echo -e "${BOLD}AI/LLM Security Tools${NC}"

    install_pip "garak" "garak"
    install_pip "llm-guard" "llm-guard"
    install_pip "promptmap" "promptmap"

    install_npm "promptfoo" "promptfoo"

    echo ""
    log_success "AI/LLM security tools installation complete"
}

main "$@"
