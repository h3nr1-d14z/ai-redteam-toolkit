# Wireshark and tshark Filters Cheatsheet

## Display Filters — Network Layer

```
# IP address filters
ip.addr == 10.10.10.5                    # Source OR destination
ip.src == 10.10.10.5                     # Source only
ip.dst == 10.10.10.5                     # Destination only
ip.addr == 10.10.10.0/24                 # Subnet
!(ip.addr == 10.10.10.5)                 # Exclude IP

# Multiple IPs
ip.addr == 10.10.10.5 || ip.addr == 10.10.10.6
ip.addr in {10.10.10.5 10.10.10.6 10.10.10.7}

# IPv6
ipv6.addr == fe80::1
ipv6.src == 2001:db8::1

# ARP
arp
arp.opcode == 1                          # ARP request
arp.opcode == 2                          # ARP reply
arp.duplicate-address-detected           # Duplicate IP detection

# ICMP
icmp
icmp.type == 8                           # Echo request (ping)
icmp.type == 0                           # Echo reply
icmp.type == 3                           # Destination unreachable
icmp.type == 11                          # TTL exceeded (traceroute)
```

---

## Display Filters — Transport Layer

```
# TCP
tcp.port == 80                           # Source OR destination port
tcp.srcport == 443                       # Source port
tcp.dstport == 22                        # Destination port
tcp.port in {80 443 8080 8443}           # Multiple ports

# TCP flags
tcp.flags.syn == 1                       # SYN packets
tcp.flags.syn == 1 && tcp.flags.ack == 0 # SYN only (connection initiation)
tcp.flags.syn == 1 && tcp.flags.ack == 1 # SYN-ACK
tcp.flags.fin == 1                       # FIN packets
tcp.flags.reset == 1                     # RST packets
tcp.flags.push == 1                      # PSH packets

# TCP analysis
tcp.analysis.retransmission              # Retransmissions
tcp.analysis.duplicate_ack               # Duplicate ACKs
tcp.analysis.zero_window                 # Zero window (flow control)
tcp.analysis.window_full                 # Window full
tcp.analysis.flags                       # Any TCP analysis flag

# TCP stream
tcp.stream eq 5                          # Specific TCP stream number

# UDP
udp.port == 53                           # DNS
udp.port == 161                          # SNMP
udp.srcport == 68                        # DHCP client
udp.dstport == 67                        # DHCP server
```

---

## Display Filters — Application Layer

```
# HTTP
http                                     # All HTTP traffic
http.request                             # Requests only
http.response                            # Responses only
http.request.method == "GET"
http.request.method == "POST"
http.request.method == "PUT"
http.request.uri contains "/admin"
http.request.uri contains "login"
http.host == "target.com"
http.host contains "corp"
http.response.code == 200
http.response.code == 401                # Unauthorized
http.response.code == 403                # Forbidden
http.response.code == 500                # Server error
http.response.code >= 400                # All errors
http.content_type contains "json"
http.cookie contains "session"
http.authorization                       # Auth headers present
http.request.uri matches "\\.(php|asp|jsp)"
http.file_data contains "password"

# HTTPS / TLS
tls                                      # All TLS traffic
tls.handshake                            # Handshake messages
tls.handshake.type == 1                  # Client Hello
tls.handshake.type == 2                  # Server Hello
tls.handshake.type == 11                 # Certificate
tls.handshake.extensions.server_name contains "target.com"  # SNI
tls.record.version == 0x0303            # TLS 1.2
tls.record.version == 0x0304            # TLS 1.3
ssl.alert_message                        # SSL/TLS alerts

# DNS
dns                                      # All DNS
dns.qry.name == "corp.local"             # Query for specific name
dns.qry.name contains "corp"             # Partial match
dns.qry.type == 1                        # A record query
dns.qry.type == 28                       # AAAA record query
dns.qry.type == 15                       # MX record query
dns.qry.type == 252                      # AXFR (zone transfer)
dns.resp.name == "corp.local"            # Response name
dns.flags.response == 1                  # DNS responses only
dns.flags.rcode == 3                     # NXDOMAIN (name not found)
dns.a                                    # A record in answer
dns.txt                                  # TXT records

# DHCP
dhcp                                     # All DHCP (bootp)
dhcp.type == 1                           # DHCP Discover
dhcp.type == 2                           # DHCP Offer
dhcp.type == 3                           # DHCP Request
dhcp.type == 5                           # DHCP ACK
dhcp.option.hostname                     # Hostnames in DHCP

# SMB
smb || smb2                              # All SMB traffic
smb2.cmd == 5                            # Tree Connect (share access)
smb2.filename                            # Files accessed
smb2.filename contains "password"

# Kerberos
kerberos                                 # All Kerberos
kerberos.msg_type == 10                  # AS-REQ
kerberos.msg_type == 11                  # AS-REP
kerberos.msg_type == 12                  # TGS-REQ
kerberos.msg_type == 13                  # TGS-REP
kerberos.error_code == 24               # Pre-auth failed (wrong password)
kerberos.CNameString contains "admin"

# SMTP
smtp                                     # All SMTP
smtp.req.command == "AUTH"               # Authentication
smtp.req.command == "MAIL"               # Sender
smtp.req.command == "RCPT"               # Recipient
smtp.response.code == 250               # OK

# FTP
ftp                                      # FTP commands
ftp-data                                 # FTP data transfer
ftp.request.command == "USER"            # Username
ftp.request.command == "PASS"            # Password
ftp.response.code == 230                 # Login successful
ftp.response.code == 530                 # Login failed

# LDAP
ldap                                     # All LDAP
ldap.bindRequest                         # Bind (authentication)
ldap.filter                              # Search filters

# SNMP
snmp                                     # All SNMP
snmp.community == "public"               # Community string
```

