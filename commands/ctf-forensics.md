Solve forensics CTF challenge: $ARGUMENTS

1. **File analysis**: Identify file type (file, magic bytes), check for embedded files (binwalk), metadata (exiftool)
2. **Steganography**: Check images for hidden data — LSB (zsteg, stegsolve), strings, embedded archives, EXIF data
3. **Memory forensics**: If memory dump — identify OS profile (Volatility), list processes, network connections, extract files, scan for malware
4. **Network forensics**: If PCAP — protocol statistics, follow TCP streams, extract files, DNS queries, HTTP requests, credentials
5. **Disk forensics**: If disk image — mount, recover deleted files (photorec/foremost), check slack space, alternate data streams
6. **Document analysis**: PDF streams, Office macros, embedded objects, hidden text layers
7. **Decode**: CyberChef for encoding chains (base64, hex, rot13, custom)

Tools: Volatility3, Wireshark, binwalk, exiftool, steghide, zsteg, foremost, CyberChef
Save to `ctf/<platform>/<challenge>/`
