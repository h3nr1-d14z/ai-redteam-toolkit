Generate shellcode for: $ARGUMENTS

1. **Requirements**: Define target arch (x86/x64/ARM), OS, bad characters, size constraints
2. **Technique selection**: Determine approach — syscall-based, egg hunter, staged, polymorphic
3. **Write assembly**: Hand-craft shellcode in NASM/GAS syntax for desired action (reverse shell, bind shell, exec)
4. **Eliminate bad chars**: Encode or restructure to avoid null bytes, newlines, or other restricted characters
5. **Encode**: Apply XOR encoding, alphanumeric encoding, or custom encoder if needed
6. **Extract bytes**: Compile and extract raw bytes, format as Python/C byte string
7. **Test**: Verify execution in controlled environment (shellcode runner, debugger)

Tools: nasm, msfvenom (reference), pwntools shellcraft, ndisasm, strace
Save to `exploitation/shellcode/<arch>-<function>.asm` with compiled bytes
