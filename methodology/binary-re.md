# Binary Reverse Engineering Methodology

## Phase 1: Triage and Initial Assessment

### File Identification
- `file binary` -- identify type (ELF, PE, Mach-O), architecture (x86, x64, ARM), linking
- `xxd binary | head -5` -- check magic bytes manually
- `rabin2 -I binary` -- comprehensive binary info (radare2)
- Check for packing/encryption: high entropy sections, known packer signatures

### Metadata Collection
- **PE (Windows):** `pestudio`, `CFF Explorer`, `dumpbin /headers binary.exe`
- **ELF (Linux):** `readelf -h binary`, `readelf -S binary` (sections), `readelf -l binary` (segments)
- **Mach-O (macOS):** `otool -h binary`, `otool -l binary`, `otool -L binary` (linked libraries)
- Note: architecture, bit width, endianness, compiler (if identifiable), build date

### Protection Assessment
| Protection | Check | Tool |
|---|---|---|
| Stripped symbols | `file binary` (stripped/not stripped) | `nm binary` (if not stripped) |
| PIE/ASLR | `readelf -h` (Type: DYN) or `checksec` | checksec, pwntools |
| Stack canaries | `checksec binary` | checksec |
| NX (DEP) | `checksec binary` | checksec |
| RELRO | `checksec binary` (Partial/Full) | checksec |
| Packing | High entropy, few imports, UPX/Themida signatures | Detect It Easy (DIE), pestudio |
| Obfuscation | Control flow flattening, junk code, opaque predicates | Manual analysis |

### Unpacking (if packed)
- UPX: `upx -d packed_binary -o unpacked_binary`
- Custom packers: run binary, dump from memory after unpacking
  - Linux: `gdb` -> break after unpacking routine -> `dump memory unpacked 0xstart 0xend`
  - Windows: x64dbg -> run to OEP (Original Entry Point) -> Scylla dump
- Detect It Easy: identify packer type for targeted unpacking

### String Extraction
- `strings -n 6 binary` -- printable strings (minimum length 6)
- `strings -e l binary` -- UTF-16 LE strings (common in Windows binaries)
- FLOSS: `floss binary` -- extract obfuscated/encrypted strings automatically
- Look for: error messages, debug strings, URLs, paths, format strings, function names, crypto constants

---

## Phase 2: Static Analysis

### Disassembly Setup
- **Ghidra:** create project, import binary, auto-analyze (select all analyzers)
- **IDA Pro:** load binary, select correct processor type, let auto-analysis complete
- **Binary Ninja:** open file, wait for analysis
- **radare2:** `r2 -A binary` (analyze all), `afl` (list functions)

### Function Identification
- Start at entry point: `_start` (ELF) or `_mainCRTStartup` (PE) leads to `main`
- Use cross-references (xrefs) to trace call graph from main
- Identify library functions: FLIRT signatures (IDA), Function ID (Ghidra), or by behavior
- Rename functions as you identify their purpose
- Tag functions by category: crypto, network, file I/O, string manipulation, validation

### Control Flow Analysis
- Follow the program flow from main through key decision points
- Identify conditional branches: what conditions lead to success/failure paths?
- Map loops: identify loop variables, bounds, exit conditions
- Document switch/case tables: often used for command processing, state machines

### Data Structure Recovery
- Identify structures from access patterns: `[base + offset]` accesses
- Map structure fields by tracking how data flows through functions
- Ghidra: use Data Type Manager to define structures, apply to variables
- Look for vtables to identify C++ class hierarchies
- Track heap allocations (`malloc`, `new`) to understand dynamic structure sizes

### Algorithm Identification
- Look for known constants:
  - SHA-256: `0x6a09e667`, `0xbb67ae85`, `0x3c6ef372`
  - AES: S-box values, Rcon array
  - MD5: `0x67452301`, `0xefcdab89`
  - CRC32: `0xEDB88320` (polynomial)
  - Base64: `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/`
- Tools: `signsrch` (signature search), `findcrypt` (IDA plugin), Ghidra's crypto analyzer
- Common patterns: XOR loop (simple encryption), substitution tables, bit rotation

### Import/Export Analysis
- List imports: `objdump -T binary` (dynamic), `objdump -t binary` (all)
- Categorize imports by purpose:
  - File I/O: `open`, `read`, `write`, `fopen`, `CreateFile`
  - Network: `socket`, `connect`, `send`, `recv`, `WSAStartup`
  - Crypto: `CryptEncrypt`, `EVP_*`, `AES_*`
  - Process: `fork`, `exec`, `CreateProcess`, `VirtualAlloc`
  - String: `strcmp`, `strlen`, `memcpy`, `strstr`
- Missing imports (packed binary) or unusual imports (anti-analysis)

---

## Phase 3: Dynamic Analysis

