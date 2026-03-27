# Scope and Rules of Engagement

## Engagement: [TARGET_NAME]

**Version**: 1.0
**Last Updated**: [YYYY-MM-DD]
**Status**: [Draft / Approved / Active / Closed]

## 1. Authorization

This security assessment is performed under explicit authorization from the target owner/administrator.

| Field | Details |
|-------|---------|
| **Authorizing Party** | [Name, Title, Organization] |
| **Authorization Method** | [Written agreement / Email / Contract reference] |
| **Authorization Reference** | [Document ID or reference number] |
| **Valid From** | [YYYY-MM-DD] |
| **Valid Until** | [YYYY-MM-DD] |

**IMPORTANT**: Do not commit the actual authorization document to this repository. Store it securely outside of version control and reference it here.

## 2. Scope Definition

### 2.1 In-Scope Targets

| Target | Type | Description |
|--------|------|-------------|
| [hostname/IP/app] | [web/api/mobile/network/cloud] | [Brief description] |

### 2.2 In-Scope Testing Types

- [ ] External network penetration testing
- [ ] Internal network penetration testing
- [ ] Web application penetration testing
- [ ] API security testing
- [ ] Mobile application testing (Android)
- [ ] Mobile application testing (iOS)
- [ ] Cloud configuration review
- [ ] Social engineering (with restrictions below)
- [ ] Physical security (with restrictions below)
- [ ] Wireless network testing
- [ ] Source code review
- [ ] Reverse engineering
- [ ] Red team exercise

### 2.3 Out-of-Scope Targets

| Target | Reason |
|--------|--------|
| [hostname/IP/app] | [Why it is excluded] |

### 2.4 Out-of-Scope Activities

- Denial of Service (DoS/DDoS) attacks
- Destruction or modification of production data
- Attacks against third-party services or infrastructure
- Physical damage to hardware
- Social engineering of individuals not explicitly listed
- [Add any additional restrictions]

## 3. Rules of Engagement

### 3.1 Testing Windows

| Window | Times | Notes |
|--------|-------|-------|
| **Preferred** | [e.g., Mon-Fri 09:00-17:00 UTC] | [Standard testing] |
| **Allowed** | [e.g., Mon-Sun 00:00-23:59 UTC] | [With notice] |
| **Blackout** | [e.g., First Monday of month] | [Maintenance window] |

### 3.2 Communication

| Role | Name | Contact | When to Contact |
|------|------|---------|-----------------|
| **Primary Contact** | [Name] | [Email/Phone] | [General updates] |
| **Emergency Contact** | [Name] | [Email/Phone] | [System impact/outage] |
| **Technical Contact** | [Name] | [Email/Phone] | [Technical questions] |

### 3.3 Escalation Procedures

1. **Low Impact Issue Found**: Document and continue testing
2. **Medium Impact Issue Found**: Document, notify primary contact within 24 hours
3. **Critical/High Impact Issue Found**: Stop exploitation, notify primary contact immediately
4. **System Instability Detected**: Stop all testing immediately, notify emergency contact
5. **Data Breach Discovered**: Stop all testing, notify emergency contact and primary contact immediately

### 3.4 Data Handling

- All engagement data must be stored in the engagement directory only
- Credentials and sensitive data discovered must be handled securely
- Do not exfiltrate real user data beyond what is needed for proof
- Minimize collection of personally identifiable information (PII)
- All data must be securely deleted at the end of the engagement per the retention policy below

### 3.5 Credentials

| Type | Details |
|------|---------|
| **Provided accounts** | [List test accounts provided, if any] |
| **Credential testing** | [Allowed / Not allowed / Limited to provided accounts] |
| **Password attacks** | [Allowed / Not allowed / Rate-limited to X attempts] |

## 4. Deliverables

| Deliverable | Format | Due Date |
|-------------|--------|----------|
| **Daily status update** | [Email / Slack / None] | [During testing] |
| **Preliminary findings** | [Report format] | [Within X days of critical find] |
| **Draft report** | [PDF / Markdown] | [X days after testing ends] |
| **Final report** | [PDF / Markdown] | [X days after review] |
| **Retest results** | [PDF / Markdown] | [After remediation] |

## 5. Retention and Cleanup

| Item | Retention Period | Destruction Method |
|------|-----------------|-------------------|
| **Engagement data** | [X days after final report] | [Secure deletion] |
| **Exploit code** | [Keep / Delete after X days] | [Secure deletion] |
| **Reports** | [X months/years] | [Per agreement] |
| **Test accounts** | [Disable after testing] | [Client responsibility] |
| **VPN/Access** | [Revoke after testing] | [Client responsibility] |

## 6. Legal and Compliance

- Testing is governed by [applicable law/jurisdiction]
- Tester agrees to maintain confidentiality of all findings
- Findings will only be shared with authorized parties listed above
- Tester will comply with [relevant compliance frameworks if applicable]

## 7. Sign-Off

| Party | Name | Date | Signature/Acknowledgment |
|-------|------|------|--------------------------|
| **Tester** | [Name] | [Date] | [Reference] |
| **Client** | [Name] | [Date] | [Reference] |

---

**Note**: This document is a template. Customize all bracketed fields for each engagement. Do not commit signed documents to version control.
