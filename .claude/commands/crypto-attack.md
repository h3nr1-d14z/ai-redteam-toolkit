Analyze cryptographic implementation on: $ARGUMENTS

## Pre-flight
- Identify crypto usage: TLS, password hashing, file encryption, key exchange
- Determine algorithms and key sizes in use

## Phase 1: TLS/SSL Analysis
1. Test TLS versions: nmap --script ssl-enum-ciphers <target>
2. Check for SSLv3, TLS 1.0/1.1 (deprecated)
3. Test cipher suites: weak ciphers (RC4, DES, NULL, EXPORT)
4. Certificate validation: expiry, chain, self-signed, wildcard
5. Check HSTS, certificate pinning

## Phase 2: Password Storage
1. Identify hashing algorithm (MD5, SHA1, SHA256, bcrypt, scrypt, Argon2)
2. Check for salting
3. Test rainbow table attacks on weak hashes
4. Crack with hashcat: /hash-crack with appropriate mode
5. Reference: cheatsheets/hashcat.md

## Phase 3: Encryption Flaws
1. ECB mode detection: identical plaintext blocks → identical ciphertext
2. Padding oracle: test for CBC padding oracle attacks (POODLE-style)
3. Key reuse: same key for multiple purposes
4. Weak random: predictable IVs, nonces, or keys
5. Hardcoded keys: search source code for encryption keys

## Phase 4: Protocol-Level
1. Downgrade attacks: force weaker protocol version
2. BEAST, CRIME, BREACH, POODLE attack checks
3. Key exchange: DHE/ECDHE vs static DH
4. Perfect forward secrecy: verify PFS support
5. Certificate transparency: check CT logs

## Tools
nmap ssl-enum-ciphers, testssl.sh, sslyze, hashcat, john, openssl

## Output
Save to engagements/<target>/findings/crypto-*.md
Reference: CEH Module 20 — Cryptography