---

## Capture Filters (BPF Syntax)

Applied before capture starts. Uses Berkeley Packet Filter syntax (different from display filters).

```
# Host filters
host 10.10.10.5
src host 10.10.10.5
dst host 10.10.10.5
not host 10.10.10.5

# Network filters
net 10.10.10.0/24
src net 192.168.1.0/24

# Port filters
port 80
src port 443
dst port 22
port 80 or port 443
portrange 8000-9000
not port 53

# Protocol filters
tcp
udp
icmp
arp

# Combine with logic
host 10.10.10.5 and port 80
host 10.10.10.5 and not port 22
tcp and port 80 and host 10.10.10.5
(tcp port 80) or (tcp port 443)
```

---

## Useful Operations

```
# Follow TCP stream: Right-click packet > Follow > TCP Stream
# Follow HTTP stream: Right-click > Follow > HTTP Stream
# Follow TLS stream (requires keys): Follow > TLS Stream

# Export objects
# File > Export Objects > HTTP        # Download files transferred via HTTP
# File > Export Objects > SMB         # Files from SMB shares
# File > Export Objects > TFTP
# File > Export Objects > DICOM

# Statistics
# Statistics > Conversations          # Who is talking to whom
# Statistics > Endpoints              # All unique hosts
# Statistics > Protocol Hierarchy     # Protocol breakdown
# Statistics > I/O Graphs            # Traffic over time
# Statistics > Flow Graph            # TCP flow visualization

# Coloring rules
# View > Coloring Rules
# TCP RST = red, HTTP = green, DNS = blue (defaults)

# Mark packets
# Right-click > Mark/Unmark Packet (Ctrl+M)
# Display filter: frame.marked == 1

# Add comments
# Right-click > Packet Comment

# Time display
# View > Time Display Format > Seconds Since Beginning of Capture
# View > Time Display Format > UTC Date and Time of Day
```

---

## TLS Decryption

```
# Method 1: Pre-master secret log (browser)
# Set environment variable before launching browser:
export SSLKEYLOGFILE=/tmp/tls_keys.log
google-chrome &
# or: firefox &

# In Wireshark: Edit > Preferences > Protocols > TLS
# Set "(Pre)-Master-Secret log filename" to /tmp/tls_keys.log

# Method 2: RSA private key (server key)
# Edit > Preferences > Protocols > TLS > RSA keys list
# IP: server_ip, Port: 443, Protocol: http, Key File: server.key
# Only works with RSA key exchange (not ECDHE/DHE)
```

