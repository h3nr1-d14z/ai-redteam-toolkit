# Red Team Operations Methodology

## Phase 1: Planning and Preparation

### Engagement Planning
- Define objectives: what does the client want tested? (detection capability, incident response, specific attack scenarios)
- Establish rules of engagement: authorized techniques, targets, exclusions, emergency procedures
- Define success criteria: what constitutes a successful engagement?
- Identify key stakeholders: who knows about the engagement (trusted agents)?
- Set up communication channels: encrypted comms, deconfliction procedures
- Define reporting requirements and cadence

### Threat Modeling
- Identify the threat actors relevant to the client (nation-state, cybercriminal, insider, hacktivist)
- Map TTPs to MITRE ATT&CK framework
- Select appropriate tools, techniques, and infrastructure for the emulated threat
- Create attack plan with primary and alternate paths
- Identify high-value targets and crown jewels

### Infrastructure Setup
- C2 framework: Cobalt Strike, Sliver, Mythic, Havoc, Brute Ratel
- Redirectors: cloud instances (multiple providers) acting as traffic redirectors
- Domain fronting or redirector domains categorized to blend with normal traffic
- Phishing infrastructure: GoPhish, Evilginx2, custom SMTP (ensure SPF/DKIM)
- Payload hosting: short-lived URLs, CDN-hosted payloads
- Communication channels: encrypted team chat, shared note-taking
- OPSEC: separate VMs per engagement, VPN chains, clean browser profiles

