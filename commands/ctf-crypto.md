Solve crypto CTF challenge: $ARGUMENTS

1. **Identify cipher**: Determine crypto system — RSA, AES, DES, XOR, custom, hash-based, elliptic curve
2. **Known attacks**:
   - RSA: small e, common modulus, Wiener, Hastad, Franklin-Reiter, Coppersmith, factorization (factordb)
   - AES: ECB block manipulation, CBC padding oracle, bit flipping, IV reuse
   - XOR: known plaintext, frequency analysis, key reuse
   - Hash: length extension, collision, rainbow tables
3. **Implementation flaws**: Weak RNG, nonce reuse, timing side channels, padding oracle
4. **Math**: Use SageMath/SymPy for modular arithmetic, lattice attacks, polynomial roots
5. **Brute force**: If keyspace is small, enumerate possibilities
6. **Solve**: Decrypt/forge/break the challenge
7. **Writeup**: Explain the mathematical flaw and exploitation

Tools: SageMath, pycryptodome, RsaCtfTool, hashcat, CyberChef
Save to `ctf/<platform>/<challenge>/`
