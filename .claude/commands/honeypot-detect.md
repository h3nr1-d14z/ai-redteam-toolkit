Honeypot detection analysis on: $ARGUMENTS

## Pre-flight
- Determine if target exhibits suspicious characteristics
- Review initial scan results for anomalies
- Understand common honeypot deployments in target environment

## Phase 1: Network-Level Detection
1. **Shodan honeyscore**: `shodan host <ip>` -- check honeyscore (0.0-1.0)
2. **Too many open ports**: genuine hosts rarely have 50+ services open
3. **Response timing**: honeypots often have uniform response times across all ports
4. **TTL analysis**: inconsistent TTL values suggest emulated network stack
5. **OS fingerprint mismatch**: nmap -O shows OS but services suggest different OS
6. **MAC address**: check OUI -- VM vendors (VMware, VirtualBox) in unexpected contexts

## Phase 2: Service-Level Detection
1. **SSH (Cowrie)**: unusual SSH banners, accepts any password, limited command set
   - Test: try invalid commands -- does it respond generically?
   - Check: SSH version string anomalies (old OpenSSH claiming modern OS)
2. **HTTP (Glastopf/Snare)**: generic error pages, too many vulnerabilities
   - Test: request non-standard paths -- real servers return consistent 404s
3. **SMB (Dionaea)**: accepts any credentials, emulated responses
   - Test: unusual SMB dialect negotiation responses
4. **RDP (RDPY)**: certificate anomalies, connection behavior differences
5. **Telnet**: too-easy root access, sandboxed command environment

## Phase 3: Behavioral Analysis
1. **Interaction depth**: send complex multi-step attacks -- does it follow expected behavior?
2. **Error handling**: real services have specific error messages; honeypots are generic
3. **Resource limits**: try resource-intensive operations -- honeypots may lack real resources
4. **Data consistency**: create files then verify -- honeypots may not persist properly
5. **Process list**: if you get shell, check for honeypot processes (cowrie, dionaea, kippo)

## Phase 4: Infrastructure Indicators
1. **Hosting**: common honeypot hosting on cloud IPs (DigitalOcean, AWS micro instances)
2. **Certificate analysis**: self-signed certs, default SSL configs
3. **HoneyDB/Shodan**: cross-reference IP against known honeypot databases
4. **Uptime**: very high uptime with no patches suggests honeypot
5. **Geographic mismatch**: IP geolocation vs claimed organization location

## Phase 5: Deception Platform Detection
1. **Canary tokens**: check for URL/DNS/file canary tokens in discovered data
2. **Honeytokens**: fake credentials, documents, or API keys planted as bait
3. **Network decoys**: Attivo, Illusive Networks, TrapX -- enterprise deception
4. **Breadcrumbs**: intentionally planted leads pointing to honeypots

## Tools
Shodan (honeyscore), nmap (OS detection), Wireshark (traffic analysis)
Custom scripts for timing analysis and behavioral testing

## Output
Save to engagements/<target>/recon/honeypot-analysis.md

## Framework Mapping
- MITRE ATT&CK: TA0043 (Reconnaissance) -> T1592 (Gather Victim Host Information)
- MITRE ATT&CK: TA0007 (Discovery) -> T1497 (Virtualization/Sandbox Evasion)
- Cyber Kill Chain: Phase 2 -- Reconnaissance (target validation)
- CEH v12: Module 12 -- Evading IDS, Firewalls, and Honeypots

## Safety
Document findings but do not disrupt honeypot operations on third-party networks.
