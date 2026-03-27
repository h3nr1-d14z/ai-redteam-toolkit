Plan red team operation against: $ARGUMENTS

1. **Objective definition**: Define goals — data exfiltration, domain admin, specific system access, physical access
2. **Threat model**: Select threat actor profile (APT, insider, opportunistic) and TTPs (MITRE ATT&CK mapping)
3. **Reconnaissance plan**: Passive/active recon phases, OSINT collection, social media, technical footprinting
4. **Initial access**: Plan delivery vectors — phishing, web exploit, supply chain, physical, wireless
5. **Infrastructure**: Plan attack infrastructure — redirectors, C2 domains, staging servers, anonymization
6. **Execution timeline**: Phase gates with go/no-go criteria, communication plan with blue team POC
7. **Rules of engagement**: Document scope, excluded systems, emergency contacts, deconfliction process
8. **Reporting**: Define evidence collection, reporting cadence, final report structure

Output: `engagements/<target>/reports/redteam-plan-<date>.md` with MITRE ATT&CK mapping
