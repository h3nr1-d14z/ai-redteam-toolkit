# OSINT (Open-Source Intelligence) Methodology

## Phase 1: Passive Reconnaissance

### Domain and Infrastructure
- WHOIS lookup: `whois target.com` -- registrant, registrar, nameservers, dates
- Historical WHOIS: whoishistory.com, DomainTools for past registration data
- DNS records: `dig target.com ANY`, `dig +short target.com MX NS TXT CNAME SOA`
- Reverse DNS: `dig -x <IP>` -- find domains hosted on an IP
- DNS history: SecurityTrails, ViewDNS.info for historical DNS changes
- Subdomain enumeration (passive): `subfinder -d target.com`, `amass enum -passive -d target.com`
- Certificate Transparency: `crt.sh`, `censys.io` -- find subdomains from issued certificates
- ASN lookup: `whois -h whois.radb.net -- '-i origin AS12345'` -- find all IP ranges for an organization
- BGP data: bgp.he.net for AS relationships and prefixes

### Web Presence
- Wayback Machine: `web.archive.org` -- historical website snapshots, deleted pages, old configurations
- Google Cache: `cache:target.com` -- recent cached version
- Common Crawl: commoncrawl.org -- historical web crawl data
- Search engine cached pages: Google, Bing, Yandex
- Paste sites: Pastebin, GitHub Gist, Ghostbin -- search for leaked data
- Code repositories: GitHub, GitLab, Bitbucket -- search for organization code, secrets, configs

### Google Dorking
```
site:target.com                           # All indexed pages
site:target.com filetype:pdf              # PDF documents
site:target.com filetype:xlsx             # Spreadsheets
site:target.com filetype:docx             # Word documents
site:target.com filetype:sql              # SQL dumps
site:target.com filetype:log              # Log files
site:target.com filetype:env              # Environment files
site:target.com inurl:admin               # Admin pages
site:target.com inurl:login               # Login pages
site:target.com inurl:api                 # API endpoints
site:target.com intitle:"index of"        # Directory listings
site:target.com ext:php intitle:phpinfo   # PHP info pages
site:target.com "password" filetype:txt   # Password files
site:target.com "error" OR "warning"      # Error pages
inurl:target.com                          # URLs containing target
"target.com" -site:target.com             # Mentions on other sites
```

### Shodan / Censys / BinaryEdge
- Search by organization: `org:"Target Company"`
- Search by hostname: `hostname:target.com`
- Search by SSL cert: `ssl.cert.subject.cn:target.com`
- Search by favicon hash: calculate favicon hash, search across the internet
- Identify exposed services: databases, admin panels, IoT devices, development servers
- Historical data: what services were previously exposed?

---

## Phase 2: People Intelligence

### Employee Enumeration
- LinkedIn: search company employees, note names, titles, departments
- Tools: `linkedin2username` -- generate username lists from LinkedIn
- Company website: about/team pages, press releases, blog authors
- Conference talks: speaker bios at security/tech conferences
- Academic papers: research publications listing affiliations

### Email Discovery
- Email format: determine pattern (first.last@, flast@, firstl@)
- Tools: `theHarvester -d target.com -b all`, Hunter.io, Snov.io
- Verify emails: `smtp-user-enum`, email verification APIs
- Google dork: `"@target.com"` -- find emails posted publicly
- PGP key servers: keys.openpgp.org -- email addresses in public keys

### Credential Intelligence
- Breach databases: HaveIBeenPwned API (for authorized use), DeHashed
- Leaked credential dumps: search for target domain in known breach data
- Password patterns: identify common password patterns for the organization
- Combo lists: username:password pairs from various breaches
- Note: only use breach data that is legally accessible and within engagement scope

### Social Media
- Twitter/X: employee posts, company announcements, tech stack hints
- Facebook: company pages, employee groups
- Instagram: office photos (badges, screens, whiteboards), employee check-ins
- GitHub: employee personal repos, commit emails, SSH keys
- Stack Overflow: employees asking questions about internal tools/tech
- Forums: employees discussing work-related topics

---

## Phase 3: Technical Intelligence

### Technology Stack Identification
- Job postings: technologies mentioned in job descriptions
- BuiltWith: `builtwith.com/target.com` -- technology profiling
- Wappalyzer: browser extension for tech detection
- HTTP headers: `Server`, `X-Powered-By`, custom headers
- Error messages: framework-specific error formats
- JavaScript files: library references, framework signatures
- DNS TXT records: SPF (email providers), DMARC, verification records for SaaS tools

