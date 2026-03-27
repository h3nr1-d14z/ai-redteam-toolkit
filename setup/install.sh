#!/usr/bin/env bash
# install.sh - AI-RedTeam-Toolkit Master Installer
#
# Usage:
#   ./setup/install.sh          Interactive category selection
#   ./setup/install.sh --all    Install everything
#   ./setup/install.sh --check  Run tool verification only
#
# Supports macOS (Homebrew) and Linux (apt).

set -euo pipefail

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
log_info()    { echo -e "${BLUE}[*]${NC} $1"; }
log_success() { echo -e "${GREEN}[+]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[!]${NC} $1"; }
log_error()   { echo -e "${RED}[-]${NC} $1"; }
log_header()  { echo -e "\n${BOLD}${CYAN}=== $1 ===${NC}\n"; }

# ---------------------------------------------------------------------------
# OS & Package Manager Detection
# ---------------------------------------------------------------------------
detect_os() {
    case "$(uname -s)" in
        Darwin*) OS="macos" ;;
        Linux*)  OS="linux" ;;
        *)
            log_error "Unsupported operating system: $(uname -s)"
            exit 1
            ;;
    esac
    log_info "Detected OS: ${OS}"
}

detect_package_manager() {
    if [[ "${OS}" == "macos" ]]; then
        if command -v brew &>/dev/null; then
            PKG_MGR="brew"
        else
            log_error "Homebrew not found. Install it from https://brew.sh"
            exit 1
        fi
    elif [[ "${OS}" == "linux" ]]; then
        if command -v apt-get &>/dev/null; then
            PKG_MGR="apt"
        elif command -v dnf &>/dev/null; then
            PKG_MGR="dnf"
        elif command -v pacman &>/dev/null; then
            PKG_MGR="pacman"
        else
            log_error "No supported package manager found (apt, dnf, pacman)."
            exit 1
        fi
    fi
    log_info "Package manager: ${PKG_MGR}"
}

# ---------------------------------------------------------------------------
# Directory creation
# ---------------------------------------------------------------------------
create_directories() {
    log_header "Creating Directory Structure"

    local dirs=(
        "commands"
        "templates/engagement"
        "templates/reports"
        "templates/findings"
        "templates/ctf"
        "templates/scripts"
        "tools/web"
        "tools/mobile"
        "tools/re"
        "tools/exploit"
        "tools/game"
        "tools/cloud"
        "tools/redteam"
        "tools/osint"
        "tools/forensics"
        "tools/ai-redteam"
        "tools/c2"
        "tools/common"
        "tools/mcp"
        "wordlists/web"
        "wordlists/api"
        "wordlists/subdomains"
        "wordlists/passwords"
        "wordlists/usernames"
        "wordlists/cloud"
        "wordlists/game"
        "methodology"
        "cheatsheets"
        "lab/docker"
        "lab/vm"
        "ctf"
        "engagements/_template"
        "examples"
    )

    for dir in "${dirs[@]}"; do
        if [[ ! -d "${ROOT_DIR}/${dir}" ]]; then
            mkdir -p "${ROOT_DIR}/${dir}"
            log_success "Created ${dir}/"
        fi
    done

    log_success "Directory structure ready"
}

# ---------------------------------------------------------------------------
# Category installers
# ---------------------------------------------------------------------------
install_category() {
    local category="$1"
    local script="${SCRIPT_DIR}/install-${category}.sh"

    if [[ -f "${script}" ]]; then
        log_header "Installing: ${category}"
        bash "${script}"
    else
        log_warn "Installer not found: ${script}"
    fi
}

