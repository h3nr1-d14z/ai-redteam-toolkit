Analyze game security for: $ARGUMENTS

## Pre-flight
- Identify engine: Unity (IL2CPP/Mono), Unreal, Godot, custom
- Identify platform: PC, Android, iOS, Web
- Check network model: client-server, P2P, authoritative server

## Phase 1: Client RE
**Unity**: Download IPA/APK → Il2CppDumper or `python3 tools/re/il2cpp-extractor.py`
  → Extract class/method names, dump assets with UnityPy
**Unreal**: SDK generation, UObject analysis
**Generic**: Ghidra/radare2 analysis, string search for game keywords

## Phase 2: Asset Extraction
- Extract sprites, textures, audio, configs from asset bundles
- Parse game config tables (level data, economy values, drop rates)
- Find hardcoded constants: energy, coins, difficulty multipliers

## Phase 3: Memory Analysis
- Scan for values: health, ammo, currency, score
- Find pointer chains for stable addresses
- **Key question**: Does server validate these values?
- If no server validation → client-side manipulation = real vulnerability

## Phase 4: Network Analysis
- Capture game traffic: Wireshark, mitmproxy
- Identify protocol: TCP/UDP, binary/JSON/protobuf
- Test replay attacks, packet manipulation
- Check for server-side validation of all client claims

## Phase 5: Economy & Logic
- Map in-app purchase flow
- Test receipt validation (fake receipts, replay)
- Check for race conditions in currency operations
- Analyze loot box / random number generation

## Output
Save to engagements/<target>/analysis.md with sections per attack vector.

## Tools (with fallbacks)
Decompile: Il2CppDumper > Ghidra > dnSpy | Memory: Cheat Engine > scanmem
Network: Wireshark > mitmproxy > tcpdump | Hook: Frida > DLL injection
Assets: UnityPy > AssetStudio > UABE | Reference: methodology/game-security.md

## Safety
Only analyze games you own or are authorized to test.
Focus on server-side validation gaps — these are the real vulnerabilities.
