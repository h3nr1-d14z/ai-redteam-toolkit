# Sample Reconnaissance Output: example.com

**Target:** example.com (fictional)
**Date:** 2026-03-15
**Tester:** Security Analyst

---

## DNS Records

```
$ dig example.com ANY

example.com.        300  IN  A       93.184.216.34
example.com.        300  IN  AAAA    2606:2800:220:1:248:1893:25c8:1946
example.com.        300  IN  MX      10 mail.example.com.
example.com.        300  IN  MX      20 mail2.example.com.
example.com.        300  IN  NS      ns1.example.com.
example.com.        300  IN  NS      ns2.example.com.
example.com.        300  IN  TXT     "v=spf1 include:_spf.google.com ~all"
example.com.        300  IN  TXT     "google-site-verification=abc123xyz"
example.com.        300  IN  SOA     ns1.example.com. admin.example.com. 2024031501 7200 3600 604800 300
```

**Observations:**
- Using Google Workspace for email (SPF record references Google)
- Google site verification present (likely uses Google Search Console)
- Two nameservers (ns1, ns2) -- self-hosted DNS
- Mail servers are on the same domain (mail.example.com, mail2.example.com)

---

## Subdomain Enumeration

```
$ subfinder -d example.com -all | sort -u

app.example.com
api.example.com
blog.example.com
cdn.example.com
ci.example.com
dashboard.example.com
dev.example.com
docs.example.com
git.example.com
grafana.example.com
jenkins.example.com
jira.example.com
mail.example.com
mail2.example.com
monitoring.example.com
ns1.example.com
ns2.example.com
portal.example.com
staging.example.com
status.example.com
test.example.com
vpn.example.com
wiki.example.com
www.example.com
```

**High-Value Targets Identified:**
- `dev.example.com` -- development environment (may have weaker security)
- `staging.example.com` -- staging (often mirrors production with test data)
- `jenkins.example.com` -- CI/CD server (if exposed, potential for RCE)
- `git.example.com` -- source code repository
- `grafana.example.com` -- monitoring dashboard (may expose internal metrics)
- `vpn.example.com` -- VPN endpoint
- `api.example.com` -- API server (primary testing target)

---

## Port Scan Results

```
$ nmap -sV -sC -T4 -oN nmap_scan.txt example.com

Nmap scan report for example.com (93.184.216.34)
Host is up (0.023s latency).
Not shown: 993 filtered ports
PORT     STATE  SERVICE    VERSION
22/tcp   open   ssh        OpenSSH 8.9p1 Ubuntu 3ubuntu0.6
80/tcp   open   http       nginx/1.24.0
443/tcp  open   ssl/http   nginx/1.24.0
| ssl-cert: Subject: CN=*.example.com
| Not valid before: 2025-01-15T00:00:00
| Not valid after:  2026-04-15T23:59:59
| http-title: Example Corp - Homepage
| http-server-header: nginx/1.24.0
3306/tcp closed mysql
5432/tcp closed postgresql
8080/tcp open   http       Apache Tomcat 9.0.83
| http-title: Apache Tomcat/9.0.83
8443/tcp open   ssl/http   Apache Tomcat 9.0.83
```

**Observations:**
- SSH exposed (OpenSSH 8.9p1 -- check for CVEs)
- nginx 1.24.0 as primary web server (reverse proxy likely)
- Wildcard SSL certificate (*.example.com)
- Apache Tomcat 9.0.83 on port 8080/8443 -- default page visible (misconfiguration)
- Database ports (3306, 5432) are closed but responded -- database may be running locally

---

## Technology Fingerprinting

```
$ whatweb https://example.com

https://example.com [200 OK]
  Country[US], HTML5, HTTPServer[nginx/1.24.0],
  JQuery[3.6.4], Meta-Author[Example Corp],
  Script[text/javascript], Strict-Transport-Security[max-age=31536000],
  Title[Example Corp - Homepage], X-Powered-By[Express],
  X-Request-ID[uuid format]
```

**Technology Stack:**
| Layer | Technology | Version | Notes |
|---|---|---|---|
| Web Server | nginx | 1.24.0 | Reverse proxy |
| Application | Node.js / Express | Unknown | X-Powered-By header |
| Frontend | React | 18.x | Identified from JS bundles |
| jQuery | jQuery | 3.6.4 | |
| App Server | Apache Tomcat | 9.0.83 | Port 8080/8443 |
| Database | PostgreSQL | Unknown | Port 5432 closed but present |
| CDN | CloudFront | | cdn.example.com CNAME |
| CI/CD | Jenkins | Unknown | jenkins.example.com |
| SCM | Gitea/GitLab | Unknown | git.example.com |
| Monitoring | Grafana | Unknown | grafana.example.com |

