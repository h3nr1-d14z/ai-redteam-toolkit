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

detect_os() {
    case "$(uname -s)" in
        Darwin*) OS="macos" ;;
        Linux*)  OS="linux" ;;
        *)
            log_warn "Unsupported OS: $(uname -s)"
            exit 1
            ;;
    esac
}

install_pkg() {
    local pkg="$1"
    local cmd="${2:-$1}"

    if command -v "${cmd}" &>/dev/null; then
        log_info "${cmd} is already installed"
        return
    fi

    if [[ "${OS}" == "macos" ]] && command -v brew &>/dev/null; then
        brew install "${pkg}" 2>/dev/null && log_success "${pkg} installed" || log_warn "Failed: ${pkg}"
    elif command -v apt-get &>/dev/null; then
        sudo apt-get install -y "${pkg}" 2>/dev/null && log_success "${pkg} installed" || log_warn "Failed: ${pkg}"
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y "${pkg}" 2>/dev/null && log_success "${pkg} installed" || log_warn "Failed: ${pkg}"
    elif command -v pacman &>/dev/null; then
        sudo pacman -S --noconfirm "${pkg}" 2>/dev/null && log_success "${pkg} installed" || log_warn "Failed: ${pkg}"
    else
        log_warn "No supported package manager for ${pkg}"
    fi
}

install_pip() {
    local pkg="$1"
    local cmd="${2:-$1}"
    if command -v "${cmd}" &>/dev/null; then
        log_info "${cmd} is already installed"
        return
    fi
    pip3 install "${pkg}" 2>/dev/null && log_success "${pkg} installed via pip" || log_warn "Failed pip install: ${pkg}"
}

install_go() {
    local module="$1"
    local cmd="$2"
    if command -v "${cmd}" &>/dev/null; then
        log_info "${cmd} is already installed"
        return
    fi
    if command -v go &>/dev/null; then
        go install "${module}" 2>/dev/null && log_success "${cmd} installed via go" || log_warn "Failed go install: ${cmd}"
    else
        log_warn "Go not installed; skipping ${cmd}"
    fi
}

main() {
    echo -e "${BOLD}Cloud Security Tools${NC}"
    detect_os

    install_pkg "awscli" "aws"
    install_pkg "terraform" "terraform"
    install_pkg "trivy" "trivy"
    install_pkg "kubectl" "kubectl"

    install_pip "scoutsuite" "scout"
    install_pip "prowler" "prowler"
    install_pip "cloudsplaining" "cloudsplaining"

    install_go "github.com/projectdiscovery/httpx/cmd/httpx@latest" "httpx"
    install_go "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest" "subfinder"

    echo ""
    log_success "Cloud security tools installation complete"
}

main "$@"
