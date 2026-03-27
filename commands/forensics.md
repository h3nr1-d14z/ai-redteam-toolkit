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
