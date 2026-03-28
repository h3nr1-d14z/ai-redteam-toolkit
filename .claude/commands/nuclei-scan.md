Run Nuclei vulnerability scan against: $ARGUMENTS

1. **Template selection**: Choose relevant templates — CVEs, exposures, misconfigurations, default-logins, technologies
2. **Configure scope**: Set target URLs, rate limiting, concurrency, timeout, and header customization
3. **Run scan**: Execute nuclei with selected templates, capture output in JSON and markdown
4. **Filter results**: Remove false positives, validate critical/high findings manually
5. **Categorize**: Group findings by severity, type, and affected component
6. **Enrich**: Add context to findings — affected endpoint, impact, remediation advice
7. **Save**: Export validated results to structured format

Command: nuclei -u <target> -severity critical,high,medium -json -o results.json
Save to `engagements/<target>/recon/nuclei-scan-<date>.md`
