# CRITICAL Finding: [Title]

| Field | Value |
|---|---|
| **ID** | VULN-[NNN] |
| **Title** | [Descriptive title] |
| **Severity** | CRITICAL |
| **CVSS v3.1 Score** | [9.0 - 10.0] |
| **CVSS v3.1 Vector** | [AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H] |
| **Category** | [e.g., Injection / RCE / Authentication Bypass] |
| **CWE** | [CWE-ID: CWE Name] |
| **OWASP Top 10** | [e.g., A03:2021 - Injection] |
| **Affected Component** | [URL / IP / Endpoint / Function] |
| **Affected Parameter** | [Parameter name] |
| **Authentication Required** | [None / Low / High] |
| **Status** | Open |
| **Date Discovered** | [YYYY-MM-DD] |
| **Discovered By** | [Tester name] |
| **Remediation Deadline** | [IMMEDIATE -- 0-7 days recommended] |

---

## PRIORITY NOTICE

This finding represents a critical security risk requiring immediate attention. Exploitation of this vulnerability could result in [complete system compromise / mass data breach / remote code execution / full authentication bypass]. Remediation or mitigation should be applied within **7 days** of this report.

---

## Description

[Provide a clear, detailed description of the vulnerability. For critical findings, emphasize:
- Why this is critical (ease of exploitation + severity of impact)
- Whether active exploitation is likely or has been observed
- The blast radius (what systems/data are affected)]

### Root Cause

[Explain the underlying technical root cause. This helps developers understand what needs to change at an architectural level, not just a patch level.]

## Reproduction Steps

**Prerequisites:**
- [Required access level -- for critical findings, this is often "none" (unauthenticated)]
- [Required tools]

**Steps:**

1. [Step 1 -- exact URL, parameter, payload]
2. [Step 2]
3. [Step 3]
4. [Observe: describe what confirms the vulnerability]

**Proof of Concept Request:**

```http
[Exact HTTP request demonstrating the vulnerability]
```

**Response:**

```http
[HTTP response showing evidence of exploitation]
```

**PoC Script:**

```python
#!/usr/bin/env python3
"""
PoC for VULN-[NNN]: [Title]
WARNING: Only use against authorized targets.
"""
import requests
import sys

def exploit(target_url):
    """Demonstrate the vulnerability."""
    print(f"[*] Testing {target_url}")

    response = requests.post(
        f"{target_url}/vulnerable/endpoint",
        json={"payload": "value"},
        timeout=10,
        verify=True
    )

    if "evidence_marker" in response.text:
        print("[+] VULNERABLE: Evidence of exploitation found")
        print(f"    Response: {response.text[:200]}")
        return True

    print("[-] Not vulnerable or patched")
    return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <target_url>")
        sys.exit(1)
    exploit(sys.argv[1])
```

## Impact

### Technical Impact

[For critical findings, describe the worst-case technical scenario:]
- [Remote Code Execution: full server compromise, ability to execute arbitrary commands]
- [Data Breach: access to all database records, credentials, PII]
- [Authentication Bypass: access to any user account including administrators]
- [Privilege Escalation: unauthenticated to full administrative access]

### Business Impact

- **Data Exposure:** [Estimated records at risk, type of data]
- **Regulatory:** [GDPR, HIPAA, PCI-DSS implications]
- **Financial:** [Estimated cost of breach, fines, remediation]
- **Reputation:** [Customer trust, media exposure risk]
- **Operational:** [Service disruption, recovery time]

### Attack Scenario

[Describe a realistic attack scenario in narrative form. How would a real attacker discover and exploit this? What would they do after exploitation?]

### Affected Scope

| Item | Detail |
|---|---|
| Systems Affected | [Server names, IPs, or ranges] |
| Data at Risk | [Type and volume] |
| Users Affected | [Number and type] |
| Lateral Movement Risk | [Can this lead to further compromise?] |

## Remediation

### Immediate Mitigation (apply now)

[Actions that can be taken immediately to reduce risk, even before a full fix is deployed:]

1. [e.g., WAF rule to block the attack pattern]
2. [e.g., Disable the affected feature/endpoint]
3. [e.g., Network-level access restriction]
4. [e.g., Rotate affected credentials]

### Permanent Fix

[Detailed remediation steps:]

1. [Primary fix with code example]
   ```python
   # BEFORE (vulnerable)
   query = f"SELECT * FROM users WHERE id = '{user_input}'"

   # AFTER (fixed)
   query = "SELECT * FROM users WHERE id = %s"
   cursor.execute(query, (user_input,))
   ```

2. [Additional fix]
3. [Validation/testing step]

### Defense-in-Depth

1. [Additional security layer 1]
2. [Additional security layer 2]
3. [Monitoring and alerting recommendation]

### Verification

1. [Steps to verify the fix is effective]
2. [Regression test to ensure functionality]
3. [Request retest from security team]

## Evidence

### Screenshot Evidence

Screenshot 1: [Description of what it shows]
Screenshot 2: [Description of what it shows]

### Captured Data (sanitized)

```
[Sanitized evidence of exploitation -- redact real sensitive data]
```

### Tool Output

```
[Relevant tool output confirming the finding]
```

## References

- [OWASP reference]
- [CWE reference]
- [CVE if applicable]
- [Vendor advisory or patch URL]
- [Related public disclosures or research]

## Remediation Tracking

| Date | Action | By | Status |
|---|---|---|---|
| [YYYY-MM-DD] | Finding reported | [Tester] | Reported |
| [YYYY-MM-DD] | Mitigation applied | [Dev/Ops] | Mitigated |
| [YYYY-MM-DD] | Permanent fix deployed | [Dev] | Fixed |
| [YYYY-MM-DD] | Fix verified by retest | [Tester] | Closed |
