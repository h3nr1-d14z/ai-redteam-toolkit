Perform active reconnaissance on: $ARGUMENTS

1. **Port scan**: Full TCP scan with service version detection on discovered hosts
2. **Service enumeration**: Banner grabbing, protocol identification, version fingerprinting
3. **Web crawling**: Spider the application, discover endpoints, map parameters and forms
4. **Directory bruteforce**: Common paths, backup files (.bak, .old, .swp), config files
5. **Virtual host discovery**: Test for vhost routing with different Host headers
6. **WAF detection**: Identify WAF/IPS (wafw00f), test bypass techniques
7. **Tech fingerprint**: Wappalyzer-style detection — frameworks, CMS, JS libraries, server software

Tools: nmap, gobuster/feroxbuster, whatweb, wafw00f, httpx
Save results to `engagements/<domain>/recon/active-recon.md`
