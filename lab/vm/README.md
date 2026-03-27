# Virtual Machine Lab Recommendations

## Online Platforms

### Hack The Box (HTB)
- **URL:** https://www.hackthebox.com
- **Type:** Subscription-based ($14/mo for VIP)
- **Focus:** Full penetration testing (web, network, AD, cloud, hardware)
- **Best For:** Intermediate to advanced practitioners
- **Features:**
  - Active machines: new boxes released weekly, community writeups after retirement
  - Retired machines: 500+ machines with official writeups (VIP)
  - Pro Labs: multi-machine enterprise networks (Dante, Offshore, RastaLabs, Zephyr)
  - Tracks: guided learning paths by topic
  - Challenges: standalone web, crypto, RE, forensics, misc challenges
  - Competitive: global ranking, seasonal competitions
- **Recommended Starting Machines:** Lame, Jerry, Nibbles, Shocker, Bashed, Blocky

### TryHackMe (THM)
- **URL:** https://tryhackme.com
- **Type:** Freemium ($14/mo for premium)
- **Focus:** Guided learning with structured rooms and paths
- **Best For:** Beginners to intermediate
- **Features:**
  - Learning Paths: Pre-Security, Complete Beginner, Jr Penetration Tester, Offensive Pentesting, Red Teaming
  - Rooms: step-by-step guided exercises with questions
  - AttackBox: browser-based attack machine (no local setup needed)
  - King of the Hill: competitive real-time challenges
  - 800+ rooms covering all security domains
- **Recommended Starting Paths:**
  - Pre-Security (absolute beginners)
  - Complete Beginner (foundational knowledge)
  - Jr Penetration Tester (hands-on pentesting)

### PicoCTF
- **URL:** https://picoctf.org
- **Type:** Free
- **Focus:** CTF-style challenges, educational
- **Best For:** Beginners, students
- **Features:**
  - Annual competition with year-round practice challenges
  - Categories: web, forensics, RE, crypto, binary exploitation, general skills
  - Difficulty ramps from very beginner-friendly to challenging
  - picoGym: permanent practice challenges from past competitions

### OverTheWire
- **URL:** https://overthewire.org/wargames/
- **Type:** Free
- **Focus:** Linux skills, binary exploitation, web
- **Best For:** Learning Linux fundamentals and basic exploitation
- **Wargames (in recommended order):**
  1. **Bandit** -- Linux basics, SSH, file manipulation (start here)
  2. **Natas** -- Web security basics
  3. **Leviathan** -- Basic binary exploitation
  4. **Narnia** -- Buffer overflows, shellcode
  5. **Behemoth** -- More binary exploitation
  6. **Krypton** -- Basic cryptography

### CyberDefenders
- **URL:** https://cyberdefenders.org
- **Type:** Free
- **Focus:** Blue team / DFIR challenges
- **Best For:** Forensics and incident response practice
- **Features:** Memory forensics, disk forensics, network forensics, malware analysis

### Pwnable.kr / Pwnable.tw
- **URL:** https://pwnable.kr / https://pwnable.tw
- **Type:** Free
- **Focus:** Binary exploitation
- **Best For:** Practicing pwn/exploit development

## Downloadable VMs

### VulnHub
- **URL:** https://www.vulnhub.com
- **Type:** Free downloadable OVA/VMDK files
- **Setup:** Import into VirtualBox or VMware
- **Recommended VMs:**
  - Kioptrix series (beginner Linux)
  - Mr. Robot (beginner-intermediate)
  - Stapler (intermediate)
  - Lampiao (intermediate)
  - DC series (DC-1 through DC-9, progressive difficulty)
  - Sunset series (various difficulty levels)

### DVWA / Juice Shop / WebGoat (Local)
- See `../docker/` directory for Docker Compose setup
- Run locally for web application testing practice

### Metasploitable 2 and 3
- **Metasploitable 2:** Classic intentionally vulnerable Linux VM
  - Download: https://sourceforge.net/projects/metasploitable/
  - Default credentials: msfadmin / msfadmin
  - Contains: FTP, SSH, Telnet, SMTP, MySQL, PostgreSQL, Samba, and many more vulnerable services
- **Metasploitable 3:** Windows and Linux vulnerable VMs
  - Requires Vagrant and VirtualBox to build
  - More modern vulnerabilities and configurations

## Recommended Lab Setup

### Hardware Requirements
- CPU: 4+ cores (8 recommended)
- RAM: 16 GB minimum (32 GB recommended)
- Storage: 100 GB free SSD space

### Virtualization Software
- **VirtualBox** (free): suitable for most labs
- **VMware Workstation Pro** (paid) / **VMware Fusion** (macOS): better performance, snapshot management
- **Proxmox** (free): server-based, good for dedicated lab hardware
- **UTM** (macOS, free): good for Apple Silicon Macs

### Attack Machine Options
- **Kali Linux:** most popular, comprehensive tool collection
- **Parrot OS:** Kali alternative, lighter weight
- **BlackArch:** Arch-based, largest tool repository
- **Commando VM:** Windows-based attack platform (for AD testing)

### Network Configuration
- Use host-only or NAT network for isolated lab
- Never bridge vulnerable VMs to your real network
- Create separate virtual network for multi-machine labs

### Recommended Setup
```
[Attack VM: Kali Linux]
        |
   [Virtual Switch / Host-Only Network]
        |
   [Target VMs]
   |- Metasploitable 2
   |- VulnHub machines
   |- Windows targets
```
