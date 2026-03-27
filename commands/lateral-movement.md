Plan lateral movement from: $ARGUMENTS

Enumerate: current access level, network segments reachable, discovered credentials/tokens.
Windows: Pass-the-Hash (mimikatz sekurlsa::pth), Pass-the-Ticket (Rubeus ptt), PsExec, WMI, WinRM, DCOM, RDP.
Linux: SSH with captured keys, sudo abuse, internal pivoting (SSH tunnels, SOCKS proxy).
Tools: CrackMapExec for spray, Impacket for protocol abuse, Chisel/ligolo for pivoting.
Check: can you reach new subnets? New services? Domain controllers? Reference: methodology/red-team-ops.md Phase 6.
Output: engagements/<target>/findings/lateral-*.md

## Safety
Verify authorization and scope before proceeding. Document all actions.
