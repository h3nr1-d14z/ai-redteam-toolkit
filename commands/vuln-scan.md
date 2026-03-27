Vulnerability scanning on: $ARGUMENTS

## Pre-flight
- Confirm target scope and scan authorization window
- Determine scan type: network, web app, authenticated, or unauthenticated
- Check for fragile systems that may crash under scanning load

## Phase 1: Network Vulnerability Scanning
1. **Nessus**: nessuscli scan --targets <ip-range> --policy Advanced Scan
2. **OpenVAS**: Greenbone web UI or CLI task creation
3. Authenticated scan: provide SSH/WinRM/SMB creds for deeper coverage
4. Unauthenticated scan: external attacker perspective
5. Compare results: cross-reference Nessus + OpenVAS to reduce false positives

## Phase 2: Web Application Scanning
1. **Nikto**: nikto -h <url> -o nikto-report.html -Format htm
2. **Nuclei**: nuclei -u <url> -t cves/ -t vulnerabilities/ -severity critical,high
3. Custom templates: nuclei -u <url> -t ~/nuclei-templates/custom/
4. Spider first: gospider -s <url> -d 3 -o spider-output then feed URLs to scanner
5. Authenticated scan: provide cookies/tokens for post-auth surface

## Phase 3: Targeted Scanning
1. **CMS-specific**: wpscan (WordPress), droopescan (Drupal), joomscan (Joomla)
2. **SSL/TLS**: testssl.sh <host> or sslyze <host>
3. **Infrastructure**: nmap --script vuln <target>
4. **Container**: trivy image <image>, grype <image>

## Phase 4: Result Analysis
1. Import all results into single view (CSV/JSON normalization)
2. Deduplicate findings across scanners
3. Prioritize by CVSS v3.1: Critical (9.0-10.0), High (7.0-8.9), Medium (4.0-6.9)
4. Verify top findings manually to eliminate false positives
5. Cross-reference with exploit-db/searchsploit for weaponized exploits
6. Check KEV catalog for active exploitation

## Phase 5: False Positive Validation
1. For each Critical/High: manually verify exploitability
2. Check version strings vs actual patching (backports)
3. Test network findings with targeted nmap scripts
4. Confirm web findings with manual Burp Suite testing

## Tools
Network: Nessus, OpenVAS/Greenbone, nmap --script vuln
Web: Nikto, nuclei, wpscan, testssl.sh | Lookup: searchsploit, CVE databases

## Output
Save to engagements/<target>/findings/vuln-scan-<date>.md with CVSS scores.

## Framework Mapping
- MITRE ATT&CK: TA0043 (Reconnaissance) -> T1595.002 (Active Scanning: Vulnerability Scanning)
- Cyber Kill Chain: Phase 2 -- Weaponization (intel gathering for exploit selection)
- CEH v12: Module 05 -- Vulnerability Analysis

## Safety
Coordinate scan windows with target owner. Rate-limit scans on production systems.
