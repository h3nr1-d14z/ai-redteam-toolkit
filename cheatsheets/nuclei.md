# Nuclei Cheatsheet

## Basic Usage
```bash
# Scan single target
nuclei -u https://target.com

# Scan from list
nuclei -l targets.txt

# Scan with specific template
nuclei -u https://target.com -t cves/2023/CVE-2023-12345.yaml

# Scan with template directory
nuclei -u https://target.com -t cves/

# Scan with multiple template paths
nuclei -u https://target.com -t cves/ -t vulnerabilities/ -t misconfiguration/

# Pipe from other tools
subfinder -d target.com | httpx | nuclei
cat urls.txt | nuclei

# Stdin targets
echo "https://target.com" | nuclei
```

## Template Selection
```bash
# By severity
nuclei -u target.com -s critical
nuclei -u target.com -s critical,high
nuclei -u target.com -s critical,high,medium

# By tags
nuclei -u target.com -tags cve
nuclei -u target.com -tags xss,sqli
nuclei -u target.com -tags oast    # Out-of-band testing
nuclei -u target.com -tags tech    # Technology detection
nuclei -u target.com -tags token   # Token/secret detection

# By template type
nuclei -u target.com -type http
nuclei -u target.com -type dns
nuclei -u target.com -type network
nuclei -u target.com -type headless

# By author
nuclei -u target.com -author pdteam

# By protocol
nuclei -u target.com -pt http
nuclei -u target.com -pt dns
nuclei -u target.com -pt network

# Exclude templates
nuclei -u target.com -exclude-tags dos
nuclei -u target.com -et cves/2020/

# Exclude severity
nuclei -u target.com -es info
```

## Performance and Configuration
```bash
# Set concurrency
nuclei -u target.com -c 50              # 50 concurrent templates
nuclei -u target.com -rl 150            # Rate limit: 150 req/sec
nuclei -u target.com -bs 25             # Bulk size (targets per template)
nuclei -u target.com -timeout 10        # Request timeout seconds

# Headers
nuclei -u target.com -H "Authorization: Bearer token"
nuclei -u target.com -H "Cookie: session=abc123"

# Proxy
nuclei -u target.com -proxy http://127.0.0.1:8080

# Follow redirects
nuclei -u target.com -fr

# Custom user agent
nuclei -u target.com -H "User-Agent: Mozilla/5.0"

# Interactsh (out-of-band server)
nuclei -u target.com -iserver oast.pro    # Custom OAST server
nuclei -u target.com -ni                  # Disable interactsh
```

## Output
```bash
# Output to file
nuclei -u target.com -o results.txt

# JSON output
nuclei -u target.com -j -o results.json

# JSON with details
nuclei -u target.com -je -o results.json  # JSON with extracted results

# Markdown report
nuclei -u target.com -me reports/         # Markdown export dir

# Verbose output
nuclei -u target.com -v                   # Verbose
nuclei -u target.com -debug               # Debug (show requests/responses)

# Silent (only results)
nuclei -u target.com -silent

# No color
nuclei -u target.com -nc
```

## Template Management
```bash
# Update templates
nuclei -update-templates
nuclei -ut

# List templates
nuclei -tl                               # List all templates

# Template info
nuclei -tl -tags cve | wc -l            # Count CVE templates
nuclei -tl -s critical | wc -l          # Count critical templates

# Template directory
ls ~/nuclei-templates/

# Custom template directory
nuclei -u target.com -t /path/to/custom/templates/
```

## Custom Template (Basic)
```yaml
id: custom-check

info:
  name: Custom Security Check
  author: yourname
  severity: medium
  description: Check for specific vulnerability
  tags: custom

http:
  - method: GET
    path:
      - "{{BaseURL}}/admin"
      - "{{BaseURL}}/admin/login"

    matchers-condition: or
    matchers:
      - type: status
        status:
          - 200

      - type: word
        words:
          - "admin panel"
          - "dashboard"
        condition: or
```

## Custom Template (Advanced)
```yaml
id: sqli-login-check

info:
  name: SQL Injection in Login Form
  author: yourname
  severity: critical
  tags: sqli,custom

http:
  - raw:
      - |
        POST /login HTTP/1.1
        Host: {{Hostname}}
        Content-Type: application/x-www-form-urlencoded

        username=admin'OR'1'='1&password=test

    matchers-condition: and
    matchers:
      - type: word
        words:
          - "Welcome"
          - "Dashboard"
        condition: or

      - type: status
        status:
          - 200
          - 302

    extractors:
      - type: regex
        name: session
        part: header
        regex:
          - "Set-Cookie: (.*?);"
```

## Common Scan Profiles
```bash
# Quick vulnerability scan
nuclei -l targets.txt -s critical,high -c 50 -rl 100 -o critical_findings.txt

# Full scan (all severities)
nuclei -l targets.txt -o full_scan.txt

# Technology detection only
nuclei -l targets.txt -tags tech -o tech_stack.txt

# CVE scan only
nuclei -l targets.txt -tags cve -s critical,high -o cve_findings.txt

# Exposure and misconfig scan
nuclei -l targets.txt -tags exposure,misconfig -o exposure.txt

# Token and secret detection
nuclei -l targets.txt -tags token,exposure -o secrets.txt

# Subdomain takeover check
nuclei -l subdomains.txt -tags takeover -o takeover.txt

# Headless browser scan (JS-rendered)
nuclei -l targets.txt -headless -tags headless -o headless.txt

# Network scan (non-HTTP)
nuclei -l hosts.txt -t network/ -o network.txt
```

## Useful Template Tags
```
cve           CVE-based checks
oast          Out-of-band testing (requires interactsh)
tech          Technology fingerprinting
exposure      Sensitive data exposure
misconfig     Misconfiguration
takeover      Subdomain takeover
default-login Default credentials
token         API keys, tokens, secrets
xss           Cross-site scripting
sqli          SQL injection
lfi           Local file inclusion
rce           Remote code execution
ssrf          Server-side request forgery
redirect      Open redirect
```