### Cloud Infrastructure
- AWS: check for S3 buckets (`target-backup`, `target-dev`, `target-assets`)
- Azure: check for blob storage (`target.blob.core.windows.net`)
- GCP: check for storage buckets
- GitHub Actions/CI: check for cloud deployment configurations
- Cloud IP ranges: cross-reference target IPs with cloud provider ranges

### Document Metadata
- Download public documents: PDFs, DOCX, XLSX from target website
- Extract metadata: `exiftool document.pdf` -- author, software, creation date, paths
- FOCA: automated metadata extraction and analysis from multiple documents
- Look for: usernames, software versions, internal paths, printer names, email addresses
- Metadata from images: EXIF data including GPS coordinates, camera model, timestamps

### Source Code Intelligence
- GitHub organization repos: public repositories, contributors
- GitHub search: `org:targetorg password`, `org:targetorg api_key`, `org:targetorg secret`
- GitDorker, trufflehog, gitleaks: automated secret scanning
- Commit history: look at commit messages, diff for accidentally committed secrets
- GitHub Actions: workflow files may reveal infrastructure details
- Package registries: npm, PyPI, Docker Hub -- packages published by target

---

## Phase 4: Infrastructure Mapping

### Network Mapping
- IP ranges: from ASN lookup, DNS records, and historical data
- Reverse IP lookup: find all domains on a given IP (ViewDNS.info, HackerTarget)
- Port scanning (active, only if authorized): `nmap -sV -sC target_ip`
- Service identification: map services to IP:port combinations
- CDN identification: is the target behind Cloudflare, Akamai, Fastly?
- Real IP discovery: historical DNS, email headers, direct IP subdomains

### Physical Intelligence
- Office locations: Google Maps, company website, job postings
- Building photos: Google Street View, social media posts
- Wi-Fi networks: WiGLE.net for known SSIDs near target locations
- Physical security: security cameras, badge readers, reception procedures (from photos/reviews)
- Nearby businesses: shared building access, co-working spaces

### Third-Party Relationships
- Vendors and partners: press releases, case studies, integration pages
- Technology providers: SaaS tools, hosting providers, CDN providers
- Subsidiaries and acquisitions: related domains and organizations
- Supply chain: identify key software/service dependencies

---

## Phase 5: Analysis and Correlation

### Data Correlation
- Cross-reference email addresses across breach databases and social media
- Map employee names to usernames to email formats
- Correlate infrastructure changes with organizational events (acquisitions, migrations)
- Build relationship graphs: people, domains, IPs, technologies

### Attack Surface Summary
- External-facing assets: domains, subdomains, IPs, services, ports
- Email infrastructure: mail servers, SPF/DMARC policy strength
- Cloud presence: identified cloud resources and potential misconfigurations
- Human attack surface: employees likely to be targeted (roles, public exposure)
- Third-party risk: vendors that could be compromised for supply chain attack

### Prioritization
- Rank findings by exploitability and potential impact
- Identify quick wins: exposed credentials, misconfigured services, leaked secrets
- Identify phishing targets: employees with high access and public profiles
- Identify infrastructure weaknesses: outdated services, missing security headers

---

## Phase 6: Reporting

### OSINT Report Structure
1. Executive summary
2. Scope and methodology
3. External attack surface map
4. Employee and credential findings
5. Technology and infrastructure findings
6. Third-party and supply chain findings
7. Risk assessment and prioritization
8. Recommendations for exposure reduction

### Key Recommendations
- Remove sensitive documents and metadata from public websites
- Implement strict SPF, DKIM, and DMARC policies
- Monitor for credential leaks in breach databases
- Review and restrict public information about technology stack
- Employee security awareness: limit sensitive information sharing
- Monitor code repositories for secret exposure
- Review cloud storage permissions and access controls

---

## Tools Quick Reference

| Task | Tools |
|---|---|
| Domain/DNS | dig, subfinder, amass, dnsrecon, dnsx |
| WHOIS | whois, DomainTools, SecurityTrails |
| Search | Google Dorks, Shodan, Censys, BinaryEdge |
| Email | theHarvester, Hunter.io, phonebook.cz |
| People | linkedin2username, Maltego |
| Credentials | HaveIBeenPwned, DeHashed |
| Code Search | trufflehog, gitleaks, GitDorker |
| Metadata | exiftool, FOCA, metagoofil |
| Web Archive | Wayback Machine, waybackurls, gau |
| Automation | SpiderFoot, Recon-ng, Maltego |
| Visualization | Maltego, Gephi, draw.io |
