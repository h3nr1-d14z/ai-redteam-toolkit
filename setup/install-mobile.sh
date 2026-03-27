#!/usr/bin/env bash
# install-mobile.sh - Install mobile application security testing tools
#
# Usage: ./setup/install-mobile.sh
#
# Tools installed:
#   jadx, apktool, frida, objection, mitmproxy

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
install_jadx() {
    if command -v jadx &>/dev/null; then
        log_info "jadx is already installed"
        return
    fi

    log_info "Installing jadx..."

    if [[ "${OS}" == "macos" ]]; then
        if command -v brew &>/dev/null; then
            if brew install jadx 2>/dev/null; then
                log_success "jadx installed via Homebrew"
                return
            fi
        fi
    else
        # Linux: check snap or download release
        if command -v snap &>/dev/null; then
            if sudo snap install jadx 2>/dev/null; then
                log_success "jadx installed via snap"
                return
            fi
        fi

        # Download latest release
        log_info "Downloading jadx from GitHub releases..."
        local tmp_dir
        tmp_dir=$(mktemp -d)
        local latest_url="https://github.com/skylot/jadx/releases/latest"
        local download_url

        download_url=$(curl -sI "${latest_url}" 2>/dev/null | grep -i "location:" | sed 's/.*tag\///' | tr -d '[:space:]')
        if [[ -n "${download_url}" ]]; then
            local version="${download_url}"
            local zip_url="https://github.com/skylot/jadx/releases/download/${version}/jadx-${version#v}.zip"
            if curl -sL "${zip_url}" -o "${tmp_dir}/jadx.zip" 2>/dev/null; then
                local install_dir="/opt/jadx"
                sudo mkdir -p "${install_dir}"
                sudo unzip -o "${tmp_dir}/jadx.zip" -d "${install_dir}" 2>/dev/null
                sudo ln -sf "${install_dir}/bin/jadx" /usr/local/bin/jadx 2>/dev/null
                sudo ln -sf "${install_dir}/bin/jadx-gui" /usr/local/bin/jadx-gui 2>/dev/null
                log_success "jadx installed to ${install_dir}"
            else
                log_warn "Failed to download jadx"
            fi
        else
            log_warn "Could not determine latest jadx version"
        fi
        rm -rf "${tmp_dir}"
    fi
}

install_apktool() {
    if command -v apktool &>/dev/null; then
        log_info "apktool is already installed"
        return
    fi

    log_info "Installing apktool..."

    if [[ "${OS}" == "macos" ]]; then
        if command -v brew &>/dev/null; then
            if brew install apktool 2>/dev/null; then
                log_success "apktool installed via Homebrew"
                return
            fi
        fi
    else
        if command -v apt-get &>/dev/null; then
            if sudo apt-get install -y apktool 2>/dev/null; then
                log_success "apktool installed via apt"
                return
            fi
        fi

        # Manual install
        log_info "Installing apktool manually..."
        local install_dir="/usr/local/bin"
        local wrapper_url="https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool"
        local jar_url

        # Get latest jar URL
        jar_url=$(curl -s https://api.github.com/repos/iBotPeaches/Apktool/releases/latest 2>/dev/null | grep "browser_download_url.*jar" | head -1 | cut -d'"' -f4)

        if [[ -n "${jar_url}" ]]; then
            sudo curl -sL "${wrapper_url}" -o "${install_dir}/apktool" 2>/dev/null
            sudo curl -sL "${jar_url}" -o "${install_dir}/apktool.jar" 2>/dev/null
            sudo chmod +x "${install_dir}/apktool"
            log_success "apktool installed"
        else
            log_warn "Failed to determine latest apktool version"
        fi
    fi
}

install_frida() {
    if command -v frida &>/dev/null; then
        log_info "frida is already installed"
        return
    fi

    log_info "Installing frida and frida-tools..."

    if pip3 install frida-tools 2>/dev/null; then
        log_success "frida-tools installed via pip"
    else
        log_warn "Failed to install frida-tools via pip"
        log_info "Try: pip3 install frida-tools --user"
    fi
}

install_objection() {
    if command -v objection &>/dev/null; then
        log_info "objection is already installed"
        return
    fi

    log_info "Installing objection..."

    if pip3 install objection 2>/dev/null; then
        log_success "objection installed via pip"
    else
        log_warn "Failed to install objection via pip"
        log_info "Try: pip3 install objection --user"
    fi
}

install_mitmproxy() {
    if command -v mitmproxy &>/dev/null; then
        log_info "mitmproxy is already installed"
        return
    fi

    log_info "Installing mitmproxy..."

    if [[ "${OS}" == "macos" ]]; then
        if command -v brew &>/dev/null; then
            if brew install mitmproxy 2>/dev/null; then
                log_success "mitmproxy installed via Homebrew"
                return
            fi
        fi
    else
        if pip3 install mitmproxy 2>/dev/null; then
            log_success "mitmproxy installed via pip"
            return
        fi
    fi

    log_warn "Failed to install mitmproxy"
    log_info "Download from: https://mitmproxy.org"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
    echo -e "${BOLD}Mobile Application Security Tools${NC}"
    echo ""

    detect_os

    # Check for Java (needed by jadx and apktool)
    if ! command -v java &>/dev/null; then
        log_warn "Java not found. jadx and apktool require Java."
        log_info "Install Java first:"
        if [[ "${OS}" == "macos" ]]; then
            log_info "  brew install openjdk@17"
        else
            log_info "  sudo apt install openjdk-17-jdk"
        fi
    fi

    # Check for Python3 (needed by frida, objection)
    if ! command -v python3 &>/dev/null; then
        log_error "Python 3 is required but not found."
        exit 1
    fi

    install_jadx
    install_apktool
    install_frida
    install_objection
    install_mitmproxy

    echo ""
    log_success "Mobile security tools installation complete"
    echo ""
    log_info "Additional setup:"
    log_info "  - Android: Install Android SDK and set ANDROID_HOME"
    log_info "  - Android: Ensure 'adb' is in your PATH"
    log_info "  - iOS: Install Xcode command line tools (macOS only)"
    log_info "  - Frida server: Push to device with 'frida-server' binary"
}

main "$@"
