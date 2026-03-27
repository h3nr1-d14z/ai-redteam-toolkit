# ffuf Cheatsheet

## Directory and File Brute-Forcing
```bash
# Basic directory brute-force
ffuf -u https://target.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt

# With extensions
ffuf -u https://target.com/FUZZ -w wordlist.txt -e .php,.html,.txt,.bak,.asp,.aspx,.jsp

# Recursive scanning
ffuf -u https://target.com/FUZZ -w wordlist.txt -recursion -recursion-depth 3

# With authentication
ffuf -u https://target.com/FUZZ -w wordlist.txt -H "Cookie: session=abc123"
ffuf -u https://target.com/FUZZ -w wordlist.txt -H "Authorization: Bearer token"
```

## Filtering Responses
```bash
# Filter by status code
ffuf -u https://target.com/FUZZ -w wordlist.txt -mc 200,301,302     # Match codes
ffuf -u https://target.com/FUZZ -w wordlist.txt -fc 404,403          # Filter codes

# Filter by response size
ffuf -u https://target.com/FUZZ -w wordlist.txt -fs 4242             # Filter exact size
ffuf -u https://target.com/FUZZ -w wordlist.txt -ms 0-100            # Match size range

# Filter by word count
ffuf -u https://target.com/FUZZ -w wordlist.txt -fw 12               # Filter word count

# Filter by line count
ffuf -u https://target.com/FUZZ -w wordlist.txt -fl 5                # Filter line count

# Filter by regex in response
ffuf -u https://target.com/FUZZ -w wordlist.txt -fr "not found|error"

# Auto-calibrate filter (detect default response and filter it)
ffuf -u https://target.com/FUZZ -w wordlist.txt -ac
```

## Parameter Fuzzing
```bash
# GET parameter name fuzzing
ffuf -u "https://target.com/page?FUZZ=test" -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -fs 4242

# GET parameter value fuzzing
ffuf -u "https://target.com/page?id=FUZZ" -w numbers.txt

# POST parameter fuzzing
ffuf -u https://target.com/login -X POST -d "username=admin&password=FUZZ" -w passwords.txt -H "Content-Type: application/x-www-form-urlencoded"

# JSON body fuzzing
ffuf -u https://target.com/api/login -X POST -d '{"user":"admin","pass":"FUZZ"}' -w passwords.txt -H "Content-Type: application/json"

# Header value fuzzing
ffuf -u https://target.com/ -H "X-Forwarded-For: FUZZ" -w ips.txt
```

## Virtual Host / Subdomain Discovery
```bash
# Virtual host fuzzing
ffuf -u http://target.com -H "Host: FUZZ.target.com" -w subdomains.txt -fs 4242

# With HTTPS
ffuf -u https://target.com -H "Host: FUZZ.target.com" -w subdomains.txt -fs 4242

# Subdomain brute-force (DNS)
ffuf -u http://FUZZ.target.com -w subdomains.txt -fs 0
```

## Multiple Wordlists (Multi-Fuzz)
```bash
# Two FUZZ keywords (clusterbomb mode by default)
ffuf -u https://target.com/FUZZ1/FUZZ2 -w dirs.txt:FUZZ1 -w files.txt:FUZZ2

# Username:password brute-force (pitchfork mode)
ffuf -u https://target.com/login -X POST \
  -d "user=USER&pass=PASS" \
  -w users.txt:USER -w passwords.txt:PASS \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -mode pitchfork -fc 401

# Clusterbomb (all combinations)
ffuf -u https://target.com/login -X POST \
  -d "user=USER&pass=PASS" \
  -w users.txt:USER -w passwords.txt:PASS \
  -mode clusterbomb -fc 401
```

## Performance and Configuration
```bash
# Set threads
ffuf -u https://target.com/FUZZ -w wordlist.txt -t 100              # 100 threads

# Set rate limit
ffuf -u https://target.com/FUZZ -w wordlist.txt -rate 50             # 50 requests/sec

# Set timeout
ffuf -u https://target.com/FUZZ -w wordlist.txt -timeout 10          # 10 seconds

# Use proxy (Burp)
ffuf -u https://target.com/FUZZ -w wordlist.txt -x http://127.0.0.1:8080

# Custom User-Agent
ffuf -u https://target.com/FUZZ -w wordlist.txt -H "User-Agent: Mozilla/5.0"

# Follow redirects
ffuf -u https://target.com/FUZZ -w wordlist.txt -r

# Delay between requests
ffuf -u https://target.com/FUZZ -w wordlist.txt -p 0.1-0.5          # Random delay
```

## Output
```bash
# Output to file
ffuf -u https://target.com/FUZZ -w wordlist.txt -o results.json

# Output formats
ffuf -u https://target.com/FUZZ -w wordlist.txt -o results.json -of json
ffuf -u https://target.com/FUZZ -w wordlist.txt -o results.csv -of csv
ffuf -u https://target.com/FUZZ -w wordlist.txt -o results.html -of html
ffuf -u https://target.com/FUZZ -w wordlist.txt -o results.md -of md

# Silent mode (only results)
ffuf -u https://target.com/FUZZ -w wordlist.txt -s

# Verbose mode
ffuf -u https://target.com/FUZZ -w wordlist.txt -v

# Color output
ffuf -u https://target.com/FUZZ -w wordlist.txt -c
```

## Useful Wordlists
```
# SecLists paths
/usr/share/seclists/Discovery/Web-Content/common.txt
/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt
/usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt
/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
/usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt
/usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt
/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
/usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt
/usr/share/seclists/Usernames/top-usernames-shortlist.txt
/usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt
```

## Common Scan Profiles
```bash
# Quick directory scan
ffuf -u https://target.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc 200,301,302,403 -t 50 -c

# Thorough directory scan with extensions
ffuf -u https://target.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -e .php,.html,.txt,.bak,.old,.zip -mc 200,301,302 -t 100 -c

# API endpoint discovery
ffuf -u https://target.com/api/FUZZ -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt -mc 200,401,403,405 -t 50 -c

# Subdomain discovery
ffuf -u http://FUZZ.target.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -mc 200,301,302 -ac -t 100 -c

# Parameter discovery
ffuf -u "https://target.com/page?FUZZ=1" -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -ac -t 50 -c
```
