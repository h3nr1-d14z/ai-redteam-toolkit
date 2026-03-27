# Volatility Memory Forensics Cheatsheet

## Volatility 3 (Python 3)

### Setup and Image Info

```bash
# Install
pip3 install volatility3

# Basic usage
vol -f memory.raw <plugin>

# Identify OS and profile (automatic in Vol3)
vol -f memory.raw windows.info
vol -f memory.raw linux.info
vol -f memory.raw mac.info

# List available plugins
vol --help
vol -f memory.raw windows.info --help   # Help for specific plugin

# Specify output format
vol -f memory.raw -r csv windows.pslist > processes.csv
vol -f memory.raw -r json windows.pslist > processes.json
vol -f memory.raw -r pretty windows.pslist   # Formatted table

# Symbol tables (download if needed)
vol -f memory.raw -s /path/to/symbols/ windows.info
```

---

### Process Analysis

```bash
# List processes
vol -f memory.raw windows.pslist
vol -f memory.raw windows.pslist --pid 1234

# Process tree (parent/child relationships)
vol -f memory.raw windows.pstree

# Process scan (find hidden/unlinked processes)
vol -f memory.raw windows.psscan

# Command line arguments for each process
vol -f memory.raw windows.cmdline
vol -f memory.raw windows.cmdline --pid 1234

# Environment variables
vol -f memory.raw windows.envars
vol -f memory.raw windows.envars --pid 1234

# Process privileges
vol -f memory.raw windows.privileges
vol -f memory.raw windows.privileges --pid 1234

# DLLs loaded by process
vol -f memory.raw windows.dlllist
vol -f memory.raw windows.dlllist --pid 1234

# Process handles (files, registry, mutexes)
vol -f memory.raw windows.handles
vol -f memory.raw windows.handles --pid 1234

# SIDs associated with processes
vol -f memory.raw windows.getsids
vol -f memory.raw windows.getsids --pid 1234

# Dump process executable
vol -f memory.raw windows.pslist --pid 1234 --dump
vol -f memory.raw windows.dumpfiles --pid 1234
```

---

### Network Analysis

```bash
# Network connections and listening ports
vol -f memory.raw windows.netscan

# Netstat equivalent
vol -f memory.raw windows.netstat

# Filter by state (look for ESTABLISHED, LISTENING)
vol -f memory.raw windows.netscan | grep ESTABLISHED
vol -f memory.raw windows.netscan | grep LISTENING
vol -f memory.raw windows.netscan | grep -v CLOSED
```

---

### File System

```bash
# Scan for file objects in memory
vol -f memory.raw windows.filescan

# Search for specific files
vol -f memory.raw windows.filescan | grep -i password
vol -f memory.raw windows.filescan | grep -i '\.doc\|\.xls\|\.pdf\|\.txt\|\.kdbx'
vol -f memory.raw windows.filescan | grep -i '\\Desktop\\'

# Dump files from memory
vol -f memory.raw windows.dumpfiles --virtaddr 0xfa8002a5b070
vol -f memory.raw windows.dumpfiles --physaddr 0x00000000a5b070

# MFT parsing (NTFS Master File Table)
vol -f memory.raw windows.mftscan.MFTScan
```

---

### Malware Detection

```bash
# Find injected code and suspicious memory regions
vol -f memory.raw windows.malfind
vol -f memory.raw windows.malfind --pid 1234
vol -f memory.raw windows.malfind --dump    # Dump suspicious regions

# What to look for in malfind output:
#   PAGE_EXECUTE_READWRITE (RWX) protection = injected code
#   MZ header (4d 5a) at start = PE injected into memory
#   Shellcode patterns (fc e8, eb fe, etc.)

# Check for API hooking (SSDT)
vol -f memory.raw windows.ssdt

# Loaded kernel modules
vol -f memory.raw windows.modules
vol -f memory.raw windows.modscan    # Scan for unlinked modules

# Driver IRP hooks
vol -f memory.raw windows.driverscan

# Callbacks (registered kernel callbacks)
vol -f memory.raw windows.callbacks

# Services
vol -f memory.raw windows.svcscan

# Scheduled tasks
vol -f memory.raw windows.scheduled_tasks
```

---

### Credential Extraction

```bash
# Dump password hashes (SAM)
vol -f memory.raw windows.hashdump

# Dump LSA secrets
vol -f memory.raw windows.lsadump

# Dump cached domain credentials
vol -f memory.raw windows.cachedump

# Registry hive list
vol -f memory.raw windows.hivelist

# Read specific registry keys
vol -f memory.raw windows.printkey
vol -f memory.raw windows.printkey --key 'Software\Microsoft\Windows\CurrentVersion\Run'
vol -f memory.raw windows.printkey --key 'SAM\Domains\Account\Users'
vol -f memory.raw windows.printkey --key 'SYSTEM\CurrentControlSet\Services'

# Dump registry hives
vol -f memory.raw windows.hivelist          # Get hive offsets
vol -f memory.raw windows.dumpfiles --virtaddr 0xXXXX   # Dump hive file
```

