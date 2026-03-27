Test SQL injection on: $ARGUMENTS

Identify injection points: GET/POST params, headers, cookies.
Manual test: single quote, boolean (AND 1=1 vs AND 1=2), UNION SELECT, time-based (pg_sleep/SLEEP).
Automate: sqlmap with appropriate tamper scripts.
If found: enumerate DBs, tables, columns.
Test for: stacked queries, file read/write, OS command execution.
Use wordlists/sqli/ for payloads.
Tool fallbacks: sqlmap > manual.
Output: engagements/<target>/findings/sqli-*.md with CVSS score.

## Safety
Verify authorization and scope before proceeding. Document all actions.

## Framework Mapping
- MITRE ATT&CK: TA0001 (Initial Access) -> T1190 (Exploit Public-Facing Application)
- MITRE ATT&CK: TA0009 (Collection) -> T1213 (Data from Information Repositories)
- Cyber Kill Chain: Phase 4 -- Exploitation
- CEH v12: Module 14 -- Hacking Web Applications (SQL Injection)
