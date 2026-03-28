Analyze network capture: $ARGUMENTS

1. **Overview**: Protocol distribution, conversation statistics, endpoints, DNS queries, time range
2. **Stream analysis**: Follow TCP/UDP streams, identify application-layer protocols, extract transferred data
3. **File extraction**: Carve files from streams (HTTP objects, FTP transfers, SMB files, email attachments)
4. **Credential capture**: Extract cleartext passwords (HTTP Basic, FTP, Telnet, SMTP), NTLM hashes, Kerberos tickets
5. **Anomaly detection**: Unusual ports, DNS tunneling, beaconing patterns (regular intervals), large data transfers
6. **C2 identification**: Identify command and control traffic — HTTP beacons, DNS queries, encoded/encrypted channels
7. **Timeline**: Build network activity timeline, correlate with host-based events

Tools: Wireshark, tshark, NetworkMiner, zeek, tcpflow
Save to `engagements/<target>/findings/network-forensics.md`
