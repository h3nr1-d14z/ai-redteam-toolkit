#!/usr/bin/env python3
"""
s3-scanner.py - AWS S3 Bucket Security Scanner

Checks S3 buckets for public access, listing permissions, writable status,
ACL exposure, and the presence of common sensitive files -- all using stdlib
HTTP requests (no boto3 dependency).

Usage:
    python3 s3-scanner.py --bucket company-backup
    python3 s3-scanner.py --company acme --generate
    python3 s3-scanner.py --list buckets.txt
    python3 s3-scanner.py --bucket target --check-files
    python3 s3-scanner.py --bucket target --json

Author : AI-RedTeam-Toolkit
License: MIT
"""

from __future__ import annotations

import argparse
import json
import os
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any
from pathlib import Path


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

S3_REGION_URL = "https://{bucket}.s3.amazonaws.com"
S3_PATH_URL = "https://s3.amazonaws.com/{bucket}"

# Common sensitive file paths to probe
SENSITIVE_FILES = [
    ".env",
    ".git/config",
    ".git/HEAD",
    "backup.sql",
    "backup.tar.gz",
    "backup.zip",
    "database.sql",
    "db_backup.sql",
    "dump.sql",
    "credentials",
    "credentials.json",
    "credentials.xml",
    "credentials.csv",
    "config.json",
    "config.yml",
    "config.yaml",
    "config.xml",
    "settings.py",
    "wp-config.php",
    ".htpasswd",
    ".htaccess",
    "id_rsa",
    "id_rsa.pub",
    "server.key",
    "server.crt",
    "private.key",
    "secret.txt",
    "passwords.txt",
    "shadow",
    "passwd",
    "aws-credentials",
    "terraform.tfstate",
    "docker-compose.yml",
    ".dockerenv",
    "kubeconfig",
]

# Suffixes/patterns for bucket name generation
BUCKET_PATTERNS = [
    "{company}",
    "{company}-backup",
    "{company}-backups",
    "{company}-bak",
    "{company}-data",
    "{company}-db",
    "{company}-dev",
    "{company}-development",
    "{company}-staging",
    "{company}-stage",
    "{company}-stg",
    "{company}-prod",
    "{company}-production",
    "{company}-internal",
    "{company}-private",
    "{company}-public",
    "{company}-assets",
    "{company}-static",
    "{company}-media",
    "{company}-uploads",
    "{company}-files",
    "{company}-logs",
    "{company}-audit",
    "{company}-archive",
    "{company}-cdn",
    "{company}-images",
    "{company}-img",
    "{company}-docs",
    "{company}-documents",
    "{company}-reports",
    "{company}-config",
    "{company}-configs",
    "{company}-secrets",
    "{company}-infra",
    "{company}-terraform",
    "{company}-tf",
    "{company}-cloudformation",
    "{company}-cf",
    "{company}-deploy",
    "{company}-releases",
    "{company}-packages",
    "{company}-artifacts",
    "{company}-ci",
    "{company}-test",
    "{company}-testing",
    "{company}-qa",
    "{company}-uat",
    "{company}-web",
    "{company}-api",
    "{company}-app",
    "{company}-mobile",
    "{company}-lambda",
    "{company}-email",
    "{company}-mail",
    "backup-{company}",
    "data-{company}",
    "s3-{company}",
    "{company}-s3",
    "{company}.com",
    "www.{company}.com",
]

DEFAULT_TIMEOUT = 10  # seconds
USER_AGENT = "Mozilla/5.0 (compatible; S3Scanner/1.0)"


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _build_opener() -> urllib.request.OpenerDirector:
    """Return an opener that accepts any SSL cert (some S3 endpoints use
    wildcard certs that can trip strict verification in lab environments)."""
    ctx = ssl.create_default_context()
    handler = urllib.request.HTTPSHandler(context=ctx)
    opener = urllib.request.build_opener(handler)
    return opener


_OPENER = _build_opener()


def _request(
    url: str,
    method: str = "GET",
    data: bytes | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, str], bytes]:
    """Perform an HTTP request and return (status, headers_dict, body).

    Returns status -1 on network-level errors.
    """
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("User-Agent", USER_AGENT)
    try:
        resp = _OPENER.open(req, timeout=timeout)
        status = resp.status
        headers = {k.lower(): v for k, v in resp.getheaders()}
        body = resp.read()
        return status, headers, body
    except urllib.error.HTTPError as exc:
        headers = {k.lower(): v for k, v in exc.headers.items()}
        body = b""
        try:
            body = exc.read()
        except Exception:
            pass
        return exc.code, headers, body
    except (urllib.error.URLError, socket.timeout, OSError) as exc:
        return -1, {}, str(exc).encode()


