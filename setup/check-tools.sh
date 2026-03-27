#!/usr/bin/env bash
# check-tools.sh - Verify installed security tools across all categories
#
# Usage: ./setup/check-tools.sh
#
# Outputs a formatted table showing installed/missing status for each tool.

set -euo pipefail

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# ---------------------------------------------------------------------------
# Counters
# ---------------------------------------------------------------------------
TOTAL=0
INSTALLED=0
MISSING=0

# ---------------------------------------------------------------------------
# Check functions
# ---------------------------------------------------------------------------
check_command() {
    local name="$1"
    local cmd="${2:-$1}"

    TOTAL=$((TOTAL + 1))

    if command -v "${cmd}" &>/dev/null; then
        local version
        version=$( (${cmd} --version 2>/dev/null || ${cmd} -version 2>/dev/null || ${cmd} -V 2>/dev/null || echo "installed") | head -1 | cut -c1-40)
        printf "  ${GREEN}%-4s${NC} %-20s ${DIM}%s${NC}\n" "[OK]" "${name}" "${version}"
        INSTALLED=$((INSTALLED + 1))
    else
        printf "  ${RED}%-4s${NC} %-20s ${DIM}%s${NC}\n" "[--]" "${name}" "not found"
        MISSING=$((MISSING + 1))
    fi
}

check_python_package() {
    local name="$1"
    local pkg="${2:-$1}"

    TOTAL=$((TOTAL + 1))

    if python3 -c "import ${pkg}" &>/dev/null 2>&1; then
        local version
        version=$(python3 -c "import ${pkg}; print(getattr(${pkg}, '__version__', 'installed'))" 2>/dev/null || echo "installed")
        printf "  ${GREEN}%-4s${NC} %-20s ${DIM}%s${NC}\n" "[OK]" "${name} (py)" "${version}"
        INSTALLED=$((INSTALLED + 1))
    else
        printf "  ${RED}%-4s${NC} %-20s ${DIM}%s${NC}\n" "[--]" "${name} (py)" "not found"
        MISSING=$((MISSING + 1))
    fi
}

check_gem() {
    local name="$1"

    TOTAL=$((TOTAL + 1))

    if gem list -i "^${name}$" &>/dev/null 2>&1; then
        printf "  ${GREEN}%-4s${NC} %-20s ${DIM}%s${NC}\n" "[OK]" "${name} (gem)" "installed"
        INSTALLED=$((INSTALLED + 1))
    else
        printf "  ${RED}%-4s${NC} %-20s ${DIM}%s${NC}\n" "[--]" "${name} (gem)" "not found"
        MISSING=$((MISSING + 1))
    fi
}

check_path_exists() {
    local name="$1"
    local path="$2"

    TOTAL=$((TOTAL + 1))

    if [[ -e "${path}" ]]; then
        printf "  ${GREEN}%-4s${NC} %-20s ${DIM}%s${NC}\n" "[OK]" "${name}" "${path}"
        INSTALLED=$((INSTALLED + 1))
    else
        printf "  ${RED}%-4s${NC} %-20s ${DIM}%s${NC}\n" "[--]" "${name}" "not found"
        MISSING=$((MISSING + 1))
    fi
}

section_header() {
    echo ""
    echo -e "${BOLD}${CYAN}  $1${NC}"
    echo -e "  ${DIM}$(printf '%.0s-' {1..50})${NC}"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
    echo ""
    echo -e "${BOLD}${CYAN}============================================${NC}"
    echo -e "${BOLD}${CYAN}  AI-RedTeam-Toolkit - Tool Verification    ${NC}"
    echo -e "${BOLD}${CYAN}============================================${NC}"

    # --- Web Pentesting ---
    section_header "Web Application Pentesting"
    check_command "nmap"
    check_command "sqlmap"
    check_command "ffuf"
    check_command "nuclei"
    check_command "subfinder"
    check_command "httpx"
    check_command "dalfox"
    check_command "arjun"
    check_command "whatweb"
    check_command "nikto"
    check_command "curl"
    check_command "jq"

    # --- Reverse Engineering ---
    section_header "Reverse Engineering"
    check_command "ghidra" "ghidraRun"
    if [[ -d "/Applications/ghidra"* ]] 2>/dev/null || [[ -d "/opt/ghidra"* ]] 2>/dev/null; then
        printf "  ${GREEN}%-4s${NC} %-20s ${DIM}%s${NC}\n" "[OK]" "ghidra (app)" "found in Applications or /opt"
        # Don't double-count if command check already passed
    fi
    check_command "radare2" "r2"
    check_command "binwalk"
    check_command "checksec"
    check_command "strings"
    check_command "objdump"
    check_command "file"

    # --- Mobile Security ---
    section_header "Mobile Application Security"
    check_command "jadx"
    check_command "apktool"
    check_command "frida" "frida"
    check_command "objection"
    check_command "mitmproxy"
    check_command "adb"

    # --- Exploitation Development ---
    section_header "Exploitation Development"
    check_python_package "pwntools" "pwn"
    check_command "ROPgadget"
    check_command "ropper"
    check_gem "one_gadget"
    check_command "nasm"
    check_command "gdb"
    check_command "gcc"
    check_command "make"

    # --- General Utilities ---
    section_header "General Utilities"
    check_command "python3"
    check_command "pip3"
    check_command "git"
    check_command "docker"
    check_command "tmux"
    check_command "wget"
    check_command "openssl"

    # --- Summary ---
    echo ""
    echo -e "${BOLD}${CYAN}============================================${NC}"
    echo -e "${BOLD}  Summary${NC}"
    echo -e "${BOLD}${CYAN}============================================${NC}"
    echo ""
    echo -e "  Total tools checked:  ${BOLD}${TOTAL}${NC}"
    echo -e "  Installed:            ${GREEN}${BOLD}${INSTALLED}${NC}"
    echo -e "  Missing:              ${RED}${BOLD}${MISSING}${NC}"
    echo ""

    if [[ ${MISSING} -eq 0 ]]; then
        echo -e "  ${GREEN}${BOLD}All tools are installed.${NC}"
    elif [[ ${MISSING} -le 5 ]]; then
        echo -e "  ${YELLOW}${BOLD}Most tools are installed. Run category installers for missing tools.${NC}"
    else
        echo -e "  ${RED}${BOLD}Several tools are missing. Run: ./setup/install.sh${NC}"
    fi
    echo ""
}

main "$@"
