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

main() {
    echo -e "${BOLD}Forensics Tools${NC}"
    detect_os

    install_pkg "yara" "yara"
    install_pkg "tshark" "tshark"
    install_pkg "sleuthkit" "fls"

    install_pip "volatility3" "vol"
    install_pip "oletools" "oleid"

    echo ""
    log_success "Forensics tools installation complete"
}

main "$@"
