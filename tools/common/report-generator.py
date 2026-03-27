#!/usr/bin/env python3
"""
report-generator.py - Automated Engagement Report Generator

Scans an engagement directory for finding files (Markdown), parses severity/CVSS
metadata, and compiles a formatted report with executive summary, table of
contents, risk ratings, and per-finding detail sections.

Usage:
    python3 report-generator.py --engagement engagements/target-corp/
    python3 report-generator.py --engagement engagements/target-corp/ --output report.md
    python3 report-generator.py --engagement engagements/target-corp/ --format json

Finding files are expected under <engagement>/findings/*.md with front-matter
style metadata:
    ---
    title: SQL Injection in Login
    severity: Critical
    cvss: 9.8
    category: Injection
    cwe: CWE-89
    status: Confirmed
    ---
    Description text follows...

Author : AI-RedTeam-Toolkit
License: MIT
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SEVERITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
    "informational": 4,
    "info": 4,
}

SEVERITY_LABELS = ["Critical", "High", "Medium", "Low", "Informational"]

RISK_THRESHOLDS = [
    # (min_score, label)
    (9.0, "Critical"),
    (7.0, "High"),
    (4.0, "Medium"),
    (0.1, "Low"),
    (0.0, "Informational"),
]


# ---------------------------------------------------------------------------
# Finding parser
# ---------------------------------------------------------------------------

_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_KV_RE = re.compile(r"^(\w[\w\-]*):\s*(.+)$", re.MULTILINE)


def parse_finding(filepath: Path) -> dict[str, Any] | None:
    """Parse a single finding Markdown file and return structured data."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"[!] Cannot read {filepath}: {exc}", file=sys.stderr)
        return None

    finding: dict[str, Any] = {
        "file": str(filepath),
        "title": filepath.stem.replace("_", " ").replace("-", " ").title(),
        "severity": "Informational",
        "cvss": 0.0,
        "category": "Uncategorized",
        "cwe": "",
        "status": "Unconfirmed",
        "description": text,
    }

    fm_match = _FRONT_MATTER_RE.match(text)
    if fm_match:
        front_matter = fm_match.group(1)
        for kv in _KV_RE.finditer(front_matter):
            key = kv.group(1).lower().strip()
            value = kv.group(2).strip()
            if key == "title":
                finding["title"] = value
            elif key == "severity":
                finding["severity"] = value.capitalize()
            elif key == "cvss":
                try:
                    finding["cvss"] = float(value)
                except ValueError:
                    pass
            elif key == "category":
                finding["category"] = value
            elif key == "cwe":
                finding["cwe"] = value
            elif key == "status":
                finding["status"] = value
        # Body is everything after front matter
        finding["description"] = text[fm_match.end():].strip()
    else:
        # Try to extract title from first Markdown heading
        heading = re.match(r"^#\s+(.+)$", text, re.MULTILINE)
        if heading:
            finding["title"] = heading.group(1).strip()

    return finding


def severity_sort_key(finding: dict[str, Any]) -> tuple[int, float, str]:
    """Sort key: severity order ascending, CVSS descending, then title."""
    sev = finding["severity"].lower()
    order = SEVERITY_ORDER.get(sev, 99)
    return (order, -finding["cvss"], finding["title"])


# ---------------------------------------------------------------------------
# Report generators
# ---------------------------------------------------------------------------

def compute_overall_risk(findings: list[dict[str, Any]]) -> str:
    """Derive overall engagement risk from the highest-severity finding."""
    if not findings:
        return "Informational"
    max_cvss = max(f["cvss"] for f in findings)
    for threshold, label in RISK_THRESHOLDS:
        if max_cvss >= threshold:
            return label
    return "Informational"


def severity_counts(findings: list[dict[str, Any]]) -> dict[str, int]:
    """Count findings per severity level."""
    counts: dict[str, int] = {label: 0 for label in SEVERITY_LABELS}
    for f in findings:
        sev = f["severity"].capitalize()
        # Normalize "Info" -> "Informational"
        if sev == "Info":
            sev = "Informational"
        counts[sev] = counts.get(sev, 0) + 1
    return counts


