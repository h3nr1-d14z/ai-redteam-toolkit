# Network Enumeration Methodology

> Based on CEH Module 04 — Enumeration Techniques

## Overview

Enumeration is the active phase of extracting usernames, machine names, shares, services, and other resources from a target network. Unlike scanning, enumeration involves active connections and directed queries against target systems.

**Prerequisites**: Completed host discovery and port scanning. You know which hosts are alive and which ports/services are open.

---

## Phase 1: NetBIOS Enumeration (TCP 137-139, UDP 137)

NetBIOS exposes machine names, domain/workgroup info, logged-in users, and MAC addresses.

### Windows Native

```bash
# Query NetBIOS name table of a remote host
nbtstat -A 10.10.10.5

# Interpret suffix codes:
#   <00> = Workstation Service (hostname)
#   <03> = Messenger Service (username)
#   <20> = File Server Service (shares available)
#   <1B> = Domain Master Browser
#   <1D> = Master Browser
#   <1E> = Browser Service Elections
```

### enum4linux (Linux)

```bash
# Full enumeration against a target
enum4linux -a 10.10.10.5

# Specific enumerations
enum4linux -U 10.10.10.5    # Users
enum4linux -S 10.10.10.5    # Shares
enum4linux -G 10.10.10.5    # Groups
enum4linux -P 10.10.10.5    # Password policy
enum4linux -o 10.10.10.5    # OS information

# With credentials
enum4linux -u 'admin' -p 'password' -a 10.10.10.5
```

### nbtscan

```bash
# Scan a range for NetBIOS names
nbtscan 10.10.10.0/24
nbtscan -r 10.10.10.0/24   # Use local port 137 for scan

# Verbose output with full name table
nbtscan -v -s : 10.10.10.0/24
```

**What to look for**: Hostnames, domain names, users currently logged in, services running (especially <20> indicating file sharing is active).

---

## Phase 2: SNMP Enumeration (UDP 161/162)

SNMP can leak system info, interfaces, routing tables, software, user accounts, and network connections when community strings are known or default.

### Discovery — Brute Force Community Strings

```bash
# Fast community string brute force
onesixtyone -c /usr/share/seclists/Discovery/SNMP/snmp-onesixtyone.txt 10.10.10.5

# Scan a range
onesixtyone -c community.txt -i targets.txt
```

### snmpwalk — Walk the MIB Tree

```bash
# Walk entire tree with SNMPv2c using 'public' community string
snmpwalk -v2c -c public 10.10.10.5

# Targeted OID walks
snmpwalk -v2c -c public 10.10.10.5 1.3.6.1.2.1.25.1.6.0    # System processes
snmpwalk -v2c -c public 10.10.10.5 1.3.6.1.4.1.77.1.2.25    # Windows users
snmpwalk -v2c -c public 10.10.10.5 1.3.6.1.2.1.25.4.2.1.2   # Running programs
snmpwalk -v2c -c public 10.10.10.5 1.3.6.1.2.1.6.13.1.3     # TCP open ports
snmpwalk -v2c -c public 10.10.10.5 1.3.6.1.2.1.25.6.3.1.2   # Installed software
snmpwalk -v2c -c public 10.10.10.5 1.3.6.1.2.1.2.2           # Network interfaces

# SNMPv3 (requires credentials)
snmpwalk -v3 -u admin -l authPriv -a SHA -A 'authpass' -x AES -X 'privpass' 10.10.10.5
```

### snmp-check — Formatted Output

```bash
# Automated enumeration with readable output
snmp-check 10.10.10.5
snmp-check -c public -v 2c 10.10.10.5
```

**What to look for**: Default community strings (public/private), user accounts, installed software (patch levels), network configuration, running processes.

---

## Phase 3: LDAP Enumeration (TCP 389/636)

LDAP is the backbone of Active Directory. Anonymous or low-privilege LDAP queries can reveal the entire directory structure.

### ldapsearch

```bash
# Anonymous bind — retrieve base naming contexts
ldapsearch -x -H ldap://10.10.10.5 -s base namingContexts

# Dump entire directory (anonymous)
ldapsearch -x -H ldap://10.10.10.5 -b "DC=corp,DC=local"

# Enumerate users
ldapsearch -x -H ldap://10.10.10.5 -b "DC=corp,DC=local" "(objectClass=user)" \
  sAMAccountName description memberOf userAccountControl

# Find accounts with no pre-authentication (AS-REP roastable)
ldapsearch -x -H ldap://10.10.10.5 -b "DC=corp,DC=local" \
  "(userAccountControl:1.2.840.113556.1.4.803:=4194304)" sAMAccountName

# Find accounts with SPNs set (Kerberoastable)
ldapsearch -x -H ldap://10.10.10.5 -b "DC=corp,DC=local" \
  "(servicePrincipalName=*)" sAMAccountName servicePrincipalName

# Authenticated query
ldapsearch -x -H ldap://10.10.10.5 -D "CN=user,DC=corp,DC=local" -w 'password' \
  -b "DC=corp,DC=local" "(objectClass=computer)" cn operatingSystem
```

