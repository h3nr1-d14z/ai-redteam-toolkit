# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mcp>=1.2.0,<2",
# ]
# ///

"""
MCP server wrapping the Nmap network scanner CLI.

Requires Nmap to be installed and available on PATH:
    - macOS: brew install nmap
    - Linux: sudo apt install nmap
    - Windows: https://nmap.org/download.html

Note: Some scan types (SYN, OS detection) require root/admin privileges.
"""

import os
import subprocess
import tempfile
import uuid
import logging
import xml.etree.ElementTree as ET
from pathlib import Path

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

mcp = FastMCP("nmap-mcp")

RESULTS_DIR = Path(tempfile.gettempdir()) / "nmap-mcp-results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

NMAP_BIN = os.environ.get("NMAP_PATH", "nmap")


def _run_nmap(args: list[str], timeout: int = 300) -> tuple[str, str | None]:
    """
    Run an nmap command. Returns (stdout, xml_file_path_or_None).
    """
    scan_id = str(uuid.uuid4())[:8]
    xml_path = RESULTS_DIR / f"{scan_id}.xml"

    cmd = [NMAP_BIN] + args + ["-oX", str(xml_path)]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout.strip()
        if result.returncode != 0 and result.stderr.strip():
            output += f"\n[stderr]: {result.stderr.strip()}"

        xml_file = str(xml_path) if xml_path.exists() else None
        return output if output else "(no output)", xml_file
    except FileNotFoundError:
        return f"Error: nmap binary not found at '{NMAP_BIN}'. Install nmap or set NMAP_PATH.", None
    except subprocess.TimeoutExpired:
        return f"Error: scan timed out after {timeout}s", None
    except Exception as e:
        return f"Error running nmap: {e}", None


def _parse_xml(xml_path: str) -> str:
    """Parse nmap XML output into a human-readable summary."""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        return f"Error parsing XML: {e}"
    except FileNotFoundError:
        return f"XML file not found: {xml_path}"

    lines = []

    # Scan info
    scan_info = root.find("scaninfo")
    if scan_info is not None:
        lines.append(
            f"Scan type: {scan_info.get('type', 'N/A')} | "
            f"Protocol: {scan_info.get('protocol', 'N/A')} | "
            f"Services: {scan_info.get('services', 'N/A')}"
        )

    # Run stats
    runstats = root.find("runstats/finished")
    if runstats is not None:
        lines.append(
            f"Elapsed: {runstats.get('elapsed', '?')}s | "
            f"Summary: {runstats.get('summary', 'N/A')}"
        )

    lines.append("")

    # Hosts
    for host in root.findall("host"):
        addr_el = host.find("address")
        addr = addr_el.get("addr", "unknown") if addr_el is not None else "unknown"

        hostnames = []
        for hn in host.findall("hostnames/hostname"):
            hostnames.append(hn.get("name", ""))
        hostname_str = f" ({', '.join(hostnames)})" if hostnames else ""

        status_el = host.find("status")
        status = status_el.get("state", "unknown") if status_el is not None else "unknown"

        lines.append(f"Host: {addr}{hostname_str} [{status}]")

        # OS detection
        for osmatch in host.findall("os/osmatch"):
            lines.append(
                f"  OS: {osmatch.get('name', 'N/A')} "
                f"(accuracy: {osmatch.get('accuracy', '?')}%)"
            )

        # Ports
        for port in host.findall("ports/port"):
            port_id = port.get("portid", "?")
            protocol = port.get("protocol", "?")

            state_el = port.find("state")
            state = state_el.get("state", "?") if state_el is not None else "?"

            service_el = port.find("service")
            if service_el is not None:
                svc_name = service_el.get("name", "")
                svc_product = service_el.get("product", "")
                svc_version = service_el.get("version", "")
                svc_info = f"{svc_name}"
                if svc_product:
                    svc_info += f" {svc_product}"
                if svc_version:
                    svc_info += f" {svc_version}"
            else:
                svc_info = ""

            lines.append(f"  {port_id}/{protocol}  {state:8s}  {svc_info}")

            # Script output
            for script in port.findall("script"):
                script_id = script.get("id", "")
                script_out = script.get("output", "").strip()
                if script_out:
                    # Indent multi-line script output
                    indented = script_out.replace("\n", "\n      ")
                    lines.append(f"    |_ {script_id}: {indented}")

        # Host scripts
        for script in host.findall("hostscript/script"):
            script_id = script.get("id", "")
            script_out = script.get("output", "").strip()
            if script_out:
                indented = script_out.replace("\n", "\n      ")
                lines.append(f"  [host-script] {script_id}: {indented}")

        lines.append("")

    return "\n".join(lines) if lines else "No results parsed from XML."