# ---------------------------------------------------------------------------
# Interactive menu
# ---------------------------------------------------------------------------
show_menu() {
    log_header "AI-RedTeam-Toolkit Installer"

    echo -e "${BOLD}Select categories to install:${NC}\n"
    echo "  1) Web Application Pentesting    (nmap, sqlmap, ffuf, nuclei, ...)"
    echo "  2) Reverse Engineering            (ghidra, radare2, binwalk, ...)"
    echo "  3) Mobile Application Security    (jadx, apktool, frida, ...)"
    echo "  4) Exploitation Development       (pwntools, ROPgadget, ropper, ...)"
    echo "  5) Cloud Security                 (awscli, terraform, trivy, ...)"
    echo "  6) Red Team Operations            (impacket, bloodhound-python, ...)"
    echo "  7) OSINT                          (amass, theHarvester, dnsx, ... )"
    echo "  8) Digital Forensics              (volatility3, yara, tshark, ...)"
    echo "  9) Game Security                  (frida-tools, ghidra helpers, ... )"
    echo " 10) AI/LLM Security                (garak, promptfoo, ... )"
    echo " 11) MCP Integrations               (GhidraMCP, ...)"
    echo " 12) All of the above"
    echo " 13) Run tool check only"
    echo "  0) Exit"
    echo ""

    read -rp "Enter choices (comma-separated, e.g., 1,2,4): " choices

    IFS=',' read -ra selections <<< "${choices}"

    for sel in "${selections[@]}"; do
        sel="$(echo "${sel}" | tr -d '[:space:]')"
        case "${sel}" in
            1) install_category "web" ;;
            2) install_category "re" ;;
            3) install_category "mobile" ;;
            4) install_category "exploit" ;;
            5) install_category "cloud" ;;
            6) install_category "redteam" ;;
            7) install_category "osint" ;;
            8) install_category "forensics" ;;
            9) install_category "game" ;;
            10) install_category "ai-security" ;;
            11) install_category "mcps" ;;
            12)
                install_category "web"
                install_category "re"
                install_category "mobile"
                install_category "exploit"
                install_category "cloud"
                install_category "redteam"
                install_category "osint"
                install_category "forensics"
                install_category "game"
                install_category "ai-security"
                install_category "mcps"
                ;;
            13)
                run_check
                return
                ;;
            0)
                log_info "Exiting."
                exit 0
                ;;
            *)
                log_warn "Unknown option: ${sel}"
                ;;
        esac
    done
}

# ---------------------------------------------------------------------------
# Tool verification
# ---------------------------------------------------------------------------
run_check() {
    local check_script="${SCRIPT_DIR}/check-tools.sh"
    local consistency_script="${SCRIPT_DIR}/check-consistency.sh"

    if [[ -f "${check_script}" ]]; then
        bash "${check_script}"
    else
        log_error "check-tools.sh not found at ${check_script}"
        exit 1
    fi

    if [[ -f "${consistency_script}" ]]; then
        bash "${consistency_script}"
    else
        log_warn "check-consistency.sh not found at ${consistency_script}"
    fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
    echo -e "${BOLD}${CYAN}"
    echo "    _    ___      ____          _ _____                      "
    echo "   / \  |_ _|    |  _ \ ___  __| |_   _|__  __ _ _ __ ___  "
    echo "  / _ \  | |_____| |_) / _ \/ _\` | | |/ _ \/ _\` | '_ \` _ \ "
    echo " / ___ \ | |_____|  _ <  __/ (_| | | |  __/ (_| | | | | | |"
    echo "/_/   \_\___|    |_| \\_\\___|\\__,_| |_|\\___|\\__,_|_| |_| |_|"
    echo -e "${NC}"
    echo -e "${BOLD}AI-Powered Offensive Security Toolkit${NC}"
    echo ""

    detect_os
    detect_package_manager

    case "${1:-}" in
        --all)
            log_info "Installing all categories..."
            create_directories
            install_category "web"
            install_category "re"
            install_category "mobile"
            install_category "exploit"
            install_category "cloud"
            install_category "redteam"
            install_category "osint"
            install_category "forensics"
            install_category "game"
            install_category "ai-security"
            install_category "mcps"
            echo ""
            log_header "Running Tool Verification"
            run_check
            ;;
        --check)
            run_check
            ;;
        --dirs)
            create_directories
            ;;
        *)
            create_directories
            show_menu
            echo ""
            log_header "Running Tool Verification"
            run_check
            ;;
    esac

    echo ""
    log_success "Setup complete. Run 'setup/check-tools.sh' anytime to verify tools."
}

main "$@"