### OPSEC Considerations
- Use separate infrastructure per engagement, never reuse between clients
- Categorize domains before use (Health, Business, Technology categories via domain categorization services)
- Age domains 30+ days before use
- Use legitimate SSL certificates (Let's Encrypt)
- Vary User-Agent strings, JA3 fingerprints, beacon intervals
- Implement kill dates on all implants
- Use malleable C2 profiles that mimic legitimate traffic

---

## Phase 2: Reconnaissance

### OSINT
- Employee enumeration: LinkedIn, company website, conference talks, GitHub profiles
- Email format discovery: Hunter.io, email permutations, catch-all testing
- Email verification: verify discovered emails without alerting targets
- Social media analysis: employee posts, photos (badge details, office layout), tech discussions
- Document metadata: FOCA, exiftool on public documents (usernames, software versions, paths)
- Credential breaches: check for employee emails in breach databases (authorized only)

### Technical Reconnaissance
- DNS enumeration: subdomains, MX records, TXT records (SPF, DMARC)
- External attack surface: Shodan, Censys, BinaryEdge for internet-facing services
- Technology stack: job postings, error messages, response headers
- SSL certificate analysis: organization details, alt names, certificate transparency
- Cloud infrastructure: identify AWS, Azure, GCP usage, enumerate public cloud resources
- VPN endpoints: identify remote access infrastructure
- Wi-Fi: wardriving to identify corporate SSIDs (if physical testing authorized)

### Intelligence Products
- Target dossier: organizational structure, key personnel, technology stack
- Attack surface map: external IPs, domains, services, entry points
- Prioritized target list: most likely to succeed, highest impact

---

## Phase 3: Initial Access

### Phishing
- Spearphishing with link: credential harvesting (Evilginx2 for MFA bypass)
- Spearphishing with attachment: macro documents, ISO/IMG containers, LNK files
- Pretext development: tailored to target role and context (invoice, HR document, IT notification)
- Delivery: direct email, LinkedIn InMail, contact form submission
- Payload types: HTA, macro-enabled Office docs, OneNote with embedded files, MSI, DLL sideloading
- Evasion: obfuscate macros, use signed binaries for execution, sandbox detection

### Exploitation of External Services
- Web application vulnerabilities: SQLi, RCE, SSRF leading to internal access
- VPN/remote access: default credentials, known CVEs, credential stuffing
- Exposed services: RDP, SSH, SMB, databases with weak credentials
- Cloud misconfigurations: public S3 buckets with credentials, exposed cloud metadata

### Physical Access (if authorized)
- Tailgating and badge cloning
- USB drop attacks: Rubber Ducky, Bash Bunny, malicious USB drives
- Rogue devices: Raspberry Pi, Wi-Fi Pineapple, LAN Turtle
- Lock picking, access control bypass

### Supply Chain
- Compromise a third-party vendor or service provider (if in scope)
- Waterhole attack: compromise a website frequented by target employees

---

## Phase 4: Execution and Establishing Foothold

### Initial Payload Execution
- LOLBins (Living off the Land): `mshta`, `wscript`, `cscript`, `rundll32`, `certutil`, `msiexec`
- PowerShell: AMSI bypass, download cradles, reflection-based loading
- DLL sideloading: place malicious DLL alongside legitimate signed executable
- Process injection: early bird injection, process hollowing, thread hijacking
- Memory-only execution: reflective DLL injection, .NET assembly loading

### C2 Establishment
- Initial callback to C2 infrastructure via HTTPS (blends with normal traffic)
- Use high-sleep intervals initially (30-60 minutes) to avoid detection
- Establish backup C2 channels: DNS, named pipes, SMB
- Verify connectivity and stability before proceeding

### Persistence
- Scheduled tasks: `schtasks /create /tn "WindowsUpdate" /tr "payload" /sc hourly`
- Registry run keys: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
- Startup folder: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`
- DLL search order hijacking: place DLL in application directory
- WMI event subscriptions: persistent WMI consumer
- COM object hijacking: modify COM object registry entries
- Service creation (requires admin): `sc create svcname binPath= "payload"`
- Group Policy: modify GPO for domain-wide persistence (domain admin required)
- Golden Ticket / Silver Ticket: Kerberos-based persistence

---

## Phase 5: Privilege Escalation

### Local Privilege Escalation (Windows)
- Service misconfigurations: unquoted paths, weak permissions, writable service binaries
- Token impersonation: SeImpersonatePrivilege (Potato attacks: JuicyPotato, PrintSpoofer, GodPotato)
- Always Install Elevated: MSI-based escalation if enabled
- DLL hijacking: missing DLLs in privileged processes
- Scheduled tasks with weak permissions
- Credential harvesting: cached credentials, credential manager, autologon
- Kernel exploits: as a last resort for unpatched systems
- Tools: `winpeas.exe`, `PowerUp.ps1`, `SharpUp.exe`

### Domain Privilege Escalation
- Kerberoasting: request TGS for service accounts, crack offline
  - `Rubeus.exe kerberoast /outfile:hashes.txt`
  - Crack: `hashcat -m 13100 hashes.txt wordlist.txt`
- AS-REP Roasting: users without pre-authentication
  - `Rubeus.exe asreproast /outfile:asrep.txt`
- Unconstrained/Constrained Delegation abuse
- Resource-Based Constrained Delegation (RBCD) abuse
- ACL abuse: WriteDACL, GenericAll, GenericWrite on domain objects
- ADCS (Active Directory Certificate Services): ESC1-ESC8 attacks
  - `Certify.exe find /vulnerable`
- Group Policy abuse: modify GPOs you have write access to
- LAPS password reading if you have the permission
- Tools: BloodHound (map attack paths), `SharpHound.exe` (collector)

---

## Phase 6: Lateral Movement

### Credential-Based Movement
- Pass-the-Hash: `mimikatz "sekurlsa::pth"`, CrackMapExec `--hash`
- Pass-the-Ticket: `Rubeus.exe ptt /ticket:base64_ticket`
- Overpass-the-Hash: request TGT with NTLM hash, use Kerberos for access
- RDP: with captured credentials or hash (requires restricted admin mode for hash)
- WinRM: `Enter-PSSession -ComputerName target -Credential $cred`
- PsExec: `psexec.exe \\target -u user -p pass cmd.exe`
- WMI: `wmic /node:target process call create "command"`
- DCOM: various DCOM objects for lateral movement
- SSH: internal Linux systems with captured keys or credentials

### Network-Based Movement
- SMB: access shares, deploy payloads via writable shares
- Internal pivoting: SOCKS proxy through compromised hosts
- Port forwarding: `ssh -L`, `netsh`, Cobalt Strike's `rportfwd`
- VPN pivoting: use captured VPN credentials for additional access

### Tool Movement
- Fileless: execute tools in memory, don't drop to disk
- LOLBins for file transfer: `certutil -urlcache`, `bitsadmin`, `powershell iwr`
- SMB for lateral tool transfer (stays internal, no internet traffic)
- Living off the Land: use built-in admin tools already present

---

## Phase 7: Collection and Exfiltration

### Data Discovery
- Identify crown jewels: databases, file shares, email servers, code repositories
- Search file shares: `dir \\server\share /s /b | findstr /i "password credential secret"`
- Search for sensitive documents: financial data, PII, IP, credentials
- Email access: Outlook Web, Exchange, mailbox search
- Database access: connect to identified databases with captured credentials

### Data Staging
- Compress and encrypt data before exfiltration
- Stage in a temporary location
- Use standard archive formats: ZIP, 7z with AES encryption
- Split large files to avoid detection on size-based alerts

### Exfiltration
- HTTPS to C2: standard C2 channel, blends with web traffic
- DNS tunneling: slow but stealthy, `dnscat2`, `iodine`
- Cloud storage: upload to attacker-controlled S3/Azure Blob
- Email: send data via compromised email accounts
- Physical: USB if physical access available
- Test data exfiltration at different rates to assess DLP capabilities
- Always use test/synthetic data unless real data exfiltration is explicitly in scope

---

## Phase 8: Cleanup and Reporting

### Artifact Cleanup
- Remove all implants, backdoors, persistence mechanisms
- Delete all tools uploaded to target systems
- Remove test accounts created during engagement
- Clear relevant log entries only if specifically authorized (usually you do NOT)
- Document all artifacts and their locations for the report
- Verify cleanup completeness

### Detection Assessment
- Document every action and whether it was detected
- Map detections to MITRE ATT&CK techniques
- Calculate detection rate, MTTD, MTTR
- Identify gaps in detection coverage
- Provide specific detection rule recommendations

### Report Deliverables
- Executive summary: objectives, results, business impact
- Attack narrative: chronological story of the engagement
- MITRE ATT&CK heat map: techniques used and detection status
- Findings: technical vulnerabilities and process gaps
- Recommendations: prioritized by impact and effort
- Cleanup verification: confirmation all artifacts removed
- IOCs: provide to blue team for historical log analysis

---

## Tools Quick Reference

| Category | Tools |
|---|---|
| C2 Frameworks | Cobalt Strike, Sliver, Mythic, Havoc, Brute Ratel |
| Phishing | GoPhish, Evilginx2, custom SMTP |
| AD Enumeration | BloodHound, SharpHound, ADRecon, PowerView |
| Credential Attacks | Mimikatz, Rubeus, Certify, hashcat |
| Privilege Escalation | WinPEAS, SharpUp, PowerUp, Seatbelt |
| Lateral Movement | CrackMapExec, Impacket, PsExec, Evil-WinRM |
| Evasion | ScareCrow, Freeze, NimPackt, custom loaders |
| Exfiltration | dnscat2, DNSExfiltrator, custom HTTPS |
| OPSEC | Proxychains, domain fronting, redirectors |
