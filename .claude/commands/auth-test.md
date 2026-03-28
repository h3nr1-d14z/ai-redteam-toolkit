Test authentication on: $ARGUMENTS

Map auth mechanism (JWT, session, OAuth, SAML, API key).
For JWT: run tools/web/jwt-toolkit.py decode <token>, test alg:none, weak secret crack, claim tampering.
For session: test fixation, prediction, timeout.
For OAuth: test redirect_uri manipulation, state parameter, scope escalation.
For password: test brute force, credential stuffing, reset poisoning.
Check MFA bypass, remember-me token security, logout completeness.
Reference: methodology/web-pentest.md Phase 3.
Output: engagements/<target>/findings/auth-*.md

## Safety
Verify authorization and scope before proceeding. Document all actions.
