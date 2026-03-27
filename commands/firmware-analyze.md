Analyze firmware image: $ARGUMENTS

1. **Extract**: Use binwalk to identify and extract filesystem, kernel, bootloader components
2. **Filesystem analysis**: Mount extracted filesystem, enumerate binaries, configs, scripts, web interfaces
3. **Credential hunt**: Search for hardcoded passwords, SSH keys, API tokens, certificates in configs and binaries
4. **Service analysis**: Identify running services (telnet, SSH, HTTP, MQTT, UPnP), check for known vulns
5. **Binary analysis**: Analyze key binaries (web server, management daemon) for vulnerabilities — BOF, command injection
6. **Crypto review**: Check for weak/custom crypto, hardcoded encryption keys, unsigned update mechanisms
7. **Network**: Identify communication protocols, cloud endpoints, update servers, debug interfaces (UART/JTAG)

Tools: binwalk, firmware-mod-kit, sasquatch, jefferson, ubi_reader, Ghidra
Save analysis to `re/firmware/<device>/analysis.md`
