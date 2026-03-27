# Red Team Engagement Report

| Field | Value |
|---|---|
| **Client** | [Client Name] |
| **Engagement Name** | [Operation Code Name] |
| **Version** | 1.0 |
| **Classification** | CONFIDENTIAL - RESTRICTED |
| **Date Range** | [YYYY-MM-DD] to [YYYY-MM-DD] |
| **Red Team Lead** | [Name] |
| **Red Team Members** | [Names] |
| **Blue Team Aware** | [Yes - Purple Team / No - Full Red Team] |
| **Report Author** | [Name] |

---

## 1. Executive Summary

### 1.1 Engagement Overview

[Client Name] engaged [Red Team Provider] to conduct a goal-oriented adversarial simulation against [target environment description]. The engagement ran from [start date] to [end date].

Unlike a traditional penetration test, this red team engagement focused on achieving specific objectives while testing the organization's detection, response, and containment capabilities.

### 1.2 Objectives and Results

| Objective | Status | Detection |
|---|---|---|
| [Gain initial access to internal network] | Achieved / Not Achieved | Detected / Undetected |
| [Access customer PII database] | Achieved / Not Achieved | Detected / Undetected |
| [Compromise domain administrator] | Achieved / Not Achieved | Detected / Undetected |
| [Exfiltrate sensitive data] | Achieved / Not Achieved | Detected / Undetected |
| [Establish persistent access] | Achieved / Not Achieved | Detected / Undetected |

### 1.3 Overall Assessment

