Perform memory hacking on: $ARGUMENTS

1. **Initial scan**: Identify target process, scan for known values (health, ammo, currency, coordinates)
2. **Value narrowing**: Change value in-game, filter scan results, repeat until single address found
3. **Pointer scan**: Find pointer chains to base address for stable memory access across restarts
4. **Structure mapping**: Map surrounding memory to identify full game object structure (health near max_health, position near velocity)
5. **Write test**: Modify values, check if server validates — distinguish client-only vs server-authoritative values
6. **Code injection**: Find code that accesses the value, NOP damage functions, hook update routines
7. **Automation**: Build Frida/CE script for reliable value modification with pointer chain resolution

Tools: Cheat Engine, GameGuardian (mobile), scanmem (Linux), Frida, x64dbg
Save to `game-hacking/memory/<game>/memory-map.md`
