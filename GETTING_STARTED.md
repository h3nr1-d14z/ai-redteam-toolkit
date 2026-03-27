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

## 4) Start a new engagement

```bash
cp -r engagements/_template engagements/acme-corp
```

Update:

- `engagements/acme-corp/README.md`
- `engagements/acme-corp/scope.md`

## 5) Run commands with your AI assistant

Examples:

- `/pentest https://target.example.com`
- `/mobile-pentest app.apk`
- `/reverse ./sample.bin`

Command definitions are in `commands/*.md`.

## 6) Where outputs go

- Recon: `engagements/<target>/recon/`
- Findings: `engagements/<target>/findings/`
- Reports: `engagements/<target>/reports/`
- Exploits/scripts: `engagements/<target>/exploits/` and `engagements/<target>/scripts/`

## 7) Safety rules

- Test only authorized targets
- Keep evidence and notes in the engagement folder
- Never commit credentials or sensitive loot
