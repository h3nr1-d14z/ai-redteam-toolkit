# Sample Report: Executive Summary Excerpt

---

| Field | Value |
|---|---|
| **Client** | Acme Financial Services Ltd. |
| **Project** | Web Application Penetration Test -- Customer Portal |
| **Date Range** | March 10-21, 2026 |
| **Classification** | CONFIDENTIAL |

---

## Executive Summary

### Engagement Overview

Acme Financial Services Ltd. engaged our security team to perform a grey-box penetration test against the customer-facing web portal (`portal.acmefinancial.example.com`) and its supporting REST API (`api.acmefinancial.example.com/v3`). The assessment was conducted between March 10 and March 21, 2026, using a combination of automated scanning and manual testing techniques following the OWASP Testing Guide v4.2 methodology.

Two test accounts were provided: a standard customer account and a customer service representative account. The assessment was performed against the staging environment, which mirrors the production configuration.

### Risk Summary

| Severity | Count |
|---|---|
| Critical | 2 |
| High | 4 |
| Medium | 6 |
| Low | 3 |
| Informational | 5 |

**Overall Risk Rating: HIGH**

The assessment identified two critical vulnerabilities that, if exploited, would allow an attacker to access financial records and personally identifiable information (PII) belonging to any customer. Combined with the high-severity findings, an attacker with a standard customer account could escalate privileges, access other customers' data, and potentially modify account settings on their behalf.

### Most Critical Findings

1. **Insecure Direct Object Reference (IDOR) in Account API** (Critical, CVSS 9.1)
   Changing the `account_id` parameter in the `/api/v3/accounts/{id}/transactions` endpoint allows any authenticated user to view the complete transaction history of any other customer. No server-side authorization check validates that the requesting user owns the specified account. During testing, we confirmed access to transaction records, account balances, and linked bank account details for 5 test accounts without authorization.

2. **SQL Injection in Transaction Search** (Critical, CVSS 9.8)
   The `search` parameter on the `/api/v3/transactions/search` endpoint is vulnerable to time-based blind SQL injection. Using automated extraction, we confirmed the ability to read arbitrary data from the backend PostgreSQL database, including the `users` table containing hashed passwords, email addresses, phone numbers, and home addresses for all customers. The database user has read access to all application schemas.

3. **Broken Authentication: Password Reset Token Predictability** (High, CVSS 8.1)
   Password reset tokens are generated using a timestamp-seeded pseudo-random number generator. An attacker who knows the approximate time a reset was requested (within a 10-second window) can brute-force the valid token within approximately 50,000 attempts, which completes in under 2 minutes against the current rate limit of 500 requests per second on the reset verification endpoint.

4. **Privilege Escalation via Mass Assignment** (High, CVSS 8.0)
   The profile update endpoint (`PUT /api/v3/users/me`) accepts and processes a `role` parameter that is not exposed in the frontend application. By adding `"role": "csr"` to the profile update JSON body, a standard customer account was elevated to customer service representative, granting access to the internal support dashboard, customer lookup functionality, and the ability to modify other customers' account settings.

### Attack Scenario

An external attacker could register a free customer account, exploit the mass assignment vulnerability to elevate their role to customer service representative, and then use the IDOR vulnerability to systematically download transaction histories and PII for all customers. The SQL injection vulnerability provides an alternative path to the same data, and could additionally be used to extract password hashes for offline cracking, potentially compromising customer accounts on other platforms where passwords have been reused.

The estimated exposure includes PII and financial records for approximately 125,000 active customer accounts.

### Positive Observations

Despite the critical findings, several security controls were implemented effectively:

- **Transport Layer Security:** All communications are encrypted with TLS 1.3, with HSTS enabled and a strong cipher suite configuration
- **Rate Limiting on Login:** The login endpoint enforces a progressive lockout after 5 failed attempts, with CAPTCHA after 3 attempts, effectively mitigating online brute-force attacks
- **Content Security Policy:** A strict CSP is in place that successfully prevented exploitation of a reflected XSS finding (downgraded from high to medium due to CSP mitigation)
- **Session Management:** Session tokens are cryptographically random, expire after 30 minutes of inactivity, and are invalidated on logout
- **Logging and Monitoring:** Detailed access logs are maintained, and our testing activity triggered three security alerts in the SOC within the first 48 hours of testing

### Strategic Recommendations

**Immediate (0-7 days):**
1. Deploy server-side authorization checks on all API endpoints that access account-specific data. Every request must validate that the authenticated user has permission to access the requested resource.
2. Implement parameterized queries for the transaction search functionality to eliminate the SQL injection vulnerability. Conduct a code review to identify and remediate any additional injection points.

**Short-Term (7-30 days):**
3. Replace the password reset token generation with `crypto.randomBytes(32)` (Node.js) or equivalent cryptographically secure random generation.
4. Implement an allowlist of accepted fields for all API endpoints that process user input. Reject or ignore any fields not explicitly expected (defense against mass assignment).
5. Deploy rate limiting on the password reset verification endpoint (maximum 10 attempts per token per minute).

**Medium-Term (30-90 days):**
6. Implement a centralized authorization middleware that enforces access control policies consistently across all API endpoints.
7. Conduct a comprehensive security code review of the entire API layer, focusing on authorization, input validation, and data exposure.
8. Implement automated security testing (DAST and SAST) in the CI/CD pipeline to catch vulnerabilities before deployment.

**Long-Term:**
9. Adopt an API security gateway that provides additional layers of input validation, rate limiting, and anomaly detection.
10. Establish a quarterly penetration testing cadence with rotating testing firms to maintain independent security validation.
11. Implement a bug bounty program to provide continuous security testing by the broader security research community.

### Next Steps

1. Review the detailed findings section of this report for complete reproduction steps and remediation guidance for each vulnerability.
2. Prioritize remediation based on the severity ratings and business context provided above.
3. Schedule a remediation verification retest for the week of April 14, 2026, to validate that critical and high findings have been successfully addressed.
4. A debrief meeting has been scheduled for March 28, 2026, to walk through the findings with the development and security teams.

---

*This executive summary is an excerpt from the complete penetration test report. For detailed reproduction steps, HTTP request/response evidence, and comprehensive remediation guidance, refer to the full report document.*