### windapsearch (Python)

```bash
# Enumerate users
windapsearch -d corp.local --dc 10.10.10.5 -U

# Enumerate groups
windapsearch -d corp.local --dc 10.10.10.5 -G

# Enumerate computers
windapsearch -d corp.local --dc 10.10.10.5 -C

# Find Domain Admins
windapsearch -d corp.local --dc 10.10.10.5 -m "Domain Admins"

# Authenticated
windapsearch -d corp.local --dc 10.10.10.5 -u 'user@corp.local' -p 'password' --da
```

**What to look for**: Usernames, group memberships (Domain Admins, Enterprise Admins), computer accounts, SPNs, description fields (often contain passwords), disabled accounts, password policies.

---

## Phase 4: DNS Enumeration (TCP/UDP 53)

DNS can reveal hostnames, subdomains, mail servers, and network architecture.

### dig

```bash
# Zone transfer attempt
dig axfr corp.local @10.10.10.5

# Standard queries
dig A corp.local @10.10.10.5
dig MX corp.local @10.10.10.5
dig NS corp.local @10.10.10.5
dig TXT corp.local @10.10.10.5
dig ANY corp.local @10.10.10.5

# Reverse lookup
dig -x 10.10.10.5 @10.10.10.5

# SRV records for AD services
dig SRV _ldap._tcp.dc._msdcs.corp.local @10.10.10.5
dig SRV _kerberos._tcp.corp.local @10.10.10.5
dig SRV _gc._tcp.corp.local @10.10.10.5
```

### dnsenum

```bash
# Full DNS enumeration with brute force
dnsenum corp.local --dnsserver 10.10.10.5

# With custom wordlist and threads
dnsenum corp.local --dnsserver 10.10.10.5 -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt --threads 10
```

### dnsrecon

```bash
# Standard enumeration
dnsrecon -d corp.local -n 10.10.10.5

# Zone transfer
dnsrecon -d corp.local -n 10.10.10.5 -t axfr

# Brute force subdomains
dnsrecon -d corp.local -n 10.10.10.5 -t brt -D /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# Reverse lookup on a range
dnsrecon -r 10.10.10.0/24 -n 10.10.10.5
```

### fierce

```bash
# DNS reconnaissance and brute force
fierce --domain corp.local --dns-servers 10.10.10.5
fierce --domain corp.local --subdomain-file /usr/share/seclists/Discovery/DNS/fierce-hostlist.txt
```

**What to look for**: Successful zone transfers (full DNS dump), subdomains, internal hostnames, mail servers, SPF/DKIM/DMARC records, SRV records revealing AD infrastructure.

---

## Phase 5: SMB Enumeration (TCP 139/445)

SMB shares, users, and sessions provide direct avenues for access and lateral movement.

### smbclient

```bash
# List shares (null session)
smbclient -L //10.10.10.5 -N

# List shares (authenticated)
smbclient -L //10.10.10.5 -U 'user%password'

# Connect to a share
smbclient //10.10.10.5/share_name -N
smbclient //10.10.10.5/share_name -U 'user%password'

# Useful commands once connected: ls, cd, get, put, mget, recurse ON, prompt OFF
```

### smbmap

```bash
# Check share permissions (null session)
smbmap -H 10.10.10.5

# Authenticated
smbmap -H 10.10.10.5 -u 'user' -p 'password' -d corp.local

# Recursive listing of a share
smbmap -H 10.10.10.5 -u 'user' -p 'password' -R 'share_name'

# Download a file
smbmap -H 10.10.10.5 -u 'user' -p 'password' --download 'share_name\path\file.txt'

# Search for files
smbmap -H 10.10.10.5 -u 'user' -p 'password' -R 'share_name' -A '\.config$|password|\.kdbx$'
```

### CrackMapExec (NetExec)

```bash
# SMB enumeration across a range
crackmapexec smb 10.10.10.0/24

# Enumerate shares
crackmapexec smb 10.10.10.5 -u 'user' -p 'password' --shares

# Enumerate users via RID brute force
crackmapexec smb 10.10.10.5 -u '' -p '' --rid-brute

# Check for signing (important for relay attacks)
crackmapexec smb 10.10.10.0/24 --gen-relay-list nosigning.txt

# Enumerate sessions, disks, logged-on users
crackmapexec smb 10.10.10.5 -u 'user' -p 'password' --sessions
crackmapexec smb 10.10.10.5 -u 'user' -p 'password' --disks
crackmapexec smb 10.10.10.5 -u 'user' -p 'password' --loggedon-users
```

