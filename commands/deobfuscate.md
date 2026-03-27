Deobfuscate code or binary: $ARGUMENTS

1. **Identify obfuscation**: Determine type — JavaScript (webpack/minified/packed), .NET (ConfuserEx, Dotfuscator), Java (ProGuard), binary packing (UPX, Themida)
2. **JavaScript**: Beautify, replace eval/Function with console.log, de-array string tables, resolve computed property access, reconstruct control flow
3. **.NET/Java**: Use dnSpy/de4dot for .NET, CFR/Procyon for Java, rename symbols, reconstruct types
4. **Binary unpacking**: Dump from memory at OEP, reconstruct IAT, fix PE headers
5. **String decryption**: Identify string decryption routines, write script to batch decrypt all strings
6. **Control flow**: Flatten switch-based obfuscation, remove opaque predicates, dead code
7. **Validate**: Compare deobfuscated output behavior with original

Tools: de4dot, dnSpy, CFR, js-beautify, AST manipulation, Ghidra scripting
Save cleaned output to `re/<category>/<name>/deobfuscated/`
