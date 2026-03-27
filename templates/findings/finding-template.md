# Finding: [Title]

| Field | Value |
|---|---|
| **ID** | VULN-[NNN] |
| **Title** | [Descriptive title] |
| **Severity** | [Critical / High / Medium / Low / Informational] |
| **CVSS v3.1 Score** | [0.0 - 10.0] |
| **CVSS v3.1 Vector** | [AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H] |
| **Category** | [e.g., Injection / Broken Access Control / Cryptographic Failure] |
| **CWE** | [CWE-ID: CWE Name] |
| **OWASP Top 10** | [e.g., A03:2021 - Injection] |
| **Affected Component** | [URL / IP / Endpoint / Function] |
| **Affected Parameter** | [Parameter name if applicable] |
| **Authentication Required** | [None / Low / High] |
| **Status** | [Open / Remediated / Accepted Risk / False Positive] |
| **Date Discovered** | [YYYY-MM-DD] |
| **Discovered By** | [Tester name] |

---

## Description

[Provide a clear, detailed description of the vulnerability. Explain what it is, why it exists, and what makes it exploitable. Write so that both technical and non-technical readers can understand the core issue.]

[If applicable, explain the root cause -- e.g., insufficient input validation, missing access control check, insecure configuration.]

## Reproduction Steps

**Prerequisites:**
- [Required access level or account]
- [Required tools: Burp Suite, curl, browser]
- [Required configuration or setup]

**Steps:**

1. [First step -- be specific with URLs, parameters, values]
2. [Second step]
3. [Third step]
4. [Observe the result: describe what confirms the vulnerability]

**Proof of Concept Request:**

```http
POST /api/vulnerable/endpoint HTTP/1.1
Host: target.example.com
Content-Type: application/json
Cookie: session=valid_session_token

{
  "input": "malicious_payload_here"
}
```

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data": "evidence_of_vulnerability"
}
```

**Automation Script (if applicable):**

```python
import requests

target = "https://target.example.com"
session = requests.Session()

# Reproduce the vulnerability
response = session.post(
    f"{target}/api/vulnerable/endpoint",
    json={"input": "malicious_payload_here"},
    cookies={"session": "valid_session_token"}
)

print(f"Status: {response.status_code}")
print(f"Evidence: {response.json()}")
```

## Impact

### Technical Impact

[Describe the direct technical consequences: unauthorized data access, code execution, privilege escalation, etc.]

### Business Impact

[Describe the business consequences: regulatory fines, data breach costs, reputation damage, service disruption, etc.]

### Affected Data / Systems

- [Type of data at risk: PII, financial records, credentials]
- [Systems that could be compromised]
- [Number of affected users/records if quantifiable]

### Exploitability Assessment

| Factor | Rating |
|---|---|
| Attack Complexity | [Low / Medium / High] |
| Privileges Required | [None / Low / High] |
| User Interaction | [None / Required] |
| Exploit Maturity | [Proof of Concept / Functional / Weaponized] |
| Reliability | [Always / Intermittent / Race Condition] |

## Remediation

### Primary Fix

[Describe the recommended fix in detail. Provide code examples where helpful.]

```python
# Example: Parameterized query instead of string concatenation
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### Additional Hardening

1. [Defense-in-depth measure 1]
2. [Defense-in-depth measure 2]
3. [Monitoring recommendation]

### Verification Steps

1. [How to verify the fix was applied correctly]
2. [Test case to confirm the vulnerability no longer exists]
3. [Regression test to ensure functionality is preserved]

### Temporary Mitigation

[If immediate patching is not possible, describe temporary measures: WAF rule, network segmentation, feature disable.]

## Evidence

### Screenshots

[Attach or reference screenshots demonstrating the vulnerability.]

Screenshot 1: [Description]
Screenshot 2: [Description]

### Log Entries

```
[Relevant log entries showing the vulnerability or exploitation]
```

### Additional Artifacts

[Tool output, scan results, or other supporting evidence.]

## References

- [OWASP: relevant page URL]
- [CWE: https://cwe.mitre.org/data/definitions/CWE-ID.html]
- [CVE if applicable]
- [Vendor advisory if applicable]
- [Related research or blog post]

## Notes

[Internal notes, discussion points, or context that may help during remediation verification.]

---

**Revision History**

| Date | Author | Change |
|---|---|---|
| [YYYY-MM-DD] | [Name] | Initial finding |
| [YYYY-MM-DD] | [Name] | Remediation verified |