@mcp.tool()
def port_scan(
    target: str,
    ports: str = "",
    scan_type: str = "connect",
    timeout: int = 300,
) -> str:
    """
    Run a port scan against a target.

    Args:
        target: Target IP, hostname, or CIDR range (e.g. "192.168.1.0/24")
        ports: Port specification (e.g. "22,80,443", "1-1000", "-" for all). Empty = nmap default (top 1000)
        scan_type: Scan type — "connect" (TCP connect), "syn" (SYN, needs root),
                   "udp" (UDP, needs root), "fin", "xmas", "null", "ping"
        timeout: Maximum scan duration in seconds (default: 300)

    Returns:
        Parsed scan results showing open ports, services, and host info
    """
    type_flags = {
        "connect": "-sT",
        "syn": "-sS",
        "udp": "-sU",
        "fin": "-sF",
        "xmas": "-sX",
        "null": "-sN",
        "ping": "-sn",
    }

    args = [type_flags.get(scan_type, "-sT")]
    if ports:
        args.extend(["-p", ports])
    args.append(target)

    raw_output, xml_file = _run_nmap(args, timeout=timeout)

    if xml_file:
        parsed = _parse_xml(xml_file)
        return f"[XML results file: {xml_file}]\n\n{parsed}"
    else:
        return raw_output


@mcp.tool()
def service_scan(target: str, ports: str = "", timeout: int = 300) -> str:
    """
    Run service version detection scan against a target.

    Uses nmap -sV to probe open ports and determine service/version info.

    Args:
        target: Target IP, hostname, or CIDR range
        ports: Port specification (empty = top 1000 ports)
        timeout: Maximum scan duration in seconds (default: 300)

    Returns:
        Detected services with version information
    """
    args = ["-sV", "--version-intensity", "5"]
    if ports:
        args.extend(["-p", ports])
    args.append(target)

    raw_output, xml_file = _run_nmap(args, timeout=timeout)

    if xml_file:
        parsed = _parse_xml(xml_file)
        return f"[XML results file: {xml_file}]\n\n{parsed}"
    else:
        return raw_output


@mcp.tool()
def script_scan(
    target: str,
    scripts: str = "default",
    ports: str = "",
    script_args: str = "",
    timeout: int = 300,
) -> str:
    """
    Run Nmap Scripting Engine (NSE) scripts against a target.

    Args:
        target: Target IP, hostname, or CIDR range
        scripts: NSE script names or categories, comma-separated
                 (e.g. "default", "vuln", "http-enum,http-headers",
                  "ssl-enum-ciphers", "smb-vuln*")
        ports: Port specification (empty = top 1000 ports)
        script_args: Script arguments (e.g. "httpspider.maxdepth=5")
        timeout: Maximum scan duration in seconds (default: 300)

    Returns:
        Script output with findings per host and port
    """
    args = ["-sC" if scripts == "default" else f"--script={scripts}"]
    if ports:
        args.extend(["-p", ports])
    if script_args:
        args.extend(["--script-args", script_args])
    args.append(target)

    raw_output, xml_file = _run_nmap(args, timeout=timeout)

    if xml_file:
        parsed = _parse_xml(xml_file)
        return f"[XML results file: {xml_file}]\n\n{parsed}"
    else:
        return raw_output


@mcp.tool()
def parse_results(xml_file: str) -> str:
    """
    Parse an existing Nmap XML output file into a readable summary.

    Args:
        xml_file: Absolute path to an nmap XML output file

    Returns:
        Parsed and formatted scan results
    """
    if not os.path.isfile(xml_file):
        return f"Error: file not found: {xml_file}"
    return _parse_xml(xml_file)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="MCP server for Nmap scanner")
    parser.add_argument(
        "--transport",
        type=str,
        default="stdio",
        choices=["stdio", "sse"],
        help="Transport protocol (default: stdio)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host for SSE transport (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8083,
        help="Port for SSE transport (default: 8083)",
    )
    args = parser.parse_args()

    if args.transport == "sse":
        logging.basicConfig(level=logging.INFO)
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        logger.info(f"Starting Nmap MCP on http://{args.host}:{args.port}/sse")
        mcp.run(transport="sse")
    else:
        mcp.run()


if __name__ == "__main__":
    main()
