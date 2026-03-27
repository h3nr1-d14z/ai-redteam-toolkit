# Digital Forensics and Incident Response (DFIR) Methodology

## Phase 1: Preparation and Acquisition

### Incident Assessment
- Determine the nature of the incident: malware, intrusion, data breach, insider threat, ransomware
- Identify affected systems and scope of compromise
- Establish chain of custody documentation
- Determine legal and regulatory requirements (evidence preservation, notification)
- Assemble response team and assign roles

### Evidence Acquisition Principles
- **Order of volatility:** collect most volatile evidence first
  1. CPU registers, cache
  2. Memory (RAM)
  3. Network connections, routing tables
  4. Running processes
  5. Disk (file system, swap)
  6. Remote logging data
  7. Physical storage, backups
- **Integrity:** create forensic images, never work on original evidence
- **Chain of custody:** document who handled evidence, when, and what was done
- **Hashing:** compute MD5 + SHA256 of all evidence before and after analysis

### Memory Acquisition
- **Linux:** `avml` (preferred), `LiME` kernel module, `/proc/kcore`
  ```
  # LiME
  insmod lime.ko "path=/evidence/memory.lime format=lime"
  ```
- **Windows:** DumpIt, WinPMEM, FTK Imager, Belkasoft RAM Capturer
- **macOS:** `osxpmem`
- Capture before shutting down or modifying the system
- Hash the memory dump immediately after capture

### Disk Acquisition
- **Linux:** `dd if=/dev/sda of=/evidence/disk.raw bs=4M status=progress`
- **Preferred:** `dc3dd` or `dcfldd` (forensic variants with built-in hashing)
  ```
  dc3dd if=/dev/sda of=/evidence/disk.raw hash=sha256 log=/evidence/acquisition.log
  ```
- **FTK Imager:** GUI-based, creates E01 format with built-in hashing
- **Remote:** `ssh root@target "dd if=/dev/sda bs=4M" | dd of=/evidence/disk.raw`
- Mount forensic image read-only: `mount -o ro,loop,noexec disk.raw /mnt/evidence`

### Live System Collection (Volatile Data)
```bash
# Date and time
date -u > /evidence/volatile/datetime.txt

# Network connections
netstat -antp > /evidence/volatile/netstat.txt
ss -tunapl > /evidence/volatile/ss.txt

# Running processes
ps auxf > /evidence/volatile/processes.txt
ls -la /proc/*/exe 2>/dev/null > /evidence/volatile/proc_exe.txt

# Open files
lsof > /evidence/volatile/lsof.txt

# Logged in users
w > /evidence/volatile/users.txt
last -aiF > /evidence/volatile/last.txt

# Network configuration
ip addr > /evidence/volatile/ip_addr.txt
ip route > /evidence/volatile/ip_route.txt
cat /etc/resolv.conf > /evidence/volatile/dns.txt

# ARP cache
arp -a > /evidence/volatile/arp.txt

# Loaded kernel modules
lsmod > /evidence/volatile/modules.txt

# Scheduled tasks
crontab -l > /evidence/volatile/crontab.txt
ls -la /etc/cron* > /evidence/volatile/cron_dirs.txt

# Environment variables
env > /evidence/volatile/env.txt
```

---

## Phase 2: Memory Analysis

### Volatility 3 (Python 3)
```bash
# Identify the OS profile
vol -f memory.raw banners.Banners
vol -f memory.raw windows.info.Info

# Process listing
vol -f memory.raw windows.pslist.PsList
vol -f memory.raw windows.pstree.PsTree
vol -f memory.raw windows.psscan.PsScan    # Find hidden processes

# Network connections
vol -f memory.raw windows.netscan.NetScan
vol -f memory.raw windows.netstat.NetStat

# DLL listing
vol -f memory.raw windows.dlllist.DllList --pid <PID>

# Command line arguments
vol -f memory.raw windows.cmdline.CmdLine

# Handles (files, registry, mutexes)
vol -f memory.raw windows.handles.Handles --pid <PID>

# Registry hives
vol -f memory.raw windows.registry.hivelist.HiveList

# Dump suspicious process memory
vol -f memory.raw windows.memmap.Memmap --pid <PID> --dump

# Malfind (find injected code)
vol -f memory.raw windows.malfind.Malfind

# SSDT hooks (rootkit detection)
vol -f memory.raw windows.ssdt.SSDT

# Linux-specific
vol -f memory.raw linux.pslist.PsList
vol -f memory.raw linux.bash.Bash          # Bash history from memory
vol -f memory.raw linux.lsof.Lsof
```

