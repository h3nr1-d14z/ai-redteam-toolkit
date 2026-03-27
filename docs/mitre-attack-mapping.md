# MITRE ATT&CK Command Mapping

Maps every AI-RedTeam-Toolkit slash command to the [MITRE ATT&CK](https://attack.mitre.org/) framework (Enterprise v14) and the Lockheed Martin Cyber Kill Chain. Use this reference to understand which adversary behaviors each command simulates and to align engagements with threat-intelligence reporting.

> **Convention**: Commands may appear under multiple tactics when they span several phases of an operation. Technique IDs link to the official MITRE page.

---

## TA0043 -- Reconnaissance

| Command | Techniques | Description |
|---------|-----------|-------------|
| `/recon` | T1595.001, T1595.002, T1592, T1590 | Active scanning (IP blocks, vulnerability scanning), gather victim host and network info |
| `/recon-active` | T1595.001, T1595.002, T1595.003 | Active scanning -- wordlist-based, port-based, and brute-force enumeration |
| `/recon-passive` | T1593, T1593.001, T1593.002, T1594, T1589 | Search open websites/domains, social media, search engines, code repos |
| `/osint` | T1593, T1594, T1589, T1590, T1591 | Full OSINT workflow -- gather victim identity, network, org info from open sources |
| `/osint-person` | T1589.001, T1589.002, T1589.003 | Gather employee names, email addresses, credentials |
| `/osint-domain` | T1590.001, T1590.002, T1590.004, T1593.002 | Domain/IP info, DNS records, WHOIS, search engines |
| `/osint-org` | T1591.001, T1591.002, T1591.004 | Gather org business relationships, physical locations, roles |
| `/subdomain-enum` | T1595.003, T1590.002 | Subdomain discovery via brute force and passive DNS |
| `/cloud-recon` | T1590.004, T1590.006, T1526 | Cloud infrastructure reconnaissance -- S3 buckets, metadata, service discovery |
| `/scan-ports` | T1595.001, T1046 | Port scanning and service version enumeration |
| `/quick-scan` | T1595.001, T1595.002 | Fast surface-level scan combining port and vulnerability checks |
| `/sniff` | T1040 | Network sniffing for passive traffic capture and analysis |

## TA0042 -- Resource Development

| Command | Techniques | Description |
|---------|-----------|-------------|
| `/payload-gen` | T1587.001, T1588.002 | Develop/obtain exploits and payloads for delivery |
| `/shellcode-gen` | T1587.004 | Develop custom shellcode (x86, x64, ARM) |
| `/rop-chain` | T1587.004 | ROP gadget chain construction for exploit development |
| `/phishing-campaign` | T1585.001, T1585.002, T1586.002, T1566 | Establish accounts/infrastructure for phishing delivery |
| `/c2-setup` | T1583.001, T1583.004, T1583.006, T1587.001 | Acquire domains, servers, web services for C2 infrastructure |
| `/generate-wordlist` | T1587 | Build custom wordlists for credential and directory attacks |
| `/redteam-plan` | T1583, T1587, T1588 | Plan and stage red team operations -- infrastructure, tools, capabilities |
| `/evasion` | T1587.001 | Develop payloads and techniques with detection evasion in mind |

## TA0001 -- Initial Access

| Command | Techniques | Description |
|---------|-----------|-------------|
| `/pentest` | T1190, T1133 | Full web pentest -- exploit public-facing applications, external services |
| `/exploit` | T1190, T1203 | Exploit specific vulnerability for initial foothold |
| `/sqli-test` | T1190 | SQL injection to exploit public-facing web applications |
| `/xss-hunt` | T1189 | XSS discovery -- potential drive-by compromise vector |
| `/ssrf-scan` | T1190 | SSRF to exploit server-side request handling |
| `/ssti-test` | T1190 | Server-side template injection for code execution |
| `/auth-test` | T1078 | Test valid accounts -- default credentials, auth bypass |
| `/upload-test` | T1190 | File upload exploitation for webshell or code execution |
| `/phishing-campaign` | T1566.001, T1566.002, T1566.003 | Spearphishing attachment, link, and service-based attacks |
| `/api-pentest` | T1190 | API security flaws enabling unauthorized access |
| `/wireless` | T1557.004 | Rogue wireless access point / evil twin for initial access |
| `/iot-hack` | T1190 | Exploit internet-facing IoT device interfaces |
| `/session-hijack` | T1078, T1550 | Hijack valid sessions for unauthorized initial access |

## TA0002 -- Execution

| Command | Techniques | Description |
|---------|-----------|-------------|
| `/exploit` | T1059, T1203 | Execute exploit payloads -- command/scripting interpreter, client exploitation |
| `/bof-exploit` | T1203 | Buffer overflow exploitation for user/client execution |
| `/shellcode-gen` | T1059.004 | Shellcode execution via command and scripting interpreter |
| `/payload-gen` | T1059, T1204 | Generate payloads requiring user execution or interpreter |
| `/rop-chain` | T1203 | ROP chain-based code execution in exploit context |
| `/frida-hook` | T1059 | Runtime code injection and hooking via Frida scripting |
| `/memory-hack` | T1055 | Process injection and memory manipulation for code execution |
| `/ctf-pwn` | T1203 | Binary exploitation challenge -- execute via overflow, format string |
| `/ssti-test` | T1059 | Template injection for server-side code execution |

## TA0003 -- Persistence

| Command | Techniques | Description |
|---------|-----------|-------------|
| `/persistence` | T1053, T1136, T1543, T1547, T1546, T1556 | Scheduled tasks, create accounts, system services, boot/logon scripts, event-triggered execution, modify auth process |
| `/c2-setup` | T1573, T1071, T1105 | Persistent C2 channel via encrypted protocols and ingress tools |
| `/ad-pentest` | T1098, T1136.002 | Account manipulation and domain account creation for persistence |
| `/phishing-campaign` | T1137 | Persistence via Office application startup (macro persistence) |

## TA0004 -- Privilege Escalation

| Command | Techniques | Description |
|---------|-----------|-------------|
| `/privesc` | T1068, T1548, T1134, T1574, T1055 | Exploit vulnerabilities, abuse elevation controls, token manipulation, DLL hijacking, process injection |
| `/container-escape` | T1611 | Escape to host -- container breakout via kernel or misconfiguration |
| `/bof-exploit` | T1068 | Exploitation for privilege escalation via buffer overflow |
| `/ad-pentest` | T1078.002, T1484 | Domain account privilege escalation, domain policy modification |
| `/rop-chain` | T1068 | ROP-based exploitation targeting kernel or privileged processes |
| `/memory-hack` | T1055 | Process injection for privilege escalation in running processes |

## TA0005 -- Defense Evasion

| Command | Techniques | Description |
|---------|-----------|-------------|
| `/evasion` | T1027, T1036, T1070, T1140, T1562 | Obfuscation, masquerading, indicator removal, deobfuscate/decode, impair defenses |
| `/deobfuscate` | T1140, T1027.013 | Deobfuscate/decode files or information, encrypted/encoded payloads |
| `/encode-decode` | T1132, T1027 | Data encoding for evasion and obfuscation |
| `/ssl-pinning-bypass` | T1553, T1562 | Subvert trust controls and impair certificate validation defenses |
| `/payload-gen` | T1027, T1036 | Generate obfuscated and masqueraded payloads |
| `/container-escape` | T1610, T1611 | Deploy containers and escape to evade container-level defenses |
| `/shellcode-gen` | T1027.009 | Embedded payloads -- shellcode packed to evade detection |
| `/cleanup` | T1070, T1070.004 | Indicator removal -- remove test artifacts, files, logs |

## TA0006 -- Credential Access

| Command | Techniques | Description |
|---------|-----------|-------------|
| `/hash-crack` | T1110.002 | Password cracking -- brute force via hash extraction |
| `/auth-test` | T1110, T1078, T1556 | Brute force, credential stuffing, test valid accounts |
| `/session-hijack` | T1539, T1550.001, T1557 | Steal web session cookies, use alternate auth material, adversary-in-the-middle |
| `/ad-pentest` | T1003, T1558 | OS credential dumping (LSASS, SAM, DCSync), Kerberoasting, AS-REP roasting |
| `/sniff` | T1040, T1557 | Network sniffing and MITM to capture credentials in transit |
| `/wireless` | T1557.004 | Capture wireless credentials via evil twin / rogue AP |
| `/crypto-attack` | T1552 | Attack cryptographic implementations to extract unsecured credentials |
| `/generate-wordlist` | T1110.002 | Generate wordlists for password brute force and spraying |
| `/sqli-test` | T1552 | Extract credentials stored in databases via SQL injection |

## TA0007 -- Discovery

| Command | Techniques | Description |
|---------|-----------|-------------|
| `/recon-active` | T1046, T1018, T1016 | Network service scanning, remote system discovery, network config |
| `/scan-ports` | T1046 | Network service discovery via port and service scanning |
| `/cloud-recon` | T1580, T1526, T1538 | Cloud infrastructure discovery -- services, policies, permissions |
| `/cloud-pentest` | T1580, T1526, T1069.003 | Cloud service dashboard, permission groups, resource discovery |
| `/infra-pentest` | T1046, T1018, T1082 | Remote system discovery, system information, network service scanning |
| `/subdomain-enum` | T1018 | Remote system discovery via subdomain enumeration |
| `/ad-pentest` | T1087.002, T1069.002, T1482 | Domain account/group discovery, domain trust discovery (BloodHound) |
| `/nuclei-scan` | T1046, T1518 | Software and service vulnerability discovery at scale |
| `/engagement-status` | T1083 | File and directory discovery -- review engagement data |
| `/binary-analyze` | T1518 | Software discovery via binary analysis and reversing |
| `/firmware-analyze` | T1082 | System information discovery through firmware extraction |

## TA0008 -- Lateral Movement

| Command | Techniques | Description |
|---------|-----------|-------------|
| `/lateral-movement` | T1021, T1570, T1550, T1563 | Remote services (SSH, RDP, SMB, WinRM), lateral tool transfer, alternate auth material, remote service session hijack |
| `/ad-pentest` | T1021.002, T1021.006, T1550.002 | SMB/Windows admin shares, pass-the-hash, Windows Remote Management |
| `/session-hijack` | T1563, T1550.001 | Remote service session hijacking, application access token reuse |
| `/exploit` | T1210 | Exploitation of remote services for lateral spread |
| `/persistence` | T1021 | Remote services for maintaining lateral access |

## TA0009 -- Collection

| Command | Techniques | Description |
|---------|-----------|-------------|
| `/screenshot` | T1113 | Screen capture for evidence and data collection |
| `/memory-forensics` | T1005 | Data from local system -- memory dump extraction and analysis |
| `/disk-forensics` | T1005, T1025 | Data from local system and removable media analysis |
| `/log-analysis` | T1530 | Data from cloud storage / log aggregation analysis |
| `/network-forensics` | T1040 | Network sniffing -- packet capture collection and analysis |
| `/sniff` | T1040 | Network traffic capture for data collection |
| `/frida-hook` | T1056 | Input capture -- hook keyboard, clipboard, crypto functions |
| `/memory-hack` | T1005 | Data from local system via memory reading and scraping |

## TA0010 -- Exfiltration

| Command | Techniques | Description |
|---------|-----------|-------------|
| `/c2-setup` | T1041 | Exfiltration over C2 channel |
| `/sniff` | T1048 | Identify exfiltration over alternative protocols via traffic analysis |
| `/cloud-pentest` | T1537 | Transfer data to cloud account |
| `/ssrf-scan` | T1048 | SSRF chains enabling exfiltration over alternative protocol (cloud metadata, internal APIs) |

## TA0011 -- Command and Control

| Command | Techniques | Description |
|---------|-----------|-------------|
| `/c2-setup` | T1071, T1573, T1105, T1572, T1090 | Application-layer protocol, encrypted channel, ingress tool transfer, tunneling, proxy |
| `/payload-gen` | T1071, T1573, T1132 | Payloads with C2 callbacks -- protocol, encryption, encoding |
| `/game-network` | T1071, T1001 | Application-layer protocol analysis, data obfuscation in game protocols |
| `/protocol-re` | T1071 | Reverse engineer C2 or custom application-layer protocols |
| `/encode-decode` | T1132, T1001 | Data encoding and obfuscation for C2 communication |
| `/evasion` | T1090, T1572 | Connection proxy and tunneling for covert C2 channels |

## TA0040 -- Impact

| Command | Techniques | Description |
|---------|-----------|-------------|
| `/incident-response` | T1486, T1490, T1489 | Respond to ransomware (data encrypted), inhibit system recovery, service stop |
| `/crypto-attack` | T1486 | Analyze/simulate data encryption for impact assessment |
| `/container-escape` | T1610 | Deploy rogue containers for resource hijacking |

---

## Commands Not Directly Mapped to ATT&CK

These commands are operational, reporting, or methodology-focused and do not directly simulate adversary TTPs:

| Command | Category | Purpose |
|---------|----------|---------|
| `/new-engagement` | Engagement Management | Initialize engagement directory and tracking |
| `/close-engagement` | Engagement Management | Finalize and archive engagement |
| `/write-report` | Reporting | Generate security assessment report |
| `/write-finding` | Reporting | Write vulnerability finding report |
| `/write-re-analysis` | Reporting | Write reverse engineering analysis document |
| `/write-ctf-writeup` | Reporting | Write CTF challenge writeup |
| `/vuln-report` | Reporting | Generate vulnerability advisory report |
| `/full-assessment` | Automation | Orchestrate end-to-end recon-to-report pipeline |
| `/timeline` | Reporting | Build chronological attack timeline |
| `/deconflict` | Utilities | Pre-engagement safety and deconfliction check |
| `/ctf` | CTF | General CTF challenge solving workflow |
| `/ctf-web` | CTF | Web-category CTF challenge |
| `/ctf-crypto` | CTF | Cryptography CTF challenge |
| `/ctf-forensics` | CTF | Forensics CTF challenge |
| `/mobile-pentest` | Mobile | Full mobile app pentest (spans multiple tactics) |
| `/android-analyze` | Mobile | Android APK static/dynamic analysis |
| `/ios-analyze` | Mobile | iOS IPA analysis |
| `/reverse` | Reverse Engineering | General binary/app reverse engineering |
| `/malware-analyze` | Reverse Engineering | Malware behavioral and static analysis |
| `/game-hack` | Game Hacking | General game security analysis workflow |
| `/unity-analyze` | Game Hacking | Unity IL2CPP/mono game client analysis |
| `/ai-redteam` | AI/LLM Security | AI/LLM red teaming -- prompt injection, jailbreaks |
| `/ai-guardrail-test` | AI/LLM Security | AI safety guardrail bypass testing |
| `/iot-hack` | IoT | IoT device security assessment |

---

## Cyber Kill Chain Mapping

Maps toolkit commands to the Lockheed Martin [Cyber Kill Chain](https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html) phases.

| Kill Chain Phase | Commands | Description |
|-----------------|----------|-------------|
| **Reconnaissance** | `/recon`, `/recon-active`, `/recon-passive`, `/osint`, `/osint-person`, `/osint-domain`, `/osint-org`, `/subdomain-enum`, `/cloud-recon`, `/scan-ports`, `/quick-scan`, `/sniff` | Identify and research targets -- harvest emails, enumerate subdomains, scan infrastructure |
| **Weaponization** | `/payload-gen`, `/shellcode-gen`, `/rop-chain`, `/exploit`, `/bof-exploit`, `/evasion`, `/generate-wordlist` | Create deliverable payloads, weaponize exploits, build evasion techniques |
| **Delivery** | `/phishing-campaign`, `/upload-test`, `/sqli-test`, `/xss-hunt`, `/ssrf-scan`, `/ssti-test`, `/wireless` | Deliver payloads via phishing, web upload, injection, wireless vectors |
| **Exploitation** | `/exploit`, `/bof-exploit`, `/sqli-test`, `/ssrf-scan`, `/ssti-test`, `/auth-test`, `/upload-test`, `/api-pentest`, `/container-escape`, `/ctf-pwn`, `/session-hijack`, `/iot-hack` | Trigger vulnerability -- code execution, injection, authentication bypass |
| **Installation** | `/persistence`, `/c2-setup`, `/payload-gen`, `/shellcode-gen`, `/ad-pentest` | Install backdoor, establish persistent access, create accounts |
| **Command & Control** | `/c2-setup`, `/payload-gen`, `/protocol-re`, `/game-network`, `/encode-decode`, `/evasion` | Establish and maintain remote control channel with target |
| **Actions on Objectives** | `/privesc`, `/lateral-movement`, `/ad-pentest`, `/memory-hack`, `/memory-forensics`, `/disk-forensics`, `/screenshot`, `/hash-crack`, `/crypto-attack`, `/cloud-pentest` | Achieve mission goals -- escalate, move laterally, collect data, exfiltrate |

---

## MITRE ATT&CK Navigator Layer

To visualize coverage in the [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/), the following techniques are exercised by this toolkit:

### Technique Coverage Summary

| Tactic | Techniques Covered | Key IDs |
|--------|-------------------|---------|
| Reconnaissance | 12 | T1589, T1590, T1591, T1593, T1594, T1595 |
| Resource Development | 6 | T1583, T1585, T1586, T1587, T1588 |
| Initial Access | 5 | T1078, T1133, T1189, T1190, T1566 |
| Execution | 4 | T1055, T1059, T1203, T1204 |
| Persistence | 8 | T1053, T1098, T1105, T1136, T1137, T1543, T1546, T1547 |
| Privilege Escalation | 6 | T1055, T1068, T1134, T1548, T1574, T1611 |
| Defense Evasion | 8 | T1027, T1036, T1070, T1132, T1140, T1553, T1562, T1610 |
| Credential Access | 8 | T1003, T1040, T1078, T1110, T1539, T1550, T1552, T1558 |
| Discovery | 9 | T1016, T1018, T1046, T1069, T1082, T1083, T1087, T1482, T1518 |
| Lateral Movement | 5 | T1021, T1210, T1550, T1563, T1570 |
| Collection | 5 | T1005, T1025, T1040, T1056, T1113 |
| Exfiltration | 3 | T1041, T1048, T1537 |
| Command and Control | 7 | T1001, T1071, T1090, T1105, T1132, T1572, T1573 |
| Impact | 3 | T1486, T1489, T1490 |

**Total unique techniques**: ~70+ across 14 tactics.

---

## Usage Notes

1. **Threat Emulation**: Use this mapping to build purple team exercises. Select an APT group in the ATT&CK Navigator, then identify which toolkit commands cover their TTPs.
2. **Gap Analysis**: Techniques without toolkit commands indicate areas where manual procedures or additional tooling is needed.
3. **Reporting**: Reference technique IDs (e.g., T1190) in vulnerability findings and red team reports for standardized threat-intelligence alignment.
4. **Compliance**: Maps to NIST CSF, ISO 27001, and PCI-DSS control testing when combined with defensive validation.
