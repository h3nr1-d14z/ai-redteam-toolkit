Analyze IoT/OT device security on: $ARGUMENTS

## Pre-flight
- Identify device type, manufacturer, model, firmware version
- Determine network connectivity (WiFi, BLE, Zigbee, Z-Wave, cellular)
- Check for web interface, mobile app, cloud backend

## Phase 1: Reconnaissance
1. Network scan: nmap device IP for open ports and services
2. Service fingerprint: identify web server, MQTT, CoAP, UPnP, Telnet
3. Banner grabbing: identify firmware version, OS
4. Shodan/Censys: search for similar exposed devices

## Phase 2: Firmware Analysis
1. Download firmware: manufacturer site, MITM update, UART/JTAG dump
2. Extract: binwalk -e firmware.bin
3. Analyze filesystem: find config files, hardcoded credentials, SSH keys
4. Search strings: grep for passwords, API keys, URLs, certificates
5. Reference: /firmware-analyze for detailed workflow

## Phase 3: Network Protocol Analysis
1. Capture traffic: Wireshark between device and cloud/app
2. Identify protocol: MQTT, CoAP, HTTP, custom binary
3. Check encryption: is traffic encrypted? Certificate validation?
4. Test replay attacks: resend captured commands
5. MQTT: test anonymous access, subscribe to # wildcard

## Phase 4: Web Interface
1. Default credentials: admin:admin, root:root, admin:password
2. Run /pentest on web management interface
3. Check for command injection in device configuration fields
4. Test firmware update mechanism (unsigned updates?)

## Phase 5: Hardware
1. Identify debug ports: UART, JTAG, SWD
2. Connect and get shell access
3. Extract flash memory contents
4. Analyze bootloader for bypass options

## Output
Save to engagements/<target>/findings/iot-*.md
Reference: CEH Module 18 — IoT and OT Hacking

## Safety
IoT devices may control physical systems. Never test safety-critical devices without proper precautions.
