Run comprehensive reconnaissance on: $ARGUMENTS

## Pre-flight
- Determine if passive-only or active recon is authorized
- For passive only, use /recon-passive instead

## Phase 1: DNS & Infrastructure (parallel)
- DNS records: dig <domain> A AAAA MX TXT NS CNAME SOA +short
- Reverse DNS: dig -x <ip>
- WHOIS: whois <domain>, whois <ip>
- Reverse IP: check for other domains on same IP
- ASN lookup: identify network ownership

## Phase 2: Web Fingerprinting
- HTTP headers: `python3 tools/web/header-analyzer.py <url>` (security grade + tech detection)
- Technology: whatweb, wappalyzer, httpx
- CMS detection: WordPress, Drupal, Joomla signatures
- robots.txt, sitemap.xml, security.txt, humans.txt

## Phase 3: Subdomain Enumeration
- Passive: subfinder, crt.sh, SecurityTrails, Wayback
- Active (if authorized): DNS brute with wordlists/web/subdomains.txt
- Takeover check: test for dangling CNAMEs
- If cloud found → run /cloud-recon $ARGUMENTS

## Phase 4: Port & Service Scanning (if authorized)
- Quick scan: nmap -sV -sC --top-ports 1000 <target>
- Full scan: nmap -sV -sC -p- <target> (background)
- UDP top 100: nmap -sU --top-ports 100 <target>

## Phase 5: SSL/TLS Analysis
- Certificate details: openssl s_client -connect <host>:443
- TLS versions: test TLSv1.0, 1.1, 1.2, 1.3
- Weak ciphers: nmap --script ssl-enum-ciphers

## Phase 6: Content Discovery
- Directory brute: ffuf -u <url>/FUZZ -w wordlists/web/directories.txt
- Parameter discovery: arjun -u <url>
- JS analysis: extract endpoints from JavaScript files
- API discovery: test wordlists/web/api-endpoints.txt

## Output
Save to engagements/<target>/recon/initial-recon.md with structured tables.

## Tool Fallbacks
Subdomain: subfinder > amass > assetfinder | Port: nmap > rustscan > masscan
Tech: whatweb > httpx > wappalyzer | DNS: dig > host > nslookup

## Safety
Passive recon first. Respect rate limits. No employee enumeration without scope approval.

## Framework Mapping
- MITRE ATT&CK: TA0043 (Reconnaissance) -> T1595 (Active Scanning), T1592 (Gather Victim Host Information)
- MITRE ATT&CK: T1590 (Gather Victim Network Information), T1593 (Search Open Websites/Domains)
- Cyber Kill Chain: Phase 1 -- Reconnaissance
- CEH v12: Module 02 -- Footprinting and Reconnaissance
