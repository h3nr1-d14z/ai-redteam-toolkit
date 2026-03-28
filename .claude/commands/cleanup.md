Clean up after engagement: $ARGUMENTS

1. **Inventory** — List all test artifacts created on target (accounts, files, data, backdoors)
2. **Remove** — Provide cleanup commands/steps for each artifact
3. **Verify** — Confirm each artifact is removed
4. **Local cleanup** — Remove tokens/credentials from /tmp, clear browser data
5. **Document** — Log all cleanup actions in engagements/<target>/reports/cleanup-log.md
6. **Archive** — Compress engagement directory for long-term storage

Never leave test artifacts on production systems.
