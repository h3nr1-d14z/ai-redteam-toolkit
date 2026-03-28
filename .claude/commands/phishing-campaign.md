Design phishing campaign for: $ARGUMENTS

1. **Reconnaissance**: Gather employee emails, org chart, email format, recent company events/communications
2. **Pretext development**: Design believable scenario — IT notification, HR update, vendor communication, executive request
3. **Infrastructure**: Set up sending domain (lookalike), configure SPF/DKIM/DMARC, set up landing page
4. **Payload selection**: Choose payload type — credential harvester, macro document, HTA, HTML smuggling, QR code
5. **Email crafting**: Write email with proper formatting, branding, urgency triggers, call to action
6. **Evasion**: Test against email security (SPF alignment, reputation, link scanning, sandbox evasion)
7. **Tracking**: Set up open/click tracking, unique tokens per recipient, callback monitoring
8. **Launch and monitor**: Send in waves, monitor results, document success rate

Tools: GoPhish, Evilginx2, custom landing pages
Save to `engagements/<target>/reports/phishing-campaign-<date>.md`
