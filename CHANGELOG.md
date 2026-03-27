# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Fixed

- Aligned README and CLAUDE command names with actual `commands/*.md` files.
- Corrected documentation to describe flat `commands/` layout instead of non-existent domain subdirectories.
- Replaced stale `targets/...` references with `engagements/...` in command workflows.
- Updated CONTRIBUTING command format to match real command file style.
- Made `.mcp.json` path portable by removing absolute user-specific path.

### Added

- Domain installers: `install-cloud.sh`, `install-redteam.sh`, `install-osint.sh`, `install-forensics.sh`, `install-game.sh`, `install-ai-security.sh`.
- WSL bootstrap: `setup/install-wsl.sh`.
- Consistency quality gate: `setup/check-consistency.py` and `setup/check-consistency.sh`.
- CI validation workflow: `.github/workflows/validate.yml`.
- `tools/c2/` placeholder directory.
- `wordlists/passwords/patterns.txt` starter list.
- Release metadata and docs: `VERSION` (`0.1.0`) and `RELEASE.md`.
- New docs: `GETTING_STARTED.md`, `DEEPTEAM_LEARNINGS.md`, and this `CHANGELOG.md`.
