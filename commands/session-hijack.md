Test session hijacking on: $ARGUMENTS

## Pre-flight
- Identify session management mechanism (cookies, tokens, URL params)
- Verify session hijacking testing is in scope

## Phase 1: Session Analysis
1. Identify session identifiers: cookie names, token locations
2. Check cookie flags: HttpOnly, Secure, SameSite, Path, Domain, Expires
3. Analyze session ID entropy: is it predictable?
4. Check session fixation: can you set session ID before auth?

## Phase 2: Hijacking Techniques
1. **Session sniffing**: Wireshark capture on shared network (HTTP only)
2. **XSS to cookie theft**: /xss-hunt → document.cookie exfiltration
3. **Session fixation**: set session cookie before login, check if retained after auth
4. **CSRF**: forge requests using victim's session (check SameSite, CSRF tokens)
5. **Session prediction**: generate multiple sessions, analyze for patterns
6. **Token replay**: capture and replay auth tokens

## Phase 3: JWT-Specific
1. Run `python3 tools/web/jwt-toolkit.py decode <token>`
2. Test alg:none: `python3 tools/web/jwt-toolkit.py none <token>`
3. Crack weak secret: `python3 tools/web/jwt-toolkit.py crack <token> --wordlist wordlists/tokens/jwt-secrets.txt`
4. Algorithm confusion: RS256→HS256 attack
5. Claim tampering: modify role, sub, admin claims

## Phase 4: Post-Hijack
1. Verify session gives access to victim's account
2. Test session invalidation: does logout actually destroy session?
3. Check concurrent sessions: can multiple sessions exist?
4. Test session timeout: how long until expiry?

## Output
Save to engagements/<target>/findings/session-*.md
Reference: CEH Module 11 — Session Hijacking

## Framework Mapping
- MITRE ATT&CK: TA0006 (Credential Access) -> T1539 (Steal Web Session Cookie)
- MITRE ATT&CK: TA0008 (Lateral Movement) -> T1563 (Remote Service Session Hijacking)
- MITRE ATT&CK: TA0005 (Defense Evasion) -> T1550 (Use Alternate Authentication Material)
- Cyber Kill Chain: Phase 7 -- Actions on Objectives
- CEH v12: Module 11 -- Session Hijacking
