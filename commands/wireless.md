Test wireless network security on: $ARGUMENTS

## Hardware Required
- Wireless adapter with monitor mode (e.g., Alfa AWUS036ACH, TP-Link TL-WN722N v1)
- For WPA3: adapter supporting SAE
- Optional: directional antenna for long-range


## Pre-flight
- Verify wireless testing is explicitly in scope
- Identify target SSIDs and BSSIDs
- Prepare wireless adapter with monitor mode support

## Phase 1: Discovery
1. Enable monitor mode: airmon-ng start wlan0
2. Scan networks: airodump-ng wlan0mon
3. Identify targets: SSID, BSSID, channel, encryption (WPA2/WPA3/WEP/Open)
4. Identify connected clients for deauth attacks

## Phase 2: WPA/WPA2 Cracking
1. Capture handshake: airodump-ng -c <ch> --bssid <bssid> -w capture wlan0mon
2. Deauth client: aireplay-ng -0 5 -a <bssid> -c <client> wlan0mon
3. Crack: hashcat -m 22000 capture.hc22000 wordlists/passwords/top-1000.txt
4. Or: aircrack-ng capture.cap -w wordlist.txt

## Phase 3: Evil Twin / Rogue AP
1. Create fake AP: hostapd with matching SSID
2. DHCP + DNS: dnsmasq for IP assignment
3. Captive portal: redirect to credential harvesting page
4. Monitor captured credentials

## Phase 4: Enterprise (WPA-Enterprise/802.1X)
1. Set up RADIUS: freeradius-wpe for credential capture
2. Create evil twin with EAP support
3. Capture RADIUS exchanges (challenge/response)
4. Offline crack captured hashes

## Phase 5: Post-Exploitation
1. ARP scanning of wireless network
2. MITM: ettercap, bettercap for traffic interception
3. DNS spoofing for phishing
4. Pivot to wired network if bridged

## Tools
aircrack-ng suite, hostapd, bettercap, Wireshark, wifite2, hashcat, hcxdumptool

## Output
Save to engagements/<target>/findings/wireless-*.md
Reference: CEH Module 16 — Hacking Wireless Networks

## Safety
Only test networks you are authorized to assess. Do not deauth production clients without approval.