---

## tshark CLI Equivalents

```bash
# Basic capture
tshark -i eth0

# Capture with filter
tshark -i eth0 -f "port 80" -w capture.pcap

# Read capture file
tshark -r capture.pcap

# Apply display filter
tshark -r capture.pcap -Y "http.request"
tshark -r capture.pcap -Y "ip.addr == 10.10.10.5"

# Extract specific fields
tshark -r capture.pcap -Y "http.request" -T fields -e ip.src -e http.host -e http.request.uri
tshark -r capture.pcap -Y "dns.qry.name" -T fields -e ip.src -e dns.qry.name

# Extract credentials from HTTP
tshark -r capture.pcap -Y "http.request.method == POST" -T fields \
  -e ip.src -e http.host -e http.request.uri -e http.file_data

# Follow TCP stream
tshark -r capture.pcap -z "follow,tcp,ascii,0"

# Protocol hierarchy
tshark -r capture.pcap -z io,phs

# Conversations
tshark -r capture.pcap -z conv,tcp
tshark -r capture.pcap -z conv,ip

# Endpoints
tshark -r capture.pcap -z endpoints,ip

# HTTP requests summary
tshark -r capture.pcap -Y http.request -T fields -e http.request.method \
  -e http.host -e http.request.uri | sort | uniq -c | sort -rn

# DNS queries
tshark -r capture.pcap -Y "dns.flags.response == 0" -T fields -e dns.qry.name | sort | uniq -c | sort -rn

# Export HTTP objects
tshark -r capture.pcap --export-objects http,/tmp/http_objects/

# Live capture specific fields
tshark -i eth0 -Y "http.request" -T fields -e ip.src -e http.host -e http.request.uri

# Ring buffer capture (10 files, 100MB each)
tshark -i eth0 -b filesize:102400 -b files:10 -w capture.pcap

# Capture statistics
tshark -r capture.pcap -z io,stat,1,"COUNT(frame)frame","COUNT(frame)tcp","COUNT(frame)http"

# Decrypt TLS with key log
tshark -r capture.pcap -o tls.keylog_file:/tmp/tls_keys.log -Y http
```

---

## Common Analysis Patterns

### Find Credentials

```
# HTTP Basic Auth (base64 encoded)
http.authorization

# HTTP POST login forms
http.request.method == "POST" && http.request.uri contains "login"

# FTP credentials
ftp.request.command == "USER" || ftp.request.command == "PASS"

# SMTP credentials
smtp.req.command == "AUTH"

# Telnet (plaintext)
telnet

# SNMP community strings
snmp

# LDAP bind (plaintext)
ldap.bindRequest && !(tls)

# Kerberos authentication
kerberos.msg_type == 10
```

### Detect Port Scanning

```
# SYN scan (many SYN, few established)
tcp.flags.syn == 1 && tcp.flags.ack == 0

# SYN scan with RST responses (closed ports)
tcp.flags.reset == 1 && tcp.flags.ack == 1

# Connect scan
tcp.flags.syn == 1

# NULL scan
tcp.flags == 0x000

# FIN scan
tcp.flags == 0x001

# XMAS scan
tcp.flags.fin == 1 && tcp.flags.push == 1 && tcp.flags.urg == 1

# High volume from single source
# Statistics > Conversations > sort by packets
```

### Identify C2 / Beaconing

```
# Regular interval connections (check Statistics > I/O Graph)
# DNS tunneling (large TXT queries)
dns.qry.type == 16 && dns.qry.name matches ".{50,}"

# ICMP tunneling (large ICMP payloads)
icmp && data.len > 64

# HTTP beaconing (regular POST to same URI)
http.request.method == "POST"
# Then: Statistics > HTTP > Requests — look for repeated URIs

# Unusual ports
tcp.dstport > 1024 && !(tcp.dstport in {3306 3389 5432 5900 8080 8443})

# Long connections
# Statistics > Conversations > sort by duration
```

### Detect ARP Spoofing

```
# Duplicate IP detection
arp.duplicate-address-detected

# ARP replies without requests (gratuitous)
arp.opcode == 2

# Compare: same IP, different MAC over time
arp
```
