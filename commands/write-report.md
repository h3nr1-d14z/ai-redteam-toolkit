Write security assessment report for: $ARGUMENTS

1. **Executive summary**: Business-level overview of engagement scope, key findings, overall risk rating
2. **Methodology**: Testing approach, tools used, timeline, standards followed (OWASP, PTES, NIST)
3. **Scope**: What was tested, what was excluded, any limitations or access issues
4. **Findings summary**: Table of all findings with severity, CVSS score, status, and one-line description
5. **Detailed findings**: Each finding with full write-up (see write-finding format)
6. **Risk matrix**: Visual severity distribution, trend comparison if repeat assessment
7. **Remediation roadmap**: Prioritized fix plan — immediate (critical), short-term (high), medium-term (medium)
8. **Positive observations**: Security controls that worked well, good practices observed

Output: `engagements/<target>/reports/security-assessment-<date>.md`
