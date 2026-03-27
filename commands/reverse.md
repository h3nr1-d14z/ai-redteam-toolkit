Reverse engineer: $ARGUMENTS

1. **Triage**: file type, architecture, protections (stripped, PIE, NX, packed)
2. **Static analysis**: strings, imports/exports, disassembly of key functions
3. **Dynamic analysis**: breakpoints, syscall tracing, network monitoring, Frida hooks
4. **Document**: save to `re/<category>/<name>/analysis.md`

For APK: decompile with jadx, analyze manifest, find secrets/endpoints.
For .NET/Java: decompile, analyze IL/bytecode.
For JS: deobfuscate, map API calls.
For binaries: Ghidra/radare2 analysis, struct reconstruction.