def generate_markdown_report(
    engagement_name: str,
    findings: list[dict[str, Any]],
    engagement_path: str,
) -> str:
    """Generate a full Markdown report."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sorted_findings = sorted(findings, key=severity_sort_key)
    counts = severity_counts(sorted_findings)
    overall_risk = compute_overall_risk(sorted_findings)
    total = len(sorted_findings)

    lines: list[str] = []

    # -- Header --
    lines.append(f"# Security Assessment Report: {engagement_name}")
    lines.append("")
    lines.append(f"**Generated:** {now}  ")
    lines.append(f"**Engagement:** `{engagement_path}`  ")
    lines.append(f"**Total Findings:** {total}  ")
    lines.append(f"**Overall Risk Rating:** **{overall_risk}**")
    lines.append("")
    lines.append("---")
    lines.append("")

    # -- Table of Contents --
    lines.append("## Table of Contents")
    lines.append("")
    lines.append("1. [Executive Summary](#executive-summary)")
    lines.append("2. [Risk Overview](#risk-overview)")
    lines.append("3. [Findings Summary Table](#findings-summary-table)")
    lines.append("4. [Detailed Findings](#detailed-findings)")
    lines.append("5. [Methodology Notes](#methodology-notes)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # -- Executive Summary --
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(
        f"This report presents the results of the security assessment for "
        f"**{engagement_name}**. A total of **{total}** finding(s) were "
        f"identified during the engagement."
    )
    lines.append("")
    if total > 0:
        lines.append("### Findings Breakdown by Severity")
        lines.append("")
        lines.append("| Severity        | Count |")
        lines.append("|-----------------|------:|")
        for label in SEVERITY_LABELS:
            count = counts.get(label, 0)
            lines.append(f"| {label:<15} | {count:>5} |")
        lines.append("")
        lines.append(
            f"The overall risk rating for this engagement is "
            f"**{overall_risk}**, determined by the highest-severity "
            f"finding (CVSS {max(f['cvss'] for f in sorted_findings):.1f})."
        )
    else:
        lines.append("No findings were identified during this engagement.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # -- Risk Overview --
    lines.append("## Risk Overview")
    lines.append("")
    if total > 0:
        # Simple text-based risk bar
        bar_parts: list[str] = []
        symbols = {
            "Critical": "X",
            "High": "!",
            "Medium": "#",
            "Low": "~",
            "Informational": ".",
        }
        for label in SEVERITY_LABELS:
            c = counts.get(label, 0)
            if c > 0:
                bar_parts.append(f"{symbols[label] * c}")
        lines.append(f"```")
        lines.append(f"Risk Distribution: [{''.join(bar_parts)}]")
        lines.append(f"Legend: X=Critical  !=High  #=Medium  ~=Low  .=Info")
        lines.append(f"```")
    else:
        lines.append("No risk indicators.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # -- Findings Summary Table --
    lines.append("## Findings Summary Table")
    lines.append("")
    if total > 0:
        lines.append("| # | Title | Severity | CVSS | Category | Status |")
        lines.append("|---|-------|----------|-----:|----------|--------|")
        for idx, f in enumerate(sorted_findings, 1):
            title = f["title"]
            sev = f["severity"]
            cvss = f"{f['cvss']:.1f}" if f["cvss"] > 0 else "N/A"
            cat = f["category"]
            status = f["status"]
            anchor = _make_anchor(f"finding-{idx}-{title}")
            lines.append(
                f"| {idx} | [{title}](#{anchor}) | {sev} | {cvss} | {cat} | {status} |"
            )
    else:
        lines.append("*No findings to display.*")
    lines.append("")
    lines.append("---")
    lines.append("")

    # -- Detailed Findings --
    lines.append("## Detailed Findings")
    lines.append("")
    for idx, f in enumerate(sorted_findings, 1):
        title = f["title"]
        anchor_title = f"Finding {idx}: {title}"
        lines.append(f"### {anchor_title}")
        lines.append("")
        lines.append(f"| Field    | Value |")
        lines.append(f"|----------|-------|")
        lines.append(f"| **Severity** | {f['severity']} |")
        cvss_str = f"{f['cvss']:.1f}" if f["cvss"] > 0 else "N/A"
        lines.append(f"| **CVSS**     | {cvss_str} |")
        lines.append(f"| **Category** | {f['category']} |")
        if f["cwe"]:
            lines.append(f"| **CWE**      | {f['cwe']} |")
        lines.append(f"| **Status**   | {f['status']} |")
        lines.append(f"| **Source**   | `{f['file']}` |")
        lines.append("")
        if f["description"]:
            lines.append(f["description"])
        else:
            lines.append("*No description provided.*")
        lines.append("")
        lines.append("---")
        lines.append("")

    # -- Methodology --
    lines.append("## Methodology Notes")
    lines.append("")
    lines.append(
        "This report was auto-generated by `report-generator.py` from the "
        "AI-RedTeam-Toolkit. Findings were parsed from individual Markdown "
        "files located in the engagement's `findings/` directory. Severity "
        "ratings follow CVSS v3.1 scoring guidelines."
    )
    lines.append("")
    lines.append(f"*Report generated on {now}*")
    lines.append("")

    return "\n".join(lines)


def generate_json_report(
    engagement_name: str,
    findings: list[dict[str, Any]],
    engagement_path: str,
) -> str:
    """Generate a JSON-formatted report."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sorted_findings = sorted(findings, key=severity_sort_key)
    counts = severity_counts(sorted_findings)
    overall_risk = compute_overall_risk(sorted_findings)

    report = {
        "report": {
            "title": f"Security Assessment Report: {engagement_name}",
            "generated": now,
            "engagement_path": engagement_path,
            "overall_risk": overall_risk,
            "total_findings": len(sorted_findings),
            "severity_counts": counts,
        },
        "findings": [
            {
                "id": idx,
                "title": f["title"],
                "severity": f["severity"],
                "cvss": f["cvss"],
                "category": f["category"],
                "cwe": f["cwe"],
                "status": f["status"],
                "source_file": f["file"],
                "description": f["description"],
            }
            for idx, f in enumerate(sorted_findings, 1)
        ],
    }
    return json.dumps(report, indent=2, ensure_ascii=False)