**What to look for**: Writable shares, sensitive files (configs, scripts, backups), SMB signing disabled (relay opportunity), null session access, guest access.

---

## Phase 6: NTP Enumeration (UDP 123)

NTP can reveal connected clients, system time (useful for Kerberos attacks), and internal IPs.

```bash
# Query NTP server for its peers
ntpq -p 10.10.10.5

# List monitored hosts (shows clients that have queried this NTP server)
ntpdc -n -c monlist 10.10.10.5

# Get NTP server variables
ntpdc -c sysinfo 10.10.10.5

# Nmap NTP scripts
nmap -sU -p 123 --script ntp-info,ntp-monlist 10.10.10.5
```

**What to look for**: Internal IP addresses of NTP clients, system time offset (critical for Kerberos), NTP server version (vulnerabilities).

---

## Phase 7: SMTP Enumeration (TCP 25)

SMTP user enumeration reveals valid email addresses and usernames.

```bash
# Manual VRFY (verify user exists)
telnet 10.10.10.5 25
HELO test
VRFY admin
VRFY root
VRFY user

# Manual EXPN (expand mailing list)
EXPN postmaster

# Manual RCPT TO (check recipient acceptance)
MAIL FROM:<test@test.com>
RCPT TO:<admin@corp.local>

# Automated with smtp-user-enum
smtp-user-enum -M VRFY -U /usr/share/seclists/Usernames/top-usernames-shortlist.txt -t 10.10.10.5
smtp-user-enum -M RCPT -U users.txt -D corp.local -t 10.10.10.5
smtp-user-enum -M EXPN -U users.txt -t 10.10.10.5

# Nmap SMTP scripts
nmap -p 25 --script smtp-enum-users,smtp-commands,smtp-open-relay 10.10.10.5
```

**What to look for**: Valid usernames, open relay status, supported commands, mail server version.

---

## Phase 8: RPC Enumeration (TCP 135/111)

RPC provides access to Windows management functions and Unix NFS/NIS services.

### Windows RPC (via SMB)

```bash
# Connect with null session
rpcclient -U "" -N 10.10.10.5

# Inside rpcclient:
srvinfo              # Server info
enumdomusers         # List domain users
enumdomgroups        # List domain groups
querygroup 0x200     # Query Domain Admins (RID 0x200 = 512)
querygroupmem 0x200  # Members of Domain Admins
queryuser 0x1f4      # Query Administrator (RID 0x1f4 = 500)
enumprivs            # Enumerate privileges
getdompwinfo         # Password policy
enumprinters         # List printers (can contain info in comments)
netshareenumall      # List all shares

# RPC endpoint mapper
rpcinfo -p 10.10.10.5
```

### Impacket RPC Tools

```bash
# RPC endpoint mapper
impacket-rpcdump 10.10.10.5
impacket-rpcdump 10.10.10.5 | grep -i 'MS-EFSRPC\|MS-RPRN\|MS-PAR'

# SAM account enumeration
impacket-samrdump 10.10.10.5

# With credentials
impacket-samrdump corp.local/user:password@10.10.10.5
```

**What to look for**: User accounts and RIDs, group memberships, password policies, printers (PetitPotam/PrinterBug), service endpoints (MS-EFSRPC for coercion attacks).

---

## Output Analysis Checklist

After completing enumeration, organize findings:

| Category | Data Collected | Next Action |
|----------|---------------|-------------|
| Usernames | List of valid users | Password attacks, AS-REP roast |
| Shares | Accessible SMB shares | Browse for sensitive data |
| Services | Running services + versions | CVE lookup, exploit search |
| DNS | Hostnames, subdomains | Expand attack surface |
| Password Policy | Lockout threshold, complexity | Tune password spray |
| Groups | Privileged group members | Target high-value accounts |
| SPNs | Service Principal Names | Kerberoasting |
| SMB Signing | Hosts without signing | NTLM relay attacks |

---

## Quick Reference — Nmap NSE Scripts for Enumeration

```bash
# SMB
nmap --script smb-enum-shares,smb-enum-users,smb-os-discovery -p 445 10.10.10.5

# SNMP
nmap -sU -p 161 --script snmp-brute,snmp-info,snmp-interfaces,snmp-processes 10.10.10.5

# LDAP
nmap -p 389 --script ldap-rootdse,ldap-search 10.10.10.5

# DNS
nmap -p 53 --script dns-zone-transfer --script-args dns-zone-transfer.domain=corp.local 10.10.10.5

# SMTP
nmap -p 25 --script smtp-enum-users --script-args smtp-enum-users.methods={VRFY,EXPN,RCPT} 10.10.10.5

# RPC
nmap -p 111 --script rpcinfo 10.10.10.5
nmap -p 135 --script msrpc-enum 10.10.10.5
```
