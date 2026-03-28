Establish persistence mechanisms on: $ARGUMENTS

1. **Enumerate**: Identify OS, architecture, privilege level, installed security products, monitoring
2. **User-level persistence**:
   - Windows: Registry Run keys, scheduled tasks, startup folder, COM hijacking
   - Linux: crontab, .bashrc/.profile, systemd user services, XDG autostart
3. **Admin-level persistence**:
   - Windows: Services, WMI event subscriptions, DLL search order hijacking, AppInit_DLLs
   - Linux: systemd services, init.d, PAM modules, LD_PRELOAD
4. **Stealth techniques**: Timestomping, log clearing, naming conventions matching legitimate software
5. **Redundancy**: Implement multiple persistence mechanisms for resilience
6. **Validation**: Test persistence survives reboot, user logoff, service restart
7. **Document**: Record all persistence artifacts for cleanup during engagement closure

IMPORTANT: Only establish with explicit authorization. Document everything for removal.
Save to `engagements/<target>/findings/persistence-*.md`
