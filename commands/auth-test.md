Test authentication and authorization on: $ARGUMENTS

1. **Login mechanisms**: Test for default creds, brute force protection, account lockout, enumeration via error messages
2. **Session management**: Cookie attributes (Secure, HttpOnly, SameSite), session fixation, concurrent sessions, timeout
3. **Password policy**: Minimum complexity, common password rejection, password reset flow security
4. **MFA**: Test bypass techniques — response manipulation, backup code brute force, lack of MFA re-verification
5. **JWT/Token**: Algorithm confusion (none/HS256/RS256), weak secrets, claim manipulation, expiry validation
6. **OAuth/SSO**: Redirect URI manipulation, state parameter validation, scope escalation, token leakage
7. **Authorization**: IDOR, role escalation, forced browsing, missing function-level access control

Save findings to `engagements/<target>/findings/auth-*.md` with CVSS scores.
