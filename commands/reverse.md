Reverse engineer: $ARGUMENTS

## Pre-flight
- Identify file type: `file <path>`, `binwalk <path>`
- Check architecture: x86, x64, ARM, MIPS
- Identify protections: stripped, PIE, NX, ASLR, canary, packed
- For APK: use `python3 tools/mobile/apk-analyzer.py <file>`
- For Unity IL2CPP: use `python3 tools/re/il2cpp-extractor.py <metadata>`

## Phase 1: Static Analysis
- Strings: `strings -n 6 <binary>` — look for URLs, keys, error messages
- Imports/exports: identify libraries and API calls
- Disassemble key functions in Ghidra (use GhidraMCP if available)
- For .NET/Java: decompile with jadx/dnSpy/ILSpy
- For JavaScript: beautify + deobfuscate

## Phase 2: Dynamic Analysis
- Set breakpoints at key functions (entry, auth, crypto, network)
- Trace system calls: strace/ltrace (Linux), procmon (Windows)
- Monitor network: Wireshark for protocol analysis
- Hook functions: Frida for runtime modification
- Memory analysis: examine heap/stack for secrets

## Phase 3: Documentation
- Map program flow and key functions
- Document findings: hardcoded secrets, vulnerabilities, backdoors
- Create scripts for automation (Ghidra scripts, Frida hooks)

## Output
Save to engagements/<target>/analysis.md with: overview, key findings, function map, scripts/

## Tools (with fallbacks)
Disassembler: Ghidra (+ MCP) > radare2 > objdump
Decompiler: Ghidra > RetDec > r2 pdg
Strings: strings > rabin2 > FLOSS
Dynamic: GDB (+ pwndbg) > lldb > strace
Hooking: Frida > DLL injection > LD_PRELOAD

## Safety
Analyze in isolated VM/sandbox. Never execute unknown binaries on host.
Reference: methodology/binary-re.md
