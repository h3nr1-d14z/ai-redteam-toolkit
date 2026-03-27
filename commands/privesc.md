Perform privilege escalation on: $ARGUMENTS

## Pre-flight
- Determine current user and privileges: `whoami`, `id`, `whoami /priv`
- Identify OS: Linux or Windows
- Check if target is in scope for privilege escalation

## Linux Privilege Escalation
1. **SUID/SGID**: `find / -perm -4000 -type f 2>/dev/null` → check GTFOBins
2. **Sudo**: `sudo -l` → check for NOPASSWD entries, wildcard abuse
3. **Cron jobs**: `cat /etc/crontab`, `ls /etc/cron.*` → writable scripts?
4. **Capabilities**: `getcap -r / 2>/dev/null` → cap_setuid, cap_dac_override
5. **Writable paths**: `/etc/passwd` writable? `.bashrc` injection?
6. **Kernel**: `uname -r` → check exploit-db for kernel exploits (last resort)
7. **Services**: running as root with writable configs?
8. **Docker**: `docker ps` → if in docker group, mount host filesystem
- Auto-scan: `linpeas.sh` or `linux-smart-enumeration`
- Reference: cheatsheets/linux-privesc.md

## Windows Privilege Escalation
1. **Services**: unquoted paths, weak permissions, writable binaries
2. **Tokens**: SeImpersonate → JuicyPotato/PrintSpoofer/GodPotato
3. **AlwaysInstallElevated**: MSI-based escalation
4. **Registry**: AutoRun, service configs, AlwaysInstallElevated keys
5. **Scheduled tasks**: writable tasks running as SYSTEM
6. **DLL hijacking**: missing DLLs in privileged processes
7. **Credentials**: cached creds, credential manager, autologon registry
8. **UAC bypass**: fodhelper, eventvwr, CMSTPLUA
- Auto-scan: `winpeas.exe` or `PowerUp.ps1` or `SharpUp.exe`
- Reference: cheatsheets/windows-privesc.md

## Output
Save to engagements/<target>/findings/privesc-*.md with exact commands used.

## Safety
Always have rollback plan. Do not modify critical system files without backup.

## Framework Mapping
- MITRE ATT&CK: TA0004 (Privilege Escalation) -> T1548 (Abuse Elevation Control Mechanism)
- MITRE ATT&CK: T1068 (Exploitation for Privilege Escalation), T1055 (Process Injection)
- MITRE ATT&CK: T1134 (Access Token Manipulation), T1574 (Hijack Execution Flow)
- Cyber Kill Chain: Phase 5 -- Installation
- CEH v12: Module 06 -- System Hacking (Privilege Escalation)
