# Getting Started

This guide is for first-time users of AI-RedTeam-Toolkit.

## 1) Prerequisites

- Authorized target scope and rules of engagement
- Git
- Python 3 + pip
- One supported platform:
  - macOS (Homebrew)
  - Linux (apt/dnf/pacman)
  - Windows via WSL2 (Ubuntu recommended)

## 2) Clone and bootstrap

```bash
git clone https://github.com/YOUR_USERNAME/AI-RedTeam-Toolkit.git
cd AI-RedTeam-Toolkit
chmod +x setup/*.sh
```

### macOS/Linux

```bash
./setup/install.sh --all
```

### Windows (WSL2)

```bash
./setup/install-wsl.sh
```

## 3) Verify toolchain

```bash
./setup/check-tools.sh
```

Fix any missing dependencies before running real engagements.

## 4) Set up your AI assistant

Choose one — or use all three together.

### Claude Code

Works out of the box. Slash commands in `.claude/commands/` are auto-detected, and skills in `.claude/skills/` are ready to use. No setup needed.

### OpenCode

Copy commands so OpenCode can detect them:

```bash
mkdir -p .opencode
cp -r .claude/commands .opencode/commands
```

OpenCode reads `CLAUDE.md` automatically — no extra configuration needed.

### oh-my-claudecode (OMC)

Adds multi-agent orchestration (autonomous loops, parallel agents, batch scanning) on top of Claude Code:

```bash
npm install -g oh-my-claudecode
omc setup
```

After setup, use workflows like `/ralph /pentest target.com` for autonomous looping or `/team 3:executor "..."` for parallel agents. See [docs/omc-integration.md](docs/omc-integration.md) for examples.

## 5) Start a new engagement

```bash
cp -r engagements/_template engagements/acme-corp
```

Update:

- `engagements/acme-corp/README.md`
- `engagements/acme-corp/scope.md`

## 6) Run commands with your AI assistant

Examples:

- `/pentest https://target.example.com`
- `/mobile-pentest app.apk`
- `/reverse ./sample.bin`

Command definitions are in `commands/*.md`.

## 7) Where outputs go

- Recon: `engagements/<target>/recon/`
- Findings: `engagements/<target>/findings/`
- Reports: `engagements/<target>/reports/`
- Exploits/scripts: `engagements/<target>/exploits/` and `engagements/<target>/scripts/`

## 8) Safety rules

- Test only authorized targets
- Keep evidence and notes in the engagement folder
- Never commit credentials or sensitive loot
