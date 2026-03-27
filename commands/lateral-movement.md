Plan and execute lateral movement from: $ARGUMENTS

1. **Situational awareness**: Enumerate local info — users, groups, network connections, shares, ARP cache, routes
2. **Credential harvesting**: Dump credentials — mimikatz (Windows), /etc/shadow (Linux), browser creds, SSH keys, tokens
3. **Network discovery**: Scan internal network for live hosts, services, shares, identify high-value targets
4. **Movement techniques**:
   - Windows: PsExec, WMI, WinRM, DCOM, RDP, SMB, Pass-the-Hash, Pass-the-Ticket
   - Linux: SSH (keys/creds), Ansible, puppet, cron, NFS
5. **Pivot setup**: Set up SOCKS proxy, port forwarding, or tunnel for further access
6. **Target access**: Move to identified targets, escalate privileges, access data
7. **Track path**: Document full movement chain for attack path diagram

Tools: Impacket, CrackMapExec, chisel, ligolo-ng, SSH, Mimikatz
Save attack path to `engagements/<target>/findings/lateral-movement-*.md`
