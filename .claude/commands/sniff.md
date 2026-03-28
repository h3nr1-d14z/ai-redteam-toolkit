Perform network sniffing and MITM on: $ARGUMENTS

## Pre-flight
- Verify network sniffing is in scope (capture only authorized traffic)
- Identify network type: switched, wireless, VPN
- Set up capture interface in promiscuous mode

## Phase 1: Passive Sniffing
1. Start capture: tcpdump -i eth0 -w capture.pcap
2. Or Wireshark with appropriate interface
3. Filter for target traffic: host, port, protocol
4. Look for: cleartext credentials, API keys, sensitive data
5. Analyze protocols: HTTP, FTP, SMTP, DNS, LDAP (often cleartext)

## Phase 2: Active MITM (ARP Spoofing)
1. Enable IP forwarding: echo 1 > /proc/sys/net/ipv4/ip_forward
2. ARP spoof: arpspoof -i eth0 -t <victim> <gateway>
3. Or bettercap: set arp.spoof.targets <victim>; arp.spoof on
4. Capture traffic: all victim traffic flows through attacker
5. SSL strip: attempt to downgrade HTTPS (sslstrip, bettercap hstshijack)

## Phase 3: DNS Spoofing
1. Set up fake DNS: dnsspoof or bettercap dns.spoof
2. Redirect target domains to attacker-controlled servers
3. Serve credential harvesting pages
4. Capture submitted credentials

## Phase 4: Credential Extraction
1. Parse PCAP: PCredz, net-creds for auto-extraction
2. HTTP basic auth, form POST data
3. FTP/Telnet credentials (cleartext)
4. NTLM hashes from SMB/HTTP NTLM auth
5. Kerberos tickets from network capture

## Tools
Wireshark, tcpdump, bettercap, ettercap, arpspoof, Responder (LLMNR/NBT-NS)

## Output
Save to engagements/<target>/findings/sniff-*.md
Reference: CEH Module 8 — Sniffing

## Safety
Only capture traffic you are authorized to intercept. Minimize exposure to third-party data.

## Framework Mapping
- MITRE ATT&CK: TA0006 (Credential Access) -> T1557 (Adversary-in-the-Middle)
- MITRE ATT&CK: T1557.002 (ARP Cache Poisoning), T1040 (Network Sniffing)
- MITRE ATT&CK: TA0009 (Collection) -> T1185 (Browser Session Hijacking)
- Cyber Kill Chain: Phase 7 -- Actions on Objectives
- CEH v12: Module 08 -- Sniffing
