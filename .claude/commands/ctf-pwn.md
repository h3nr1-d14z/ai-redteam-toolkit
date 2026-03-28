Solve pwn/binary exploitation CTF challenge: $ARGUMENTS

1. **Recon**: file, checksec (NX, PIE, canary, RELRO), strings, ltrace/strace for behavior
2. **Vulnerability**: Find the bug — buffer overflow, format string, use-after-free, integer overflow, heap corruption
3. **Offset**: Calculate offset to control EIP/RIP using cyclic pattern
4. **Exploit strategy**: Based on protections:
   - No NX: ret2shellcode
   - NX only: ret2libc, ROP chain
   - NX+PIE: info leak first, then ROP
   - Full RELRO+PIE+canary: leak canary + PIE base, then ROP
5. **Payload**: Build exploit with pwntools — handle remote/local, payload generation, shell interaction
6. **Get flag**: Exploit remote service, cat flag
7. **Writeup**: Document vulnerability, exploitation technique, and key takeaways

Tools: pwntools, GDB+pwndbg/GEF, ROPgadget, one_gadget, checksec
Save to `ctf/<platform>/<challenge>/`
