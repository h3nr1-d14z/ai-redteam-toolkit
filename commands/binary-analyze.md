Perform binary analysis on: $ARGUMENTS

1. **Triage**: File type (file/rabin2), architecture, endianness, compiler, linked libraries
2. **Protections**: Check NX, ASLR/PIE, stack canaries, RELRO, Fortify, stripped symbols (checksec)
3. **Strings**: Extract and categorize strings — URLs, paths, error messages, format strings, crypto constants
4. **Imports/Exports**: Map external function calls, identify dangerous functions (strcpy, gets, sprintf, system)
5. **Control flow**: Identify main, entry points, interesting functions, cross-references to critical calls
6. **Vulnerability hunting**: Find buffer overflows, format strings, integer overflows, use-after-free patterns
7. **Struct reconstruction**: Identify data structures, vtables, object layouts from access patterns

Tools: Ghidra, radare2, checksec, strings, objdump, ltrace/strace
Save analysis to `re/binaries/<name>/analysis.md`
