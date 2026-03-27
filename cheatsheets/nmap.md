# Nmap Cheatsheet

## Host Discovery
```bash
nmap -sn 192.168.1.0/24                  # Ping sweep (no port scan)
nmap -sn -PE 192.168.1.0/24              # ICMP echo ping
nmap -sn -PA80,443 192.168.1.0/24        # TCP ACK ping on ports 80,443
nmap -sn -PS22,80,443 192.168.1.0/24     # TCP SYN ping
nmap -sn -PU53 192.168.1.0/24            # UDP ping
nmap -Pn 192.168.1.1                     # Skip host discovery (treat as up)
nmap -sL 192.168.1.0/24                  # List targets without scanning
```

## Scan Types
```bash
nmap -sS 192.168.1.1                     # SYN scan (stealth, default with root)
nmap -sT 192.168.1.1                     # TCP connect scan (no root needed)
nmap -sU 192.168.1.1                     # UDP scan
nmap -sA 192.168.1.1                     # ACK scan (firewall rule detection)
nmap -sW 192.168.1.1                     # Window scan (like ACK but checks window size)
nmap -sN 192.168.1.1                     # NULL scan (no flags set)
nmap -sF 192.168.1.1                     # FIN scan
nmap -sX 192.168.1.1                     # Xmas scan (FIN+PSH+URG)
nmap -sO 192.168.1.1                     # IP protocol scan
```

## Port Specification
```bash
nmap -p 80 192.168.1.1                   # Single port
nmap -p 80,443,8080 192.168.1.1          # Multiple ports
nmap -p 1-1000 192.168.1.1               # Port range
nmap -p- 192.168.1.1                     # All 65535 ports
nmap -p U:53,T:80,443 192.168.1.1        # UDP and TCP specific ports
nmap --top-ports 100 192.168.1.1         # Top 100 most common ports
nmap -F 192.168.1.1                      # Fast scan (top 100 ports)
```

## Service and Version Detection
```bash
nmap -sV 192.168.1.1                     # Service version detection
nmap -sV --version-intensity 5 target    # Version intensity (0-9, default 7)
nmap -sV --version-all target            # Try every single probe
nmap -A 192.168.1.1                      # Aggressive: OS + version + scripts + traceroute
nmap -O 192.168.1.1                      # OS detection
nmap -O --osscan-guess target            # Aggressive OS guessing
```

## NSE Scripts
```bash
nmap -sC 192.168.1.1                     # Default scripts (same as --script=default)
nmap --script=vuln 192.168.1.1           # Vulnerability scripts
nmap --script=safe 192.168.1.1           # Safe scripts only
nmap --script=http-enum target           # HTTP directory enumeration
nmap --script=http-sql-injection target  # SQL injection detection
nmap --script=smb-vuln* target           # All SMB vulnerability scripts
nmap --script=ssl-heartbleed target      # Heartbleed check
nmap --script=dns-brute target           # DNS brute force
nmap --script=ftp-anon target            # Anonymous FTP check

# Script with arguments
nmap --script=http-brute --script-args http-brute.path=/admin target
nmap --script=smb-enum-shares --script-args smbusername=admin,smbpassword=pass target

# List available scripts
ls /usr/share/nmap/scripts/ | grep http
nmap --script-help=http-enum
```

## Useful Script Categories
```bash
nmap --script=auth target                # Authentication-related
nmap --script=broadcast target           # Broadcast discovery
nmap --script=brute target               # Brute force attacks
nmap --script=default target             # Default safe scripts
nmap --script=discovery target           # Host and service discovery
nmap --script=exploit target             # Exploitation scripts
nmap --script=external target            # External resource queries
nmap --script=fuzzer target              # Fuzzing scripts
nmap --script=intrusive target           # Intrusive scripts (may crash services)
nmap --script=malware target             # Malware detection
nmap --script=vuln target                # Vulnerability detection
```

## Timing and Performance
```bash
nmap -T0 target                          # Paranoid (IDS evasion, very slow)
nmap -T1 target                          # Sneaky (IDS evasion)
nmap -T2 target                          # Polite (reduced load)
nmap -T3 target                          # Normal (default)
nmap -T4 target                          # Aggressive (fast, reliable networks)
nmap -T5 target                          # Insane (fastest, may miss results)

nmap --min-rate 1000 target              # Minimum packets per second
nmap --max-rate 500 target               # Maximum packets per second
nmap --max-retries 2 target              # Maximum retransmissions
nmap --host-timeout 30m target           # Give up on host after 30 min
```

## Evasion Techniques
```bash
nmap -f target                           # Fragment packets (8-byte fragments)
nmap --mtu 16 target                     # Custom MTU (must be multiple of 8)
nmap -D RND:5 target                     # Decoy scan with 5 random decoys
nmap -D 10.0.0.1,10.0.0.2,ME target     # Specific decoys
nmap -S 10.0.0.1 target                  # Spoof source IP
nmap --source-port 53 target             # Spoof source port (DNS)
nmap --data-length 25 target             # Append random data to packets
nmap --randomize-hosts target            # Randomize target scan order
nmap --spoof-mac 0 target                # Random MAC address
nmap --spoof-mac Dell target             # Vendor-prefixed MAC
nmap --badsum target                     # Send bad checksums (detect FW/IDS)
```

## Output Formats
```bash
nmap -oN output.txt target               # Normal text output
nmap -oX output.xml target               # XML output
nmap -oG output.gnmap target             # Grepable output
nmap -oA output_base target              # All three formats at once
nmap -oS output.txt target               # Script kiddie output (for fun)

# Combine with verbosity
nmap -v target                           # Verbose
nmap -vv target                          # Very verbose
nmap -d target                           # Debug output
nmap --reason target                     # Show reason for port state
nmap --open target                       # Show only open ports
```

## Common Full Scans
```bash
# Initial fast scan
nmap -sV -sC -O -T4 -oA initial target

# Full TCP scan
nmap -sV -sC -p- -T4 -oA full_tcp target

# Full UDP scan (slow)
nmap -sU -sV --top-ports 200 -T4 -oA udp target

# Vulnerability scan
nmap -sV --script=vuln -oA vuln target

# Stealth scan for IDS evasion
nmap -sS -T2 -f --data-length 25 -D RND:3 -oA stealth target

# Comprehensive pentest scan
nmap -sS -sV -sC -O -p- -T4 --min-rate 1000 -oA comprehensive target
```

## Parsing Output
```bash
# Extract open ports from grepable output
grep "open" output.gnmap | cut -d' ' -f2 | sort -u

# Extract IPs with specific port open
grep "80/open" output.gnmap | awk '{print $2}'

# Convert XML to HTML report
xsltproc output.xml -o report.html
```
