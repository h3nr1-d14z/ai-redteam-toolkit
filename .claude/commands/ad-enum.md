Active Directory enumeration on: $ARGUMENTS

## Pre-flight
- Confirm AD environment is in scope for enumeration
- Determine access level: unauthenticated, low-privilege domain user, or admin
- Identify Domain Controller IP(s) and domain name
- Verify network connectivity to DC (ports 88, 389, 445, 636)

## Phase 1: Unauthenticated Enumeration
1. **Kerbrute user enum**: `kerbrute userenum -d <domain> --dc <dc-ip> users.txt`
2. **Null session SMB**: `crackmapexec smb <dc-ip> --shares -u '' -p ''`
3. **LDAP anonymous**: `ldapsearch -x -H ldap://<dc-ip> -b "" -s base`
4. **DNS**: `dig @<dc-ip> _ldap._tcp.dc._msdcs.<domain> SRV`
5. **Enum4linux-ng**: `enum4linux-ng -A <dc-ip>`
6. **RPC null**: `rpcclient -U '' -N <dc-ip>` then enumdomusers

## Phase 2: Authenticated Enumeration (Domain User)
1. **BloodHound collection**: `SharpHound.exe -c All,GPOLocalGroup --outputdirectory /tmp/`
   - Or: `bloodhound-python -c All -u <user> -p <pass> -d <domain> -dc <dc>`
2. **PowerView**:
   - Users: `Get-DomainUser | select samaccountname,description,memberof`
   - Groups: `Get-DomainGroup -AdminCount | select name`
   - Computers: `Get-DomainComputer | select dnshostname,operatingsystem`
   - Shares: `Find-DomainShare -CheckShareAccess`
   - ACLs: `Find-InterestingDomainAcl -ResolveGUIDs`
   - GPOs: `Get-DomainGPO | select displayname,gpcfilesyspath`
3. **CrackMapExec**:
   - Users: `crackmapexec smb <dc> -u <user> -p <pass> --users`
   - Shares: `crackmapexec smb <dc> -u <user> -p <pass> --shares`
   - Sessions: `crackmapexec smb <range> -u <user> -p <pass> --sessions`
   - Pass policy: `crackmapexec smb <dc> -u <user> -p <pass> --pass-pol`

## Phase 3: Kerberos Enumeration
1. **SPNs** (Kerberoast targets): `GetUserSPNs.py <domain>/<user>:<pass> -dc-ip <dc>`
2. **AS-REP roastable**: `GetNPUsers.py <domain>/ -usersfile users.txt -dc-ip <dc>`
3. **Delegation**: `Get-DomainComputer -TrustedToAuth | select dnshostname,msds-allowedtodelegateto`
4. **Constrained delegation**: find accounts with delegation rights

## Phase 4: Trust and Forest Mapping
1. **Trusts**: `Get-DomainTrust` or `nltest /domain_trusts /all_trusts`
2. **Forest trusts**: `Get-ForestTrust`
3. **Foreign group members**: `Get-DomainForeignGroupMember`
4. **SID history**: check for cross-domain privilege escalation paths

## Phase 5: BloodHound Analysis
1. Import SharpHound data into BloodHound GUI
2. Run built-in queries: Shortest Path to DA, Kerberoastable Users, AS-REP Roastable
3. Mark owned users/computers
4. Find attack paths: owned -> DA
5. Check: DCSync rights, GenericAll/WriteDACL on high-value targets

## Tools
BloodHound + SharpHound, PowerView/PowerSploit, CrackMapExec/NetExec
Impacket (GetUserSPNs, GetNPUsers, secretsdump), kerbrute, enum4linux-ng
ldapsearch, rpcclient, ADRecon

## Output
Save to engagements/<target>/recon/ad-enumeration.md with attack path diagram.

## Framework Mapping
- MITRE ATT&CK: TA0007 (Discovery) -> T1087.002 (Account Discovery: Domain Account)
- MITRE ATT&CK: T1069.002 (Permission Groups: Domain Groups)
- MITRE ATT&CK: T1018 (Remote System Discovery), T1482 (Domain Trust Discovery)
- Cyber Kill Chain: Phase 2 -- Reconnaissance (internal)
- CEH v12: Module 06 -- System Hacking / OSCP AD Methodology

## Safety
Enumeration may trigger alerts. Coordinate with Blue Team if in purple team exercise.
