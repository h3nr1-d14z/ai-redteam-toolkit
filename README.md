# AI-RedTeam-Toolkit

**AI-powered offensive security framework. 95 slash commands across 11 security domains.**

A comprehensive, template-driven toolkit for pentesters and red teamers using AI coding assistants. Provides structured methodologies, reusable tools, automated setup, and deep AI integration for every phase of security testing -- from reconnaissance through reporting.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/AI-RedTeam-Toolkit.git
cd AI-RedTeam-Toolkit

# Run the interactive installer
chmod +x setup/*.sh
./setup/install.sh

# Or install everything at once
./setup/install.sh --all

# Start a new engagement
cp -r engagements/_template engagements/my-target
# Edit engagements/my-target/README.md with target details

# Open with your AI assistant and use slash commands
# Example: /pentest https://target.example.com
```

New to the toolkit? Start with [GETTING_STARTED.md](GETTING_STARTED.md) for a first-run walkthrough.

## Platform Support

- **macOS**: supported via Homebrew
- **Linux**: supported via apt/dnf/pacman flows in setup scripts
- **Windows**: supported through **WSL2 (Ubuntu recommended)**

For Windows users, open WSL in the repo root and run:

```bash
./setup/install-wsl.sh
```

## Features

- **95 Slash Commands** across 11 security domains, usable with AI coding assistants
- **MITRE ATT&CK Mapping** -- every command mapped to ATT&CK tactics/techniques and Cyber Kill Chain phases
- **Certification Alignment** -- study paths for CEH v12, OSCP, PNPT, CND, PenTest+, eJPT, CRTP, and GPEN
- **MCP Integrations** for direct tool-to-AI communication (Ghidra, more planned)
- **Structured Methodologies** for every engagement type
- **Engagement Templates** with authorization tracking, scope definition, and reporting
- **Automated Tool Installation** with OS detection for macOS and Linux
- **Custom Wordlists** organized by category for web, API, cloud, and more
- **Lab Environments** with Docker-based vulnerable applications
- **Finding Templates** with CVSS v3.1 scoring and standardized format
- **Report Templates** for professional deliverables
- **Multi-Tool Support** for Claude Code (native), OpenCode, and oh-my-claudecode (OMC) for multi-agent orchestration

## Supported Domains

| Domain | Key Capabilities | Commands |
|--------|-----------------|----------|
| **Web Application Pentesting** | OWASP Top 10, API security, injection, auth bypass | 11 |
| **Mobile Security** | Android/iOS RE, Frida hooking, traffic interception | 6 |
| **Reverse Engineering** | Ghidra (MCP), radare2, malware analysis, firmware RE | 6 |
| **Exploitation Development** | Buffer overflow, ROP chains, shellcode, heap exploits | 6 |
| **Game Hacking** | Unity/Unreal RE, memory manipulation, anti-cheat | 5 |
| **Cloud Security** | AWS/Azure/GCP audit, container escape, IaC review | 7 |
| **Red Team Operations** | Phishing, privesc, lateral movement, AD attacks, C2 | 8 |
| **OSINT** | Subdomain enum, email harvest, metadata extraction | 6 |
| **Digital Forensics** | Memory/disk forensics, log analysis, timeline | 6 |
| **CTF** | Web, pwn, RE, crypto, forensics challenge solving | 6 |
| **AI/LLM Security** | Prompt injection, model probing, adversarial ML | 3 |

## Installation

### Master Installer

The master installer detects your OS and package manager, then lets you choose which tool categories to install:

```bash
# Interactive mode (choose categories)
./setup/install.sh

# Install all categories
./setup/install.sh --all

# Check which tools are installed
./setup/install.sh --check

# Create directory structure only
./setup/install.sh --dirs
```

### Per-Category Installation

Each category can be installed independently:

```bash
./setup/install-web.sh       # Web pentesting: nmap, sqlmap, ffuf, nuclei, subfinder, httpx, dalfox, arjun, whatweb, nikto
./setup/install-re.sh        # Reverse engineering: ghidra, radare2, binwalk, checksec
./setup/install-mobile.sh    # Mobile security: jadx, apktool, frida, objection, mitmproxy
./setup/install-exploit.sh   # Exploitation: pwntools, ROPgadget, ropper, one_gadget, nasm
./setup/install-cloud.sh     # Cloud security: awscli, terraform, trivy, ScoutSuite, Prowler
./setup/install-redteam.sh   # Red team ops: impacket, bloodhound-python, crackmapexec
./setup/install-osint.sh     # OSINT: amass, theHarvester, dnsx, whois
./setup/install-forensics.sh # Forensics: volatility3, yara, tshark, sleuthkit
./setup/install-game.sh      # Game security: frida-tools, mitmproxy, radare2
./setup/install-ai-security.sh # AI/LLM security: garak, llm-guard, promptfoo
./setup/install-mcps.sh      # MCP servers: GhidraMCP
```

### Tool Verification

```bash
./setup/check-tools.sh
./setup/check-consistency.sh
```

`check-tools.sh` outputs installation status of security tools.

`check-consistency.sh` validates repository integrity rules (command/docs parity, flat command layout, no stale `targets/` references, required release files, and portable `.mcp.json`).

## Usage Examples

### Web Application Pentest

```
You: /pentest https://target.example.com

AI performs:
1. Reconnaissance (subdomain enum, port scanning, tech fingerprinting)
2. Automated scanning (nuclei, nikto)
3. Manual testing guided by findings
4. Exploit development for confirmed vulnerabilities
5. Report generation with CVSS scores
```

### Reverse Engineering with Ghidra MCP

```
You: /reverse ./firmware.bin

AI performs (via GhidraMCP):
1. Loads binary into Ghidra
2. Runs auto-analysis
3. Identifies key functions and strings
4. Decompiles functions of interest
5. Documents findings with annotated pseudocode
```

### Mobile App Security

```
You: /mobile-pentest app.apk

AI performs:
1. Decompiles APK with jadx
2. Static analysis of decompiled source
3. Identifies hardcoded secrets, insecure storage, weak crypto
4. Generates Frida hooks for dynamic testing
5. Tests API endpoints from mobile client perspective
```

### Red Team Engagement

```
You: /redteam-plan target-corp

AI assists with:
1. OSINT and reconnaissance
2. Initial access vector development
3. Payload generation with evasion
4. Privilege escalation techniques
5. Lateral movement strategies
6. Persistence mechanism setup
```

### CTF Challenge

```
You: /ctf-pwn ./challenge_binary

AI performs:
1. Binary analysis (checksec, file, strings)
2. Vulnerability identification
3. Exploit development (BOF, ROP, format string)
4. Flag extraction
5. Writeup generation
```

## Slash Commands Reference

### Engagement Management (2 commands)

| Command | Description |
|---------|-------------|
| `/new-engagement` | Initialize a new security engagement |
| `/close-engagement` | Close and finalize an engagement |

### Web Application Pentesting (14 commands)

| Command | Description |
|---------|-------------|
| `/pentest` | Full web application penetration test workflow |
| `/recon` | Comprehensive reconnaissance |
| `/recon-active` | Active reconnaissance |
| `/recon-passive` | Passive reconnaissance |
| `/exploit` | Develop a specific exploit |
| `/sqli-test` | SQL injection testing and exploitation |
| `/xss-hunt` | Cross-site scripting discovery and payload crafting |
| `/ssrf-scan` | Server-side request forgery testing |
| `/ssti-test` | Server-side template injection |
| `/auth-test` | Authentication and session testing |
| `/api-pentest` | API security assessment |
| `/upload-test` | File upload vulnerability testing |
| `/nuclei-scan` | Run nuclei vulnerability scanner |
| `/scan-ports` | Port scanning and service enumeration |

### Mobile Security (5 commands)

| Command | Description |
|---------|-------------|
| `/mobile-pentest` | Full mobile application pentest |
| `/android-analyze` | Android APK analysis and reverse engineering |
| `/ios-analyze` | iOS IPA analysis |
| `/frida-hook` | Generate Frida hooking scripts |
| `/ssl-pinning-bypass` | SSL/TLS certificate pinning bypass |

### Reverse Engineering (7 commands)

| Command | Description |
|---------|-------------|
| `/reverse` | Reverse engineer a binary or application |
| `/binary-analyze` | Binary analysis |
| `/malware-analyze` | Malware analysis workflow |
| `/firmware-analyze` | Firmware extraction and analysis |
| `/protocol-re` | Network protocol reverse engineering |
| `/deobfuscate` | Code deobfuscation |
| `/encode-decode` | Encode or decode data |

### Exploitation Development (4 commands)

| Command | Description |
|---------|-------------|
| `/bof-exploit` | Buffer overflow exploit development |
| `/rop-chain` | ROP chain construction |
| `/shellcode-gen` | Custom shellcode development |
| `/payload-gen` | Payload generation |

### Game Hacking (4 commands)

| Command | Description |
|---------|-------------|
| `/game-hack` | Game security analysis workflow |
| `/unity-analyze` | Unity game client analysis |
| `/game-network` | Game network protocol analysis |
| `/memory-hack` | Memory scanning and manipulation |

### Cloud Security (5 commands)

| Command | Description |
|---------|-------------|
| `/cloud-pentest` | Cloud security assessment |
| `/cloud-recon` | Cloud infrastructure reconnaissance |
| `/infra-pentest` | Infrastructure penetration test |
| `/container-escape` | Container escape techniques |
| `/subdomain-enum` | Subdomain enumeration |

### Red Team Operations (7 commands)

| Command | Description |
|---------|-------------|
| `/redteam-plan` | Red team operation planning |
| `/phishing-campaign` | Phishing campaign setup |
| `/privesc` | Privilege escalation techniques |
| `/lateral-movement` | Lateral movement techniques |
| `/persistence` | Persistence mechanism development |
| `/ad-pentest` | Active Directory penetration test |
| `/c2-setup` | C2 framework configuration |

### OSINT (5 commands)

| Command | Description |
|---------|-------------|
| `/osint` | Full OSINT investigation workflow |
| `/osint-person` | OSINT on a person |
| `/osint-domain` | OSINT on a domain |
| `/osint-org` | OSINT on an organization |
| `/subdomain-enum` | Subdomain enumeration |

### Digital Forensics (5 commands)

| Command | Description |
|---------|-------------|
| `/forensics` | Digital forensics investigation workflow |
| `/memory-forensics` | Memory dump analysis |
| `/disk-forensics` | Disk image analysis |
| `/log-analysis` | Log file analysis and correlation |
| `/network-forensics` | Network capture forensic analysis |

### CTF (6 commands)

| Command | Description |
|---------|-------------|
| `/ctf` | CTF challenge solving workflow |
| `/ctf-web` | Web category CTF challenge |
| `/ctf-pwn` | Binary exploitation CTF challenge |
| `/ctf-crypto` | Cryptography CTF challenge |
| `/ctf-forensics` | Forensics CTF challenge |
| `/write-ctf-writeup` | Write a CTF challenge writeup |

### Reporting and Writing (4 commands)

| Command | Description |
|---------|-------------|
| `/write-report` | Write security assessment report |
| `/write-finding` | Write vulnerability finding report |
| `/write-re-analysis` | Write reverse engineering analysis |
| `/vuln-report` | Generate vulnerability report |

### AI/LLM Security (2 commands)

| Command | Description |
|---------|-------------|
| `/ai-redteam` | AI/LLM red teaming workflow |
| `/ai-guardrail-test` | AI guardrail and safety testing |

### Automation and Utilities (26 commands)

| Command | Description |
|---------|-------------|
| `/full-assessment` | Run full pipeline: recon, scan, pentest, report |
| `/quick-scan` | Fast 15-minute surface security scan |
| `/engagement-status` | Check engagement progress and findings count |
| `/screenshot` | Capture and document evidence |
| `/timeline` | Build chronological attack timeline |
| `/cleanup` | Remove test artifacts after engagement |
| `/deconflict` | Pre-engagement safety and deconfliction check |
| `/vuln-scan` | Vulnerability scanning with Nessus/OpenVAS |
| `/metasploit` | Metasploit workflow: search, exploit, meterpreter |
| `/password-attack` | Online and offline password cracking |
| `/hash-crack` | Hash cracking workflows |
| `/generate-wordlist` | Generate custom wordlists |
| `/enumerate` | Deep enumeration: NetBIOS, SNMP, LDAP, DNS, SMB, RPC |
| `/honeypot-detect` | Detect and identify honeypots |
| `/pivot` | Network pivoting: SSH tunnels, chisel, ligolo, proxychains |
| `/ad-enum` | AD enumeration: BloodHound, PowerView |
| `/post-exploit` | Post-exploitation: persistence, collection, exfiltration |
| `/web-server-hack` | Web server exploitation and misconfiguration |
| `/evasion` | IDS/Firewall/WAF evasion techniques |
| `/wireless` | Wireless network security testing |
| `/iot-hack` | IoT/OT device security analysis |
| `/session-hijack` | Session hijacking techniques |
| `/sniff` | Network sniffing and MITM attacks |
| `/steganography` | Detect and analyze hidden data in files |
| `/crypto-attack` | Cryptographic implementation analysis |
| `/incident-response` | Incident response workflow |

## Directory Structure

```
AI-RedTeam-Toolkit/
├── CLAUDE.md                    # AI assistant instructions (core brain)
├── README.md                    # This file
├── LICENSE                      # MIT License
├── CONTRIBUTING.md              # Contribution guidelines
├── .gitignore                   # Security-aware gitignore
├── .mcp.json                    # MCP server configuration
│
├── setup/                       # Installation and setup scripts
│   ├── install.sh               # Master installer (interactive)
│   ├── install-web.sh           # Web pentesting tools
│   ├── install-re.sh            # Reverse engineering tools
│   ├── install-mobile.sh        # Mobile security tools
│   ├── install-exploit.sh       # Exploitation development tools
│   ├── install-cloud.sh         # Cloud security tools
│   ├── install-redteam.sh       # Red team operation tools
│   ├── install-osint.sh         # OSINT tools
│   ├── install-forensics.sh     # Forensics tools
│   ├── install-game.sh          # Game security tools
│   ├── install-ai-security.sh   # AI/LLM security tools
│   ├── install-mcps.sh          # MCP server installation
│   └── check-tools.sh           # Tool verification report
│
├── commands/                    # Slash command definitions (flat .md files)
│   ├── pentest.md
│   ├── recon.md
│   ├── sqli-test.md
│   ├── cloud-pentest.md
│   ├── redteam-plan.md
│   └── ... (71 total command files)
│
├── templates/                   # Reusable templates
│   ├── engagement/              # Engagement setup templates
│   ├── reports/                 # Report format templates
│   ├── findings/                # Vulnerability finding templates
│   ├── ctf/                     # CTF templates
│   └── scripts/                 # Script templates
│
├── tools/                       # Custom security tools
│   ├── web/                     # Web exploitation tools
│   ├── mobile/                  # Mobile testing tools
│   ├── re/                      # RE helper tools
│   ├── exploit/                 # Exploit development tools
│   ├── game/                    # Game hacking tools
│   ├── cloud/                   # Cloud security tools
│   ├── redteam/                 # Red team tools
│   ├── osint/                   # OSINT tools
│   ├── forensics/               # Forensics tools
│   ├── ai-redteam/              # AI security tools
│   ├── c2/                      # C2 framework assets
│   ├── common/                  # Shared utilities
│   └── mcp/                     # MCP server integrations
│
├── wordlists/                   # Custom wordlists
│   ├── web/                     # Web paths, parameters, headers
│   ├── api/                     # API endpoints, methods
│   ├── subdomains/              # Subdomain wordlists
│   ├── passwords/               # Password patterns
│   ├── usernames/               # Common usernames
│   ├── cloud/                   # Cloud resource names
│   └── game/                    # Game-specific terms
│
├── engagements/                 # Active/past engagements (gitignored)
│   └── _template/               # New engagement template
│       ├── README.md            # Engagement info and tracking
│       ├── scope.md             # Scope and rules of engagement
│       ├── recon/               # Reconnaissance data
│       ├── exploits/            # PoC exploits
│       ├── findings/            # Vulnerability writeups
│       ├── evidence/            # Screenshots, logs, captures
│       ├── loot/                # Extracted credentials/data
│       ├── scripts/             # Engagement-specific scripts
│       └── reports/             # Final reports
│
├── methodology/                 # Testing methodologies by domain
├── cheatsheets/                 # Quick reference cheatsheets
├── examples/                    # Example usage and workflows
│
├── ctf/                         # CTF challenge solutions
│   └── <platform>/
│       └── <challenge>/
│           ├── solve.py         # Solution script
│           ├── writeup.md       # Detailed writeup
│           └── files/           # Challenge files
│
└── lab/                         # Local lab environments
    ├── docker/                  # Docker-based vulnerable apps
    └── vm/                      # VM setup scripts and notes
```

## AI Assistant Setup

AI-RedTeam-Toolkit works natively with three AI coding assistants. Pick one or use all three together.

| Assistant | Support | Setup Required |
|-----------|---------|----------------|
| **Claude Code** | Full — slash commands, skills, MCP integrations | None — works out of the box |
| **OpenCode** | Full — slash commands | Copy commands to `.opencode/commands/` |
| **oh-my-claudecode (OMC)** | Extended — multi-agent orchestration on top of Claude Code | `npm install -g oh-my-claudecode && omc setup` |

### Claude Code

Works out of the box. Slash commands are auto-detected from `.claude/commands/*.md`.

**Skills** in `.claude/skills/` extend Claude's behavior for security-specific workflows:

| Skill | Trigger |
|-------|---------|
| Full pentest workflow | `/pentest` |
| Reverse engineering | `/reverse` |
| Reconnaissance | `/recon` |
| CTF solving | `/ctf` |
| Exploit development | `/exploit` |
| Game hacking | `/game-hack` |
| Mobile pentesting | `/mobile-pentest` |
| SSRF exploitation | `/ssrf-scan` |

**MCP Integration** -- GhidraMCP connects Claude Code directly to Ghidra for binary analysis. See [MCP Integrations](#mcp-integrations) below.

### OpenCode

Commands must be in `.opencode/commands/`. Copy from `.claude/commands/`:

```bash
# Works everywhere: macOS, Linux, WSL
mkdir -p .opencode
cp -r .claude/commands .opencode/commands
```

> **Symlink alternative** (macOS/Linux native only — does NOT work on WSL):
> ```bash
> mkdir -p .opencode
> ln -s ../.claude/commands .opencode/commands
> ```

To resync after command updates:
```bash
rsync -a --delete .claude/commands/ .opencode/commands/
```

OpenCode reads `CLAUDE.md` as its project instructions file automatically — no extra configuration needed.

### oh-my-claudecode (OMC)

OMC adds multi-agent orchestration on top of Claude Code for autonomous, parallel, and iterative security workflows.

**Install:**
```bash
npm install -g oh-my-claudecode
omc setup
```

**OMC workflows for this toolkit:**

| Workflow | Command | Use Case |
|----------|---------|----------|
| Autonomous pentest loop | `/ralph /pentest target.com` | Runs until thorough, self-reviewing |
| Parallel agents | `/team 3:executor "pentest target.com"` | Agents split web/API/infra in parallel |
| Batch multi-target | /ultrawork | Recon/scan multiple targets simultaneously |
| Root-cause tracing | `/trace "why does X work?"` | Trace a vulnerability to its root cause |
| Multi-model analysis | /sciomc | Claude + Codex + Gemini on a complex binary |
| Continuous monitoring | `/loop 5m /quick-scan target` | Poll target during an engagement |
| Iterative exploit dev | `/ralph /exploit "SQLi on /api/users"` | Loop until working exploit |

See [docs/omc-integration.md](docs/omc-integration.md) for full OMC workflow examples.

### Command Locations

All three locations contain the same 95 command files — use whichever matches your assistant:

```
commands/*.md              # Universal mirror (any AI assistant)
.claude/commands/*.md      # Claude Code (auto-detected as /commands)
.opencode/commands/*.md    # OpenCode (auto-detected as /commands)
```

## MCP Integrations

### GhidraMCP (Reverse Engineering)

Connects Claude directly to Ghidra for binary analysis through the Model Context Protocol.

```bash
# Install GhidraMCP
./setup/install-mcps.sh

# Configuration lives in .mcp.json
```

**Capabilities via MCP:**
- Load and analyze binaries
- Decompile functions to pseudocode
- List and search functions, strings, cross-references
- Rename and annotate symbols
- Navigate call graphs and data flow

### Future MCP Integrations (Planned)

- Burp Suite MCP (web proxy integration)
- Wireshark MCP (packet analysis)
- IDA Pro MCP (alternative RE integration)
- Metasploit MCP (exploitation framework)

## Certification Alignment

The toolkit includes structured study paths that map commands and labs to major security certifications:

| Certification | Issuer | Coverage |
|--------------|--------|----------|
| **CEH v12** | EC-Council | All 20 modules mapped to commands and labs |
| **OSCP** | OffSec | 5-phase study path ordered by exam relevance |
| **PNPT** | TCM Security | All 5 courses with command-level practice guides |
| **CND** | EC-Council | Defensive validation using offensive commands |
| **PenTest+** | CompTIA | All 5 domains with weighted command mapping |
| **eJPT** | INE | Core topic areas with beginner-friendly commands |
| **CRTP** | Altered Security | AD-focused attack chain commands |
| **GPEN** | GIAC/SANS | Full pentest lifecycle command mapping |

See [docs/certification-paths.md](docs/certification-paths.md) for complete study guides with recommended lab platforms.

For MITRE ATT&CK technique mapping across all 14 tactics, see [docs/mitre-attack-mapping.md](docs/mitre-attack-mapping.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding slash commands, templates, tools, and lab environments.

Additional docs:
- [GETTING_STARTED.md](GETTING_STARTED.md)
- [DEEPTEAM_LEARNINGS.md](DEEPTEAM_LEARNINGS.md)
- [CHANGELOG.md](CHANGELOG.md)
- [RELEASE.md](RELEASE.md)
- [docs/mitre-attack-mapping.md](docs/mitre-attack-mapping.md)
- [docs/certification-paths.md](docs/certification-paths.md)

Key points:
- Follow the existing file structure and naming conventions
- Test on at least one platform (macOS or Linux)
- Never commit credentials, PII, or malware samples
- Include documentation with every contribution

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- The offensive security and CTF community for methodologies and shared knowledge
- Open source security tool authors and maintainers
- OWASP for web security testing standards
- MITRE for ATT&CK framework and CWE catalog
- The AI coding assistant ecosystem for enabling new approaches to security work

---

**Disclaimer**: This toolkit is for authorized security testing and educational purposes only. Always obtain proper authorization before testing any system. The authors are not responsible for misuse.
