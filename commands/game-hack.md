Analyze game security for: $ARGUMENTS

1. **Recon**: identify engine (Unity/Unreal/custom), platform, network model, anti-cheat
2. **Client RE**: decompile/disassemble, find game logic (health, damage, currency, speed)
3. **Memory**: scan for values, find pointers, test server-side validation
4. **Network**: capture traffic, identify protocol, test replay/manipulation
5. **Exploit**: develop Frida hooks, DLL injection, packet manipulator
6. **Document**: save to `game-hacking/<game>/`

For Unity: IL2CPP dump or Mono decompile. For Unreal: SDK generation.
Focus on server-side validation gaps — these are the real vulnerabilities.
