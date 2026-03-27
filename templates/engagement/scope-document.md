# Scope Definition Document

| Field | Value |
|---|---|
| **Client** | [Client Name] |
| **Project** | [Project Name] |
| **Version** | 1.0 |
| **Date** | [YYYY-MM-DD] |
| **Prepared By** | [Name] |
| **Approved By** | [Client Approver Name] |

---

## 1. Engagement Overview

### 1.1 Objective

[State the primary objective of the engagement. What is the client trying to learn or validate?]

Examples:
- Assess the security posture of the production web application before launch
- Validate the effectiveness of recent security improvements
- Identify vulnerabilities that could lead to unauthorized data access
- Simulate an advanced persistent threat to test detection capabilities

### 1.2 Engagement Type

| Type | Selected | Notes |
|---|---|---|
| External Penetration Test | [ ] | Internet-facing assets |
| Internal Penetration Test | [ ] | Internal network/systems |
| Web Application Test | [ ] | Specific web applications |
| API Security Test | [ ] | REST / GraphQL / gRPC APIs |
| Mobile Application Test | [ ] | Android / iOS apps |
| Cloud Security Assessment | [ ] | AWS / Azure / GCP |
| Red Team Engagement | [ ] | Goal-oriented adversarial simulation |
| Social Engineering | [ ] | Phishing / Vishing / Physical |
| Wireless Assessment | [ ] | WiFi / Bluetooth |
| Code Review | [ ] | Source code analysis |

### 1.3 Testing Perspective

| Perspective | Selected | Description |
|---|---|---|
| Black-Box | [ ] | No prior knowledge; simulates external attacker |
| Grey-Box | [ ] | Limited information; credentials and basic docs provided |
| White-Box | [ ] | Full access; source code, architecture docs, credentials |

---

## 2. Target Inventory

### 2.1 Web Applications

