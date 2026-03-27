# Certification Preparation Paths

Maps industry security certifications to AI-RedTeam-Toolkit commands and lab exercises. Use these paths to practice hands-on skills while studying for exams.

> **Tip**: Each command maps to a `commands/<name>.md` file containing detailed methodology steps. Run the command in your AI assistant to get guided, interactive practice.

---

## CEH v12 (Certified Ethical Hacker)

EC-Council CEH v12 -- 20 modules mapped to toolkit commands.

| Module | Topic | Commands to Practice | Lab Suggestion |
|--------|-------|---------------------|----------------|
| M01 | Introduction to Ethical Hacking | `/new-engagement`, `/deconflict` | Review `methodology/` docs |
| M02 | Footprinting and Reconnaissance | `/recon`, `/recon-passive`, `/osint`, `/osint-domain`, `/osint-org` | Run passive recon against lab targets |
| M03 | Scanning Networks | `/scan-ports`, `/recon-active`, `/quick-scan` | Scan DVWA/Metasploitable with nmap |
| M04 | Enumeration | `/subdomain-enum`, `/recon-active`, `/scan-ports` | Enumerate services on HackTheBox |
| M05 | Vulnerability Analysis | `/nuclei-scan`, `/pentest`, `/full-assessment` | Run nuclei against OWASP Juice Shop |
| M06 | System Hacking | `/privesc`, `/hash-crack`, `/persistence` | Linux/Windows privesc labs (TryHackMe) |
| M07 | Malware Threats | `/malware-analyze`, `/reverse`, `/binary-analyze` | Analyze samples in REMnux sandbox |
| M08 | Sniffing | `/sniff`, `/network-forensics` | Capture traffic on lab network with Wireshark |
| M09 | Social Engineering | `/phishing-campaign`, `/osint-person` | GoPhish campaign against test mailboxes |
| M10 | Denial-of-Service | (out of scope -- DoS not supported) | Study conceptually only |
| M11 | Session Hijacking | `/session-hijack`, `/auth-test` | Cookie theft on DVWA |
| M12 | Evading IDS, Firewalls, Honeypots | `/evasion`, `/payload-gen`, `/encode-decode` | Test evasion against Snort/Suricata lab |
| M13 | Hacking Web Servers | `/pentest`, `/infra-pentest`, `/nuclei-scan` | Attack Metasploitable web services |
| M14 | Hacking Web Applications | `/sqli-test`, `/xss-hunt`, `/ssrf-scan`, `/ssti-test`, `/upload-test`, `/api-pentest` | DVWA, bWAPP, Juice Shop |
| M15 | SQL Injection | `/sqli-test`, `/pentest` | SQLi labs on DVWA, sqlilabs |
| M16 | Hacking Wireless Networks | `/wireless`, `/sniff` | Test lab Wi-Fi with aircrack-ng |
| M17 | Hacking Mobile Platforms | `/mobile-pentest`, `/android-analyze`, `/ios-analyze`, `/frida-hook`, `/ssl-pinning-bypass` | Analyze InsecureBankv2 APK |
| M18 | IoT and OT Hacking | `/iot-hack`, `/firmware-analyze`, `/protocol-re` | Firmware extraction with binwalk on lab device |
| M19 | Cloud Computing | `/cloud-pentest`, `/cloud-recon`, `/container-escape` | CloudGoat, flAWS.cloud |
| M20 | Cryptography | `/crypto-attack`, `/hash-crack`, `/encode-decode`, `/ctf-crypto` | CryptoHack, OverTheWire Krypton |

### CEH Study Tips

- **Exam format**: 125 MCQs, 4 hours. Focus on tool names and attack phases.
- **Hands-on**: CEH Practical requires demonstrating attacks -- practice each command above in lab environments.
- **Coverage**: This toolkit covers ~18 of 20 modules directly (DoS and some theoretical modules are study-only).

---

## OSCP (Offensive Security Certified Professional)

OffSec PEN-200 -- Structured by exam-relevance priority. The OSCP exam requires exploiting machines in a timed lab, so commands are ordered by practical importance.

### Phase 1: Information Gathering (Critical -- Every Exam Machine)

| Topic | Commands | Practice Target |
|-------|---------|----------------|
| Active information gathering | `/recon`, `/recon-active`, `/scan-ports` | HackTheBox easy machines |
| Passive information gathering | `/recon-passive`, `/osint-domain` | OSINT exercises on TryHackMe |
| Vulnerability scanning | `/nuclei-scan`, `/quick-scan` | Metasploitable 2/3 |
| Enumeration (DNS, SMB, SNMP, HTTP) | `/subdomain-enum`, `/recon-active` | Prove grounds Practice |

