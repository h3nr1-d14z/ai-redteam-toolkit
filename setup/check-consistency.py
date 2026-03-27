#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def extract_backtick_commands(text: str) -> set[str]:
    return set(re.findall(r"`/([a-z0-9-]+)`", text))


def main() -> int:
    failures: list[str] = []
    infos: list[str] = []

    commands_dir = ROOT / "commands"
    readme = ROOT / "README.md"
    claude = ROOT / "CLAUDE.md"
    mcp = ROOT / ".mcp.json"

    command_files = sorted(p.stem for p in commands_dir.glob("*.md"))
    command_set = set(command_files)

    if not command_files:
        failures.append("No command files found in commands/*.md")
    else:
        infos.append(f"commands/*.md count: {len(command_files)}")

    readme_text = readme.read_text(encoding="utf-8")
    claude_text = claude.read_text(encoding="utf-8")

    for source_name, text in (("README.md", readme_text), ("CLAUDE.md", claude_text)):
        documented = extract_backtick_commands(text)
        missing = sorted(documented - command_set)
        undocumented = sorted(command_set - documented)
        if missing:
            failures.append(f"{source_name} has commands missing files: {', '.join(missing)}")
        if undocumented:
            failures.append(f"{source_name} is missing documented entries for: {', '.join(undocumented)}")
        infos.append(f"{source_name} documented command count: {len(documented)}")

    banned_layout_patterns = [
        r"commands/<domain>/",
        r"commands/web/",
        r"commands/mobile/",
        r"commands/re/",
        r"commands/exploit/",
        r"commands/game/",
        r"commands/cloud/",
        r"commands/redteam/",
        r"commands/osint/",
        r"commands/forensics/",
        r"commands/ctf/",
        r"commands/ai-security/",
    ]

    for pattern in banned_layout_patterns:
        if re.search(pattern, readme_text) or re.search(pattern, claude_text):
            failures.append(f"Banned legacy commands layout pattern found: {pattern}")

    commands_with_targets = []
    for path in commands_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if "targets/" in text:
            commands_with_targets.append(path.name)
    if commands_with_targets:
        failures.append("Found stale targets/ references in commands: " + ", ".join(sorted(commands_with_targets)))

    required_paths = [
        ROOT / "GETTING_STARTED.md",
        ROOT / "DEEPTEAM_LEARNINGS.md",
        ROOT / "CHANGELOG.md",
        ROOT / "tools" / "c2",
        ROOT / "wordlists" / "passwords",
        ROOT / "setup" / "install-cloud.sh",
        ROOT / "setup" / "install-redteam.sh",
        ROOT / "setup" / "install-osint.sh",
        ROOT / "setup" / "install-forensics.sh",
        ROOT / "setup" / "install-game.sh",
        ROOT / "setup" / "install-ai-security.sh",
        ROOT / "setup" / "install-wsl.sh",
    ]

    for path in required_paths:
        if not path.exists():
            failures.append(f"Missing required path: {path.relative_to(ROOT)}")

    try:
        mcp_data = json.loads(mcp.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"Failed to parse .mcp.json: {exc}")
        mcp_data = {}

    if mcp_data:
        blob = json.dumps(mcp_data)
        if "/Users/" in blob or re.search(r"[A-Za-z]:\\\\", blob) or "/home/" in blob:
            failures.append(".mcp.json contains absolute user-specific paths")

    print("[check-consistency] INFO")
    for info in infos:
        print(f"- {info}")

    if failures:
        print("\n[check-consistency] FAIL")
        for item in failures:
            print(f"- {item}")
        return 1

    print("\n[check-consistency] PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
