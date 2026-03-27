# Rules of Engagement

| Field | Value |
|---|---|
| **Engagement Name** | [Project Name / Code Name] |
| **Client** | [Client Organization] |
| **Service Provider** | [Testing Organization] |
| **Document Version** | 1.0 |
| **Effective Date** | [YYYY-MM-DD] |
| **Expiration Date** | [YYYY-MM-DD] |
| **Classification** | CONFIDENTIAL |

---

## 1. Purpose

This document defines the rules, boundaries, and procedures governing the security assessment engagement between [Client] and [Service Provider]. Both parties agree to abide by the terms outlined herein.

## 2. Engagement Type

- [ ] Black-Box Penetration Test
- [ ] Grey-Box Penetration Test
- [ ] White-Box Penetration Test
- [ ] Red Team Assessment
- [ ] Purple Team Exercise
- [ ] Vulnerability Assessment
- [ ] Social Engineering Assessment
- [ ] Physical Security Assessment
- [ ] Mobile Application Assessment
- [ ] API Security Assessment
- [ ] Cloud Security Assessment

## 3. Scope Definition

### 3.1 In-Scope Targets

| Target | Type | Environment | Notes |
|---|---|---|---|
| [https://app.example.com] | Web Application | Production | [Primary target] |
| [10.0.1.0/24] | Network Range | Internal | [Office network] |
| [api.example.com] | REST API | Staging | [API v2 only] |
| [Android app: com.example.app] | Mobile App | Production | [Latest version] |

### 3.2 Out-of-Scope

The following are explicitly excluded from testing:

| Target / Activity | Reason |
|---|---|
| [Third-party services (Stripe, Auth0)] | Not owned by client |
| [Production database direct access] | Risk of data corruption |
| [10.0.2.0/24 network range] | Contains critical infrastructure |
| [Denial of Service attacks] | Business continuity risk |
| [Physical access testing] | Not authorized for this engagement |
| [Social engineering of C-level executives] | Out of scope per client request |

### 3.3 Testing Windows

| Window | Schedule |
|---|---|
| Primary Testing Hours | [Monday-Friday, 09:00-18:00 UTC] |
| Extended Testing (if approved) | [Saturday, 10:00-16:00 UTC] |
| Maintenance Window (destructive tests) | [Sunday, 02:00-06:00 UTC] |
| Blackout Periods | [List any dates/times when testing is prohibited] |

## 4. Authorized Actions

### 4.1 Permitted Activities

The following activities are authorized within the defined scope:

- [x] Port scanning and service enumeration
- [x] Vulnerability scanning (authenticated and unauthenticated)
- [x] Web application testing (OWASP Top 10)
- [x] API endpoint testing
- [x] Authentication and session testing
- [x] Authorization and access control testing
- [x] Business logic testing
- [x] Input validation testing (SQL injection, XSS, command injection)
- [x] File upload testing
- [x] Exploitation of discovered vulnerabilities (proof of concept)
- [x] Password attacks against test accounts only
- [x] SSL/TLS configuration assessment
- [ ] Social engineering (phishing) -- [Authorized / Not Authorized]
- [ ] Physical security testing -- [Authorized / Not Authorized]
- [ ] Wireless network testing -- [Authorized / Not Authorized]

### 4.2 Exploitation Boundaries

| Action | Permitted | Conditions |
|---|---|---|
| Proof of concept exploitation | Yes | Non-destructive only |
| Privilege escalation | Yes | Document and report each escalation |
| Lateral movement | Yes | Within in-scope systems only |
| Data exfiltration demonstration | Limited | Use synthetic/test data; max 10 records as proof |
| Persistence mechanisms | [Yes/No] | [Reversible only; document all placements] |
| Password cracking (offline) | Yes | Test/provided accounts only |
| Brute-force attacks (online) | Limited | Max 100 attempts per account; respect lockout |
| Automated scanning | Yes | Throttle to [N] requests/second |

### 4.3 Prohibited Actions

The following are strictly prohibited regardless of scope:

1. Denial of Service (DoS/DDoS) attacks or intentional service disruption
2. Modification or deletion of production data
3. Accessing, copying, or exfiltrating real customer/user data
4. Testing against out-of-scope systems
5. Social engineering against unauthorized targets
6. Installing persistent backdoors (unless explicitly authorized for red team)
7. Sharing findings with unauthorized parties
8. Physical damage to hardware or infrastructure
9. Attacks that could impact third-party services or users
10. Any illegal activity beyond the authorized scope

## 5. Communication Plan

### 5.1 Contacts

**Client Side:**

| Role | Name | Email | Phone |
|---|---|---|---|
| Primary Contact | [Name] | [email] | [phone] |
| Technical Contact | [Name] | [email] | [phone] |
| Emergency Contact | [Name] | [email] | [phone] |
| Executive Sponsor | [Name] | [email] | [phone] |

**Testing Team:**

| Role | Name | Email | Phone |
|---|---|---|---|
| Engagement Lead | [Name] | [email] | [phone] |
| Lead Tester | [Name] | [email] | [phone] |
| Emergency Contact | [Name] | [email] | [phone] |

### 5.2 Communication Channels

| Purpose | Channel |
|---|---|
| Daily status updates | [Email / Slack / Teams] |
| Urgent findings | [Phone call + encrypted email] |
| Document sharing | [Encrypted file share / secure portal] |
| Questions and clarifications | [Slack channel / Email] |

### 5.3 Status Reporting

| Report | Frequency | Recipient |
|---|---|---|
| Daily status summary | Daily (end of testing day) | Primary Contact |
| Critical finding notification | Immediate (within 1 hour) | Technical + Emergency Contact |
| Weekly progress report | Weekly | All stakeholders |
| Final report | Within [N] business days of testing completion | All stakeholders |

## 6. Escalation Procedures

### 6.1 Critical Finding Escalation

When a critical vulnerability is discovered (CVSS 9.0+), the following procedure applies:

1. Tester immediately stops exploitation of the specific finding
2. Tester notifies Engagement Lead within 15 minutes
3. Engagement Lead contacts Client Technical Contact within 1 hour
4. Client confirms receipt and response plan within 4 hours
5. Written summary provided via encrypted email within 24 hours

### 6.2 Incident Escalation

If testing causes an unintended impact (service disruption, data exposure):

1. Tester immediately stops all testing activities
2. Tester notifies Engagement Lead immediately
3. Engagement Lead calls Client Emergency Contact
4. Joint assessment of impact and remediation
5. Testing resumes only after written approval from Client
6. Incident documented in final report

### 6.3 Emergency Stop

Either party can invoke an emergency stop at any time:

- **Stop Phrase:** "[Agreed upon stop phrase]"
- **Method:** Phone call to Emergency Contact
- **Effect:** All testing activities cease immediately
- **Resumption:** Requires written authorization from both parties

## 7. Legal and Compliance

### 7.1 Authorization

This document, combined with the signed authorization letter and master services agreement, constitutes legal authorization for the described testing activities. The tester(s) shall carry a copy of the authorization letter during the engagement.

### 7.2 Data Handling

| Item | Requirement |
|---|---|
| Findings and evidence | Encrypted at rest (AES-256) and in transit (TLS 1.2+) |
| Client credentials | Stored in encrypted password manager; destroyed after engagement |
| Test data | No real customer data stored; synthetic data used for evidence |
| Report storage | Encrypted; retained for [N] months per agreement |
| Data destruction | All client data destroyed within [N] days of engagement close |

### 7.3 Confidentiality

All findings, data, and communications are confidential. Neither party will disclose engagement details to third parties without written consent. The testing team will not publish, present, or reference specific findings without explicit written permission.

### 7.4 Liability

[Reference the master services agreement or state liability terms. Typically includes a hold-harmless clause for testing activities within the defined scope.]

## 8. Testing Infrastructure

### 8.1 Tester Source Information

| Item | Value |
|---|---|
| Testing Source IPs | [IP addresses / ranges] |
| VPN Connection | [VPN details if provided by client] |
| User Agents | [Custom user agent string for identification] |
| Testing Machines | [OS / hardware description] |

### 8.2 Accounts Provided

| Username | Role | Purpose | Expiration |
|---|---|---|---|
| [testuser1] | Standard User | Authenticated testing | [Date] |
| [testadmin] | Administrator | Admin panel testing | [Date] |

## 9. Deliverables

| Deliverable | Due Date | Format |
|---|---|---|
| Daily status emails | Each testing day | Email |
| Critical finding alerts | As discovered | Phone + Email |
| Draft report | [N] business days after testing | PDF (encrypted) |
| Final report | [N] business days after review | PDF (encrypted) |
| Remediation verification | [N] business days after fixes | PDF (encrypted) |
| Debrief presentation | [Scheduled date] | Presentation + Meeting |

## 10. Signatures

By signing below, both parties agree to the rules of engagement defined in this document.

**Client:**

Name: _________________________ Title: _________________________

Signature: _________________________ Date: _________________________

**Service Provider:**

Name: _________________________ Title: _________________________

Signature: _________________________ Date: _________________________

---

**Document Control**

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | [YYYY-MM-DD] | [Author] | Initial document |
