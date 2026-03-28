Enumerate subdomains for: $ARGUMENTS

1. **Passive sources**: crt.sh, SecurityTrails, VirusTotal, Amass passive, subfinder
2. **DNS bruteforce**: Common wordlist (api, admin, dev, staging, cdn, mail, vpn, git, ci, jenkins, grafana, kibana)
3. **Permutations**: Generate permutations of discovered subdomains (dev-api, api-dev, api2, api-v2)
4. **Resolution**: Resolve all discovered subdomains, identify live hosts, check HTTP/HTTPS response
5. **Categorize**: Group by purpose (web apps, mail, APIs, internal tools, CDN, cloud services)
6. **Screenshot**: Capture HTTP response headers and page titles for each live subdomain
7. **Cloud check**: Identify cloud-hosted subdomains (AWS, GCP, Azure) and test for subdomain takeover

Tools: subfinder, amass, httpx, nuclei (takeover templates)
Save results to `engagements/<domain>/recon/subdomains.md`