| ID | URL | Description | Environment | Tech Stack | Auth Required |
|---|---|---|---|---|---|
| WEB-01 | [https://app.example.com] | [Main application] | [Prod/Staging] | [React, Node.js, PostgreSQL] | [Yes/No] |
| WEB-02 | [https://admin.example.com] | [Admin portal] | [Prod/Staging] | [Angular, Django] | [Yes] |

### 2.2 APIs

| ID | Base URL | Type | Documentation | Auth Method |
|---|---|---|---|---|
| API-01 | [https://api.example.com/v2] | [REST] | [Swagger URL] | [Bearer Token / API Key / OAuth] |
| API-02 | [https://graphql.example.com] | [GraphQL] | [Schema available] | [JWT] |

### 2.3 Network Ranges

| ID | CIDR / Range | Description | Location |
|---|---|---|---|
| NET-01 | [10.0.1.0/24] | [Office network] | [HQ Building A] |
| NET-02 | [203.0.113.0/28] | [DMZ] | [Cloud provider] |

### 2.4 Mobile Applications

| ID | Platform | Package / Bundle | Version | Distribution |
|---|---|---|---|---|
| MOB-01 | [Android] | [com.example.app] | [2.3.1] | [Play Store / APK provided] |
| MOB-02 | [iOS] | [com.example.app] | [2.3.1] | [TestFlight / IPA provided] |

### 2.5 Cloud Infrastructure

| ID | Provider | Account / Subscription | Services | Region |
|---|---|---|---|---|
| CLD-01 | [AWS] | [Account ID] | [EC2, S3, Lambda, RDS] | [us-east-1] |
| CLD-02 | [Azure] | [Subscription ID] | [App Service, SQL DB] | [East US] |

### 2.6 Other Assets

| ID | Asset | Type | Description |
|---|---|---|---|
| OTH-01 | [asset] | [Wireless / IoT / Hardware] | [description] |

---

## 3. In-Scope Activities

### 3.1 Testing Activities Matrix

| Activity | WEB-01 | WEB-02 | API-01 | NET-01 | MOB-01 |
|---|---|---|---|---|---|
| Reconnaissance | Yes | Yes | Yes | Yes | Yes |
| Vulnerability Scanning | Yes | Yes | Yes | Yes | Yes |
| Manual Testing | Yes | Yes | Yes | Yes | Yes |
| Exploitation (PoC) | Yes | Yes | Yes | Limited | Yes |
| Authenticated Testing | Yes | Yes | Yes | N/A | Yes |
| Business Logic Testing | Yes | Yes | Yes | N/A | Yes |
| Password Attacks | Limited | Limited | N/A | Yes | N/A |

### 3.2 Specific Test Areas

**Authentication and Session Management:**
- Login functionality and credential handling
- Session token generation and management
- Password reset and account recovery
- Multi-factor authentication (if present)
- Account lockout mechanisms

**Authorization and Access Control:**
- Horizontal privilege escalation (user-to-user)
- Vertical privilege escalation (user-to-admin)
- IDOR (Insecure Direct Object References)
- Function-level access control
- API authorization checks

**Input Validation:**
- SQL injection (all input vectors)
- Cross-site scripting (reflected, stored, DOM)
- Command injection
- Server-side template injection
- XML external entity injection
- File upload validation

**Business Logic:**
- Workflow bypass
- Race conditions
- Price manipulation
- Quantity manipulation
- Feature abuse

**Configuration and Deployment:**
- Server configuration review
- TLS/SSL configuration
- Security header analysis
- Default credentials
- Information disclosure

---

## 4. Out-of-Scope

### 4.1 Excluded Targets

| Target | Reason for Exclusion |
|---|---|
| [legacy.example.com] | [Scheduled for decommission; not worth testing] |
| [10.0.2.0/24] | [Critical production database servers] |
| [Third-party widget: analytics.vendor.com] | [Not owned by client] |
| [Payment processing: stripe.com endpoints] | [Third-party; covered by PCI compliance] |

### 4.2 Excluded Activities

| Activity | Reason |
|---|---|
| Denial of Service | Risk to production availability |
| Physical security testing | Not authorized for this engagement |
| Social engineering of specific individuals | Privacy and HR concerns |
| Modification of production data | Data integrity risk |
| Testing outside defined hours | Change management requirements |
| Attacks against shared infrastructure | Multi-tenant risk |

### 4.3 Conditional Scope

| Activity | Condition |
|---|---|
| [Exploitation of critical findings] | [Requires verbal approval from Technical Contact before proceeding] |
| [Testing during off-hours] | [Requires 24-hour advance written approval] |
| [Password cracking of real hashes] | [Only if hashes obtained during authorized testing] |

---

## 5. Testing Schedule

### 5.1 Timeline

| Phase | Start Date | End Date | Duration |
|---|---|---|---|
| Kickoff Meeting | [YYYY-MM-DD] | [YYYY-MM-DD] | 1 day |
| Reconnaissance | [YYYY-MM-DD] | [YYYY-MM-DD] | [N] days |
| Active Testing | [YYYY-MM-DD] | [YYYY-MM-DD] | [N] days |
| Exploitation / Validation | [YYYY-MM-DD] | [YYYY-MM-DD] | [N] days |
| Report Writing | [YYYY-MM-DD] | [YYYY-MM-DD] | [N] days |
| Report Delivery | [YYYY-MM-DD] | [YYYY-MM-DD] | 1 day |
| Debrief Meeting | [YYYY-MM-DD] | [YYYY-MM-DD] | 1 day |
| Remediation Retest | [YYYY-MM-DD] | [YYYY-MM-DD] | [N] days |

### 5.2 Testing Windows

| Day | Hours (UTC) | Activity |
|---|---|---|
| Monday-Friday | 09:00-18:00 | Standard testing |
| Saturday | Not authorized | No testing |
| Sunday | 02:00-06:00 | Automated scanning (if approved) |

### 5.3 Blackout Dates

| Date | Reason |
|---|---|
| [YYYY-MM-DD] | [Product launch / maintenance window] |

---

## 6. Access and Credentials

### 6.1 Network Access

| Method | Details | Provider |
|---|---|---|
| VPN | [VPN type, server address] | [Client IT] |
| Direct Network | [Physical/remote access details] | [Client IT] |
| Jump Host | [IP, access method] | [Client IT] |

### 6.2 Test Accounts

| ID | Username | Role | Application | MFA | Notes |
|---|---|---|---|---|---|
| ACC-01 | [testuser1@example.com] | Standard User | [WEB-01, API-01] | [Yes/No] | [Regular user access] |
| ACC-02 | [testadmin@example.com] | Administrator | [WEB-01, WEB-02] | [Yes/No] | [Full admin access] |
| ACC-03 | [testmanager@example.com] | Manager | [WEB-01] | [Yes/No] | [Manager role testing] |

### 6.3 Documentation Provided

| Document | Provided | Format |
|---|---|---|
| Architecture diagram | [Yes/No] | [PDF/Visio] |
| API documentation | [Yes/No] | [Swagger/Postman] |
| Source code access | [Yes/No] | [Git repo URL] |
| Previous test reports | [Yes/No] | [PDF] |
| Network diagram | [Yes/No] | [PDF/Visio] |

---

## 7. Contacts

### 7.1 Client Contacts

| Role | Name | Email | Phone | Availability |
|---|---|---|---|---|
| Project Sponsor | [Name] | [email] | [phone] | Business hours |
| Technical Contact | [Name] | [email] | [phone] | Business hours |
| Emergency Contact | [Name] | [email] | [phone] | 24/7 |
| IT Operations | [Name] | [email] | [phone] | Business hours |

### 7.2 Testing Team

| Role | Name | Email | Phone |
|---|---|---|---|
| Engagement Manager | [Name] | [email] | [phone] |
| Lead Tester | [Name] | [email] | [phone] |
| Tester | [Name] | [email] | [phone] |

---

## 8. Approval

By signing below, both parties confirm the scope defined in this document is accurate and authorized.

**Client Authorization:**

Name: _________________________ Title: _________________________

Signature: _________________________ Date: _________________________

**Service Provider Acknowledgment:**

Name: _________________________ Title: _________________________

Signature: _________________________ Date: _________________________

---

**Revision History**

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | [YYYY-MM-DD] | [Author] | Initial scope definition |
