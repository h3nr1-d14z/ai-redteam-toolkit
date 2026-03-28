Web server exploitation on: $ARGUMENTS

## Pre-flight
- Identify web server type and version: Apache, Nginx, IIS, Tomcat, Node.js
- Gather results from /recon and /scan-ports
- Check for known CVEs matching server version

## Phase 1: Server Identification
1. **Banner grab**: `curl -I <url>` -- check Server header
2. **Detailed fingerprint**: `whatweb <url>` or `httpx -title -status-code -tech-detect`
3. **Error pages**: trigger 404/500 errors to reveal server version
4. **Default files**: check for server-specific defaults (/server-status, /server-info)
5. **HTTP methods**: `nmap --script http-methods <target>` -- check PUT, DELETE, TRACE

## Phase 2: Default Credentials
1. **Apache Tomcat**: /manager/html (tomcat:tomcat, admin:admin, tomcat:s3cret)
2. **JBoss**: /admin-console, /jmx-console (admin:admin)
3. **WebLogic**: /console (weblogic:welcome1)
4. **Jenkins**: /login, /script (no auth or admin:admin)
5. **phpMyAdmin**: /phpmyadmin (root:, root:root, root:toor)
6. **Grafana**: /login (admin:admin)
7. Reference: wordlists/passwords/default-creds.txt

## Phase 3: Directory Traversal & File Disclosure
1. **Path traversal**: `curl <url>/..%2f..%2f..%2fetc/passwd`
2. **Null byte**: `curl <url>/file.php%00.jpg` (legacy systems)
3. **Encoding bypass**: double URL encode, Unicode normalization
4. **Git exposure**: `curl <url>/.git/HEAD` -- if found, use git-dumper
5. **.env exposure**: `curl <url>/.env` -- check for leaked credentials
6. **Backup files**: test .bak, .old, .swp, ~, .orig extensions
7. **Config files**: .htaccess, web.config, WEB-INF/web.xml, application.yml

## Phase 4: Server Misconfiguration
1. **Directory listing**: browse directories without index files
2. **HTTP methods**: test PUT for file upload, TRACE for XST
3. **CORS**: check Access-Control-Allow-Origin for wildcard or null
4. **Security headers**: missing X-Frame-Options, CSP, HSTS, X-Content-Type-Options
5. **Verbose errors**: trigger errors to leak stack traces, file paths, DB info
6. **Admin interfaces**: exposed management panels without auth

## Phase 5: Known CVE Exploitation
1. **Version lookup**: `searchsploit apache 2.4` or `searchsploit tomcat 9`
2. **Nuclei CVE scan**: `nuclei -u <url> -t cves/ -severity critical,high`
3. **Notable CVEs**:
   - Apache: CVE-2021-41773 (path traversal), CVE-2021-42013 (RCE)
   - Tomcat: CVE-2017-12617 (PUT RCE), Ghostcat CVE-2020-1938
   - IIS: CVE-2017-7269 (WebDAV RCE), shortname enumeration
   - Nginx: off-by-slash alias traversal, merge_slashes misconfiguration
4. **Metasploit**: `search type:exploit name:<server>`

## Phase 6: Virtual Host Enumeration
1. **Brute force vhosts**: `ffuf -w wordlists/web/vhosts.txt -u <url> -H "Host: FUZZ.<domain>"`
2. **Compare responses**: filter by response size to find valid vhosts
3. **Certificate SANs**: check SSL cert for additional hostnames
4. **Reverse DNS / PTR**: look for additional hostnames

## Tools
whatweb, httpx, nikto, nuclei, searchsploit, ffuf, git-dumper, curl, nmap scripts

## Output
Save to engagements/<target>/findings/web-server-*.md with CVSS scores.

## Framework Mapping
- MITRE ATT&CK: TA0001 (Initial Access) -> T1190 (Exploit Public-Facing Application)
- MITRE ATT&CK: TA0007 (Discovery) -> T1082 (System Information Discovery)
- MITRE ATT&CK: TA0001 -> T1078.001 (Valid Accounts: Default Accounts)
- Cyber Kill Chain: Phase 4 -- Exploitation
- CEH v12: Module 13 -- Hacking Web Servers

## Safety
Test default credentials carefully to avoid lockouts. Report exposed admin panels immediately.