### Debugger Setup
- **Linux:** `gdb` with GEF, pwndbg, or PEDA: `gdb -q binary`
- **Windows:** x64dbg (user-mode), WinDbg (kernel-mode)
- **macOS:** `lldb binary`
- **Cross-platform:** radare2 `r2 -d binary`

### Breakpoint Strategy
- Break on `main` to start at program logic
- Break on interesting functions identified in static analysis
- Break on library calls: `b strcmp`, `b recv`, `b malloc`
- Hardware breakpoints on data: `watch *0xaddress` (break when memory is accessed)
- Conditional breakpoints: `b *0xaddr if $rax == 0x41414141`

### Execution Tracing
- Step through code: `si` (instruction), `s` (source line), `ni` (over calls)
- Record execution trace for later analysis
- `strace binary` (Linux): system call trace
- `ltrace binary` (Linux): library call trace
- Process Monitor (Windows): file, registry, network activity
- API Monitor (Windows): detailed API call logging with parameters

### Memory Inspection
- Examine memory at addresses: `x/20gx $rsp` (stack), `x/s 0xaddr` (string)
- Watch for memory corruption: buffer overflows, use-after-free, double-free
- Heap analysis: `heap` (GEF/pwndbg), examine chunk metadata
- Memory maps: `vmmap` (GEF), `info proc mappings` (GDB)

### Anti-Debug Bypass
- **Linux:** `ptrace(PTRACE_TRACEME)` check -- patch or set return value to 0
- **Windows:** `IsDebuggerPresent()` -- set EAX to 0 at return; `NtQueryInformationProcess` -- hook or patch
- **Timing checks:** `rdtsc`, `GetTickCount` -- NOP out or return consistent values
- **Exception-based:** INT 3 / INT 2D tricks -- handle in debugger
- **Self-debugging:** binary forks and traces itself -- kill the tracer process
- General: set breakpoint after the check and modify the result register

---

## Phase 4: Specialized Analysis

### Cryptographic Analysis
- Identify crypto algorithms from constants, patterns, or library calls
- Track key derivation: where does the key come from? Hardcoded, derived, user input?
- Track IV/nonce generation: is it random, static, predictable?
- Map encryption/decryption flow: what data is encrypted, when, and where is the result used?
- Check for weak crypto: ECB mode, DES, MD5 for integrity, hardcoded keys, short keys

### Network Protocol RE
- Capture traffic with Wireshark while running the binary under a debugger
- Correlate network sends with code: break on `send`/`recv`, examine buffers
- Map packet structures: header, length, type, payload
- Identify serialization: protobuf (varint encoding), JSON, custom binary
- Break on encryption functions to capture plaintext network data

### File Format RE
- Track file read operations: break on `fread`, `ReadFile`
- Observe how file data is parsed: header validation, field extraction
- Map the file format: magic bytes, version, offset table, data sections
- Build a parser/generator for the format
- Look for parsing vulnerabilities: integer overflows in length fields, buffer overflows

### Malware-Specific (if applicable)
- Run in isolated VM with snapshot capability
- Monitor with Process Monitor, Wireshark, FakeNet-NG (fake network services)
- Identify C2 communication: domains, IPs, protocols
- Extract configuration: decode embedded C2 addresses, encryption keys
- Identify capabilities: keylogging, screen capture, file exfiltration, persistence
- Extract IOCs: file hashes, network indicators, mutex names, registry keys

---

## Phase 5: Documentation

### Analysis Report
- Binary identification: name, hash (MD5, SHA256), type, architecture
- Executive summary: what does this binary do?
- Protection analysis: what protections are in place?
- Functional analysis: detailed description of key functionality
- Algorithm documentation: crypto, encoding, validation logic
- Data structures: recovered structures with field descriptions
- Network behavior: protocols, endpoints, data format
- File system behavior: files read, written, modified
- IOCs (if malware): hashes, network indicators, file artifacts

### Artifact Preservation
- Save annotated IDB/Ghidra project with renamed functions and structures
- Export function list with addresses and descriptions
- Save decompiled pseudocode for key functions
- Document pointer chains and structure layouts
- Save debugger scripts for reproducibility

---

## Tools Quick Reference

| Task | Tools |
|---|---|
| Triage | file, readelf, otool, Detect It Easy, pestudio |
| Disassembly | Ghidra, IDA Pro, Binary Ninja, radare2 |
| Debugging (Linux) | GDB + GEF/pwndbg, radare2 |
| Debugging (Windows) | x64dbg, WinDbg |
| Debugging (macOS) | lldb |
| .NET | dnSpy, ILSpy, dotPeek |
| Java | jadx, JD-GUI, Procyon, CFR |
| Strings | strings, FLOSS |
| Crypto | signsrch, findcrypt (IDA), Ghidra crypto analyzer |
| Monitoring | strace, ltrace, Process Monitor, API Monitor |
| Unpacking | UPX, Detect It Easy, manual OEP dump |
| Diffing | BinDiff, Diaphora |
