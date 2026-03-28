Test IDS/Firewall/WAF evasion techniques on: $ARGUMENTS

## Pre-flight
- Identify security controls in place: WAF, IDS/IPS, firewall rules
- Determine if evasion testing is in scope

## IDS/IPS Evasion
1. **Fragmentation**: nmap -f, --mtu 8/16/24 to split packets
2. **Decoy scans**: nmap -D RND:5,ME to blend with decoys
3. **Timing**: nmap -T0/-T1 for slow scan below threshold
4. **Protocol manipulation**: use unusual protocols (IPv6, ICMP tunneling)
5. **Encryption**: tunnel traffic through SSH/VPN/SSL
6. **Payload encoding**: msfvenom encoders (shikata_ga_nai, xor)

## WAF Bypass
1. **Encoding**: URL encode, double encode, Unicode, hex
2. **Case variation**: SeLeCt, UnIoN, ScRiPt
3. **Comments**: /**/UNION/**/SELECT, /*!50000UNION*/
4. **HTTP parameter pollution**: id=1&id=2 (WAF checks first, app uses second)
5. **Content-Type switching**: application/json vs form-urlencoded
6. **HTTP method override**: X-HTTP-Method-Override, _method param
7. **Chunked transfer**: split payload across chunks

## Firewall Evasion
1. **Port hopping**: use common allowed ports (80, 443, 53)
2. **Protocol tunneling**: DNS tunneling (dnscat2, iodine), ICMP tunneling
3. **Source port manipulation**: nmap --source-port 53
4. **IP spoofing**: nmap -S <spoofed-ip>

## Tools
nmap (evasion flags), wafw00f (WAF detection), sqlmap tamper scripts, Burp Suite match/replace

## Output
Save to engagements/<target>/findings/evasion-*.md
Reference: CEH Module 12 — Evading IDS, Firewalls, and Honeypots

## Framework Mapping
- MITRE ATT&CK: TA0005 (Defense Evasion) -> T1562 (Impair Defenses)
- MITRE ATT&CK: T1027 (Obfuscated Files or Information), T1036 (Masquerading)
- MITRE ATT&CK: T1090 (Proxy), T1572 (Protocol Tunneling)
- Cyber Kill Chain: Phase 5 -- Installation / Phase 6 -- Command & Control
- CEH v12: Module 12 -- Evading IDS, Firewalls, and Honeypots