### Memory Analysis Checklist
- Identify suspicious processes: unusual names, wrong parent, running from temp directories
- Check for process injection: malfind, suspicious memory regions (RWX)
- Extract network indicators: C2 connections, DNS requests
- Recover command history: bash history, PowerShell commands
- Find credentials: strings search for passwords, tokens, keys
- Identify persistence: registry keys, scheduled tasks from memory
- Extract files from memory: executables, documents, scripts

---

## Phase 3: Disk and File System Analysis

### File System Timeline
```bash
# Create timeline with Sleuth Kit
fls -r -m "/" /evidence/disk.raw > bodyfile.txt
mactime -b bodyfile.txt -d > timeline.csv

# Create super-timeline with Plaso
log2timeline.py /evidence/plaso.dump /evidence/disk.raw
psort.py -o l2tcsv /evidence/plaso.dump -w /evidence/timeline.csv
```

### Key Locations (Linux)
| Location | Evidence |
|---|---|
| `/var/log/auth.log` | Authentication events, SSH logins, sudo usage |
| `/var/log/syslog` | System events, service starts, errors |
| `/var/log/apache2/` | Web server access and error logs |
| `/var/log/nginx/` | Nginx access and error logs |
| `/etc/passwd`, `/etc/shadow` | User accounts (check for additions) |
| `/etc/crontab`, `/var/spool/cron/` | Scheduled tasks |
| `/home/*/.bash_history` | User command history |
| `/home/*/.ssh/` | SSH keys, known_hosts, authorized_keys |
| `/tmp/`, `/dev/shm/` | Temporary files, attacker tools |
| `/etc/systemd/system/` | Systemd service files (persistence) |

### Key Locations (Windows)
| Location | Evidence |
|---|---|
| `C:\Windows\System32\winevt\Logs\` | Windows Event Logs |
| `C:\Users\*\NTUSER.DAT` | User registry hive (recent files, run keys) |
| `C:\Windows\Prefetch\` | Prefetch files (program execution history) |
| `C:\$MFT` | Master File Table (all file metadata) |
| `C:\$UsnJrnl` | USN Journal (file change log) |
| `C:\Windows\System32\config\` | SAM, SYSTEM, SOFTWARE registry hives |
| `C:\Users\*\AppData\Local\Temp\` | Temporary files, dropped malware |
| `C:\Windows\Tasks\` | Scheduled tasks |
| `C:\Users\*\AppData\Roaming\Microsoft\Windows\Recent\` | Recent file access (LNK files) |
| `C:\Users\*\AppData\Local\Microsoft\Windows\WebCache\` | Browser history (Edge/IE) |

### Windows Event Log Analysis
| Event ID | Log | Description |
|---|---|---|
| 4624 | Security | Successful logon |
| 4625 | Security | Failed logon |
| 4648 | Security | Explicit credential logon (runas, RDP) |
| 4672 | Security | Special privileges assigned (admin logon) |
| 4688 | Security | Process creation (if auditing enabled) |
| 4698/4702 | Security | Scheduled task created/updated |
| 4720 | Security | User account created |
| 4732 | Security | Member added to local group |
| 7045 | System | New service installed |
| 1102 | Security | Audit log cleared |
| 1 | Sysmon | Process creation with command line and hashes |
| 3 | Sysmon | Network connection |
| 11 | Sysmon | File creation |

### Deleted File Recovery
- Sleuth Kit: `tsk_recover -e /evidence/disk.raw /evidence/recovered/`
- PhotoRec: carve files by signature from raw disk
- Scalpel: configurable file carving
- Check for files in unallocated space, slack space

### Artifact Analysis Tools
- Autopsy: GUI for Sleuth Kit with automated analysis modules
- Eric Zimmerman tools (Windows): MFTECmd, PECmd, LECmd, EvtxECmd, RECmd
- RegRipper: extract information from Windows registry hives
- KAPE: automated artifact collection and processing

---

## Phase 4: Network Forensics

### PCAP Analysis
```bash
# Basic statistics
capinfos capture.pcap