---

## Directory Enumeration

```
$ feroxbuster -u https://example.com -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt

200  GET   142l  385w  5842c https://example.com/
200  GET    45l  120w  1893c https://example.com/about
200  GET    38l   95w  1456c https://example.com/contact
200  GET    12l   30w   420c https://example.com/login
200  GET    15l   35w   510c https://example.com/register
302  GET     0l    0w     0c https://example.com/dashboard -> /login
302  GET     0l    0w     0c https://example.com/admin -> /login
200  GET     1l    1w    28c https://example.com/api/health
200  GET    52l  180w  3200c https://example.com/docs
403  GET     7l   10w   162c https://example.com/server-status
200  GET     5l   12w   198c https://example.com/robots.txt
200  GET    18l   45w   780c https://example.com/sitemap.xml
200  GET     3l    8w    92c https://example.com/.well-known/security.txt
```

**Interesting Findings:**
- `/admin` and `/dashboard` redirect to `/login` (authentication required)
- `/api/health` returns health check data (information disclosure)
- `/server-status` returns 403 (Apache mod_status may be accessible from internal network)
- `/robots.txt` present -- check for disallowed paths
- `security.txt` present -- review for responsible disclosure info

---

## robots.txt Content

```
$ curl https://example.com/robots.txt

User-agent: *
Disallow: /admin/
Disallow: /api/internal/
Disallow: /debug/
Disallow: /backup/
Disallow: /staging-old/
Sitemap: https://example.com/sitemap.xml
```

**Note:** `/api/internal/`, `/debug/`, `/backup/`, and `/staging-old/` are explicitly hidden -- these should be tested.

---

## Security Headers

```
$ curl -s -I https://example.com

HTTP/2 200
server: nginx/1.24.0
content-type: text/html; charset=utf-8
x-powered-by: Express
strict-transport-security: max-age=31536000
x-content-type-options: nosniff
x-frame-options: SAMEORIGIN
x-request-id: 7b2f4c8e-1a3d-4f5b-9c8e-2d1f6a7b3c4e
content-security-policy: default-src 'self'; script-src 'self' https://cdn.example.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;
referrer-policy: strict-origin-when-cross-origin
```

**Header Assessment:**
| Header | Value | Rating |
|---|---|---|
| HSTS | max-age=31536000 | Good (missing includeSubdomains and preload) |
| X-Content-Type-Options | nosniff | Good |
| X-Frame-Options | SAMEORIGIN | Good |
| CSP | Present | Moderate (script-src allows CDN, style-src has unsafe-inline) |
| Referrer-Policy | strict-origin-when-cross-origin | Good |
| X-Powered-By | Express | Bad (information disclosure -- should be removed) |
| Server | nginx/1.24.0 | Bad (version disclosure -- should be removed) |

---

## OSINT Findings

### Public Code Repositories
- GitHub organization found: `github.com/example-corp`
- 12 public repositories including `example-api`, `example-frontend`, `example-deploy`
- `.env.example` file in `example-api` reveals database connection format and variable names
- Commit by developer "jsmith" includes AWS region reference (`us-east-1`)

### Employee Information
- 45 employees identified on LinkedIn
- Technology team: 12 engineers, 3 DevOps, 2 security
- Email format confirmed: `first.last@example.com`
- CTO publicly discusses tech stack in blog posts and conference talks

### Certificate Transparency
- Wildcard certificate covers all subdomains
- Historical certificates reveal previously used subdomains: `beta.example.com`, `legacy-api.example.com`

---

## Summary and Priority Targets

| Priority | Target | Reason |
|---|---|---|
| 1 | `api.example.com` | Primary API -- authentication, authorization, business logic testing |
| 2 | `app.example.com` | Main web application -- OWASP Top 10 |
| 3 | `staging.example.com` | Staging environment -- often has weaker controls |
| 4 | `jenkins.example.com` | CI/CD -- if accessible, potential for code execution |
| 5 | Port 8080 (Tomcat) | Default page visible -- check for manager access |
| 6 | `dev.example.com` | Development environment -- may expose debug endpoints |
| 7 | `git.example.com` | Source code -- if accessible, major information disclosure |
