Analyze memory dump: $ARGUMENTS

1. **Profile identification**: Determine OS and version (Volatility imageinfo/kdbgscan or Volatility3 auto-detect)
2. **Process analysis**: List processes (pslist, pstree, psscan), identify suspicious processes, hidden/injected processes
3. **Network**: Extract network connections (netscan), identify C2 callbacks, lateral movement connections
4. **Code injection**: Check for injected code (malfind), hollowed processes, reflective DLL injection
5. **Credentials**: Extract password hashes (hashdump), cached credentials, Kerberos tickets, LSA secrets
6. **File extraction**: Dump suspicious executables, DLLs, loaded drivers for further analysis
7. **Registry/handles**: Analyze registry hives, open handles, mutexes for persistence and IOCs

Tools: Volatility3 (preferred) or Volatility2, strings, YARA
Save to `engagements/<target>/findings/memory-forensics.md`
