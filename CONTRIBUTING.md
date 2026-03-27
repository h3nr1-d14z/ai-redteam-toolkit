# Contributing to AI-RedTeam-Toolkit

Thank you for your interest in contributing. This guide explains how to add slash commands, templates, tools, and other content to the toolkit.

## Table of Contents

- [Getting Started](#getting-started)
- [Adding Slash Commands](#adding-slash-commands)
- [Adding Templates](#adding-templates)
- [Adding Tools](#adding-tools)
- [Adding Wordlists](#adding-wordlists)
- [Adding Lab Environments](#adding-lab-environments)
- [Adding MCP Integrations](#adding-mcp-integrations)
- [Code Standards](#code-standards)
- [Pull Request Process](#pull-request-process)

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes following the guidelines below
4. Test your changes
5. Submit a pull request

## Adding Slash Commands

Slash commands live in a flat directory: `commands/*.md`. Each command is a markdown file that serves as the AI instruction set.

### File Structure

```
commands/<command-name>.md
```

### Command File Format

Use the current repository command format:

```markdown
Run <clear action description> on: $ARGUMENTS

1. **Step name**: Action details
2. **Step name**: Action details
3. **Step name**: Action details

Tools: tool-a, tool-b
Save findings to `engagements/<target>/...`
```

### Naming Conventions

- Use lowercase with hyphens: `sql-inject.md`, not `SQLInject.md`
- Be descriptive: `cloud-enum-s3.md`, not `s3.md`
- Keep one command per file and choose names users can invoke directly (for example `sqli-test.md` maps to `/sqli-test`)

### Domain Coverage

Keep command naming consistent with existing domains (web, mobile, reverse engineering, exploit dev, game, cloud, red team, osint, forensics, ctf, ai security) while still storing files in `commands/`.

## Adding Templates

Templates live in `templates/`. They provide starting points for common tasks.

### Engagement Templates

Place in `templates/engagement/`:

```markdown
# [Template Name]

## Target Information
- **Name**: [TARGET_NAME]
- **Type**: [web|mobile|game|binary|cloud|network]
- **Environment**: [production|staging|development|lab]

## Scope
[Define in-scope and out-of-scope items]

## Methodology
[Step-by-step approach]
```

### Report Templates

Place in `templates/reports/`:

- Follow CVSS v3.1 scoring
- Include executive summary section
- Include technical details section
- Include remediation recommendations
- Include appendices for raw data

### Finding Templates

Place in `templates/findings/`:

```markdown
# [Finding Title]

- **Severity**: [Critical|High|Medium|Low|Informational]
- **CVSS Score**: [0.0-10.0]
- **CVSS Vector**: [CVSS:3.1/...]
- **CWE**: [CWE-XXX]

## Description
[What the vulnerability is]

## Impact
[What an attacker can do]

## Reproduction Steps
1. [Step by step]

## Evidence
[Screenshots, code, logs]

## Remediation
[How to fix it]
```

## Adding Tools

Custom tools go in `tools/<domain>/`. Each tool should be a self-contained script or small project.

### Requirements

1. Include a header comment explaining purpose and usage
2. Handle errors gracefully
3. Include `--help` output
4. Follow the language conventions below
5. Add any dependencies to the relevant installer in `setup/`

### Example Tool Header (Python)

```python
#!/usr/bin/env python3
"""
tool-name - Brief description of what this tool does.

Usage:
    python3 tool-name.py [options] <target>

Options:
    -h, --help     Show this help message
    -o, --output   Output file path
    -v, --verbose  Verbose output

Author: Your Name
License: MIT
"""
```

### Example Tool Header (Bash)

```bash
#!/usr/bin/env bash
# tool-name - Brief description of what this tool does.
#
# Usage: ./tool-name.sh [options] <target>
#
# Options:
#   -h, --help     Show this help message
#   -o, --output   Output file path
#   -v, --verbose  Verbose output
```

## Adding Wordlists

Custom wordlists go in `wordlists/<category>/`.

### Guidelines

- Keep wordlists focused and curated (not massive dumps)
- Include a comment header explaining the purpose
- Sort entries alphabetically where applicable
- Remove duplicates
- Do not include default credentials for real services
- Name descriptively: `graphql-field-names.txt`, not `list1.txt`

### Categories

| Directory | Content |
|-----------|---------|
| `wordlists/web/` | Web paths, parameters, headers |
| `wordlists/api/` | API endpoints, methods, parameters |
| `wordlists/subdomains/` | Subdomain enumeration |
| `wordlists/passwords/` | Password patterns (not real passwords) |
| `wordlists/usernames/` | Common usernames |
| `wordlists/cloud/` | Cloud resource names, bucket names |
| `wordlists/game/` | Game-specific terms, protocol keywords |

## Adding Lab Environments

Lab environments go in `lab/docker/` or `lab/vm/`.

### Docker Labs

Provide a `docker-compose.yml` and a `README.md`:

```yaml
# lab/docker/lab-name/docker-compose.yml
version: '3.8'
services:
  vulnerable-app:
    build: .
    ports:
      - "8080:80"
```

### Requirements

- Must be self-contained (no external dependencies beyond Docker)
- Include setup instructions in README.md
- Include teardown/cleanup instructions
- Document what vulnerabilities are present
- Never expose to public networks by default

## Adding MCP Integrations

MCP (Model Context Protocol) integrations go in `tools/mcp/`.

### Structure

```
tools/mcp/<mcp-name>/
  README.md           # Setup and usage instructions
  install.sh          # Installation script
  config-example.json # Example configuration
```

### Requirements

- Installation script must be idempotent
- Document all configuration options
- Include validation/health-check functionality
- Add installer call to `setup/install-mcps.sh`

## Code Standards

### Python

- Python 3.8+ compatible
- Use type hints for function signatures
- Use `argparse` for CLI arguments
- Follow PEP 8 style
- Use `#!/usr/bin/env python3` shebang

### Bash

- Use `#!/usr/bin/env bash`
- Use `set -euo pipefail` at the top
- Quote all variables: `"${var}"`
- Use functions for reusable logic
- Support `--help` flag

### JavaScript / Frida

- Use modern ES6+ syntax
- Include JSDoc comments for functions
- Handle errors with try/catch

### C (Exploits/Shellcode)

- Include compilation instructions in comments
- Document target architecture and OS
- Minimize dependencies

### General

- No hardcoded credentials or tokens
- No real target data in committed code
- Use descriptive variable and function names
- Comment complex logic

## Pull Request Process

1. **Branch naming**: `feature/description`, `fix/description`, `docs/description`
2. **Commit messages**: Use conventional commits format
   - `feat(web): add GraphQL injection command`
   - `fix(setup): correct radare2 install path on Linux`
   - `docs(re): update Ghidra MCP setup instructions`
3. **Testing**: Verify your changes work on at least one platform (macOS or Linux)
4. **Documentation**: Update relevant README files if adding new features
5. **Security review**: Ensure no sensitive data is included
6. **One feature per PR**: Keep pull requests focused

## Reporting Issues

When reporting issues, include:

- OS and version
- AI assistant being used (Claude Code, OpenCode, etc.)
- Steps to reproduce
- Expected vs actual behavior
- Relevant logs or error messages

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
