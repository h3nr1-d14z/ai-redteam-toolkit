Deep service enumeration on: $ARGUMENTS

## Pre-flight
- Confirm target IP/range is in scope for active enumeration
- Identify OS type if known (Windows/Linux) to prioritize protocols
- Ensure you have results from /scan-ports before deep enumeration

## Phase 1: NetBIOS & SMB Enumeration
1. NetBIOS: `nbtstat -A <ip>` (Windows) or `nmblookup -A <ip>` (Linux)
2. Enum4linux: `enum4linux -a <ip>` — users, shares, groups, OS info
3. SMB shares: `smbclient -L //<ip> -N` (null session)
4. SMB map: `smbmap -H <ip>` — permissions on shares
5. CrackMapExec: `crackmapexec smb <ip> --shares`
6. RPC: `rpcclient -U "" -N <ip>` → enumdomusers, enumdomgroups, querydominfo

## Phase 2: SNMP Enumeration
1. Community string brute: `onesixtyone -c wordlists/snmp-communities.txt <ip>`
2. SNMP walk: `snmpwalk -v2c -c <community> <ip> .1`
3. Key OIDs: system info (.1.3.6.1.2.1.1), interfaces (.1.3.6.1.2.1.2), routes, ARP
4. Users: `snmpwalk -v2c -c public <ip> 1.3.6.1.4.1.77.1.2.25`
5. Processes: `snmpwalk -v2c -c public <ip> 1.3.6.1.2.1.25.4.2.1.2`

## Phase 3: LDAP Enumeration
1. Base query: `ldapsearch -x -H ldap://<ip> -b "" -s base namingContexts`
2. Full dump: `ldapsearch -x -H ldap://<ip> -b "DC=domain,DC=local"`
3. Users: filter `(objectClass=user)` — extract sAMAccountName, description, memberOf
4. Computers: filter `(objectClass=computer)`
5. If authenticated: `ldapdomaindump -u 'DOMAIN\user' -p 'pass' <ip>`

## Phase 4: DNS Enumeration
1. Zone transfer: `dig axfr @<dns-server> <domain>`
2. Reverse lookup: `dig -x <ip> @<dns-server>`
3. Brute force: `dnsenum --dnsserver <dns-server> <domain>`
4. SRV records: `dig SRV _ldap._tcp.dc._msdcs.<domain> @<dns-server>`
5. Fierce: `fierce --domain <domain> --dns-servers <dns-server>`

## Phase 5: NFS & FTP
1. NFS exports: `showmount -e <ip>` → mount accessible shares
2. Mount: `mount -t nfs <ip>:/share /mnt/nfs`
3. FTP anonymous: `ftp <ip>` → anonymous / anonymous@
4. FTP enum: check for writable dirs, sensitive files, version vulns

## Tools
NetBIOS: nbtstat, nmblookup, enum4linux | SMB: smbclient, smbmap, crackmapexec
SNMP: snmpwalk, onesixtyone, snmp-check | LDAP: ldapsearch, ldapdomaindump
DNS: dig, dnsenum, fierce | NFS: showmount | FTP: ftp, nmap scripts

## Output
Save to engagements/<target>/recon/enumeration-<service>.md

## Framework Mapping
- MITRE ATT&CK: TA0007 (Discovery) → T1046 (Network Service Discovery), T1087 (Account Discovery)
- Cyber Kill Chain: Phase 2 — Reconnaissance
- CEH v12: Module 04 — Enumeration

## Safety
Only enumerate services on authorized targets. Null sessions may trigger alerts.
