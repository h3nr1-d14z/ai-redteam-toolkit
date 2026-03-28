Plan red team operation against: $ARGUMENTS

Define objectives, threat model (nation-state/criminal/insider), scope, ROE.
Map to MITRE ATT&CK.
Plan phases: recon (OSINT, tech fingerprint), initial access (phishing, exploitation, physical), execution (LOLBins, PowerShell), persistence (registry, scheduled tasks, implants), lateral movement (pass-the-hash, Kerberoasting), collection and exfiltration.
Set up infrastructure: C2, redirectors, phishing, payloads.
OPSEC: separate infra per engagement, domain categorization, malleable C2 profiles.
Reference: methodology/red-team-ops.md.
Output: engagements/<target>/reports/redteam-plan.md

## Safety
Verify authorization and scope before proceeding. Document all actions.
