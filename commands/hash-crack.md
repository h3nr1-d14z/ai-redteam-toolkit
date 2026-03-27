Crack hashes: $ARGUMENTS

1. **Identify hash type**: Determine algorithm from format/length — MD5, SHA1, SHA256, NTLM, bcrypt, NTLMv2, Kerberos
2. **Hashcat mode**: Map to hashcat mode (-m) — 0:MD5, 100:SHA1, 1000:NTLM, 1800:sha512crypt, 3200:bcrypt, 13100:Kerberoast
3. **Wordlist attack**: Run with rockyou.txt, SecLists common passwords, target-specific wordlists
4. **Rule-based**: Apply rules (best64, dive, OneRuleToRuleThemAll) for mutation-based cracking
5. **Mask attack**: If patterns known, use mask attack (e.g., ?u?l?l?l?d?d?d?d for Password1234)
6. **Combination**: Combine wordlists, append/prepend common patterns (years, seasons, company name)
7. **Results**: Document cracked passwords, pattern analysis, and password policy recommendations

Tools: hashcat, john (John the Ripper), hashid, haiti
Save cracked results to `engagements/<target>/findings/cracked-hashes.md`
