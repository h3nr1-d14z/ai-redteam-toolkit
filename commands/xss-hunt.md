Hunt for XSS vulnerabilities on: $ARGUMENTS

1. **Map reflection points**: Find all parameters reflected in response (URL params, POST body, headers, cookies)
2. **Context analysis**: Determine injection context — HTML body, attribute, JavaScript, URL, CSS
3. **Filter testing**: Test WAF/filter bypass — encoding (HTML entities, URL, Unicode, hex), case variation, tag alternatives
4. **Stored XSS**: Test all user input that is stored and displayed (comments, profiles, filenames, metadata)
5. **DOM XSS**: Analyze JS sources (location, document.referrer, postMessage) and sinks (innerHTML, eval, document.write)
6. **Payloads**: Context-specific payloads — event handlers, SVG, MathML, template literals, prototype pollution to XSS
7. **Impact**: Demonstrate session hijack, keylogging, phishing overlay, or data exfiltration

Tools: Burp Suite, dalfox, XSStrike, browser DevTools
Save findings to `engagements/<target>/findings/xss-*.md` with CVSS score and PoC.
