Analyze game network protocol for: $ARGUMENTS

1. **Capture setup**: Configure packet capture — Wireshark for raw, mitmproxy for HTTP/WebSocket, custom proxy for TCP
2. **Encryption**: Identify if traffic is encrypted beyond TLS — custom XOR, AES, proprietary. Intercept before encryption with Frida
3. **Protocol structure**: Map packet format — header (length, type, sequence), body (serialization: protobuf, flatbuffers, custom binary)
4. **Message catalog**: Document all message types — login, movement, action, chat, inventory, purchase
5. **Replay attacks**: Capture and replay packets — test for sequence validation, timestamp checks, session binding
6. **Manipulation**: Modify packet values (coordinates, damage, item IDs) — test server-side validation
7. **Speed/teleport**: Test movement validation — rapid position updates, impossible coordinates, speed checks

Tools: Wireshark, mitmproxy, Frida, custom Python proxy, protoc (for protobuf)
Save to `game-hacking/network/<game>/protocol-analysis.md`