def _make_anchor(text: str) -> str:
    """Convert heading text to a GitHub-compatible anchor slug."""
    slug = text.lower()
    slug = re.sub(r"[^\w\s\-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    return slug


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def discover_findings(engagement_dir: Path) -> list[dict[str, Any]]:
    """Find and parse all finding files under the engagement directory."""
    findings_dir = engagement_dir / "findings"
    if not findings_dir.is_dir():
        print(
            f"[!] Findings directory not found: {findings_dir}",
            file=sys.stderr,
        )
        return []

    finding_files = sorted(findings_dir.glob("*.md"))
    if not finding_files:
        print(f"[*] No .md files found in {findings_dir}", file=sys.stderr)
        return []

    findings: list[dict[str, Any]] = []
    for fp in finding_files:
        parsed = parse_finding(fp)
        if parsed:
            findings.append(parsed)

    print(f"[+] Parsed {len(findings)} finding(s) from {findings_dir}", file=sys.stderr)
    return findings


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Auto-compile engagement findings into a formatted report.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --engagement engagements/target-corp/\n"
            "  %(prog)s --engagement engagements/target-corp/ --output report.md\n"
            "  %(prog)s --engagement engagements/target-corp/ --format json\n"
        ),
    )
    parser.add_argument(
        "--engagement",
        required=True,
        help="Path to the engagement directory (must contain findings/*.md).",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output file path. Defaults to stdout.",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "md", "json"],
        default="markdown",
        dest="fmt",
        help="Output format (default: markdown).",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    engagement_path = Path(args.engagement).resolve()
    if not engagement_path.is_dir():
        print(
            f"[!] Engagement directory does not exist: {engagement_path}",
            file=sys.stderr,
        )
        return 1

    engagement_name = engagement_path.name
    findings = discover_findings(engagement_path)

    if args.fmt in ("markdown", "md"):
        report = generate_markdown_report(
            engagement_name, findings, str(engagement_path)
        )
    else:
        report = generate_json_report(
            engagement_name, findings, str(engagement_path)
        )

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"[+] Report written to {out_path}", file=sys.stderr)
    else:
        print(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
