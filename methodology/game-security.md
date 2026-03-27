# Game Security Testing Methodology

## Phase 1: Reconnaissance and Client Analysis

### Game Client Identification
- Identify game engine: Unity (look for `UnityEngine.dll`, `Assembly-CSharp.dll`, `globalgamemanagers`), Unreal (look for `.pak` files, `UE4` strings), custom engine
- Identify client type: native (C++), managed (.NET/Mono, Java), web-based (WebGL, HTML5)
- Identify platform: PC (Windows/Linux/macOS), mobile (Android/iOS), console, browser
- Identify anti-cheat: EasyAntiCheat, BattlEye, Vanguard, GameGuard, custom
- Check for DRM: Steam DRM, Denuvo, custom

### Network Architecture
- Client-server model: authoritative server vs client-authoritative
- Protocol: TCP, UDP, WebSocket, custom protocol
- Identify server endpoints: DNS lookup, packet capture on launch
- Check for dedicated servers vs peer-to-peer
- Identify CDN, matchmaking, auth, and game servers separately

### File System Analysis
- Game installation directory structure
- Configuration files: INI, XML, JSON, YAML (check for editable values)
- Save files: location, format, encryption
- Asset files: textures, models, audio, scripts
- Log files: debug information, server addresses, tokens
- Registry entries (Windows): `HKCU\Software\<Developer>\<Game>`

---

## Phase 2: Client Reverse Engineering

### Unity Games
- **IL2CPP builds:** use `Il2CppDumper` to extract method signatures and offsets, then analyze with Ghidra/IDA
- **Mono builds:** decompile `Assembly-CSharp.dll` with dnSpy or ILSpy -- full source recovery
- Key targets in code:
  - Player stats: health, damage, speed, stamina
  - Currency and inventory systems
  - Anti-cheat implementation
  - Network packet construction and parsing
  - Authentication and session management
  - In-app purchase validation
- Asset extraction: `AssetStudio` or `UABE` (Unity Asset Bundle Extractor)
- Modify assets: textures (wallhack via transparent walls), models, audio

### Unreal Engine Games
- `.pak` file extraction: `UnrealPakTool`, `QuickBMS` with Unreal script
- Blueprint analysis: decompile UAsset files
- C++ binary: analyze with Ghidra/IDA, look for `UObject` hierarchy
- SDK generation: use `Dumper-7` or `UnrealDumper` to generate SDK headers
- Key structures: `UWorld`, `ULevel`, `APlayerController`, `ACharacter`, `UGameInstance`

### Native C++ Games
- Static analysis: Ghidra or IDA for disassembly and decompilation
- Identify key functions: player update loop, damage calculation, network send/receive
- String analysis: find debug messages, error strings, network protocol strings
- Vtable analysis: reconstruct class hierarchies
- RTTI (Run-Time Type Information): recover class names if not stripped

---

## Phase 3: Memory Analysis and Manipulation

### Memory Scanning
- **Cheat Engine** (Windows): attach to game process, scan for known values
- **GameGuardian** (Android): memory scanner for mobile games
- **scanmem/GameConqueror** (Linux): open-source memory scanner

### Finding Game Values
1. Scan for known value (e.g., health = 100)
2. Change value in game (take damage, health = 85)
3. Scan for changed value (scan for 85)
4. Repeat until single address found
5. Modify value and verify in-game effect

### Common Memory Targets
| Target | Type | Notes |
|---|---|---|
| Health/HP | float or int | Often 0-100 or 0-maxHP |
| Ammo | int | Current clip and reserve |
| Currency/Gold | int or int64 | May be server-validated |
| Position (X,Y,Z) | float[3] | Teleportation, noclip |
| Speed | float | Movement speed multiplier |
| Damage | float | Weapon damage values |
| Cooldowns | float | Ability cooldown timers |
| Visibility | bool/int | Player visibility flag |

### Pointer Chains
- Game values are often in dynamically allocated objects
- Find pointer chain from static base address to target value
- Cheat Engine: pointer scan to find stable paths
- Structure dissection: map object layout to understand field offsets

### Code Injection
- DLL injection: `CreateRemoteThread`, `SetWindowsHookEx`, manual mapping
- Function hooking: detour/trampoline hooks on game functions
- Inline patching: NOP out checks, modify conditional jumps
- Shellcode injection: allocate memory in target process, write and execute
- Mono injection (Unity Mono): `mono_get_root_domain()`, `mono_thread_attach()`, load custom assembly

---

## Phase 4: Network Protocol Analysis

### Traffic Capture
- Wireshark with display filter for game traffic: `ip.addr == <server_ip>`
- For encrypted traffic: hook send/recv functions with Frida to capture pre-encryption data
- Log packet data: timestamp, direction, size, decoded content
- Record gameplay sessions for replay analysis

### Protocol Reverse Engineering
- Identify packet structure: header format, length fields, message type IDs, payload
- Common patterns:
  - Length-prefixed messages: `[2-byte length][message type][payload]`
  - Fixed-size headers with variable payloads
  - Protobuf, FlatBuffers, or MessagePack serialization
- Map message types to game actions: move, attack, use item, chat, buy
- Identify sequence numbers, timestamps, checksums
- Look for authentication tokens in packets

### Protocol Attacks
- **Packet replay:** capture and resend packets (duplicate actions, items)
- **Packet modification:** change values in transit (damage, position, item IDs)
- **Speed hacking:** send movement packets faster than normal (server may or may not validate)
- **Sequence manipulation:** skip required steps (e.g., payment verification)
- **Race conditions:** send simultaneous requests for the same resource
- **Desync attacks:** cause client-server state mismatch

