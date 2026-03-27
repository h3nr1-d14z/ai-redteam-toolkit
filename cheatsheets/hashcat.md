# Hashcat Cheatsheet

## Basic Usage
```bash
# Basic attack
hashcat -m <mode> -a <attack_type> hashes.txt wordlist.txt

# Show cracked hashes
hashcat -m <mode> hashes.txt --show

# Restore interrupted session
hashcat --restore

# Benchmark all hash modes
hashcat -b

# Benchmark specific mode
hashcat -b -m 1000
```

## Common Hash Modes (-m)
```
0       MD5
100     SHA-1
1400    SHA-256
1700    SHA-512
900     MD4
10      md5($pass.$salt)
20      md5($salt.$pass)
3200    bcrypt
1800    sha512crypt ($6$)
500     md5crypt ($1$)
7400    sha256crypt ($5$)
1000    NTLM
3000    LM
5600    NetNTLMv2
5500    NetNTLMv1
13100   Kerberos 5 TGS-REP (Kerberoast)
18200   Kerberos 5 AS-REP (AS-REP Roast)
7500    Kerberos 5 AS-REQ Pre-Auth (etype 23)
22000   WPA-PBKDF2-PMKID+EAPOL (WiFi)
16500   JWT (HMAC-SHA256)
11300   Bitcoin/Litecoin wallet
15700   Ethereum wallet (PBKDF2)
1500    DES (Unix)
6900    GOST R 34.11-94
10900   PBKDF2-SHA256
12500   RAR3
13000   RAR5
11600   7-Zip
17200   PKZIP (Compressed)
13400   KeePass
9400    MS Office 2007
9500    MS Office 2010
9600    MS Office 2013
2611    vBulletin < 3.8.5
400     WordPress (phpass)
7900    Drupal7
121     SMF > v1.1
```

## Attack Types (-a)
```bash
# Dictionary attack
hashcat -m 0 -a 0 hashes.txt wordlist.txt

# Dictionary with rules
hashcat -m 0 -a 0 hashes.txt wordlist.txt -r rules/best64.rule

# Combination attack (word1 + word2)
hashcat -m 0 -a 1 hashes.txt wordlist1.txt wordlist2.txt

# Brute-force / mask attack
hashcat -m 0 -a 3 hashes.txt ?a?a?a?a?a?a

# Hybrid: wordlist + mask
hashcat -m 0 -a 6 hashes.txt wordlist.txt ?d?d?d?d    # word + 4 digits
hashcat -m 0 -a 7 hashes.txt ?d?d?d?d wordlist.txt    # 4 digits + word
```

## Mask Charsets
```
?l    Lowercase a-z
?u    Uppercase A-Z
?d    Digits 0-9
?s    Special characters (space !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
?a    All printable (?l?u?d?s)
?b    0x00-0xff (all bytes)

# Custom charsets
-1 ?l?d         Define charset 1 as lowercase + digits
-2 ?u?l         Define charset 2 as upper + lower
hashcat -m 0 -a 3 -1 ?l?d hashes.txt ?1?1?1?1?1?1?1?1

# Examples
?u?l?l?l?l?d?d?d?d          # Ullllddddd (Password1234)
?u?l?l?l?l?l?l?d?d?s        # Ulllllldd! (Password12!)
?d?d?d?d?d?d                 # 6-digit PIN
```

## Rules
```bash
# Built-in rules
hashcat -m 0 -a 0 hashes.txt wordlist.txt -r /usr/share/hashcat/rules/best64.rule
hashcat -m 0 -a 0 hashes.txt wordlist.txt -r /usr/share/hashcat/rules/rockyou-30000.rule
hashcat -m 0 -a 0 hashes.txt wordlist.txt -r /usr/share/hashcat/rules/d3ad0ne.rule
hashcat -m 0 -a 0 hashes.txt wordlist.txt -r /usr/share/hashcat/rules/dive.rule
hashcat -m 0 -a 0 hashes.txt wordlist.txt -r /usr/share/hashcat/rules/OneRuleToRuleThemAll.rule

# Multiple rules (chained)
hashcat -m 0 -a 0 hashes.txt wordlist.txt -r rule1.rule -r rule2.rule

# Common rule functions
:       Do nothing (passthrough)
l       Lowercase all
u       Uppercase all
c       Capitalize first, lowercase rest
t       Toggle case of all characters
$X      Append character X
^X      Prepend character X
d       Duplicate word (wordword)
r       Reverse word
sa@     Replace 'a' with '@'
se3     Replace 'e' with '3'
si1     Replace 'i' with '1'
so0     Replace 'o' with '0'
ss$     Replace 's' with '$'

# Example rule file (rules.txt)
:
c
u
c$1
c$1$!
c$1$2$3
sa@
se3so0
c$!
$2$0$2$4
```

## Performance Options
```bash
# Force device type
hashcat -D 1              # CPU only
hashcat -D 2              # GPU only

# Specific device
hashcat -d 1              # Use device 1

# Workload profiles
hashcat -w 1              # Low (desktop usable)
hashcat -w 2              # Default
hashcat -w 3              # High (dedicated cracking)
hashcat -w 4              # Nightmare (may crash)

# Optimized kernels
hashcat -O                # Optimized (limits password length to 32)

# Temperature limit
hashcat --hwmon-temp-abort=100
```

## Useful Options
```bash
# Output cracked to file
hashcat -m 0 hashes.txt wordlist.txt -o cracked.txt

# Output format
hashcat -m 0 hashes.txt wordlist.txt -o cracked.txt --outfile-format=2
# 1 = hash[:salt]
# 2 = plain
# 3 = hash[:salt]:plain
# 5 = hash[:salt]:plain:hex_plain

# Skip and limit (resume position)
hashcat -m 0 -a 3 hashes.txt ?a?a?a?a --skip 1000000 --limit 2000000

# Increment mode (try length 1, then 2, then 3...)
hashcat -m 0 -a 3 hashes.txt ?a?a?a?a?a?a?a?a --increment --increment-min 4 --increment-max 8

# Username in hash file (user:hash)
hashcat -m 0 hashes.txt wordlist.txt --username

# Potfile (disable or custom)
hashcat -m 0 hashes.txt wordlist.txt --potfile-disable
hashcat -m 0 hashes.txt wordlist.txt --potfile-path custom.pot

# Session name
hashcat -m 0 hashes.txt wordlist.txt --session mysession
hashcat --session mysession --restore
```

## Hash Identification
```bash
# Tools to identify hash type
hashid "5f4dcc3b5aa765d61d8327deb882cf99"
hash-identifier
hashcat --identify hash.txt
nth (Name-That-Hash): nth -t "hash_value"
```

## Common Attack Patterns
```bash
# Quick dictionary attack
hashcat -m 0 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt -O

# Dictionary with best rules
hashcat -m 0 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule -O

# Kerberoast
hashcat -m 13100 -a 0 kerberoast.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# AS-REP Roast
hashcat -m 18200 -a 0 asrep.txt /usr/share/wordlists/rockyou.txt

# NTLM hashes
hashcat -m 1000 -a 0 ntlm.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# NetNTLMv2
hashcat -m 5600 -a 0 netntlmv2.txt /usr/share/wordlists/rockyou.txt

# WiFi WPA
hashcat -m 22000 -a 0 handshake.hc22000 /usr/share/wordlists/rockyou.txt

# JWT secret
hashcat -m 16500 -a 0 jwt.txt /usr/share/wordlists/rockyou.txt

# bcrypt (slow -- use small wordlist with rules)
hashcat -m 3200 -a 0 bcrypt.txt /usr/share/wordlists/rockyou.txt -w 3
```
