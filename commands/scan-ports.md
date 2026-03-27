Perform port scanning on: $ARGUMENTS

1. **Quick scan**: Top 1000 ports TCP SYN scan for rapid service identification
2. **Full scan**: All 65535 TCP ports to find services on non-standard ports
3. **UDP scan**: Top 100 UDP ports (DNS, SNMP, NTP, TFTP, DHCP, IPMI)
4. **Service detection**: Version detection (-sV) on all open ports, OS fingerprinting
5. **Script scan**: NSE scripts for discovered services (vuln, default, auth categories)
6. **Categorize**: Group services by type — web, database, remote access, file sharing, messaging
7. **Identify risks**: Flag high-risk services — unencrypted protocols, default ports, management interfaces

Command: nmap -sC -sV -p- -oA engagements/<target>/recon/nmap-full <target>
Save to `engagements/<target>/recon/port-scan.md`