---

### Timeline and Miscellaneous

```bash
# Create timeline of all events
vol -f memory.raw timeliner.Timeliner > timeline.csv

# Clipboard contents
vol -f memory.raw windows.clipboard

# Screenshots (from GDI)
vol -f memory.raw windows.screenshot --dump

# Symlinks
vol -f memory.raw windows.symlinkscan

# Mutant/Mutex objects (malware IOCs)
vol -f memory.raw windows.mutantscan

# Virtual address descriptor (memory maps)
vol -f memory.raw windows.vadinfo --pid 1234
vol -f memory.raw windows.vadwalk --pid 1234
```

---

## Volatility 2 (Python 2 — Legacy)

### Image Identification

```bash
# Identify OS profile
vol.py -f memory.raw imageinfo

# Suggested profiles output: Win7SP1x64, Win2008R2SP1x64, etc.
# Use the first suggested profile:
vol.py -f memory.raw --profile=Win7SP1x64 <plugin>

# KDBGScan (alternative profile detection)
vol.py -f memory.raw kdbgscan
```

---

### Process Analysis (Vol2)

```bash
# List processes
vol.py -f memory.raw --profile=Win7SP1x64 pslist

# Process tree
vol.py -f memory.raw --profile=Win7SP1x64 pstree

# Hidden process scan
vol.py -f memory.raw --profile=Win7SP1x64 psscan

# Compare pslist vs psscan to find hidden processes:
# Processes in psscan but NOT in pslist = potentially hidden by rootkit

# Command lines
vol.py -f memory.raw --profile=Win7SP1x64 cmdline

# DLL list
vol.py -f memory.raw --profile=Win7SP1x64 dlllist -p 1234

# Dump process memory
vol.py -f memory.raw --profile=Win7SP1x64 procdump -p 1234 -D /tmp/dump/

# Dump process address space
vol.py -f memory.raw --profile=Win7SP1x64 memdump -p 1234 -D /tmp/dump/

# Strings from process memory
vol.py -f memory.raw --profile=Win7SP1x64 memdump -p 1234 -D /tmp/
strings /tmp/1234.dmp | grep -i password
strings -el /tmp/1234.dmp | grep -i password   # Wide strings (UTF-16)
```

---

### Network (Vol2)

```bash
# XP/2003
vol.py -f memory.raw --profile=WinXPSP3x86 connections
vol.py -f memory.raw --profile=WinXPSP3x86 connscan
vol.py -f memory.raw --profile=WinXPSP3x86 sockets
vol.py -f memory.raw --profile=WinXPSP3x86 sockscan

# Vista+/7/8/10
vol.py -f memory.raw --profile=Win7SP1x64 netscan
```

---

### Files and Registry (Vol2)

```bash
# Scan for file objects
vol.py -f memory.raw --profile=Win7SP1x64 filescan

# Dump a file by offset
vol.py -f memory.raw --profile=Win7SP1x64 dumpfiles -Q 0x000000003e8ad250 -D /tmp/dump/
# -n to include filename in output

# Registry hives
vol.py -f memory.raw --profile=Win7SP1x64 hivelist

# Print registry key
vol.py -f memory.raw --profile=Win7SP1x64 printkey -K 'Software\Microsoft\Windows\CurrentVersion\Run'
vol.py -f memory.raw --profile=Win7SP1x64 printkey -K 'SAM\Domains\Account\Users\Names'

# Dump registry hive by offset
vol.py -f memory.raw --profile=Win7SP1x64 hivedump -o 0x8a8001c8 -D /tmp/dump/

# Search for registry keys by name
vol.py -f memory.raw --profile=Win7SP1x64 printkey -K 'ControlSet001\Services' | grep -i malware
```

---

### Malware Analysis (Vol2)

```bash
# Injected code detection
vol.py -f memory.raw --profile=Win7SP1x64 malfind -D /tmp/dump/
vol.py -f memory.raw --profile=Win7SP1x64 malfind -p 1234

# SSDT hooks
vol.py -f memory.raw --profile=Win7SP1x64 ssdt | grep -v 'ntoskrnl\|win32k'

# Inline API hooks
vol.py -f memory.raw --profile=Win7SP1x64 apihooks -p 1234

# IDT (Interrupt Descriptor Table)
vol.py -f memory.raw --profile=Win7SP1x64 idt

# Driver objects
vol.py -f memory.raw --profile=Win7SP1x64 driverscan
vol.py -f memory.raw --profile=Win7SP1x64 driverirp

# Loaded modules
vol.py -f memory.raw --profile=Win7SP1x64 modules
vol.py -f memory.raw --profile=Win7SP1x64 modscan    # Find unlinked modules

# Dump kernel module
vol.py -f memory.raw --profile=Win7SP1x64 moddump -b 0xXXXXXXXX -D /tmp/dump/
```

