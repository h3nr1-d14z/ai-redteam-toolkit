# BloodHound Cheatsheet

## Setup

```bash
# Install Neo4j (BloodHound backend database)
# Debian/Ubuntu:
sudo apt install neo4j
# macOS:
brew install neo4j

# Start Neo4j
sudo neo4j console
# Default creds: neo4j / neo4j (change on first login at http://localhost:7474)

# Start BloodHound GUI
./BloodHound --no-sandbox
# Login with Neo4j credentials (bolt://localhost:7687)

# BloodHound CE (Community Edition — newer, web-based)
# Docker:
curl -L https://ghst.ly/getbhce | docker compose -f - up
# Access at http://localhost:8080
```

---

## Data Collection — SharpHound (Windows)

```powershell
# Full collection (all methods)
.\SharpHound.exe -c all
.\SharpHound.exe -c all --zipfilename collection.zip

# Collection methods breakdown:
#   Default     = Group, LocalAdmin, Session, Trusts, ACL, Container, ObjectProps
#   All         = Default + GPOLocalGroup, SPNTargets, DCOnly
#   DCOnly      = ACL, Container, Group, ObjectProps, Trusts (queries DC only, stealthier)
#   Session     = Session data (who is logged in where)
#   LoggedOn    = Privileged session collection (needs admin on targets)
#   ComputerOnly = LocalAdmin, Session, ObjectProps per computer

# Stealth — DC only (no touching workstations)
.\SharpHound.exe -c DCOnly --zipfilename stealth.zip

# Target specific domain
.\SharpHound.exe -c all -d corp.local --ldapusername user --ldappassword pass

# Exclude Domain Controllers from session collection
.\SharpHound.exe -c all --excludedcs

# Loop session collection every 10 minutes for 2 hours
.\SharpHound.exe -c Session --loop --loopinterval 00:10:00 --loopduration 02:00:00

# Run from non-domain-joined machine (runas)
runas /netonly /user:CORP\user "SharpHound.exe -c all"

# PowerShell version
Import-Module .\SharpHound.ps1
Invoke-BloodHound -CollectionMethod All -OutputDirectory C:\temp -ZipFileName collection.zip
Invoke-BloodHound -CollectionMethod DCOnly -Stealth
```

---

## Data Collection — bloodhound-python (Linux)

```bash
# Full collection (from Linux, no domain join required)
bloodhound-python -u 'user' -p 'password' -d corp.local -ns 10.10.10.5 -c all

# Specify DC explicitly
bloodhound-python -u 'user' -p 'password' -d corp.local -dc dc01.corp.local -c all

# Use NTLM hash instead of password
bloodhound-python -u 'user' --hashes 'LM:NT' -d corp.local -ns 10.10.10.5 -c all

# Specific collection methods
bloodhound-python -u 'user' -p 'password' -d corp.local -ns 10.10.10.5 -c group,localadmin,session,acl,trusts

# Output as ZIP
bloodhound-python -u 'user' -p 'password' -d corp.local -ns 10.10.10.5 -c all --zip

# Use Kerberos authentication
bloodhound-python -u 'user' -p 'password' -d corp.local -dc dc01.corp.local -c all --auth-method kerberos

# DNS resolution via specific server
bloodhound-python -u 'user' -p 'password' -d corp.local -ns 10.10.10.5 -c all --dns-tcp
```

---

## Import Data

```
# BloodHound Legacy (Electron app):
# 1. Click the upload icon (up arrow) in the top right
# 2. Select the ZIP file or individual JSON files
# 3. Wait for import to complete

# BloodHound CE (web):
# 1. Go to File Ingest panel
# 2. Upload ZIP file
# 3. Monitor import progress

# Verify data loaded:
# Click the hamburger menu > Database Info
# Check: Users, Computers, Groups, Sessions, ACLs counts
```

---

## Built-In Queries

### High-Value Targets

```
# Find all Domain Admins
MATCH (g:Group) WHERE g.name =~ '(?i).*DOMAIN ADMINS.*' MATCH (g)<-[:MemberOf*1..]-(u) RETURN u.name

# Find Shortest Path to Domain Admins
# GUI: Click "Find Shortest Paths to Domain Admins" in Analysis tab
# Cypher:
MATCH p=shortestPath((u {owned:true})-[*1..]->(g:Group {name:'DOMAIN ADMINS@CORP.LOCAL'})) RETURN p

# Shortest path from owned principals to Domain Admins
MATCH p=shortestPath((u {owned:true})-[r*1..]->(g:Group {name:'DOMAIN ADMINS@CORP.LOCAL'}))
WHERE NONE(rel IN r WHERE type(rel) = 'MemberOf') OR ALL(rel IN r WHERE type(rel) = 'MemberOf')
RETURN p
```

