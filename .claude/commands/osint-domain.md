Perform OSINT investigation on domain: $ARGUMENTS

1. **Registration**: WHOIS (current and historical), registrar, creation date, nameservers, registrant info
2. **DNS history**: Historical DNS records, subdomain enumeration, zone transfer attempts
3. **Certificate transparency**: Search crt.sh for all issued certificates, discover subdomains and internal names
4. **Web archive**: Wayback Machine snapshots, find old pages, removed content, previous tech stacks
5. **Technology**: Identify hosting provider, CDN, CMS, frameworks, analytics IDs, ad networks
6. **Reputation**: Check blacklists, spam databases, malware databases, VirusTotal
7. **Related domains**: Find domains sharing same analytics ID, registrant, IP, nameserver

Tools: whois, dig, crt.sh, Wayback Machine, SecurityTrails, BuiltWith
Save to `engagements/<target>/recon/osint-domain-<domain>.md`
