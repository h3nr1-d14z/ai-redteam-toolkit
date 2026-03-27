Analyze disk image: $ARGUMENTS

1. **Image verification**: Verify hash integrity, identify filesystem type (NTFS, ext4, APFS, FAT32)
2. **Mount and browse**: Mount image read-only, enumerate filesystem structure, identify user profiles
3. **Timeline**: Build filesystem timeline (MFT, journal, timestamps) — creation, modification, access patterns
4. **Deleted files**: Recover deleted files using file carving (foremost, photorec, scalpel), check recycle bin
5. **Artifacts**:
   - Windows: Registry hives, prefetch, SRUM, event logs, amcache, shimcache, USN journal
   - Linux: /var/log, .bash_history, crontabs, systemd journals, /tmp
   - macOS: FSEvents, Spotlight, Unified logs, Quarantine events
6. **Hidden data**: Check alternate data streams (NTFS), file slack space, hidden partitions, encrypted volumes
7. **Report**: Document findings with timeline and evidence references

Tools: Autopsy, Sleuth Kit (fls, icat, mmls), KAPE, plaso/log2timeline
Save to `engagements/<target>/findings/disk-forensics.md`