### Phase 2: Web Application Attacks (High Priority)

| Topic | Commands | Practice Target |
|-------|---------|----------------|
| SQL injection | `/sqli-test` | SQLi labs, PortSwigger Academy |
| XSS and client-side attacks | `/xss-hunt` | PortSwigger XSS labs |
| File inclusion / upload | `/upload-test`, `/pentest` | DVWA file inclusion |
| Command injection | `/pentest`, `/exploit` | PentesterLab |
| SSRF and SSTI | `/ssrf-scan`, `/ssti-test` | PortSwigger SSRF labs |
| API attacks | `/api-pentest` | OWASP crAPI |
| Authentication bypass | `/auth-test`, `/session-hijack` | Juice Shop auth labs |

### Phase 3: Exploitation (High Priority)

| Topic | Commands | Practice Target |
|-------|---------|----------------|
| Buffer overflow (Windows) | `/bof-exploit`, `/shellcode-gen` | TryHackMe BOF prep room |
| Buffer overflow (Linux) | `/bof-exploit`, `/rop-chain` | OverTheWire Narnia |
| Public exploit modification | `/exploit`, `/payload-gen` | Exploit-DB + Prove Grounds |
| Custom exploit development | `/exploit`, `/bof-exploit` | VulnHub machines |
| Shellcode and payloads | `/shellcode-gen`, `/payload-gen` | Custom shellcode labs |

### Phase 4: Post-Exploitation (Essential for Exam Points)

| Topic | Commands | Practice Target |
|-------|---------|----------------|
| Linux privilege escalation | `/privesc` | TryHackMe Linux PrivEsc room |
| Windows privilege escalation | `/privesc` | TryHackMe Windows PrivEsc room |
| Password attacks | `/hash-crack`, `/generate-wordlist` | HackTheBox machines |
| Lateral movement (AD) | `/lateral-movement`, `/ad-pentest` | Prove Grounds AD sets |
| Persistence | `/persistence` | Custom lab VMs |
| Active Directory attacks | `/ad-pentest`, `/hash-crack` | GOAD (Game of Active Directory) |

### Phase 5: Reporting and Documentation

| Topic | Commands | Practice Target |
|-------|---------|----------------|
| Engagement management | `/new-engagement`, `/close-engagement` | Every practice machine |
| Evidence collection | `/screenshot`, `/timeline` | Document every exploit chain |
| Report writing | `/write-report`, `/write-finding`, `/vuln-report` | Practice professional reports |

### OSCP Study Tips

- **Exam format**: 23 hours 45 minutes hands-on + 24 hours report writing. 3 standalone machines + 1 AD set.
- **Prioritize**: Enumeration > Web attacks > Privesc > AD attacks > BOF.
- **Practice**: Aim for 50+ machines on HackTheBox/Prove Grounds before attempting the exam.
- **Reporting**: Use `/write-report` on every practice machine to build the habit.

---

## PNPT (Practical Network Penetration Tester)

TCM Security PNPT -- 5 courses mapped to toolkit practice.

### Course 1: Practical Ethical Hacking (PEH)

| Topic | Commands | Notes |
|-------|---------|-------|
| Networking & Linux fundamentals | `/scan-ports`, `/recon` | Build baseline skills |
| Reconnaissance | `/recon`, `/recon-passive`, `/recon-active`, `/osint` | Thorough info gathering |
| Scanning & enumeration | `/scan-ports`, `/subdomain-enum`, `/nuclei-scan` | Service fingerprinting |
| Exploitation | `/exploit`, `/pentest`, `/sqli-test`, `/xss-hunt` | Common vulnerability exploitation |
| Post-exploitation | `/privesc`, `/persistence`, `/hash-crack` | Escalate and maintain |
| Active Directory | `/ad-pentest`, `/lateral-movement`, `/hash-crack` | Kerberoasting, pass-the-hash |
| Report writing | `/write-report`, `/write-finding` | Professional deliverables |

### Course 2: Windows Privilege Escalation

| Topic | Commands | Notes |
|-------|---------|-------|
| Windows enumeration | `/privesc`, `/recon-active` | Enumerate services, permissions, scheduled tasks |
| Kernel exploits | `/exploit`, `/privesc` | Identify and apply kernel CVEs |
| Token impersonation | `/privesc` | Potato attacks, SeImpersonate |
| Password mining | `/hash-crack`, `/generate-wordlist` | SAM dump, cached creds |
| DLL hijacking | `/privesc`, `/payload-gen` | Writable PATH directories |