### Tools for Network Analysis
- Wireshark: packet capture and analysis with custom dissectors
- mitmproxy: for HTTP/WebSocket game protocols
- Custom proxy: write a man-in-the-middle proxy for the game protocol
- Frida: hook socket send/recv for pre-encryption capture

---

## Phase 5: Server-Side Validation Testing

### Client-Authority Testing
- **Position validation:** teleport via memory edit or packet -- does the server accept it?
- **Speed validation:** increase movement speed -- does the server check against max speed?
- **Damage validation:** modify damage values -- does the server trust client damage calculations?
- **Cooldown validation:** skip ability cooldowns -- does the server enforce them?
- **Inventory manipulation:** give yourself items via packet modification -- server-validated?
- **Currency manipulation:** change currency amount client-side -- reflected on server?

### Economy and Item System
- Duplicate items: race condition on item transfer/trade
- Negative quantity: buy -1 items (may add currency instead of subtracting)
- Integer overflow: buy 2,147,483,647 items (32-bit int overflow)
- Price manipulation: modify purchase requests with different prices
- Currency conversion: exploit rounding errors between currencies
- Gift/trade abuse: self-trade, trade cancel timing exploits
- In-app purchase receipt validation: can you forge or replay receipts?

### Matchmaking and Ranking
- ELO/rank manipulation: lose intentionally then stomp lower ranks
- Queue sniping: join queue at same time as a friend for coordinated matches
- Disconnect abuse: leave losing games without penalty
- Region hopping: exploit latency for combat advantage

### Authentication and Session
- Session token theft or prediction
- Account enumeration
- Password reset abuse
- Multi-session exploitation: login from multiple clients simultaneously
- Token replay after logout

---

## Phase 6: Anti-Cheat Analysis

### Anti-Cheat Identification
| Anti-Cheat | Indicators |
|---|---|
| EasyAntiCheat | `EasyAntiCheat.sys`, `EasyAntiCheat_EOS.sys`, `EasyAntiCheat` service |
| BattlEye | `BEService.exe`, `BEClient.dll`, `BEService` service |
| Vanguard | `vgc.sys`, `vgk.sys` (kernel driver, always-on) |
| GameGuard | `GameGuard.des`, `NPGameMon.exe` |
| Custom | Game-specific DLLs, integrity checks |

### Anti-Cheat Capabilities
- **Kernel-level:** driver loaded, can scan all memory, monitor system calls
- **User-level:** runs in user space, scans game memory, monitors loaded modules
- **Server-side:** behavior analysis, statistical anomaly detection, replay verification
- **Hybrid:** combination of client and server-side checks

### Common Anti-Cheat Checks
- Process list scanning for known cheat tools
- Module (DLL) enumeration for injected libraries
- Memory integrity: checksum verification of game code sections
- Driver enumeration: detect debuggers, hypervisors
- Screenshot capture and analysis
- Hardware ID (HWID) banning
- Behavioral analysis: movement patterns, reaction time, accuracy statistics

### Testing Anti-Cheat (Authorized Research Only)
- Identify what checks are performed: hook NtQuerySystemInformation, NtQueryVirtualMemory
- Determine scanning frequency and triggers
- Test basic bypasses: rename tools, hide processes, use hypervisor-based approaches
- Document findings: what was detected, what was not, time to detection
- Report bypass methods to the game developer for hardening

---

## Phase 7: Mobile Game Specific

### Android
- Decompile APK: jadx for Java/Kotlin, Il2CppDumper for Unity IL2CPP
- Memory manipulation: GameGuardian on rooted device
- Frida hooks: modify game logic at runtime
- Save file manipulation: edit files in `/data/data/<package>/`
- Speed hack: modify system time or hook time-related functions
- Network: proxy game traffic through Burp Suite

### iOS
- Decrypt IPA: `frida-ios-dump` on jailbroken device
- Memory manipulation: iGameGuardian on jailbroken device
- Frida hooks: same approach as Android
- Save file manipulation: access via jailbroken file system
- In-app purchase testing: local receipt validation bypass

### Common Mobile Game Vulnerabilities
- Client-side validation of purchases (receipt not verified with Apple/Google)
- Save file stored in plaintext (modify currency, items, progress)
- Timestamp manipulation for energy/timer-based games
- Offline progress calculation trusting client-submitted values
- Debug endpoints left in release builds

---

## Phase 8: Reporting

### Finding Classification
| Category | Examples |
|---|---|
| Critical | Server-side RCE, arbitrary item/currency generation that server accepts |
| High | Client-authoritative damage/health, economy exploitation (duplication) |
| Medium | Wallhacks via asset modification, speed hacks with partial server validation |
| Low | Cosmetic manipulation, minor information disclosure |
| Info | Anti-cheat bypass methods, client-side only cheats (server-validated) |

### Report Focus
- Prioritize server-side vulnerabilities over client-side cheats
- Quantify economic impact: how much virtual currency could be generated?
- Assess competitive impact: how does this affect fair play?
- Recommend server-side validation for all client-authoritative findings
- Provide anti-cheat improvement recommendations

### Tools Quick Reference

| Task | Tools |
|---|---|
| Memory | Cheat Engine, GameGuardian, scanmem |
| .NET/Unity Mono | dnSpy, ILSpy, Unity Explorer |
| Unity IL2CPP | Il2CppDumper, Cpp2IL |
| Unreal | Dumper-7, UnrealPakTool |
| Native Binary | Ghidra, IDA Pro, x64dbg, Binary Ninja |
| Network | Wireshark, mitmproxy, custom proxies |
| Injection | DLL injection tools, Frida, Cheat Engine |
| Mobile | GameGuardian, Frida, jadx, Il2CppDumper |
| Assets | AssetStudio, UABE, QuickBMS |
