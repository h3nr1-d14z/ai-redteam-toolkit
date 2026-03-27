#!/usr/bin/env bash
# install-re.sh - Install reverse engineering tools
#
# Usage: ./setup/install-re.sh
#
# Tools installed:
#   ghidra (check/guide), radare2, binwalk, checksec

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
# Tool installations
# ---------------------------------------------------------------------------
install_ghidra() {
    log_info "Checking for Ghidra..."

    # Check common locations
    local found=false

    if command -v ghidra &>/dev/null || command -v ghidraRun &>/dev/null; then
        log_success "Ghidra found in PATH"
        found=true
    fi

    # macOS common locations
    if [[ "${OS}" == "macos" ]]; then
        for dir in /Applications/ghidra* /opt/ghidra* "${HOME}/ghidra"*; do
            if [[ -d "${dir}" ]] 2>/dev/null; then
                log_success "Ghidra found at: ${dir}"
                found=true
                break
            fi
        done

        if [[ "${found}" == false ]]; then
            if command -v brew &>/dev/null; then
                log_info "Attempting to install Ghidra via Homebrew cask..."
                if brew install --cask ghidra 2>/dev/null; then
                    log_success "Ghidra installed via Homebrew"
                    found=true
                else
                    log_warn "Could not install Ghidra via Homebrew"
                fi
            fi
        fi
    fi

    # Linux common locations
    if [[ "${OS}" == "linux" ]]; then
        for dir in /opt/ghidra* /usr/local/ghidra* "${HOME}/ghidra"*; do
            if [[ -d "${dir}" ]] 2>/dev/null; then
                log_success "Ghidra found at: ${dir}"
                found=true
                break
            fi
        done
    fi

    if [[ "${found}" == false ]]; then
        log_warn "Ghidra not found."
        log_info "Download Ghidra from: https://ghidra-sre.org"
        log_info "Installation steps:"
        log_info "  1. Install Java 17+: brew install openjdk@17  (macOS)"
        log_info "     or: sudo apt install openjdk-17-jdk  (Linux)"
        log_info "  2. Download and extract Ghidra"
        log_info "  3. Run: ./ghidraRun"
    fi
}

install_radare2() {
    if command -v r2 &>/dev/null; then
        log_info "radare2 is already installed"
        return
    fi

    log_info "Installing radare2..."

    if [[ "${OS}" == "macos" ]]; then
        if command -v brew &>/dev/null; then
            if brew install radare2 2>/dev/null; then
                log_success "radare2 installed via Homebrew"
                return
            fi
        fi
    else
        if command -v apt-get &>/dev/null; then
            if sudo apt-get install -y radare2 2>/dev/null; then
                log_success "radare2 installed via apt"
                return
            fi
        fi
    fi

    # Fallback: build from source
    log_info "Trying to install radare2 from source..."
    if command -v git &>/dev/null; then
        local tmp_dir
        tmp_dir=$(mktemp -d)
        if git clone --depth 1 https://github.com/radareorg/radare2.git "${tmp_dir}/radare2" 2>/dev/null; then
            cd "${tmp_dir}/radare2"
            if ./sys/install.sh 2>/dev/null; then
                log_success "radare2 installed from source"
            else
                log_warn "Failed to build radare2 from source"
            fi
            rm -rf "${tmp_dir}"
        else
            log_warn "Failed to clone radare2 repository"
        fi
    else
        log_warn "git not available, cannot install radare2 from source"
    fi
}

install_binwalk() {
    if command -v binwalk &>/dev/null; then
        log_info "binwalk is already installed"
        return
    fi

    log_info "Installing binwalk..."

    if [[ "${OS}" == "macos" ]]; then
        if command -v brew &>/dev/null; then
            if brew install binwalk 2>/dev/null; then
                log_success "binwalk installed via Homebrew"
                return
            fi
        fi
    else
        if command -v apt-get &>/dev/null; then
            if sudo apt-get install -y binwalk 2>/dev/null; then
                log_success "binwalk installed via apt"
                return
            fi
        fi
    fi

    # Fallback: pip
    log_info "Trying pip install..."
    if pip3 install binwalk 2>/dev/null; then
        log_success "binwalk installed via pip"
    else
        log_warn "Failed to install binwalk"
    fi
}

install_checksec() {
    if command -v checksec &>/dev/null; then
        log_info "checksec is already installed"
        return
    fi

    log_info "Installing checksec..."

    if [[ "${OS}" == "macos" ]]; then
        if command -v brew &>/dev/null; then
            if brew install checksec 2>/dev/null; then
                log_success "checksec installed via Homebrew"
                return
            fi
        fi
    else
        if command -v apt-get &>/dev/null; then
            if sudo apt-get install -y checksec 2>/dev/null; then
                log_success "checksec installed via apt"
                return
            fi
        fi
    fi

    # Fallback: install from GitHub
    log_info "Installing checksec from GitHub..."
    local install_path="/usr/local/bin/checksec"
    if curl -sL https://raw.githubusercontent.com/slimm609/checksec.sh/master/checksec -o /tmp/checksec 2>/dev/null; then
        chmod +x /tmp/checksec
        if sudo mv /tmp/checksec "${install_path}" 2>/dev/null; then
            log_success "checksec installed to ${install_path}"
        else
            # Try without sudo
            local local_bin="${HOME}/.local/bin"
            mkdir -p "${local_bin}"
            mv /tmp/checksec "${local_bin}/checksec"
            log_success "checksec installed to ${local_bin}/checksec"
            log_info "Make sure ${local_bin} is in your PATH"
        fi
    else
        log_warn "Failed to download checksec"
    fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
    echo -e "${BOLD}Reverse Engineering Tools${NC}"
    echo ""

    detect_os

    install_ghidra
    install_radare2
    install_binwalk
    install_checksec

    echo ""
    log_success "Reverse engineering tools installation complete"
}

main "$@"
