Quick 15-minute security scan on: $ARGUMENTS

Fast surface assessment (no exploitation).
1) Port scan top 1000.
2) tools/web/header-analyzer.py for security headers + grade.
3) Nuclei critical+high only.
4) SSL/TLS analysis.
5) Passive subdomain enum.
6) Technology fingerprint.
7) Summary with severity ratings.
Output: engagements/<target>/recon/quick-scan-<date>.md.
No exploitation — recon and scanning only.

## Safety
Verify authorization and scope before proceeding. Document all actions.
