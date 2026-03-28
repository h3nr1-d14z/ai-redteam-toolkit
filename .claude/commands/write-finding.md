Write vulnerability finding report for: $ARGUMENTS

1. **Title**: Clear, descriptive vulnerability title
2. **Severity**: CVSS v3.1 score with vector string, qualitative rating (Critical/High/Medium/Low/Info)
3. **Description**: What the vulnerability is, where it exists, why it is dangerous
4. **Evidence**: HTTP request/response pairs, screenshots, code snippets proving the vulnerability
5. **Reproduction steps**: Numbered step-by-step instructions anyone can follow to reproduce
6. **Impact**: Business impact — data exposure, account takeover, RCE, financial loss
7. **Remediation**: Specific fix recommendation with code examples where applicable, references (CWE, OWASP)

Output: `engagements/<target>/findings/<vuln-type>-<component>.md` in standard finding template format.
