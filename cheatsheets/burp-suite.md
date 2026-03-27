# Burp Suite Cheatsheet

## Proxy Setup
```
Browser Proxy: 127.0.0.1:8080
Install CA: http://burp (browse from proxied browser)
Mobile: set device WiFi proxy to <burp_ip>:8080, install CA cert

# Invisible proxying (for non-proxy-aware clients)
Proxy > Options > Proxy Listeners > Edit > Request handling > Support invisible proxying

# Match and Replace (auto-modify requests)
Proxy > Options > Match and Replace
  - Remove security headers: X-Frame-Options, CSP
  - Add custom headers
  - Modify cookies
```

## Key Shortcuts
```
Ctrl+R          Send to Repeater
Ctrl+I          Send to Intruder
Ctrl+Shift+R    Go to Repeater
Ctrl+Shift+I    Go to Intruder
Ctrl+Shift+T    Go to Target
Ctrl+Shift+P    Go to Proxy
Ctrl+Shift+D    Go to Dashboard
Ctrl+Space      Issue Repeater request (in Repeater tab)
Ctrl+U          URL-encode selected text
Ctrl+Shift+U    URL-decode selected text
Ctrl+B          Base64-encode selected text
Ctrl+Shift+B    Base64-decode selected text
Ctrl+H          HTML-encode selected text
Ctrl+Shift+H    HTML-decode selected text
Ctrl+F          Search in current response/request
Ctrl+Z          Undo
Ctrl+Shift+Z    Redo
```

## Target Scope
```
Target > Scope > Add
  - Include: https://target.com
  - Include: *.target.com
  - Exclude: logout URLs, static assets

# Filter proxy history to scope
Proxy > HTTP History > Filter > Show only in-scope items

# Reduce noise
Project options > Out-of-scope requests > Drop all out-of-scope requests
```

## Proxy Interception
```
# Intercept rules
Proxy > Intercept > Options > Intercept Client Requests
  - Match: URL, File extension, Method, Content-Type
  - Example: Only intercept requests to *.target.com

# Response interception
Proxy > Intercept > Options > Intercept Server Responses
  - Intercept responses to intercepted requests

# Useful interception filters
  - Drop: *.js, *.css, *.png, *.jpg, *.gif (reduce noise)
  - Intercept: POST requests only
```

## Repeater Tips
```
# Right-click menu in Repeater
- Change request method (GET <-> POST)
- Change body encoding (URL-encoded <-> JSON <-> XML)
- Copy as curl command
- Paste from curl command

# Follow redirects
Repeater > Settings icon > Follow redirections: Always/On-site/Never

# Auto-update Content-Length
Repeater > Settings icon > Update Content-Length (usually enabled by default)
```

## Intruder Attack Types
```
# Sniper: single payload set, inserts into one position at a time
# Use for: testing each parameter individually
Positions: param1=PAYLOAD&param2=value
           param1=value&param2=PAYLOAD

# Battering Ram: single payload set, inserts same value in all positions
# Use for: same payload in multiple places (username == password)
Positions: user=PAYLOAD&pass=PAYLOAD

# Pitchfork: multiple payload sets, one per position, iterates in parallel
# Use for: paired lists (username1+password1, username2+password2)
Positions: user=PAYLOAD1&pass=PAYLOAD2

# Cluster Bomb: multiple payload sets, tests all combinations
# Use for: brute force all username+password combinations
Positions: user=PAYLOAD1&pass=PAYLOAD2
```

## Intruder Payloads
```
# Common payload types
Simple list        Load wordlist or paste values
Runtime file       Load from file (for large lists)
Numbers            Range: 1-1000, step 1
Dates              Date ranges and formats
Brute forcer       Character set + min/max length
Recursive grep     Extract from previous response
Null payloads      Empty payloads (for race conditions)

# Payload processing
Add prefix/suffix
Encode: URL, Base64, HTML, Hash
Match/Replace
Substring
Reverse

# Grep - Extract (identify interesting responses)
Intruder > Settings > Grep - Extract
  - Add: define regex to extract data from responses
  - Example: extract error messages, tokens, user data
```