---

### Credential Extraction (Vol2)

```bash
# SAM hashes
vol.py -f memory.raw --profile=Win7SP1x64 hashdump
# Output: Administrator:500:aad3b435...:31d6cfe0...:::

# LSA secrets
vol.py -f memory.raw --profile=Win7SP1x64 lsadump

# Cached domain logons
vol.py -f memory.raw --profile=Win7SP1x64 cachedump

# Mimikatz plugin (extract plaintext if WDigest enabled)
vol.py -f memory.raw --profile=Win7SP1x64 mimikatz
# Requires volatility mimikatz plugin installed
```

---

### Console History (Vol2)

```bash
# Command history (cmd.exe)
vol.py -f memory.raw --profile=Win7SP1x64 cmdscan
vol.py -f memory.raw --profile=Win7SP1x64 consoles

# cmdscan = command history buffer
# consoles = full console input/output including screen content
```

---

## Malware Analysis Workflow

```bash
# 1. Identify suspicious processes
vol -f memory.raw windows.pstree          # Look for unusual parent/child
vol -f memory.raw windows.malfind         # Find injected code

# 2. Check process details
vol -f memory.raw windows.cmdline --pid SUSPECT_PID
vol -f memory.raw windows.dlllist --pid SUSPECT_PID
vol -f memory.raw windows.handles --pid SUSPECT_PID

# 3. Check network activity
vol -f memory.raw windows.netscan | grep SUSPECT_PID

# 4. Dump suspicious process
vol -f memory.raw windows.pslist --pid SUSPECT_PID --dump
vol -f memory.raw windows.malfind --pid SUSPECT_PID --dump

# 5. Analyze dumped binary
file pid.SUSPECT_PID.*.dmp
strings pid.SUSPECT_PID.*.dmp | grep -i 'http\|cmd\|exec\|shell\|password'
sha256sum pid.SUSPECT_PID.*.dmp          # Check on VirusTotal

# 6. Check persistence
vol -f memory.raw windows.printkey --key 'Software\Microsoft\Windows\CurrentVersion\Run'
vol -f memory.raw windows.svcscan | grep -i SUSPECT
vol -f memory.raw windows.scheduled_tasks

# 7. Extract IOCs
# IPs from netscan
# Domains from strings
# File paths from handles/filescan
# Registry keys from printkey
# Mutexes from mutantscan
```

---

## Linux Memory Analysis

```bash
# Volatility 3 Linux plugins
vol -f memory.lime linux.bash           # Bash history
vol -f memory.lime linux.pslist         # Process list
vol -f memory.lime linux.pstree         # Process tree
vol -f memory.lime linux.lsmod          # Loaded kernel modules
vol -f memory.lime linux.lsof           # Open files
vol -f memory.lime linux.sockstat       # Network sockets
vol -f memory.lime linux.malfind        # Injected code
vol -f memory.lime linux.check_syscall  # Syscall table hooks
vol -f memory.lime linux.check_idt      # IDT hooks
vol -f memory.lime linux.tty_check      # TTY devices
vol -f memory.lime linux.keyboard_notifiers  # Keylogger detection
vol -f memory.lime linux.proc.Maps --pid 1234  # Process memory maps

# Acquire Linux memory (on live system)
sudo insmod lime.ko "path=/tmp/memory.lime format=lime"
```

---

## Quick Reference — Suspicious Indicators

| Indicator | What It Means | Plugin |
|-----------|--------------|--------|
| Process in psscan but not pslist | Hidden process (DKOM rootkit) | psscan vs pslist |
| RWX memory region with MZ header | Injected PE in process | malfind |
| svchost.exe not child of services.exe | Fake svchost (malware) | pstree |
| csrss.exe/lsass.exe more than one instance | Impersonation | pslist |
| Unusual parent for cmd.exe/powershell.exe | Likely exploitation | pstree |
| ESTABLISHED connection to unusual IP | C2 communication | netscan |
| Module in modscan but not modules | Hidden kernel module | modscan vs modules |
| Non-Microsoft entry in SSDT | Kernel hook | ssdt |
| Run key with unknown binary | Persistence | printkey |
| Process with no command line | Potentially injected | cmdline |
