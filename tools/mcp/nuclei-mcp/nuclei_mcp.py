# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mcp>=1.2.0,<2",
# ]
# ///

"""
MCP server wrapping the Nuclei vulnerability scanner CLI.

Requires Nuclei to be installed and available on PATH:
    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

Or via Homebrew:
    brew install nuclei
"""

import json
import os
import subprocess
import tempfile
import uuid
import logging
from pathlib import Path

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

mcp = FastMCP("nuclei-mcp")

# Directory to store scan results
RESULTS_DIR = Path(tempfile.gettempdir()) / "nuclei-mcp-results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

NUCLEI_BIN = os.environ.get("NUCLEI_PATH", "nuclei")


def _run_nuclei(args: list[str], timeout: int = 300) -> str:
    """Run a nuclei command and return stdout."""
    cmd = [NUCLEI_BIN] + args
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
        return output if output else "(no output)"
    except FileNotFoundError:
        return f"Error: nuclei binary not found at '{NUCLEI_BIN}'. Install nuclei or set NUCLEI_PATH."
    except subprocess.TimeoutExpired:
        return f"Error: scan timed out after {timeout}s"
    except Exception as e:
        return f"Error running nuclei: {e}"


@mcp.tool()
def scan(
    target: str,
    severity: str = "",
    templates: str = "",
    extra_args: str = "",
    timeout: int = 300,
) -> str:
    """
    Run a Nuclei vulnerability scan against a target.

    Args:
        target: Target URL or host (e.g. "https://example.com")
        severity: Comma-separated severity filter (e.g. "critical,high,medium")
        templates: Comma-separated template IDs or paths (e.g. "cves/,exposures/")
        extra_args: Additional CLI flags passed directly to nuclei
        timeout: Maximum scan duration in seconds (default: 300)

    Returns:
        Scan results including a scan_id for later retrieval, plus findings
    """
    scan_id = str(uuid.uuid4())[:8]
    output_file = RESULTS_DIR / f"{scan_id}.jsonl"

    args = ["-target", target, "-jsonl", "-output", str(output_file), "-silent"]

    if severity:
        args.extend(["-severity", severity])
    if templates:
        args.extend(["-templates", templates])
    if extra_args:
        args.extend(extra_args.split())

    raw = _run_nuclei(args, timeout=timeout)

    # Read structured results if available
    findings = []
    if output_file.exists():
        for line in output_file.read_text().splitlines():
            try:
                findings.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    summary_lines = [
        f"Scan ID: {scan_id}",
        f"Target: {target}",
        f"Findings: {len(findings)}",
        "",
    ]

    for f in findings:
        info = f.get("info", {})
        summary_lines.append(
            f"  [{info.get('severity', 'unknown').upper()}] "
            f"{info.get('name', 'N/A')} - {f.get('matched-at', 'N/A')}"
        )

    if not findings:
        summary_lines.append("  No vulnerabilities found (or scan produced no structured output).")
        if raw and not raw.startswith("Error"):
            summary_lines.append(f"\nRaw output:\n{raw}")

    return "\n".join(summary_lines)


@mcp.tool()
def list_templates(category: str = "", severity: str = "") -> str:
    """
    List available Nuclei templates.

    Args:
        category: Filter by template category/directory (e.g. "cves", "exposures", "misconfiguration")
        severity: Filter by severity level (e.g. "critical", "high")

    Returns:
        List of matching template IDs
    """
    args = ["-tl", "-silent"]
    if severity:
        args.extend(["-severity", severity])
    if category:
        args.extend(["-templates", category])
    return _run_nuclei(args, timeout=60)


@mcp.tool()
def get_results(scan_id: str) -> str:
    """
    Retrieve results from a previous scan by its scan ID.

    Args:
        scan_id: The scan ID returned by a previous scan() call

    Returns:
        JSON-lines formatted scan results, or an error if not found
    """
    output_file = RESULTS_DIR / f"{scan_id}.jsonl"
    if not output_file.exists():
        return f"No results found for scan_id '{scan_id}'. Check the ID and try again."

    content = output_file.read_text().strip()
    if not content:
        return f"Scan {scan_id} completed but produced no findings."

    findings = []
    for line in content.splitlines():
        try:
            finding = json.loads(line)
            info = finding.get("info", {})
            findings.append(
                f"[{info.get('severity', 'unknown').upper()}] "
                f"{info.get('name', 'N/A')} - {finding.get('matched-at', 'N/A')}"
            )
        except json.JSONDecodeError:
            findings.append(line)

    return f"Results for scan {scan_id} ({len(findings)} findings):\n" + "\n".join(findings)


@mcp.tool()
def get_template_info(template_id: str) -> str:
    """
    Show detailed information about a specific Nuclei template.

    Args:
        template_id: Template ID or path (e.g. "cves/2023/CVE-2023-12345")

    Returns:
        Template metadata including name, author, severity, description, and tags
    """
    args = ["-templates", template_id, "-tl", "-silent", "-json"]
    output = _run_nuclei(args, timeout=30)

    # Also try to show the template content by locating it
    # nuclei -templates <id> -validate gives useful info
    validate_args = ["-templates", template_id, "-validate", "-silent"]
    validation = _run_nuclei(validate_args, timeout=30)

    result_lines = [f"Template: {template_id}", ""]
    if output and not output.startswith("Error"):
        result_lines.append(f"Listing output:\n{output}")
    if validation and not validation.startswith("Error"):
        result_lines.append(f"\nValidation:\n{validation}")

    if all(
        line.startswith("Error") or line == "(no output)"
        for line in [output, validation]
    ):
        result_lines.append("Could not retrieve template info. Verify the template ID exists.")

    return "\n".join(result_lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="MCP server for Nuclei scanner")
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
        default=8082,
        help="Port for SSE transport (default: 8082)",
    )
    args = parser.parse_args()

    if args.transport == "sse":
        logging.basicConfig(level=logging.INFO)
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        logger.info(f"Starting Nuclei MCP on http://{args.host}:{args.port}/sse")
        mcp.run(transport="sse")
    else:
        mcp.run()


if __name__ == "__main__":
    main()
