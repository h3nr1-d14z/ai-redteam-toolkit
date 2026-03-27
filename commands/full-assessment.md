Run full automated assessment pipeline on: $ARGUMENTS

Phase 1: /deconflict then /recon.
Phase 2: /nuclei-scan (critical+high) + /scan-ports.
Phase 3: /pentest — if API found also /api-pentest, if cloud also /cloud-pentest, if auth also /auth-test.
Phase 4: /exploit for confirmed vulns.
Phase 5: /write-report to compile.
Save progress after each phase.
If any phase fails, continue with next.
For OMC users: /ralph /full-assessment for autopilot mode.
Output: engagements/<target>/reports/full-assessment-<date>.md

## Safety
Verify authorization and scope before proceeding. Document all actions.