## Scanner
```
# Active scan
Right-click request > Do active scan
Scanner > Scan configuration > select audit checks

# Passive scan (automatic, always running for proxied traffic)
Dashboard > Event log (check for passive findings)

# Scan specific insertion points
Right-click > Scan defined insertion points
Select specific parameters to scan

# Scan configurations
- Minimize false positives: reduce scan speed, increase confidence
- Maximize coverage: enable all audit checks
- Custom: select specific vulnerability categories
```

## Essential Extensions (BApp Store)
```
# Install via Extender > BApp Store

Logger++              Enhanced request/response logging with filtering
Autorize             Authorization testing (automatic IDOR check)
AuthMatrix           Matrix-based authorization testing
Turbo Intruder       Fast, scriptable HTTP fuzzer (Python)
Param Miner          Discover hidden parameters and headers
Active Scan++        Enhanced active scanning
Hackvertor           Advanced encoding/decoding/transformation
JSON Web Tokens      JWT decode, modify, and attack
Upload Scanner       Test file upload vulnerabilities
InQL                 GraphQL introspection and injection
Collaborator Everywhere   Add Collaborator payloads to all requests
Software Vulnerability Scanner   CVE detection from version banners
IP Rotate            Rotate source IP via cloud providers
```

## Turbo Intruder (Fast Fuzzing)
```python
# Basic request fuzzing
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=50,
                           requestsPerConnection=100,
                           pipeline=True)
    for word in open('/usr/share/seclists/Discovery/Web-Content/common.txt'):
        engine.queue(target.req, word.rstrip())

def handleResponse(req, interesting):
    if req.status == 200:
        table.add(req)

# Race condition testing
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           requestsPerConnection=50,
                           pipeline=False)
    for i in range(50):
        engine.queue(target.req, gate='race1')
    engine.openGate('race1')  # Send all simultaneously

def handleResponse(req, interesting):
    table.add(req)
```

## Collaborator (Out-of-Band Testing)
```
# Generate Collaborator payload
Burp > Collaborator client > Copy to clipboard
Result: xyz123.burpcollaborator.net

# Use in payloads
SSRF: http://xyz123.burpcollaborator.net
XXE:  <!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://xyz123.burpcollaborator.net">]>
Blind XSS: <script src=//xyz123.burpcollaborator.net></script>
DNS: anything.xyz123.burpcollaborator.net

# Poll for interactions
Burp > Collaborator client > Poll now
Check: DNS, HTTP, SMTP interactions
```

## Useful Configurations
```
# Session handling rules (maintain authenticated session)
Project options > Sessions > Session handling rules
  - Add rule: check session is valid
  - Macro: login request sequence
  - Scope: define which tools use this rule

# Upstream proxy (route through Tor, corporate proxy)
User options > Connections > Upstream proxy servers
  - SOCKS proxy: 127.0.0.1:9050 (Tor)
  - HTTP proxy: corporate-proxy:8080

# SSL/TLS settings
User options > TLS > enable "Use custom protocols and ciphers" if needed
Project options > TLS > Client TLS Certificates (mutual TLS)

# Invisible proxy for mobile/thick clients
Proxy > Options > Edit listener > Request handling
  - Redirect to host: target.com
  - Redirect to port: 443
  - Enable "Support invisible proxying"
```

## Common Workflows
```
# Authorization testing with Autorize
1. Install Autorize extension
2. Browse app as admin (captures requests)
3. Set low-privilege cookie in Autorize
4. Autorize replays each request with low-priv cookie
5. Review results: Bypassed (red) = authorization issue

# CSRF testing
1. Intercept state-changing request
2. Right-click > Engagement tools > Generate CSRF PoC
3. Modify PoC if needed
4. Open in browser without active session

# WebSocket testing
1. Proxy > WebSockets history
2. Right-click > Send to Repeater
3. Modify and resend WebSocket messages
```