### Kerberos Attacks

```
# Kerberoastable users (users with SPNs)
MATCH (u:User) WHERE u.hasspn = true RETURN u.name, u.serviceprincipalnames

# Kerberoastable users that are admins
MATCH (u:User {hasspn:true})-[:MemberOf*1..]->(g:Group {highvalue:true}) RETURN u.name, g.name

# AS-REP Roastable users (no pre-auth required)
MATCH (u:User) WHERE u.dontreqpreauth = true RETURN u.name

# AS-REP Roastable users that are admins
MATCH (u:User {dontreqpreauth:true})-[:MemberOf*1..]->(g:Group {highvalue:true}) RETURN u.name, g.name
```

### Delegation

```
# Unconstrained delegation computers (exclude DCs)
MATCH (c:Computer {unconstraineddelegation:true}) WHERE NOT c.name CONTAINS 'DC' RETURN c.name

# Constrained delegation principals
MATCH (u) WHERE u.allowedtodelegate IS NOT NULL RETURN u.name, u.allowedtodelegate

# Resource-based constrained delegation
MATCH (c:Computer) WHERE c.allowedtoact IS NOT NULL RETURN c.name
```

### DCSync Rights

```
# Users with DCSync rights
MATCH (u)-[:MemberOf*0..]->(g:Group)-[r:GetChanges|GetChangesAll]->(d:Domain)
RETURN u.name, type(r), d.name

# Direct DCSync (non-group)
MATCH (u)-[r:GetChanges|GetChangesAll]->(d:Domain) RETURN u.name, type(r), d.name
```

### ACL Abuse Paths

```
# Users with GenericAll on other users
MATCH (u1:User)-[r:GenericAll]->(u2:User) RETURN u1.name, u2.name

# Users with WriteDacl on groups
MATCH (u:User)-[r:WriteDacl]->(g:Group) RETURN u.name, g.name

# Users who can change passwords (ForceChangePassword)
MATCH (u1:User)-[r:ForceChangePassword]->(u2:User) RETURN u1.name, u2.name

# Full ACL abuse paths from owned to high value
MATCH p=(u {owned:true})-[r:GenericAll|GenericWrite|WriteDacl|WriteOwner|Owns|ForceChangePassword|AddMember|AllExtendedRights*1..]->(t {highvalue:true})
RETURN p

# Users who can add members to groups
MATCH (u)-[r:AddMember]->(g:Group) RETURN u.name, g.name

# WriteOwner on high value targets
MATCH (u)-[r:WriteOwner]->(t {highvalue:true}) RETURN u.name, t.name
```

### Sessions and Lateral Movement

```
# Where Domain Admins are logged in
MATCH (u:User)-[:MemberOf*1..]->(g:Group {name:'DOMAIN ADMINS@CORP.LOCAL'})
MATCH (c:Computer)-[:HasSession]->(u)
RETURN u.name, c.name

# Computers where owned users have admin rights
MATCH (u {owned:true})-[:AdminTo]->(c:Computer) RETURN u.name, c.name

# Derivative local admin (multi-hop admin chains)
MATCH p=shortestPath((u:User {owned:true})-[:AdminTo|HasSession|MemberOf*1..]->(c:Computer))
RETURN p

# Shortest path from owned to specific target
MATCH p=shortestPath((u {owned:true})-[*1..]->(t:Computer {name:'TARGET.CORP.LOCAL'}))
RETURN p
```

### GPO Abuse

```
# GPOs that affect Domain Admins group
MATCH (g:GPO)-[r:GpLink]->(ou:OU)-[r2:Contains*1..]->(u:User)-[:MemberOf*1..]->(da:Group {name:'DOMAIN ADMINS@CORP.LOCAL'})
RETURN g.name, ou.name, u.name

# Users with write access to GPOs
MATCH (u:User)-[r:GenericAll|GenericWrite|WriteDacl|WriteOwner]->(g:GPO)
RETURN u.name, g.name

# GPOs applied to computers
MATCH (g:GPO)-[r:GpLink]->(ou:OU)-[r2:Contains*1..]->(c:Computer)
RETURN g.name, c.name
```