[Summary paragraph: Was the red team able to achieve its primary objectives? How effective were the organization's defenses? What was the mean time to detect (MTTD) and mean time to respond (MTTR)?]

---

## 2. Rules of Engagement Summary

### 2.1 Scope

**In Scope:**
- [Network ranges]
- [Applications]
- [Physical locations if applicable]
- [Personnel (for social engineering if authorized)]

**Out of Scope:**
- [Excluded systems]
- [Denial of Service]
- [Third-party infrastructure]

### 2.2 Authorized Techniques

| MITRE ATT&CK Tactic | Authorized | Notes |
|---|---|---|
| Reconnaissance | Yes | [Constraints] |
| Resource Development | Yes | [Constraints] |
| Initial Access | Yes | [Phishing authorized / Physical authorized] |
| Execution | Yes | [No destructive payloads] |
| Persistence | Yes | [Reversible methods only] |
| Privilege Escalation | Yes | [Constraints] |
| Defense Evasion | Yes | [Constraints] |
| Credential Access | Yes | [No production password cracking] |
| Discovery | Yes | [Constraints] |
| Lateral Movement | Yes | [Constraints] |
| Collection | Yes | [Synthetic data preferred] |
| Exfiltration | Yes | [Rate limited / test data only] |
| Impact | No | [DoS/destruction not authorized] |

### 2.3 Deconfliction

| Item | Detail |
|---|---|
| Deconfliction Contact | [Name, Phone, Email] |
| Emergency Stop Phrase | [Phrase] |
| Source IPs | [IPs used by red team] |
| Implant Identifiers | [C2 beacon signatures for deconfliction] |

---

## 3. Attack Narrative

### 3.1 Timeline Overview

```
Day 1-3:   Reconnaissance and OSINT
Day 4-5:   Resource development and infrastructure setup
Day 6:     Initial access via [method]
Day 7-8:   Internal reconnaissance and privilege escalation
Day 9-10:  Lateral movement to target systems
Day 11:    Objective achieved - [objective]
Day 12:    Data staging and exfiltration test
Day 13:    Persistence establishment
Day 14:    Cleanup and debrief preparation
```

### 3.2 Phase 1: Reconnaissance

**Duration:** [Date range]
**MITRE ATT&CK:** T1592, T1589, T1591, T1593, T1594

**Activities:**
- [Describe OSINT activities: LinkedIn profiling, email harvesting, technology fingerprinting]
- [Describe external scanning: subdomain enumeration, port scanning, service identification]
- [Describe information gathered and how it informed the attack plan]

**Key Findings:**
- [Finding 1: e.g., Employee email format discovered via LinkedIn]
- [Finding 2: e.g., Exposed development server at dev.target.com]
- [Finding 3: e.g., VPN endpoint identified with outdated software]

**Detection:** [Was any recon activity detected by the blue team? SOC alert? Firewall block?]

### 3.3 Phase 2: Initial Access

**Duration:** [Date range]
**MITRE ATT&CK:** [Specific technique IDs]

**Attack Vector:** [Detailed description of how initial access was obtained]

Example narrative:
"Using the email addresses harvested during reconnaissance, a targeted phishing campaign was launched against 15 employees in the finance department. The phishing email impersonated an internal IT notification and contained a link to a cloned SSO page hosted on [infrastructure]. Three employees entered credentials. The credentials for [user] provided VPN access to the internal network."

**Evidence:**
- [Phishing email content (sanitized)]
- [Screenshot of credential capture]
- [VPN connection log]

**Detection:** [Describe if/when/how the blue team detected this activity]

### 3.4 Phase 3: Execution and Discovery

**Duration:** [Date range]
**MITRE ATT&CK:** [Specific technique IDs]

**Activities:**
- [Command execution methods used]
- [Internal network scanning and enumeration]
- [Active Directory enumeration]
- [Service and share discovery]

**Key Discoveries:**
- [Network topology findings]
- [High-value targets identified]
- [Misconfigurations discovered]

**Detection:** [Blue team detection status]

### 3.5 Phase 4: Privilege Escalation

**Duration:** [Date range]
**MITRE ATT&CK:** [Specific technique IDs]

**Escalation Path:**
1. [Starting privilege level]
2. [Method used to escalate]
3. [Resulting privilege level]
4. [Further escalation if applicable]

**Evidence:**
- [Commands executed]
- [Screenshots of privilege verification]

**Detection:** [Blue team detection status]

### 3.6 Phase 5: Lateral Movement

**Duration:** [Date range]
**MITRE ATT&CK:** [Specific technique IDs]

**Movement Path:**
```
[Initial Host] --> [Host 2] --> [Host 3] --> [Target System]
  (user priv)    (local admin)  (svc account)  (domain admin)
```

**Techniques Used:**
- [e.g., Pass-the-Hash, Kerberoasting, RDP, WMI, PSExec]
- [Describe each hop and the technique used]

**Detection:** [Blue team detection status at each stage]

### 3.7 Phase 6: Objective Completion

**Duration:** [Date range]

**Objective 1: [Objective Name]**
- Status: [Achieved / Not Achieved]
- Method: [How the objective was completed]
- Evidence: [Proof of objective completion]
- Impact: [What this means for the organization]

**Objective 2: [Objective Name]**
- Status: [Achieved / Not Achieved]
- Method: [How the objective was completed]
- Evidence: [Proof of objective completion]
- Impact: [What this means for the organization]

### 3.8 Phase 7: Persistence and Exfiltration

**Duration:** [Date range]
**MITRE ATT&CK:** [Specific technique IDs]

**Persistence Mechanisms Established:**
1. [Mechanism 1: e.g., Scheduled task on SERVER01]
2. [Mechanism 2: e.g., Golden ticket for domain]
3. [Mechanism 3: e.g., Web shell on web server]

**Exfiltration Test:**
- Method: [e.g., HTTPS to external C2, DNS tunneling]
- Data Volume: [e.g., 500MB test data]
- Duration: [e.g., 2 hours]
- Detection: [Was exfiltration detected?]

---

## 4. MITRE ATT&CK Mapping

| Tactic | Technique | ID | Used | Detected |
|---|---|---|---|---|
| Initial Access | Phishing: Spearphishing Link | T1566.002 | Yes | No |
| Execution | Command and Scripting Interpreter: PowerShell | T1059.001 | Yes | Yes |
| Persistence | Scheduled Task/Job | T1053 | Yes | No |
| Privilege Escalation | Exploitation for Privilege Escalation | T1068 | Yes | No |
| Defense Evasion | Obfuscated Files or Information | T1027 | Yes | No |
| Credential Access | OS Credential Dumping: LSASS Memory | T1003.001 | Yes | Yes |
| Discovery | Network Service Discovery | T1046 | Yes | No |
| Lateral Movement | Remote Services: SMB/Windows Admin Shares | T1021.002 | Yes | No |
| Collection | Data from Local System | T1005 | Yes | No |
| Exfiltration | Exfiltration Over C2 Channel | T1041 | Yes | No |

**Detection Rate:** [N] of [Total] techniques detected = [Percentage]%

---

## 5. Detection and Response Assessment

### 5.1 Blue Team Performance

| Metric | Value |
|---|---|
| Total Red Team Actions | [N] |
| Actions Detected | [N] |
| Detection Rate | [N]% |
| Mean Time to Detect (MTTD) | [hours/days] |
| Mean Time to Respond (MTTR) | [hours/days] |
| Alerts Generated | [N] |
| True Positive Rate | [N]% |
| Containment Actions Taken | [N] |

### 5.2 Detection Gaps

| Gap | Impact | Recommendation |
|---|---|---|
| [No detection for lateral movement via WMI] | [Attacker moved freely between systems] | [Enable WMI event logging, create detection rule] |
| [Phishing email bypassed email gateway] | [Initial access succeeded] | [Update email filtering rules, add URL sandboxing] |
| [No alerting on Kerberoasting] | [Service account credentials compromised] | [Monitor for TGS requests with RC4 encryption] |

### 5.3 Effective Detections

| Detection | Alert Source | Response Time |
|---|---|---|
| [PowerShell execution on server] | [EDR / SIEM Rule] | [2 hours] |
| [LSASS memory access] | [EDR alert] | [30 minutes] |

---

## 6. Findings and Recommendations

### 6.1 Technical Findings

| ID | Finding | Severity | MITRE ATT&CK |
|---|---|---|---|
| RT-001 | [Finding] | Critical | [Technique ID] |
| RT-002 | [Finding] | High | [Technique ID] |
| RT-003 | [Finding] | Medium | [Technique ID] |

### 6.2 Process and People Findings

| ID | Finding | Category |
|---|---|---|
| RP-001 | [e.g., Phishing click rate of 20%] | Security Awareness |
| RP-002 | [e.g., No incident escalation for 48 hours] | Incident Response |
| RP-003 | [e.g., SOC did not correlate related alerts] | Detection |

### 6.3 Recommendations

#### Immediate (0-7 days)
1. [Remove persistence mechanisms (locations provided in cleanup section)]
2. [Reset compromised credentials]
3. [Patch exploited vulnerability]

#### Short-Term (7-30 days)
1. [Implement missing detection rules]
2. [Update incident response playbooks]
3. [Conduct targeted security awareness training]

#### Medium-Term (30-90 days)
1. [Network segmentation improvements]
2. [Implement privileged access management]
3. [Deploy additional monitoring capabilities]

#### Long-Term (90+ days)
1. [Zero trust architecture planning]
2. [Regular adversarial simulation program]
3. [Security operations maturity improvements]

---

## 7. Cleanup and Artifacts

### 7.1 Artifacts to Remove

| Artifact | Location | Type | Status |
|---|---|---|---|
| [C2 beacon] | [SERVER01 - C:\Windows\Temp\svc.exe] | Implant | Removed |
| [Scheduled task] | [SERVER01 - WindowsUpdate] | Persistence | Removed |
| [Web shell] | [WEBSVR - /var/www/html/.config.php] | Persistence | Removed |
| [Test accounts] | [Active Directory - redteam_svc] | Account | Removed |

### 7.2 Cleanup Verification

All red team artifacts have been removed and verified. The following steps were taken:
1. [All implants deactivated and binaries removed]
2. [All persistence mechanisms removed]
3. [All test accounts disabled and deleted]
4. [All tools removed from target systems]
5. [Red team infrastructure decommissioned]

---

## 8. Appendix

### A. Infrastructure Used

| Component | Details |
|---|---|
| C2 Server | [IP / Domain / Provider] |
| Phishing Infrastructure | [Domain / IP] |
| Redirectors | [IPs] |
| Payload Hosting | [Details] |

### B. Tools Used

| Tool | Purpose |
|---|---|
| [Cobalt Strike / Sliver / Mythic] | Command and Control |
| [Evilginx / GoPhish] | Phishing |
| [BloodHound] | Active Directory analysis |
| [Rubeus] | Kerberos attacks |
| [Mimikatz] | Credential extraction |
| [CrackMapExec] | Network enumeration and exploitation |

### C. IOCs for Blue Team Validation

Provide these IOCs to the blue team so they can search historical logs and improve detections:

**IP Addresses:**
- [Red team source IPs]

**Domains:**
- [Red team domains]

**File Hashes:**
- [Implant hashes - SHA256]

**User Agents:**
- [Custom user agents used]

**Named Pipes / Services:**
- [C2 named pipes or service names]

---

**Document Control**

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | [YYYY-MM-DD] | [Author] | Initial report |
