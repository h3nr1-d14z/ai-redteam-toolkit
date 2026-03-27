Run incident response workflow for: $ARGUMENTS

## Phase 1: Preparation
1. Assemble IR team and define roles
2. Establish communication channels (out-of-band)
3. Prepare forensic tools and clean media
4. Document timeline start

## Phase 2: Detection & Analysis
1. Identify indicators of compromise (IoCs)
2. Collect initial evidence: logs, alerts, user reports
3. Determine scope: which systems affected?
4. Classify severity: Critical / High / Medium / Low
5. Run /log-analysis for log correlation

## Phase 3: Containment
1. **Short-term**: isolate affected systems (network segment, disable accounts)
2. **Long-term**: apply temporary patches, increase monitoring
3. Preserve evidence before containment changes state
4. Document all containment actions with timestamps

## Phase 4: Eradication
1. Identify root cause and attack vector
2. Remove malware, backdoors, persistence mechanisms
3. Patch exploited vulnerabilities
4. Reset compromised credentials
5. Verify eradication is complete

## Phase 5: Recovery
1. Restore from clean backups
2. Rebuild compromised systems
3. Monitor closely for re-infection
4. Gradually restore normal operations
5. Validate system integrity

## Phase 6: Lessons Learned
1. Conduct post-incident review within 72 hours
2. Document: timeline, root cause, response effectiveness, gaps
3. Update detection rules and playbooks
4. Run /timeline to build attack chronology
5. Write incident report

## Tools
Volatility (memory), Velociraptor (endpoint), TheHive (case management), MISP (threat intel)

## Output
Save to engagements/<target>/reports/incident-response-<date>.md
Reference: CND — Incident Response module
