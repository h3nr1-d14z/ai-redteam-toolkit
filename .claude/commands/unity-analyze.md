Analyze Unity game client: $ARGUMENTS

1. **Identify runtime**: Determine if Mono or IL2CPP build (check for GameAssembly.dll vs Assembly-CSharp.dll)
2. **IL2CPP dump**: Use Il2CppDumper to extract class/method signatures, generate dummy DLLs for analysis
3. **Mono decompile**: If Mono, decompile Assembly-CSharp.dll with dnSpy/ILSpy — full source recovery
4. **Map game logic**: Find key classes — PlayerController, GameManager, NetworkManager, CurrencySystem, HealthSystem
5. **Identify cheats**: Locate speed/damage multipliers, god mode flags, currency values, cooldown timers
6. **Asset extraction**: Use AssetStudio/UABE to extract textures, configs, scriptable objects, asset bundles
7. **Hook development**: Write Frida/Harmony hooks for identified targets, test server-side validation

Tools: Il2CppDumper, dnSpy, AssetStudio, Frida, Harmony/BepInEx
Save to `game-hacking/unity/<game>/analysis.md`
