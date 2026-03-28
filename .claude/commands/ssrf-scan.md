Exploit SSRF via: $ARGUMENTS

Identify SSRF endpoint.
Test schemes: http, https, file, gopher, dict.
Cloud metadata: AWS 169.254.169.254, GCP metadata.google.internal.
Internal scan: Docker ranges (172.17.0.x), localhost ports.
Use wordlists/ssrf/targets.txt.
Test bypasses: DNS rebinding, URL encoding, redirect chains, IPv6.
Exfiltrate: /proc/self/environ, /metrics, Prometheus, internal APIs.
Reference: cheatsheets for common ports.
Output: engagements/<target>/findings/ssrf-*.md

## Safety
Verify authorization and scope before proceeding. Document all actions.
