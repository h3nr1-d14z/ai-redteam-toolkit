Analyze logs for security incidents: $ARGUMENTS

1. **Ingest**: Identify log sources — web server, auth, system, application, firewall, proxy, DNS
2. **Normalize**: Parse log formats, extract timestamp, source IP, action, target, status into structured format
3. **Baseline**: Establish normal patterns — peak hours, common user agents, typical request rates
4. **Anomaly detection**: Identify outliers — unusual times, abnormal request volumes, new user agents, rare endpoints
5. **Attack indicators**:
   - Web: SQLi/XSS patterns, path traversal, scanner signatures, brute force (401/403 floods)
   - Auth: Failed logins, password spraying (same password, many users), impossible travel
   - System: Privilege escalation, new services, cron modifications, unusual processes
6. **Correlation**: Cross-reference events across log sources, build attack timeline
7. **IOC extraction**: Extract attacker IPs, user agents, tools, accessed resources, compromised accounts

Tools: grep/awk/jq, ELK stack, Splunk, custom Python scripts
Save to `engagements/<target>/findings/log-analysis.md`
