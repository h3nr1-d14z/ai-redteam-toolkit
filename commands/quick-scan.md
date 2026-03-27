Run a quick 15-minute security scan on: $ARGUMENTS

Fast surface-level assessment:
1. Port scan top 1000 ports with service detection
2. HTTP security headers check
3. Nuclei scan (critical+high templates only)
4. SSL/TLS version and cipher analysis
5. Passive subdomain enumeration
6. Technology fingerprinting
7. Summary with severity ratings

Output: engagements/<target>/recon/quick-scan-<date>.md
No exploitation — recon and scanning only.
