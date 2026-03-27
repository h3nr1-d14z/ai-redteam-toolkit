# Hardware Requirements Guide

Some security testing domains require specialized hardware beyond a standard laptop.

## Wireless Hacking (CEH Module 16)

| Hardware | Purpose | Recommended |
|----------|---------|-------------|
| WiFi adapter (monitor mode) | Packet capture, injection | Alfa AWUS036ACH (dual-band), TP-Link TL-WN722N v1 |
| Directional antenna | Long-range testing | Yagi or panel antenna |
| WiFi Pineapple | Evil twin, rogue AP | Hak5 WiFi Pineapple Mark VII |
| GPS dongle | Wardriving | GlobalSat BU-353-S4 |

**Note**: Not all WiFi adapters support monitor mode. Check chipset compatibility (Atheros AR9271, Realtek RTL8812AU are well-supported).

## IoT / OT / Hardware Hacking (CEH Module 18)

| Hardware | Purpose | Recommended |
|----------|---------|-------------|
| USB-to-UART adapter | Serial console access | FT232RL, CP2102, CH340 |
| Logic analyzer | Protocol analysis (SPI, I2C, UART) | Saleae Logic 8, DSLogic Plus |
| JTAG/SWD debugger | Firmware extraction, debugging | Segger J-Link, ST-Link V2 |
| Bus Pirate | SPI/I2C/UART interaction | Bus Pirate v3.6/v4 |
| Flash programmer | Read/write flash chips | CH341A programmer |
| SDR (Software Defined Radio) | RF analysis | HackRF One, RTL-SDR v3 |
| BLE sniffer | Bluetooth Low Energy | nRF52840 dongle, Ubertooth One |
| Multimeter | Identify pins, voltage | Any decent digital multimeter |
| Oscilloscope | Glitching, signal analysis | Rigol DS1054Z (budget), Siglent |
| Soldering station | Component access | Hakko FX-888D |

## Network Sniffing (CEH Module 8)

| Hardware | Purpose | Recommended |
|----------|---------|-------------|
| Network TAP | Passive traffic capture | Dualcomm ETAP-2003, Throwing Star LAN Tap |
| Managed switch | Port mirroring (SPAN) | Any managed switch with mirror port |
| USB Ethernet adapter | Additional capture interface | Plugable USB3-E1000 |

## Physical Penetration Testing

| Hardware | Purpose | Recommended |
|----------|---------|-------------|
| Lock pick set | Physical access testing | Sparrows, Peterson |
| RFID cloner | Badge cloning | Proxmark3 RDV4 |
| Rubber Ducky | USB HID attack | Hak5 USB Rubber Ducky |
| Bash Bunny | Multi-payload USB | Hak5 Bash Bunny |
| LAN Turtle | Covert network implant | Hak5 LAN Turtle |
| Raspberry Pi | Dropbox / rogue device | RPi 4 or RPi Zero 2 W |
| Flipper Zero | Multi-tool (RFID, NFC, IR, Sub-GHz) | Flipper Zero |

## Mobile Testing

| Hardware | Purpose | Recommended |
|----------|---------|-------------|
| Rooted Android phone | Dynamic analysis | Google Pixel (easy to root) |
| Jailbroken iPhone | iOS testing | iPhone SE or older model |
| USB debugging cable | ADB/device connection | OEM USB cable |

## Minimum Setup by Domain

| Domain | Software Only | Hardware Needed |
|--------|:------------:|:---------------:|
| Web Pentest | Yes | No |
| API Security | Yes | No |
| Mobile (static) | Yes | No |
| Mobile (dynamic) | Partial | Test device recommended |
| Cloud Security | Yes | No |
| Red Team | Mostly | Physical tests need hardware |
| OSINT | Yes | No |
| Digital Forensics | Mostly | Write blocker for disk forensics |
| CTF | Yes | No |
| RE / Exploit Dev | Yes | No |
| Game Hacking | Yes | No |
| AI/LLM Security | Yes | No |
| **Wireless** | **No** | **WiFi adapter required** |
| **IoT/OT** | **Partial** | **UART/JTAG/SDR required** |
| **Network Sniffing** | Partial | TAP recommended for passive |
| **Physical Pentest** | **No** | **Lock picks, RFID, implants** |
