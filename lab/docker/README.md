# Docker Lab Environment

## Overview

This Docker Compose configuration sets up three intentionally vulnerable web applications for security testing practice.

| Application | URL | Description |
|---|---|---|
| DVWA | http://localhost:8081 | Classic PHP/MySQL vulnerable app |
| Juice Shop | http://localhost:3000 | Modern JavaScript vulnerable app |
| WebGoat | http://localhost:8080/WebGoat | Guided Java security lessons |
| WebWolf | http://localhost:9090 | Attacker simulation tool (WebGoat companion) |

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2+
- At least 4 GB of available RAM
- At least 5 GB of available disk space

## Quick Start

```bash
# Start all services
docker compose up -d

# Verify all containers are running
docker compose ps

# View logs
docker compose logs -f

# Stop all services
docker compose down

# Stop and remove all data (fresh start)
docker compose down -v
```

## Application Setup

### DVWA (Damn Vulnerable Web Application)

1. Browse to http://localhost:8081
2. Login with `admin` / `password`
3. Click "Create / Reset Database" on the setup page
4. Login again with `admin` / `password`
5. Set the security level via "DVWA Security" in the sidebar
   - Low: no protections (learn the vulnerability)
   - Medium: some protections (learn bypass techniques)
   - High: strong protections (advanced bypass)
   - Impossible: properly secured (see the correct implementation)

**Covers:** SQL Injection, XSS (Reflected, Stored, DOM), Command Injection, CSRF, File Inclusion, File Upload, Brute Force, Weak Session IDs, Insecure CAPTCHA

### OWASP Juice Shop

1. Browse to http://localhost:3000
2. Register a new account (or use the API)
3. Start solving challenges (they are discovered by exploring the application)
4. Access the scoreboard: http://localhost:3000/#/score-board
5. Each challenge has a difficulty rating (1-6 stars)

**Covers:** Injection, Broken Authentication, Sensitive Data Exposure, XXE, Broken Access Control, Security Misconfiguration, XSS, Insecure Deserialization, Using Components with Known Vulnerabilities, Insufficient Logging

### OWASP WebGoat

1. Browse to http://localhost:8080/WebGoat
2. Register a new account
3. Follow the guided lessons in order
4. Use WebWolf (http://localhost:9090) as an attacker mailbox and file server for certain lessons

**Covers:** Guided lessons on SQL Injection, Path Traversal, Authentication Bypass, JWT, XXE, SSRF, Client-Side attacks, Cryptography, and more. Each lesson explains the vulnerability and provides a hands-on exercise.

## Network Isolation

All containers run on an isolated Docker bridge network (`172.20.0.0/24`). They cannot access your host network services unless explicitly configured.

**Do NOT expose these services to the internet or any untrusted network.**

## Troubleshooting

```bash
# Container won't start - check logs
docker compose logs dvwa
docker compose logs juice-shop
docker compose logs webgoat

# Port already in use - change port mapping in docker-compose.yml
# Example: change "8081:80" to "9081:80"

# DVWA database error - reset the database
docker compose down -v
docker compose up -d
# Then click "Create / Reset Database" in DVWA setup page

# Out of disk space
docker system prune -a    # WARNING: removes all unused Docker data

# Check resource usage
docker stats
```

## Recommended Testing Tools

Use these tools against the lab applications for practice:

- **Burp Suite Community/Pro** -- proxy and web testing
- **OWASP ZAP** -- free alternative to Burp Suite
- **sqlmap** -- automated SQL injection
- **Nikto** -- web server scanner
- **ffuf/gobuster** -- directory brute-forcing
- **Nuclei** -- vulnerability scanner
- **curl** -- manual HTTP requests
- **Browser DevTools** -- inspect network traffic, DOM, storage
