# Engagement: [TARGET_NAME]

## Target Information

| Field | Value |
|-------|-------|
| **Target Name** | [TARGET_NAME] |
| **Target Type** | [web / mobile / game / binary / cloud / network / iot] |
| **Target URL/IP** | [URL or IP address] |
| **Environment** | [production / staging / development / lab] |
| **Platform** | [Linux / Windows / macOS / Android / iOS / Cloud Provider] |

## Authorization

| Field | Value |
|-------|-------|
| **Authorized By** | [Name and role of authorizing person] |
| **Authorization Date** | [YYYY-MM-DD] |
| **Authorization Document** | [Reference to signed agreement - DO NOT commit the actual document] |
| **Authorization Scope** | [Brief description of what is authorized] |

## Engagement Details

| Field | Value |
|-------|-------|
| **Start Date** | [YYYY-MM-DD] |
| **End Date** | [YYYY-MM-DD] |
| **Status** | [not-started / in-progress / completed / on-hold] |
| **Tester(s)** | [Names or handles] |
| **Report Delivered** | [Yes / No] |

## Scope

### In Scope

- [List specific targets, endpoints, IP ranges]
- [List specific functionalities to test]
- [List specific test types authorized]

### Out of Scope

- [List explicitly excluded targets]
- [List excluded test types (e.g., DoS)]
- [List excluded time windows]

## Rules of Engagement

- [Specific rules about testing hours]
- [Rules about data handling]
- [Escalation contacts and procedures]
- [Rules about social engineering if applicable]
- [Rules about physical access if applicable]

## Methodology

1. **Reconnaissance**: [approach]
2. **Enumeration**: [approach]
3. **Vulnerability Analysis**: [approach]
4. **Exploitation**: [approach]
5. **Post-Exploitation**: [approach if authorized]
6. **Reporting**: [approach]
7. **Cleanup**: [approach]

## Findings Summary

| ID | Title | Severity | CVSS | Status |
|----|-------|----------|------|--------|
| F-001 | [Finding title] | [Critical/High/Medium/Low/Info] | [0.0-10.0] | [Open/Fixed/Accepted] |

## Directory Structure

```
[TARGET_NAME]/
  README.md       # This file
  scope.md        # Detailed scope and rules of engagement
  recon/          # Reconnaissance data and notes
  exploits/       # Proof-of-concept exploit scripts
  findings/       # Individual vulnerability write-ups
  evidence/       # Screenshots, recordings, logs
  loot/           # Extracted data (credentials, tokens - handle securely)
  scripts/        # Custom scripts for this engagement
  reports/        # Final deliverable reports
```

## Notes

[Any additional notes, observations, or context about this engagement]