### Course 3: Linux Privilege Escalation

| Topic | Commands | Notes |
|-------|---------|-------|
| Linux enumeration | `/privesc`, `/recon-active` | SUID, cron, capabilities |
| Kernel exploits | `/exploit`, `/privesc` | Dirty COW, etc. |
| SUID/SGID abuse | `/privesc` | GTFOBins reference |
| Cron and PATH abuse | `/privesc` | Writable scripts, PATH injection |
| Wildcard injection | `/privesc`, `/exploit` | Tar, rsync wildcards |

### Course 4: Open-Source Intelligence (OSINT) Fundamentals

| Topic | Commands | Notes |
|-------|---------|-------|
| Email and identity OSINT | `/osint-person`, `/osint` | Email permutations, social media |
| Domain OSINT | `/osint-domain`, `/subdomain-enum` | WHOIS, DNS, certificate transparency |
| Organization OSINT | `/osint-org`, `/cloud-recon` | Business relationships, employees |
| Image and metadata | `/osint` | EXIF, geolocation |

### Course 5: External Pentest Playbook

| Topic | Commands | Notes |
|-------|---------|-------|
| External reconnaissance | `/recon`, `/osint-domain`, `/subdomain-enum`, `/cloud-recon` | Full external footprint |
| Vulnerability assessment | `/nuclei-scan`, `/scan-ports`, `/quick-scan` | Automated + manual scanning |
| Exploitation | `/exploit`, `/pentest`, `/api-pentest` | Exploit confirmed vulns |
| Reporting | `/write-report`, `/vuln-report`, `/close-engagement` | Client-ready deliverables |

### PNPT Study Tips

- **Exam format**: 5 days hands-on + 2 days reporting. External pentest + AD environment.
- **Key differentiator**: Report quality matters as much as exploitation.
- **AD focus**: Spend extra time on `/ad-pentest` -- the AD portion is heavily weighted.
- **OSINT**: Unlike OSCP, PNPT includes OSINT as a graded component.

---

## CND (Certified Network Defender)

EC-Council CND -- Defensive/blue-team certification. Maps toolkit commands used for defensive validation, monitoring, and incident response.

### Module Mapping

| Module | Topic | Commands for Validation | Defensive Focus |
|--------|-------|------------------------|----------------|
| M01 | Network Attacks and Defense Strategies | `/recon`, `/scan-ports` | Understand attacker methodology to build defenses |
| M02 | Administrative Network Security | `/deconflict`, `/new-engagement` | Policy, procedure, authorization frameworks |
| M03 | Technical Network Security | `/infra-pentest`, `/scan-ports` | Validate firewall rules, ACLs, segmentation |
| M04 | Network Perimeter Security | `/recon-active`, `/nuclei-scan`, `/quick-scan` | Test perimeter controls -- IDS/IPS effectiveness |
| M05 | Endpoint Security | `/privesc`, `/malware-analyze` | Validate endpoint hardening and AV/EDR |
| M06 | Cloud Security | `/cloud-pentest`, `/cloud-recon`, `/container-escape` | Audit cloud configs, test container isolation |
| M07 | Wireless Security | `/wireless`, `/sniff` | Validate wireless encryption and access controls |
| M08 | IoT Security | `/iot-hack`, `/firmware-analyze` | Test IoT device hardening |
| M09 | Cryptography and PKI | `/crypto-attack`, `/ssl-pinning-bypass`, `/encode-decode` | Validate crypto implementations, cert management |
| M10 | Network Traffic Monitoring | `/sniff`, `/network-forensics`, `/log-analysis` | Validate monitoring and alerting pipelines |
| M11 | Network Logs Monitoring and Analysis | `/log-analysis`, `/timeline` | SIEM validation, log correlation testing |
| M12 | Incident Response | `/incident-response`, `/forensics`, `/timeline` | IR playbook testing and validation |
| M13 | Business Continuity and Disaster Recovery | `/incident-response` | Validate backup/recovery procedures |
| M14 | Risk Management and Vulnerability Assessment | `/nuclei-scan`, `/full-assessment`, `/vuln-report` | Vulnerability management program validation |

### CND Defensive Command Usage

These commands help defenders validate their security controls:

