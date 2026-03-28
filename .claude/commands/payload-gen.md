Generate payload for: $ARGUMENTS

1. **Target context**: Identify target platform, architecture, delivery mechanism, and constraints
2. **Payload type**: Select appropriate type — reverse shell, bind shell, web shell, stager, meterpreter, custom
3. **Encoding**: Apply encoding to evade detection — base64, XOR, AES, polymorphic, custom encoder
4. **Delivery format**: Generate in required format — Python, PowerShell, C, EXE, DLL, ELF, raw bytes, HTA, macro
5. **Evasion**: Add AV/EDR evasion techniques — sleep timers, sandbox detection, AMSI bypass, ETW patching
6. **Handler setup**: Provide listener setup instructions (nc, msfconsole, custom handler)
7. **Test**: Verify payload execution and callback in lab environment

Tools: msfvenom, pwntools, custom generators
Save to `exploitation/payloads/<type>-<target>.<ext>` with usage instructions
