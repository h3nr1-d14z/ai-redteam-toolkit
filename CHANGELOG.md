# Changelog

All notable changes to this project will be documented in this file.

## [0.2.1] - 2026-03-26

### Added

- MITRE ATT&CK mapping (`docs/mitre-attack-mapping.md`): all 85 slash commands mapped to ATT&CK Enterprise v14 techniques across all 14 tactics (TA0043 through TA0040), plus Cyber Kill Chain phase mapping and technique coverage summary.
- Certification study paths (`docs/certification-paths.md`): structured preparation guides for CEH v12 (all 20 modules), OSCP (5 phases by exam relevance), PNPT (5 courses), CND (14 modules with defensive focus), PenTest+, eJPT, CRTP, and GPEN. Includes recommended lab platforms.
- README: added "Certification Alignment" section with certification coverage table.
- README: added MITRE ATT&CK and certification alignment to Features list.
- README: added links to new docs in Additional docs section.

### Changed

- README: updated command count from 85 to 95 in headline and Features section.

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
