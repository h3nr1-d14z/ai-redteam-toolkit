Perform privilege escalation on: $ARGUMENTS

1. **Enumerate**: Run enumeration scripts — LinPEAS/WinPEAS, linux-exploit-suggester, PowerUp, Seatbelt
2. **Linux privesc checks**:
   - SUID/SGID binaries (GTFOBins), writable paths in cron, sudo misconfig (sudo -l)
   - Kernel exploits, capabilities, writable /etc/passwd, NFS no_root_squash, Docker group
3. **Windows privesc checks**:
   - Unquoted service paths, writable service binaries, AlwaysInstallElevated, SeImpersonate/SeAssignPrimaryToken
   - Missing patches, stored credentials (cmdkey), DLL hijacking, UAC bypass
4. **Automated exploitation**: Use known techniques for identified vectors
5. **Verify escalation**: Confirm elevated privileges (whoami, id), test access to sensitive resources
6. **Chain escalation**: If needed, chain multiple vulnerabilities for full escalation path
7. **Document**: Record full escalation chain with reproduction steps

Tools: LinPEAS, WinPEAS, GTFOBins, PEASS-ng, PowerUp, BeRoot
Save to `engagements/<target>/findings/privesc-*.md`
