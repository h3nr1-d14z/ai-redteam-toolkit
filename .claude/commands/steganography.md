Steganography analysis and detection on: $ARGUMENTS

## Pre-flight
- Determine objective: hiding data (offensive) or detecting hidden data (forensic/CTF)
- Identify file type: image (PNG/JPG/BMP), audio (WAV/MP3), video, document, network
- Collect suspected carrier files for analysis

## Phase 1: Image Steganography Detection
1. **Metadata**: `exiftool <file>` -- check for unusual metadata, embedded thumbnails
2. **Strings**: `strings -n 8 <file>` -- look for embedded text, URLs, base64
3. **Binwalk**: `binwalk <file>` -- detect embedded files, appended archives
4. **Steghide**: `steghide info <file>` -- check for steghide-embedded data
5. **Zsteg**: `zsteg <file>` -- PNG/BMP LSB analysis (bit planes, channels)
6. **StegSolve**: visual analysis -- cycle through bit planes, color channels
7. **File carving**: `foremost <file>` or `scalpel` -- extract embedded files

## Phase 2: Image Steganography Embedding
1. **Steghide**: `steghide embed -cf cover.jpg -ef secret.txt -p <passphrase>`
2. **OpenStego**: GUI-based LSB embedding with encryption
3. **LSB manual**: Python script to embed in least significant bits
4. **Append**: `cat image.png secret.zip > stego.png` (simple concatenation)
5. **Snow**: `snow -C -m "secret message" -p <pass> cover.txt stego.txt` (whitespace)

## Phase 3: Audio Steganography
1. **Spectrogram**: Open in Audacity -> Spectrogram view (visual messages in frequency)
2. **LSB audio**: `python3 tools/stego/audio-lsb.py extract <file>`
3. **DeepSound**: Windows tool for hiding data in audio files
4. **Sonic Visualiser**: detailed spectrogram and waveform analysis
5. **DTMF decode**: if tones detected, decode phone keypad sequences

## Phase 4: Advanced Detection
1. **Statistical analysis**: chi-square test for LSB randomness
2. **Histogram analysis**: compare with clean reference image
3. **File size anomaly**: is file larger than expected for its resolution/quality?
4. **Multiple passes**: try common passwords (empty, filename, challenge name for CTFs)
5. **Stegcracker**: `stegcracker <file> wordlist.txt` -- brute-force steghide passphrase

## Tools
Detection: steghide, zsteg, stegsolve, binwalk, exiftool, strings, foremost, stegcracker
Embedding: steghide, OpenStego, Snow, LSB scripts
Audio: Audacity, Sonic Visualiser, DeepSound

## Output
Save findings to engagements/<target>/findings/stego-analysis.md or ctf/<event>/stego/

## Framework Mapping
- MITRE ATT&CK: TA0010 (Exfiltration) -> T1027 (Obfuscated Files or Information)
- MITRE ATT&CK: TA0011 (Command and Control) -> T1001.002 (Steganography)
- Cyber Kill Chain: Phase 7 -- Actions on Objectives (data hiding for exfiltration)
- CEH v12: Module 06 -- System Hacking (Steganography)

## Safety
Only analyze files you are authorized to examine. Preserve original files.