# Extract conversations
tshark -r capture.pcap -q -z conv,tcp
tshark -r capture.pcap -q -z conv,ip

# Extract DNS queries
tshark -r capture.pcap -Y "dns.qr == 0" -T fields -e dns.qry.name | sort -u

# Extract HTTP requests
tshark -r capture.pcap -Y "http.request" -T fields -e http.host -e http.request.uri

# Extract files from HTTP
tshark -r capture.pcap --export-objects http,/evidence/http_objects/

# Extract TLS handshake info
tshark -r capture.pcap -Y "tls.handshake.type == 1" -T fields -e tls.handshake.extensions_server_name

# Follow a TCP stream
tshark -r capture.pcap -z "follow,tcp,ascii,0"
```

### Log Analysis
- Centralized logs: SIEM queries for suspicious patterns
- Web server logs: unusual user agents, SQL injection attempts, scanning patterns
- Firewall logs: blocked connections, allowed connections to unusual destinations
- DNS logs: domain generation algorithm (DGA) patterns, excessive queries, tunneling
- Authentication logs: brute force, credential stuffing, unusual login locations/times
- Email logs: phishing delivery, unusual attachments, forwarding rules

### Network IOC Extraction
- IP addresses: C2 servers, exfiltration destinations
- Domains: malicious domains, DGA domains
- URLs: malware download URLs, phishing pages
- User agents: custom or unusual user agents
- JA3/JA3S hashes: TLS fingerprints for malware identification
- DNS queries: encoded data in DNS queries (tunneling indicators)

---

## Phase 5: Timeline Reconstruction

### Timeline Building
1. Collect timestamps from all sources: file system, logs, memory, network
2. Normalize to UTC
3. Merge into single timeline (Plaso/log2timeline automates this)
4. Identify the initial compromise point (patient zero)
5. Map attacker activity chronologically
6. Identify data access and exfiltration windows
7. Determine persistence mechanisms and their installation time

### Pivot Points
- First known malicious activity
- Credential compromise events
- Lateral movement events
- Data access and staging
- Exfiltration events
- Persistence installation
- Anti-forensics activity (log clearing, timestomping)

---

## Phase 6: Reporting

### Incident Report Structure
1. **Executive Summary:** what happened, when, impact, current status
2. **Incident Timeline:** chronological narrative of the attack
3. **Scope of Compromise:** affected systems, accounts, data
4. **Root Cause:** how the attacker gained initial access
5. **Attack Path:** step-by-step progression through the environment
6. **Data Impact:** what data was accessed, exfiltrated, or destroyed
7. **IOCs:** hashes, IPs, domains, file names for detection
8. **Remediation Actions:** what was done to contain and eradicate
9. **Recommendations:** how to prevent recurrence
10. **Evidence Inventory:** list of all evidence collected with hashes

### IOC Documentation
| IOC Type | Value | Context |
|---|---|---|
| File Hash (SHA256) | [hash] | Malware sample from server |
| IP Address | [IP] | C2 server |
| Domain | [domain] | Phishing/C2 infrastructure |
| File Path | [path] | Persistence mechanism location |
| Registry Key | [key] | Autostart entry |
| Scheduled Task | [name] | Persistence mechanism |
| Mutex | [name] | Malware instance lock |
| User Account | [name] | Attacker-created account |

---

## Tools Quick Reference

| Task | Tools |
|---|---|
| Memory Acquisition | LiME, AVML, DumpIt, WinPMEM |
| Memory Analysis | Volatility 3, MemProcFS |
| Disk Acquisition | dd, dc3dd, FTK Imager |
| Disk Analysis | Autopsy, Sleuth Kit, X-Ways |
| Timeline | Plaso/log2timeline, mactime |
| Windows Artifacts | Eric Zimmerman tools, RegRipper, KAPE |
| Network | Wireshark, tshark, NetworkMiner, zeek |
| Log Analysis | ELK Stack, Splunk, chainsaw (Windows EVTX) |
| File Carving | PhotoRec, Scalpel, binwalk |
| Malware | VirusTotal, YARA, ssdeep, PEStudio |
| Automation | Velociraptor, GRR, TheHive |