| Defensive Activity | Commands | What to Validate |
|-------------------|---------|-----------------|
| Perimeter testing | `/recon`, `/scan-ports`, `/nuclei-scan` | Are external services properly hardened? |
| IDS/IPS validation | `/evasion`, `/payload-gen` | Do detection systems catch known attack patterns? |
| Log monitoring | `/log-analysis`, `/timeline` | Are security events properly logged and alerted? |
| Incident response | `/incident-response`, `/forensics`, `/memory-forensics`, `/disk-forensics` | Can the team detect, contain, and eradicate threats? |
| Vulnerability scanning | `/nuclei-scan`, `/full-assessment` | Is the vulnerability management cycle effective? |
| Endpoint hardening | `/privesc`, `/malware-analyze` | Are endpoints resistant to privilege escalation? |
| Network segmentation | `/lateral-movement`, `/infra-pentest` | Can an attacker move between network zones? |
| Cloud security posture | `/cloud-pentest`, `/cloud-recon` | Are cloud resources properly configured? |

### CND Study Tips

- **Exam format**: 100 MCQs, 4 hours. Focus on defensive concepts and tools.
- **Hands-on**: Use toolkit commands offensively against lab targets, then build defensive rules to detect and block each attack.
- **Purple team approach**: Run `/evasion` to test if your Snort/Suricata rules catch encoded payloads.

---

## Additional Certifications -- Quick Reference

### CompTIA PenTest+ (PT0-002)

| Domain | Weight | Key Commands |
|--------|--------|-------------|
| Planning and Scoping | 14% | `/new-engagement`, `/deconflict`, `/redteam-plan` |
| Information Gathering | 22% | `/recon`, `/recon-passive`, `/recon-active`, `/osint`, `/scan-ports`, `/subdomain-enum` |
| Attacks and Exploits | 30% | `/pentest`, `/exploit`, `/sqli-test`, `/xss-hunt`, `/privesc`, `/ad-pentest`, `/wireless` |
| Reporting and Communication | 18% | `/write-report`, `/write-finding`, `/vuln-report`, `/close-engagement` |
| Tools and Code Analysis | 16% | `/binary-analyze`, `/deobfuscate`, `/reverse`, `/nuclei-scan` |

### eJPT (eLearnSecurity Junior Penetration Tester)

| Topic Area | Key Commands |
|-----------|-------------|
| Networking fundamentals | `/scan-ports`, `/recon-active`, `/sniff` |
| Web app testing | `/pentest`, `/sqli-test`, `/xss-hunt` |
| Host and network pentesting | `/infra-pentest`, `/privesc`, `/exploit` |
| Reporting | `/write-report`, `/write-finding` |

### CRTP (Certified Red Team Professional)

| Topic Area | Key Commands |
|-----------|-------------|
| AD enumeration | `/ad-pentest`, `/recon-active` |
| AD privilege escalation | `/ad-pentest`, `/privesc` |
| Lateral movement | `/lateral-movement`, `/ad-pentest` |
| Persistence | `/persistence`, `/ad-pentest` |
| Evasion | `/evasion`, `/payload-gen` |

### GPEN (GIAC Penetration Tester)

| Topic Area | Key Commands |
|-----------|-------------|
| Reconnaissance | `/recon`, `/osint`, `/scan-ports` |
| Password attacks | `/hash-crack`, `/generate-wordlist`, `/auth-test` |
| Exploitation | `/exploit`, `/pentest`, `/bof-exploit` |
| Post-exploitation | `/privesc`, `/lateral-movement`, `/persistence` |
| Web application attacks | `/sqli-test`, `/xss-hunt`, `/ssrf-scan`, `/api-pentest` |

---

## Recommended Practice Lab Platforms

| Platform | Cost | Best For | URL |
|----------|------|----------|-----|
| HackTheBox | Free/VIP | OSCP, CEH, PNPT | hackthebox.com |
| TryHackMe | Free/Premium | Beginners, CEH, eJPT | tryhackme.com |
| Prove Grounds | Free/VIP | OSCP-style machines | offsec.com |
| PortSwigger Academy | Free | Web app attacks (OSCP, CEH M14-15) | portswigger.net |
| CloudGoat | Free | Cloud security (CND, CEH M19) | github.com/RhinoSecurityLabs |
| GOAD | Free | AD attacks (OSCP, PNPT, CRTP) | github.com/Orange-Cyberdefense/GOAD |
| VulnHub | Free | Offline practice machines | vulnhub.com |
| CryptoHack | Free | Cryptography (CEH M20) | cryptohack.org |
| PicoCTF | Free | CTF practice | picoctf.org |
| flAWS.cloud | Free | AWS cloud security | flaws.cloud |
