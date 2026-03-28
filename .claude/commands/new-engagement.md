Initialize a new security engagement for: $ARGUMENTS

1. **Create structure**: Build `engagements/<target>/` with subdirs: `recon/`, `exploits/`, `findings/`, `reports/`
2. **Scope doc**: Create `engagements/<target>/README.md` with target info, scope boundaries, authorization reference, rules of engagement, testing window
3. **Checklist**: Generate `engagements/<target>/checklist.md` with testing phases (recon, scanning, exploitation, reporting) and status tracking
4. **Tool config**: Prepare Burp/nuclei/nmap config files in `engagements/<target>/recon/`
5. **Timeline**: Set engagement start date, estimated duration, and reporting deadline

Output: engagements/<target>/ directory fully scaffolded and ready for testing.
