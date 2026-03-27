Run a full automated security assessment pipeline on: $ARGUMENTS

Orchestrate these phases automatically:
1. **Recon** — DNS, headers, tech stack, subdomains, ports, SSL, reverse IP
2. **Scan** — Nuclei (critical+high), port scan, service identification
3. **Web pentest** — Auth, injection (SQLi/XSS/SSRF/SSTI), access control, business logic
4. **API test** — If API endpoints found, test REST/GraphQL/WebSocket security
5. **Report** — Compile all findings into final report

Save progress after each phase. If any phase fails, continue with next.
Output: engagements/<target>/reports/full-assessment-<date>.md

## Safety
Verify authorization before starting. Confirm scope. Check testing window.
