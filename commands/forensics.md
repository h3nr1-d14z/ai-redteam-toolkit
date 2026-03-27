Perform digital forensics analysis on: $ARGUMENTS

1. **Preserve evidence**: Verify integrity (hashes), document chain of custody, work on copies only
2. **Triage**: Identify evidence type (memory, disk, network, logs), prioritize by volatility
3. **Timeline**: Build event timeline from filesystem timestamps, logs, browser history, registry
4. **Artifact collection**: Extract relevant artifacts — user activity, installed programs, network connections, startup items
5. **Malware indicators**: Scan for IOCs — suspicious processes, network connections, persistence mechanisms, file anomalies
6. **Data recovery**: Recover deleted files, check unallocated space, alternate data streams, slack space
7. **Report**: Document findings with evidence chain, timeline, IOCs, and conclusions

Tools: Autopsy, Volatility, Sleuth Kit, KAPE, Timeline Explorer
Save to `engagements/<target>/findings/forensics-analysis.md`
