Run comprehensive reconnaissance on the target: $ARGUMENTS

Perform in parallel:
1. DNS enumeration (A, AAAA, MX, TXT, NS, CNAME)
2. HTTP header analysis (server, security headers, cookies, tech stack)
3. Subdomain brute force (api, admin, dev, staging, cdn, mail, dashboard, etc.)
4. Common path enumeration (robots.txt, sitemap.xml, .env, .git/HEAD, admin, swagger)
5. SSL/TLS analysis (cert details, TLS versions, weak ciphers)
6. WHOIS and reverse IP lookup
7. Port scan (21, 22, 80, 443, 3000, 3306, 5432, 6379, 8000, 8080, 9090, 9200)

Save results to `engagements/<domain>/recon/initial-recon.md` with structured tables.