---

## Custom Cypher Queries

### Reconnaissance

```
# All domain trusts
MATCH (d1:Domain)-[r:TrustedBy]->(d2:Domain) RETURN d1.name, r, d2.name

# Count objects per type
MATCH (n) RETURN labels(n), count(n) ORDER BY count(n) DESC

# Find computers with old OS
MATCH (c:Computer) WHERE c.operatingsystem =~ '(?i).*(2008|2003|XP|Vista|7).*'
RETURN c.name, c.operatingsystem

# Users with passwords never expiring
MATCH (u:User {pwdneverexpires:true}) RETURN u.name

# Users with passwords not required
MATCH (u:User {passwordnotreqd:true}) RETURN u.name

# Enabled users with description field (often contains passwords)
MATCH (u:User) WHERE u.enabled = true AND u.description IS NOT NULL
RETURN u.name, u.description

# Computers with LAPS
MATCH (c:Computer) WHERE c.haslaps = true RETURN c.name

# Computers without LAPS
MATCH (c:Computer) WHERE c.haslaps = false RETURN c.name
```

### ADCS (Certificate Services)

```
# Find CA servers
MATCH (c:Computer)-[:MemberOf*1..]->(g:Group)
WHERE g.name =~ '(?i).*CERT PUBLISHERS.*'
RETURN c.name

# ESC1 — users who can enroll in vulnerable templates
MATCH (u)-[:Enroll|AutoEnroll]->(ct:CertTemplate)
WHERE ct.enrolleesuppliessubject = true AND ct.requiresmanagerapproval = false
AND ct.authenticationenabled = true
RETURN u.name, ct.name
```

---

## Mark as Owned / High Value

```
# In GUI: Right-click node > Mark as Owned / Mark as High Value

# Via Cypher (Neo4j browser at http://localhost:7474):
# Mark user as owned
MATCH (u:User {name:'COMPROMISED_USER@CORP.LOCAL'}) SET u.owned = true RETURN u

# Mark computer as owned
MATCH (c:Computer {name:'COMPROMISED_HOST.CORP.LOCAL'}) SET c.owned = true RETURN c

# Mark as high value
MATCH (c:Computer {name:'FILE_SERVER.CORP.LOCAL'}) SET c.highvalue = true RETURN c

# Clear owned status
MATCH (n {owned:true}) SET n.owned = false RETURN n.name

# List all owned nodes
MATCH (n {owned:true}) RETURN n.name, labels(n)

# List all high value targets
MATCH (n {highvalue:true}) RETURN n.name, labels(n)
```

---

## Path Analysis Workflow

```
# 1. Import data and mark owned nodes
# 2. Run "Shortest Paths to Domain Admins from Owned Principals"
# 3. Examine each relationship in the path:

#   MemberOf         = User is member of group (no action needed)
#   AdminTo          = Local admin on computer (PtH, PsExec)
#   HasSession       = User has active session (dump creds)
#   GenericAll       = Full control (reset password, add to group, Kerberoast)
#   GenericWrite     = Write any property (targeted Kerberoast, RBCD)
#   WriteDacl        = Modify ACL (grant yourself GenericAll)
#   WriteOwner       = Change owner (then WriteDacl yourself)
#   ForceChangePassword = Reset password without knowing current
#   AddMember        = Add user to group
#   Owns             = Object owner (can WriteDacl)
#   AllExtendedRights = Read LAPS password, force change password
#   GetChanges + GetChangesAll = DCSync
#   Contains         = OU contains object (GPO relevance)
#   GpLink           = GPO linked to OU

# 4. Execute each step, mark new nodes as owned
# 5. Re-run queries to find new paths
```

---

## Cleanup and Maintenance

```
# Clear database (start fresh)
# Neo4j Browser:
MATCH (n) DETACH DELETE n

# Remove all session data (re-collect only sessions)
MATCH ()-[r:HasSession]->() DELETE r

# Export query results to CSV (Neo4j Browser)
# Run query, click download icon in results panel

# Backup Neo4j database
sudo neo4j-admin dump --database=neo4j --to=/tmp/neo4j_backup.dump

# Restore
sudo neo4j-admin load --database=neo4j --from=/tmp/neo4j_backup.dump --force
```
