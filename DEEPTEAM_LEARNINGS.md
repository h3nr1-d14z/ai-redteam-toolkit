# DeepTeam Learnings

Collected implementation learnings from validating and hardening this toolkit.

## 2026-03-27

### 1) Keep command names file-backed

- Canonical command source is `commands/*.md`.
- Any docs table listing `/command-name` must map directly to `<command-name>.md`.

### 2) One structural truth for commands

- Commands are currently in a flat layout (`commands/*.md`).
- Documentation must not claim domain subfolders unless the repo is actually migrated.

### 3) Engagement path standardization

- Use `engagements/<target>/...` consistently.
- Avoid stale references to `targets/<domain>/...`.

### 4) Setup script parity per domain

- If a domain is advertised in docs, it should have a corresponding installer in `setup/`.
- Added installers for cloud, redteam, osint, forensics, game, and ai-security.

### 5) Platform support clarity

- Windows support should explicitly route through WSL2.
- Provide a single bootstrap script (`setup/install-wsl.sh`) to reduce first-run friction.

### 6) Portable MCP config

- Avoid absolute, user-specific paths in `.mcp.json`.
- Prefer project-relative paths for repository portability.
