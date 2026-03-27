Reverse engineer network protocol for: $ARGUMENTS

1. **Capture traffic**: Set up packet capture (tcpdump/Wireshark) during normal client-server interaction
2. **Identify structure**: Determine transport (TCP/UDP/WebSocket), encoding (binary/JSON/protobuf/msgpack), encryption (TLS/custom)
3. **Message catalog**: Identify distinct message types, map request-response pairs, document message flow
4. **Field analysis**: Identify fields — length prefixes, message IDs, sequence numbers, timestamps, checksums
5. **Replay testing**: Replay captured packets, observe server response, identify session-bound fields
6. **Dissector**: Write Wireshark dissector or Python parser for the protocol
7. **Documentation**: Create protocol specification with message format diagrams and field descriptions

Tools: Wireshark, tcpdump, mitmproxy, custom Python scripts, Frida (for TLS interception)
Save to `re/protocols/<protocol-name>/specification.md`
