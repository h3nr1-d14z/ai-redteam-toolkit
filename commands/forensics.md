Digital forensics analysis on: $ARGUMENTS

Identify evidence type: disk image, memory dump, PCAP, logs.
Preserve chain of custody.
For memory: /memory-forensics with Volatility3.
For disk: /disk-forensics with Autopsy/Sleuthkit.
For network: /network-forensics with Wireshark/tshark.
For logs: /log-analysis with timeline correlation.
Build timeline: correlate events across all sources.
Extract IoCs: IPs, domains, hashes, file paths.
Reference: methodology/forensics.md.
Output: engagements/<target>/reports/forensics-<date>.md

## Safety
Verify authorization and scope before proceeding. Document all actions.

## Framework Mapping
- MITRE ATT&CK: Used for mapping adversary TTPs discovered during forensic analysis
- MITRE ATT&CK: TA0007 (Discovery) -> T1083 (File and Directory Discovery) -- forensic recovery
- MITRE ATT&CK: TA0005 (Defense Evasion) -> T1070 (Indicator Removal) -- detecting anti-forensics
- Cyber Kill Chain: Post-incident analysis across all phases
- CEH v12: Module 20 -- Computer Forensics
