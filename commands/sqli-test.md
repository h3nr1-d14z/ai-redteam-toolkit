Run SQL injection testing on: $ARGUMENTS

1. **Identify injection points**: Crawl target, find parameters (GET/POST/Cookie/Header)
2. **Test manually**: Single quote, boolean-based, UNION-based, time-based payloads
3. **Automate**: Run sqlmap with appropriate tamper scripts for WAF bypass
4. **Extract data**: Enumerate databases, tables, columns if injectable
5. **Escalate**: Test for OS command execution (xp_cmdshell, LOAD_FILE), file read/write (INTO OUTFILE)
6. **Second-order**: Test stored input that gets used in later SQL queries
7. **Document**: Save findings to `engagements/<target>/findings/sqli-*.md` with CVSS score

Tools: sqlmap, Burp Suite, manual testing
Output: engagements/<target>/findings/
