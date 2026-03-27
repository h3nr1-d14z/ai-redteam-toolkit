Perform passive reconnaissance on: $ARGUMENTS

1. **OSINT**: Search public sources for target info — company structure, tech stack, employee names, email patterns
2. **DNS passive**: Query crt.sh, SecurityTrails, VirusTotal for subdomains and certificate transparency logs
3. **Google dorking**: site:, inurl:, filetype:, intitle: searches for exposed files, login panels, error pages
4. **Archive**: Check Wayback Machine for old endpoints, deprecated APIs, removed pages
5. **GitHub/GitLab**: Search for leaked credentials, API keys, internal URLs, config files mentioning target
6. **Metadata**: Collect document metadata (FOCA/exiftool) from publicly available PDFs, docs, images
7. **Social media**: LinkedIn employee count, tech roles, job postings revealing stack info

Save results to `engagements/<domain>/recon/passive-recon.md`. No direct contact with target infrastructure.
