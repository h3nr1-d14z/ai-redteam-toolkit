#!/usr/bin/env bash
# install-mcps.sh - Install and configure MCP (Model Context Protocol) servers
#
# Usage: ./setup/install-mcps.sh
#
# Currently supports:
#   - GhidraMCP (Ghidra bridge for AI-assisted reverse engineering)
#
# Future MCPs can be added by following the pattern below.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[*]${NC} $1"; }
log_success() { echo -e "${GREEN}[+]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[!]${NC} $1"; }
log_error()   { echo -e "${RED}[-]${NC} $1"; }
log_header()  { echo -e "\n${BOLD}${CYAN}--- $1 ---${NC}\n"; }

# ---------------------------------------------------------------------------
# GhidraMCP Installation
# ---------------------------------------------------------------------------
install_ghidra_mcp() {
    log_header "GhidraMCP Setup"

    local mcp_dir="${ROOT_DIR}/tools/mcp/ghidra"
    mkdir -p "${mcp_dir}"

    # Check for Java (required by Ghidra)
    if ! command -v java &>/dev/null; then
        log_warn "Java not found. Ghidra and GhidraMCP require Java 17+."
        log_info "Install Java first:"
        if [[ "$(uname -s)" == "Darwin" ]]; then
            log_info "  brew install openjdk@17"
        else
            log_info "  sudo apt install openjdk-17-jdk"
        fi
        return 1
    fi

    local java_version
    java_version=$(java -version 2>&1 | head -1 | cut -d'"' -f2 | cut -d'.' -f1)
    log_info "Java version detected: ${java_version}"

    if [[ "${java_version}" -lt 17 ]] 2>/dev/null; then
        log_warn "Java 17+ is recommended for Ghidra. Current version: ${java_version}"
    fi

    # Check if GhidraMCP is already cloned
    if [[ -d "${mcp_dir}/GhidraMCP" ]]; then
        log_info "GhidraMCP repository already exists. Updating..."
        cd "${mcp_dir}/GhidraMCP"
        git pull --ff-only 2>/dev/null || log_warn "Could not update GhidraMCP repo"
    else
        log_info "Cloning GhidraMCP..."
        if git clone https://github.com/LaurieWired/GhidraMCP.git "${mcp_dir}/GhidraMCP" 2>/dev/null; then
            log_success "GhidraMCP cloned successfully"
        else
            log_error "Failed to clone GhidraMCP. Check network connectivity."
            return 1
        fi
    fi

    # Build GhidraMCP
    cd "${mcp_dir}/GhidraMCP"
    if [[ -f "build.gradle" ]]; then
        log_info "Building GhidraMCP..."
        if ./gradlew buildExtension 2>/dev/null; then
            log_success "GhidraMCP built successfully"
        else
            log_warn "GhidraMCP build failed. Check Java version and Ghidra installation."
            log_info "You may need to set GHIDRA_INSTALL_DIR environment variable."
        fi
    fi

    # Validate .mcp.json configuration
    validate_mcp_config

    log_success "GhidraMCP setup complete"
}

# ---------------------------------------------------------------------------
# MCP Configuration Validation
# ---------------------------------------------------------------------------
validate_mcp_config() {
    log_header "Validating MCP Configuration"

    local mcp_config="${ROOT_DIR}/.mcp.json"

    if [[ -f "${mcp_config}" ]]; then
        log_info "Found .mcp.json at ${mcp_config}"

        # Basic JSON validation
        if command -v jq &>/dev/null; then
            if jq empty "${mcp_config}" 2>/dev/null; then
                log_success ".mcp.json is valid JSON"

                # Check for mcpServers key
                if jq -e '.mcpServers' "${mcp_config}" &>/dev/null; then
                    local server_count
                    server_count=$(jq '.mcpServers | length' "${mcp_config}")
                    log_info "Found ${server_count} MCP server(s) configured"

                    # List configured servers
                    jq -r '.mcpServers | keys[]' "${mcp_config}" 2>/dev/null | while read -r server; do
                        log_info "  - ${server}"
                    done
                else
                    log_warn ".mcp.json exists but has no 'mcpServers' key"
                fi
            else
                log_error ".mcp.json contains invalid JSON"
            fi
        else
            log_warn "jq not installed, skipping JSON validation"
        fi
    else
        log_info "No .mcp.json found. Creating example configuration..."

        cat > "${mcp_config}" << 'MCPJSON'
{
  "mcpServers": {
    "ghidra": {
      "command": "python3",
      "args": ["-m", "ghidra_mcp"],
      "env": {}
    }
  }
}
MCPJSON

        log_success "Created example .mcp.json at ${mcp_config}"
        log_info "Edit this file to match your MCP server configuration."
    fi
}

# ---------------------------------------------------------------------------
# Future MCP: Template
# ---------------------------------------------------------------------------
# install_future_mcp() {
#     log_header "Future MCP Setup"
#     local mcp_dir="${ROOT_DIR}/tools/mcp/future-mcp"
#     mkdir -p "${mcp_dir}"
#     # Installation steps here
#     log_success "Future MCP setup complete"
# }

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
    echo -e "${BOLD}${CYAN}MCP Integration Installer${NC}"
    echo ""

    install_ghidra_mcp

    echo ""
    log_header "MCP Installation Summary"
    log_info "Installed MCPs:"
    log_info "  - GhidraMCP (Ghidra bridge for AI-assisted RE)"
    echo ""
    log_info "To add new MCPs, edit setup/install-mcps.sh"
    log_info "MCP configuration: .mcp.json in project root"
    echo ""
}

main "$@"
