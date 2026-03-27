# Release Guide

Current target release: **v0.1.0**

## Release criteria

Run all checks from repository root:

```bash
bash -n setup/*.sh
./setup/check-consistency.sh
./setup/check-tools.sh
```

Required conditions:

- `setup/check-consistency.sh` returns PASS
- Shell scripts are syntax-valid
- Core docs exist: `README.md`, `GETTING_STARTED.md`, `CHANGELOG.md`, `DEEPTEAM_LEARNINGS.md`
- `VERSION` is set to intended release

## Tagging process

```bash
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

## Post-release updates

- Create new `## [Unreleased]` section in `CHANGELOG.md`
- Bump `VERSION` for next cycle
- Capture additional operational learnings in `DEEPTEAM_LEARNINGS.md`
