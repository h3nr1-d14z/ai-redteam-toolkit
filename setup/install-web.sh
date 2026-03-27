#!/usr/bin/env bash
# install-web.sh - Install web application pentesting tools
#
# Usage: ./setup/install-web.sh
#
# Tools installed:
#   nmap, sqlmap, ffuf, nuclei, subfinder, httpx, dalfox, arjun, whatweb, nikto

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
log_error()   { echo -e "${RED}[-]${NC} $1"; }

# ---------------------------------------------------------------------------
# OS Detection
# ---------------------------------------------------------------------------
detect_os() {
    case "$(uname -s)" in
        Darwin*) OS="macos" ;;
        Linux*)  OS="linux" ;;
        *)
            log_error "Unsupported OS: $(uname -s)"
            exit 1
            ;;
    esac
}

# ---------------------------------------------------------------------------
# Install helpers
# ---------------------------------------------------------------------------
install_with_brew() {
    local pkg="$1"
    if command -v "${pkg}" &>/dev/null; then
        log_info "${pkg} is already installed"
    else
        log_info "Installing ${pkg} via Homebrew..."
        if brew install "${pkg}" 2>/dev/null; then
            log_success "${pkg} installed"
        else
            log_warn "Failed to install ${pkg} via Homebrew"
        fi
    fi
}

install_with_apt() {
    local pkg="$1"
    local cmd="${2:-$1}"
    if command -v "${cmd}" &>/dev/null; then
        log_info "${cmd} is already installed"
    else
        log_info "Installing ${pkg} via apt..."
        if sudo apt-get install -y "${pkg}" 2>/dev/null; then
            log_success "${pkg} installed"
        else
            log_warn "Failed to install ${pkg} via apt"
        fi
    fi
}

install_with_pip() {
    local pkg="$1"
    local cmd="${2:-$1}"
    if command -v "${cmd}" &>/dev/null; then
        log_info "${cmd} is already installed"
    else
        log_info "Installing ${pkg} via pip..."
        if pip3 install "${pkg}" 2>/dev/null; then
            log_success "${pkg} installed"
        else
            log_warn "Failed to install ${pkg} via pip"
        fi
    fi
}

install_with_go() {
    local pkg="$1"
    local cmd="$2"
    if command -v "${cmd}" &>/dev/null; then
        log_info "${cmd} is already installed"
    else
        if command -v go &>/dev/null; then
            log_info "Installing ${cmd} via go install..."
            if go install "${pkg}" 2>/dev/null; then
                log_success "${cmd} installed"
            else
                log_warn "Failed to install ${cmd} via go install"
            fi
        else
            log_warn "Go not installed. Cannot install ${cmd}. Install Go first."
        fi
    fi
}

# ---------------------------------------------------------------------------
# Tool installations
# ---------------------------------------------------------------------------
install_nmap() {
    if command -v nmap &>/dev/null; then
        log_info "nmap is already installed"
        return
    fi
    if [[ "${OS}" == "macos" ]]; then
        install_with_brew "nmap"
    else
        install_with_apt "nmap"
    fi
}

install_sqlmap() {
    if command -v sqlmap &>/dev/null; then
        log_info "sqlmap is already installed"
        return
    fi
    if [[ "${OS}" == "macos" ]]; then
        install_with_brew "sqlmap"
    else
        install_with_pip "sqlmap"
    fi
}

install_ffuf() {
    if command -v ffuf &>/dev/null; then
        log_info "ffuf is already installed"
        return
    fi
    if [[ "${OS}" == "macos" ]]; then
        install_with_brew "ffuf"
    else
        install_with_go "github.com/ffuf/ffuf/v2@latest" "ffuf"
    fi
}

install_nuclei() {
    if command -v nuclei &>/dev/null; then
        log_info "nuclei is already installed"
        return
    fi
    if [[ "${OS}" == "macos" ]]; then
        install_with_brew "nuclei"
    else
        install_with_go "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest" "nuclei"
    fi
}

install_subfinder() {
    if command -v subfinder &>/dev/null; then
        log_info "subfinder is already installed"
        return
    fi
    if [[ "${OS}" == "macos" ]]; then
        install_with_brew "subfinder"
    else
        install_with_go "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest" "subfinder"
    fi
}

install_httpx() {
    if command -v httpx &>/dev/null; then
        log_info "httpx is already installed"
        return
    fi
    if [[ "${OS}" == "macos" ]]; then
        install_with_brew "httpx"
    else
        install_with_go "github.com/projectdiscovery/httpx/cmd/httpx@latest" "httpx"
    fi
}

install_dalfox() {
    if command -v dalfox &>/dev/null; then
        log_info "dalfox is already installed"
        return
    fi
    if [[ "${OS}" == "macos" ]]; then
        install_with_brew "dalfox"
    else
        install_with_go "github.com/hahwul/dalfox/v2@latest" "dalfox"
    fi
}

install_arjun() {
    install_with_pip "arjun"
}

install_whatweb() {
    if command -v whatweb &>/dev/null; then
        log_info "whatweb is already installed"
        return
    fi
    if [[ "${OS}" == "macos" ]]; then
        install_with_brew "whatweb"
    else
        install_with_apt "whatweb"
    fi
}

install_nikto() {
    if command -v nikto &>/dev/null; then
        log_info "nikto is already installed"
        return
    fi
    if [[ "${OS}" == "macos" ]]; then
        install_with_brew "nikto"
    else
        install_with_apt "nikto"
    fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
    echo -e "${BOLD}Web Application Pentesting Tools${NC}"
    echo ""

    detect_os

    install_nmap
    install_sqlmap
    install_ffuf
    install_nuclei
    install_subfinder
    install_httpx
    install_dalfox
    install_arjun
    install_whatweb
    install_nikto

    echo ""
    log_success "Web pentesting tools installation complete"
}

main "$@"