# ---------------------------------------------------------------------------
# Scanning logic
# ---------------------------------------------------------------------------

class BucketResult:
    """Holds all scan results for a single bucket."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.exists: bool | None = None
        self.region: str = ""
        self.public_read: bool | None = None
        self.public_write: bool | None = None
        self.acl_accessible: bool | None = None
        self.acl_grants: list[dict[str, str]] = []
        self.objects: list[dict[str, str]] = []
        self.object_count: int = 0
        self.sensitive_files: list[str] = []
        self.errors: list[str] = []

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "bucket": self.name,
            "exists": self.exists,
        }
        if self.region:
            d["region"] = self.region
        if self.exists:
            d["public_read"] = self.public_read
            d["public_write"] = self.public_write
            d["acl_accessible"] = self.acl_accessible
            if self.acl_grants:
                d["acl_grants"] = self.acl_grants
            d["object_count"] = self.object_count
            if self.objects:
                d["objects_sample"] = self.objects[:50]
            if self.sensitive_files:
                d["sensitive_files_found"] = self.sensitive_files
        if self.errors:
            d["errors"] = self.errors
        return d


def _base_url(bucket: str) -> str:
    return S3_REGION_URL.format(bucket=bucket)


def check_exists(bucket: str) -> BucketResult:
    """HEAD request to see if the bucket exists and is reachable."""
    result = BucketResult(bucket)
    url = _base_url(bucket)
    status, headers, _ = _request(url, method="HEAD")

    if status == -1:
        result.exists = False
        result.errors.append("DNS/network error -- bucket likely does not exist")
        return result

    region = headers.get("x-amz-bucket-region", "")
    result.region = region

    if status in (200, 301, 307, 403):
        result.exists = True
    elif status == 404:
        result.exists = False
    else:
        result.exists = None
        result.errors.append(f"Unexpected HEAD status: {status}")

    return result


def check_public_read(result: BucketResult) -> None:
    """Try to list bucket contents without auth (GET /)."""
    url = _base_url(result.name)
    status, headers, body = _request(url)

    if status == 200:
        result.public_read = True
        _parse_listing(result, body)
    elif status == 403:
        result.public_read = False
    else:
        result.public_read = False
        result.errors.append(f"Public read check returned status {status}")


def _parse_listing(result: BucketResult, body: bytes) -> None:
    """Parse S3 ListBucketResult XML."""
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        result.errors.append("Failed to parse bucket listing XML")
        return

    # S3 uses a namespace
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0] + "}"

    for contents in root.findall(f"{ns}Contents"):
        key_el = contents.find(f"{ns}Key")
        size_el = contents.find(f"{ns}Size")
        modified_el = contents.find(f"{ns}LastModified")
        obj: dict[str, str] = {}
        if key_el is not None and key_el.text:
            obj["key"] = key_el.text
        if size_el is not None and size_el.text:
            obj["size"] = size_el.text
        if modified_el is not None and modified_el.text:
            obj["last_modified"] = modified_el.text
        if obj:
            result.objects.append(obj)
    result.object_count = len(result.objects)


def check_public_write(result: BucketResult) -> None:
    """Attempt to PUT a small test object (non-destructive probe)."""
    test_key = ".s3scanner-write-test"
    url = f"{_base_url(result.name)}/{test_key}"
    payload = b"s3scanner write test -- safe to delete"
    status, _, _ = _request(url, method="PUT", data=payload)

    if status == 200:
        result.public_write = True
        # Try to clean up
        _request(url, method="DELETE")
    elif status in (403, 405):
        result.public_write = False
    else:
        result.public_write = False
        if status != -1:
            result.errors.append(f"Write check returned status {status}")


def check_acl(result: BucketResult) -> None:
    """Try to read the bucket ACL."""
    url = f"{_base_url(result.name)}/?acl"
    status, _, body = _request(url)

    if status == 200:
        result.acl_accessible = True
        _parse_acl(result, body)
    else:
        result.acl_accessible = False


def _parse_acl(result: BucketResult, body: bytes) -> None:
    """Parse S3 AccessControlPolicy XML."""
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        result.errors.append("Failed to parse ACL XML")
        return

    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0] + "}"

    for grant in root.findall(f".//{ns}Grant"):
        grantee = grant.find(f"{ns}Grantee")
        perm_el = grant.find(f"{ns}Permission")
        entry: dict[str, str] = {}
        if grantee is not None:
            uri = grantee.find(f"{ns}URI")
            display = grantee.find(f"{ns}DisplayName")
            gtype = grantee.attrib.get(
                f"{{http://www.w3.org/2001/XMLSchema-instance}}type", ""
            )
            if uri is not None and uri.text:
                entry["grantee_uri"] = uri.text
            elif display is not None and display.text:
                entry["grantee_name"] = display.text
            entry["type"] = gtype
        if perm_el is not None and perm_el.text:
            entry["permission"] = perm_el.text
        if entry:
            result.acl_grants.append(entry)


def check_sensitive_files(result: BucketResult) -> None:
    """Probe for known sensitive file paths."""
    for fpath in SENSITIVE_FILES:
        url = f"{_base_url(result.name)}/{fpath}"
        status, _, _ = _request(url, method="HEAD", timeout=5)
        if status == 200:
            result.sensitive_files.append(fpath)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def scan_bucket(
    bucket: str,
    check_files: bool = False,
    verbose: bool = True,
) -> BucketResult:
    """Run the full scan pipeline on a single bucket."""
    if verbose:
        print(f"\n[*] Scanning bucket: {bucket}")

    result = check_exists(bucket)

    if not result.exists:
        if verbose:
            print(f"    [-] Bucket does not exist or is unreachable")
        return result

    if verbose:
        region_info = f" (region: {result.region})" if result.region else ""
        print(f"    [+] Bucket exists{region_info}")

    # Public read
    check_public_read(result)
    if verbose:
        status = "YES" if result.public_read else "No"
        print(f"    [{'!' if result.public_read else '-'}] Public read: {status}")
        if result.public_read and result.objects:
            print(f"        Listed {result.object_count} object(s)")
            for obj in result.objects[:10]:
                key = obj.get("key", "?")
                size = obj.get("size", "?")
                print(f"          - {key} ({size} bytes)")
            if result.object_count > 10:
                print(f"          ... and {result.object_count - 10} more")

    # Public write
    check_public_write(result)
    if verbose:
        status = "YES" if result.public_write else "No"
        tag = "!!" if result.public_write else "-"
        print(f"    [{tag}] Public write: {status}")

    # ACL
    check_acl(result)
    if verbose:
        status = "YES" if result.acl_accessible else "No"
        tag = "!" if result.acl_accessible else "-"
        print(f"    [{tag}] ACL accessible: {status}")
        if result.acl_accessible and result.acl_grants:
            for g in result.acl_grants:
                grantee = g.get("grantee_uri", g.get("grantee_name", "Owner"))
                perm = g.get("permission", "?")
                print(f"          {grantee}: {perm}")

    # Sensitive files
    if check_files:
        if verbose:
            print(f"    [*] Checking {len(SENSITIVE_FILES)} sensitive file paths...")
        check_sensitive_files(result)
        if verbose:
            if result.sensitive_files:
                print(f"    [!!] Found {len(result.sensitive_files)} sensitive file(s):")
                for sf in result.sensitive_files:
                    print(f"          - {sf}")
            else:
                print(f"    [-] No sensitive files detected")

    return result


def generate_bucket_names(company: str) -> list[str]:
    """Generate common bucket name variants for a company."""
    company = company.lower().strip()
    names: list[str] = []
    for pattern in BUCKET_PATTERNS:
        names.append(pattern.format(company=company))
    # Also try with dots and underscores
    if "-" not in company:
        alt = company.replace(".", "-")
        if alt != company:
            for pattern in BUCKET_PATTERNS[:15]:  # Just the most common
                names.append(pattern.format(company=alt))
    return list(dict.fromkeys(names))  # deduplicate preserving order


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_summary(results: list[BucketResult]) -> None:
    """Print a text summary of all scanned buckets."""
    print("\n" + "=" * 70)
    print("SCAN SUMMARY")
    print("=" * 70)

    existing = [r for r in results if r.exists]
    readable = [r for r in existing if r.public_read]
    writable = [r for r in existing if r.public_write]
    acl_open = [r for r in existing if r.acl_accessible]
    with_sensitive = [r for r in existing if r.sensitive_files]

    print(f"  Buckets scanned    : {len(results)}")
    print(f"  Buckets found      : {len(existing)}")
    print(f"  Publicly readable  : {len(readable)}")
    print(f"  Publicly writable  : {len(writable)}")
    print(f"  ACL accessible     : {len(acl_open)}")
    print(f"  Sensitive files    : {len(with_sensitive)}")

    if readable or writable or with_sensitive:
        print("\n  ** HIGH RISK BUCKETS **")
        for r in results:
            flags: list[str] = []
            if r.public_read:
                flags.append("READ")
            if r.public_write:
                flags.append("WRITE")
            if r.sensitive_files:
                flags.append(f"SENSITIVE({len(r.sensitive_files)})")
            if flags:
                print(f"    {r.name}: {', '.join(flags)}")

    print("=" * 70)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AWS S3 bucket security scanner (stdlib only, no boto3).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --bucket company-backup\n"
            "  %(prog)s --company acme --generate\n"
            "  %(prog)s --list buckets.txt\n"
            "  %(prog)s --bucket target --check-files\n"
            "  %(prog)s --bucket target --json\n"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--bucket", "-b",
        help="Single bucket name to scan.",
    )
    group.add_argument(
        "--company", "-c",
        help="Company name for bucket name generation (use with --generate).",
    )
    group.add_argument(
        "--list", "-l",
        dest="bucket_list",
        help="File containing one bucket name per line.",
    )
    parser.add_argument(
        "--generate", "-g",
        action="store_true",
        help="Generate common bucket names from --company and scan them.",
    )
    parser.add_argument(
        "--check-files",
        action="store_true",
        help="Check for common sensitive files in each bucket.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output results in JSON format.",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Write output to a file instead of stdout.",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress per-bucket progress output (still prints summary/JSON).",
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"HTTP timeout in seconds (default: {DEFAULT_TIMEOUT}).",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    global DEFAULT_TIMEOUT
    DEFAULT_TIMEOUT = args.timeout

    # Determine bucket list
    buckets: list[str] = []

    if args.bucket:
        buckets = [args.bucket.strip()]
    elif args.company:
        if args.generate:
            buckets = generate_bucket_names(args.company)
            if not args.quiet:
                print(f"[+] Generated {len(buckets)} bucket name(s) for '{args.company}'")
        else:
            # Without --generate, treat company as a single bucket name
            buckets = [args.company.strip()]
    elif args.bucket_list:
        list_path = Path(args.bucket_list)
        if not list_path.is_file():
            print(f"[!] File not found: {list_path}", file=sys.stderr)
            return 1
        buckets = [
            line.strip()
            for line in list_path.read_text().splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        if not args.quiet:
            print(f"[+] Loaded {len(buckets)} bucket(s) from {list_path}")

    if not buckets:
        print("[!] No buckets to scan.", file=sys.stderr)
        return 1

    # Run scans
    verbose = not args.quiet and not args.json_output
    results: list[BucketResult] = []

    for bucket in buckets:
        result = scan_bucket(
            bucket,
            check_files=args.check_files,
            verbose=verbose,
        )
        results.append(result)

    # Output
    if args.json_output:
        output = json.dumps(
            [r.to_dict() for r in results],
            indent=2,
            ensure_ascii=False,
        )
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"[+] JSON report written to {args.output}")
        else:
            print(output)
    else:
        print_summary(results)
        if args.output:
            # Write a text report to file
            import io
            buf = io.StringIO()
            for r in results:
                buf.write(f"Bucket: {r.name}\n")
                buf.write(f"  Exists: {r.exists}\n")
                if r.exists:
                    buf.write(f"  Region: {r.region or 'unknown'}\n")
                    buf.write(f"  Public Read: {r.public_read}\n")
                    buf.write(f"  Public Write: {r.public_write}\n")
                    buf.write(f"  ACL Accessible: {r.acl_accessible}\n")
                    if r.objects:
                        buf.write(f"  Objects ({r.object_count}):\n")
                        for obj in r.objects[:50]:
                            buf.write(f"    - {obj.get('key', '?')}\n")
                    if r.sensitive_files:
                        buf.write(f"  Sensitive Files:\n")
                        for sf in r.sensitive_files:
                            buf.write(f"    - {sf}\n")
                buf.write("\n")
            Path(args.output).write_text(buf.getvalue(), encoding="utf-8")
            print(f"[+] Report written to {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
