Generate vulnerability report for: $ARGUMENTS

1. **Gather findings**: Collect all discovered vulnerabilities from `engagements/<target>/findings/`
2. **Classify**: Assign CVSS v3.1 scores, categorize by type (injection, auth, config, logic)
3. **Prioritize**: Rank by risk (CVSS score x exploitability x business impact)
4. **Write details**: For each finding — title, severity, CVSS vector, description, evidence (screenshots/request-response), reproduction steps, impact, remediation
5. **Executive summary**: High-level risk overview, critical stats, top risks, overall security posture
6. **Remediation roadmap**: Quick wins, short-term fixes, long-term improvements with effort estimates
7. **Positive findings**: Document security controls that were effective

Output: `engagements/<target>/reports/vulnerability-report-<date>.md`
