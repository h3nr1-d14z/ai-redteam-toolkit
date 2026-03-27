# Roadmap

## Vision

AI-RedTeam-Toolkit aims to become the **AI-first offensive security automation platform** — where AI doesn't just assist, it drives full security assessments autonomously.

---

## v0.1.0 — Foundation (Released)

- [x] 78 slash commands across 11 security domains
- [x] 12 methodology guides
- [x] 14 cheatsheets
- [x] 15 setup scripts (OS-aware)
- [x] GhidraMCP integration
- [x] Cross-tool: Claude Code + OpenCode
- [x] Engagement templates + report templates
- [x] CI validation workflow
- [x] Docker lab (DVWA, Juice Shop, WebGoat)

---

## v0.2.0 — Working Toolkit (In Progress)

### Custom Tools
- [ ] JWT Toolkit — decode, crack, forge, algorithm confusion
- [ ] Header Analyzer — security header check + grading
- [ ] CORS Scanner — misconfiguration testing
- [ ] S3 Scanner — bucket enumeration + permission check
- [ ] APK Analyzer — Android static analysis
- [ ] Report Generator — auto-compile findings to report
- [ ] Evidence Collector — screenshot + HTTP capture
- [ ] IAM Analyzer — AWS policy analysis
- [ ] IL2CPP Extractor — Unity game metadata parser
- [ ] Subdomain Takeover — dangling CNAME checker

### Enhanced Commands
- [ ] Upgrade top 20 commands (13 → 40 lines each)
- [ ] Add safety checks, conditional logic, tool fallbacks

### MCP Expansion
- [ ] GhidraMCP: 3 → 11 operations
- [ ] Nuclei MCP — run scans from AI
- [ ] Nmap MCP — port scanning from AI

### Labs & Wordlists
- [ ] API vulnerability lab (Flask)
- [ ] Cloud lab (LocalStack)
- [ ] 50+ curated wordlists

---

## v0.3.0 — AI Automation Engine

- [ ] YAML pipeline engine — chain commands automatically
- [ ] Smart command chaining — AI decides next step based on findings
- [ ] Findings database (SQLite) — dedup, trends, export
- [ ] OMC workflow presets — `/ralph` autopilot, `/team` parallel

---

## v0.4.0 — Intelligence & Reporting

- [ ] Threat intel integration (NVD, ExploitDB, Shodan)
- [ ] Auto CVE matching (service version → known vulns)
- [ ] PDF report generator
- [ ] Findings dashboard (TUI)

---

## v0.5.0 — Specialized Labs

- [ ] Domain-specific Docker labs (API, mobile, cloud, AD, game)
- [ ] Progressive challenges with auto-grading
- [ ] Learning paths (OSCP prep, bug bounty, red team)

---

## v1.0.0 — Mature Platform

- [ ] Plugin system for community tools
- [ ] Cloud-native (Docker image, Codespaces)
- [ ] Documentation site
- [ ] Stable API for integrations

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add tools, commands, templates, and wordlists.
