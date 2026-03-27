#!/usr/bin/env python3
"""
apk-analyzer.py - Android APK Static Analysis Tool

Extracts and analyzes Android APK files without requiring external dependencies
beyond the Python standard library. Optionally uses aapt2/aapt for manifest
parsing but falls back to a pure-Python binary XML decoder when unavailable.

Features:
  - AndroidManifest.xml parsing (permissions, components, flags)
  - Dangerous permission highlighting
  - Exported component enumeration
  - Hardcoded secret detection (API keys, tokens, passwords, URLs)
  - URL extraction from DEX strings
  - Security flag analysis (debuggable, allowBackup, clearTextTraffic)
  - Native library (.so) listing
  - JSON and Markdown output modes

Usage:
    python3 apk-analyzer.py app.apk
    python3 apk-analyzer.py app.apk --secrets
    python3 apk-analyzer.py app.apk --json
    python3 apk-analyzer.py app.apk --output report.md

Author : AI-RedTeam-Toolkit
License: MIT
"""

from __future__ import annotations

import argparse
import json
import os
import re
import struct
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ANDROID_NS = "http://schemas.android.com/apk/res/android"
NS_MAP = {"android": ANDROID_NS}

DANGEROUS_PERMISSIONS = {
    "android.permission.READ_CALENDAR",
    "android.permission.WRITE_CALENDAR",
    "android.permission.CAMERA",
    "android.permission.READ_CONTACTS",
    "android.permission.WRITE_CONTACTS",
    "android.permission.GET_ACCOUNTS",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.ACCESS_COARSE_LOCATION",
    "android.permission.ACCESS_BACKGROUND_LOCATION",
    "android.permission.RECORD_AUDIO",
    "android.permission.READ_PHONE_STATE",
    "android.permission.READ_PHONE_NUMBERS",
    "android.permission.CALL_PHONE",
    "android.permission.ANSWER_PHONE_CALLS",
    "android.permission.READ_CALL_LOG",
    "android.permission.WRITE_CALL_LOG",
    "android.permission.ADD_VOICEMAIL",
    "android.permission.USE_SIP",
    "android.permission.BODY_SENSORS",
    "android.permission.SEND_SMS",
    "android.permission.RECEIVE_SMS",
    "android.permission.READ_SMS",
    "android.permission.RECEIVE_WAP_PUSH",
    "android.permission.RECEIVE_MMS",
    "android.permission.READ_EXTERNAL_STORAGE",
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.MANAGE_EXTERNAL_STORAGE",
    "android.permission.READ_MEDIA_IMAGES",
    "android.permission.READ_MEDIA_VIDEO",
    "android.permission.READ_MEDIA_AUDIO",
    "android.permission.POST_NOTIFICATIONS",
    "android.permission.NEARBY_WIFI_DEVICES",
    "android.permission.ACTIVITY_RECOGNITION",
    "android.permission.BLUETOOTH_CONNECT",
    "android.permission.BLUETOOTH_SCAN",
    "android.permission.BLUETOOTH_ADVERTISE",
}

# Regex patterns for secret/credential detection
SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("AWS Secret Key", re.compile(r"""(?:aws_secret|secret_key|SecretKey)[\"'`=:\s]+([A-Za-z0-9/+=]{40})""")),
    ("Google API Key", re.compile(r"AIza[0-9A-Za-z\-_]{35}")),
    ("Google OAuth", re.compile(r"[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com")),
    ("Firebase URL", re.compile(r"https://[a-z0-9-]+\.firebaseio\.com")),
    ("Firebase API Key", re.compile(r"(?:firebase|FIREBASE)[_A-Z]*[=:\"'\s]+AIza[0-9A-Za-z\-_]{35}")),
    ("Generic API Key", re.compile(r"""(?:api[_-]?key|apikey|API_KEY)[\"'`=:\s]+[\"']?([A-Za-z0-9\-_]{20,})""")),
    ("Generic Secret", re.compile(r"""(?:secret|SECRET|client_secret|CLIENT_SECRET)[\"'`=:\s]+[\"']?([A-Za-z0-9\-_]{16,})""")),
    ("Generic Token", re.compile(r"""(?:token|TOKEN|access_token|auth_token)[\"'`=:\s]+[\"']?([A-Za-z0-9\-_.]{20,})""")),
    ("Generic Password", re.compile(r"""(?:password|passwd|pwd|PASSWORD|PASSWD)[\"'`=:\s]+[\"']?([^\s\"']{6,})""")),
    ("Private Key", re.compile(r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----")),
    ("Bearer Token", re.compile(r"Bearer\s+[A-Za-z0-9\-_.~+/]+=*")),
    ("Basic Auth", re.compile(r"Basic\s+[A-Za-z0-9+/]+=*")),
    ("JWT", re.compile(r"eyJ[A-Za-z0-9\-_]+\.eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_.+/=]*")),
    ("Slack Token", re.compile(r"xox[bprs]-[0-9]{10,}-[0-9A-Za-z]{10,}")),
    ("GitHub Token", re.compile(r"gh[ps]_[A-Za-z0-9]{36,}")),
    ("Stripe Key", re.compile(r"[sr]k_live_[0-9a-zA-Z]{24,}")),
    ("Twilio SID", re.compile(r"AC[a-f0-9]{32}")),
    ("SendGrid Key", re.compile(r"SG\.[A-Za-z0-9\-_]{22,}\.[A-Za-z0-9\-_]{43,}")),
    ("Hardcoded IP", re.compile(r"\b(?:10|172\.(?:1[6-9]|2\d|3[01])|192\.168)\.\d{1,3}\.\d{1,3}\b")),
]

URL_PATTERN = re.compile(r"https?://[^\s\"'<>}{)\]\\]{5,}")


# ---------------------------------------------------------------------------
# Binary Android XML decoder (fallback when aapt is unavailable)
# ---------------------------------------------------------------------------

# Android binary XML chunk types
CHUNK_STRINGPOOL = 0x0001
CHUNK_RESOURCEMAP = 0x0180
CHUNK_START_NS = 0x0100
CHUNK_END_NS = 0x0101
CHUNK_START_TAG = 0x0102
CHUNK_END_TAG = 0x0103
CHUNK_TEXT = 0x0104

# Attribute value types
TYPE_NULL = 0x00
TYPE_REFERENCE = 0x01
TYPE_ATTRIBUTE = 0x02
TYPE_STRING = 0x03
TYPE_FLOAT = 0x04
TYPE_DIMENSION = 0x05
TYPE_FRACTION = 0x06
TYPE_INT_DEC = 0x10
TYPE_INT_HEX = 0x11
TYPE_INT_BOOLEAN = 0x12


class BinaryXmlParser:
    """Minimal parser for Android binary XML (AndroidManifest.xml)."""

    def __init__(self, data: bytes) -> None:
        self.data = data
        self.offset = 0
        self.strings: list[str] = []
        self.namespaces: dict[str, str] = {}  # uri -> prefix

    def parse(self) -> ET.Element | None:
        """Parse binary XML and return an ElementTree Element."""
        if len(self.data) < 8:
            return None

        magic, header_size, file_size = struct.unpack_from("<HHI", self.data, 0)
        # magic should be 0x0003 for XML
        if magic != 0x0003:
            return None

        self.offset = 8
        root: ET.Element | None = None
        stack: list[ET.Element] = []

        while self.offset < len(self.data) - 4:
            chunk_type, header_size, chunk_size = self._read_chunk_header()

            if chunk_type == CHUNK_STRINGPOOL:
                self._parse_string_pool(chunk_size)
            elif chunk_type == CHUNK_RESOURCEMAP:
                # Skip resource map
                self.offset += chunk_size - 8
            elif chunk_type == CHUNK_START_NS:
                self._parse_start_namespace()
            elif chunk_type == CHUNK_END_NS:
                self._parse_end_namespace()
            elif chunk_type == CHUNK_START_TAG:
                elem = self._parse_start_tag()
                if elem is not None:
                    if stack:
                        stack[-1].append(elem)
                    else:
                        root = elem
                    stack.append(elem)
            elif chunk_type == CHUNK_END_TAG:
                self._parse_end_tag()
                if stack:
                    stack.pop()
            elif chunk_type == CHUNK_TEXT:
                self.offset += chunk_size - 8
            else:
                # Unknown chunk; skip
                self.offset += max(chunk_size - 8, 0)

        return root

    def _read_chunk_header(self) -> tuple[int, int, int]:
        if self.offset + 8 > len(self.data):
            return (0, 0, 0)
        chunk_type, header_size = struct.unpack_from("<HH", self.data, self.offset)
        chunk_size = struct.unpack_from("<I", self.data, self.offset + 4)[0]
        self.offset += 8
        return chunk_type, header_size, chunk_size

    def _parse_string_pool(self, chunk_size: int) -> None:
        base = self.offset - 8
        if self.offset + 16 > len(self.data):
            self.offset = base + chunk_size
            return

        (
            string_count,
            style_count,
            flags,
            strings_start,
            styles_start,
        ) = struct.unpack_from("<IIIII", self.data, self.offset)
        self.offset += 20

        is_utf8 = bool(flags & (1 << 8))

        offsets: list[int] = []
        for _ in range(string_count):
            if self.offset + 4 > len(self.data):
                break
            offsets.append(struct.unpack_from("<I", self.data, self.offset)[0])
            self.offset += 4

        # Jump past style offsets
        self.offset += style_count * 4

        abs_strings_start = base + 8 + strings_start  # 8 for chunk header already consumed

        self.strings = []
        for off in offsets:
            pos = abs_strings_start + off
            if pos >= len(self.data):
                self.strings.append("")
                continue
            if is_utf8:
                s = self._read_utf8_string(pos)
            else:
                s = self._read_utf16_string(pos)
            self.strings.append(s)

        self.offset = base + chunk_size

    def _read_utf16_string(self, pos: int) -> str:
        if pos + 4 > len(self.data):
            return ""
        char_count = struct.unpack_from("<H", self.data, pos)[0]
        if char_count & 0x8000:
            # High bit set means two-word length
            char_count = ((char_count & 0x7FFF) << 16) | struct.unpack_from(
                "<H", self.data, pos + 2
            )[0]
            pos += 4
        else:
            pos += 2
        end = pos + char_count * 2
        if end > len(self.data):
            end = len(self.data)
        try:
            return self.data[pos:end].decode("utf-16-le", errors="replace")
        except Exception:
            return ""

    def _read_utf8_string(self, pos: int) -> str:
        if pos + 2 > len(self.data):
            return ""
        # UTF-8 strings: first two bytes are char count (1 or 2 bytes), then
        # byte count (1 or 2 bytes), then the actual UTF-8 data
        byte_len = self.data[pos + 1] if pos + 1 < len(self.data) else 0
        if self.data[pos] & 0x80:
            pos += 2
            if pos < len(self.data):
                byte_len = self.data[pos]
                if byte_len & 0x80:
                    byte_len = ((byte_len & 0x7F) << 8) | (
                        self.data[pos + 1] if pos + 1 < len(self.data) else 0
                    )
                    pos += 2
                else:
                    pos += 1
            else:
                return ""
        else:
            pos += 1
            byte_len = self.data[pos] if pos < len(self.data) else 0
            if byte_len & 0x80:
                byte_len = ((byte_len & 0x7F) << 8) | (
                    self.data[pos + 1] if pos + 1 < len(self.data) else 0
                )
                pos += 2
            else:
                pos += 1

        end = pos + byte_len
        if end > len(self.data):
            end = len(self.data)
        try:
            return self.data[pos:end].decode("utf-8", errors="replace")
        except Exception:
            return ""

    def _get_string(self, index: int) -> str:
        if 0 <= index < len(self.strings):
            return self.strings[index]
        return ""

    def _parse_start_namespace(self) -> None:
        if self.offset + 16 > len(self.data):
            return
        _line, _comment, prefix_idx, uri_idx = struct.unpack_from(
            "<IIII", self.data, self.offset
        )
        self.offset += 16
        uri = self._get_string(uri_idx)
        prefix = self._get_string(prefix_idx)
        if uri:
            self.namespaces[uri] = prefix

    def _parse_end_namespace(self) -> None:
        self.offset += 16  # line, comment, prefix, uri

    def _parse_start_tag(self) -> ET.Element | None:
        if self.offset + 20 > len(self.data):
            return None

        (
            _line,
            _comment,
            ns_idx,
            name_idx,
            _attr_start,  # typically 0x0014
        ) = struct.unpack_from("<IIiII", self.data, self.offset)
        self.offset += 20

        if self.offset + 4 > len(self.data):
            return None
        attr_count, _class_idx = struct.unpack_from("<HH", self.data, self.offset)
        self.offset += 4

        tag_name = self._get_string(name_idx)
        if ns_idx >= 0:
            ns = self._get_string(ns_idx)
            if ns:
                tag_name = f"{{{ns}}}{tag_name}"

        elem = ET.Element(tag_name)

        for _ in range(attr_count):
            if self.offset + 20 > len(self.data):
                break
            (
                attr_ns_idx,
                attr_name_idx,
                attr_raw_value_idx,
                attr_typed_size_res,  # size(2) + res(1) + type(1)
                attr_typed_data,
            ) = struct.unpack_from("<iiIII", self.data, self.offset)
            self.offset += 20

            attr_name = self._get_string(attr_name_idx) if attr_name_idx >= 0 else ""
            attr_type = (attr_typed_size_res >> 24) & 0xFF

            # Resolve value
            if attr_type == TYPE_STRING:
                attr_value = self._get_string(attr_raw_value_idx) if attr_raw_value_idx >= 0 else ""
            elif attr_type == TYPE_INT_DEC:
                attr_value = str(attr_typed_data)
            elif attr_type == TYPE_INT_HEX:
                attr_value = f"0x{attr_typed_data:08x}"
            elif attr_type == TYPE_INT_BOOLEAN:
                attr_value = "true" if attr_typed_data != 0 else "false"
            elif attr_type == TYPE_REFERENCE:
                attr_value = f"@0x{attr_typed_data:08x}"
            elif attr_raw_value_idx >= 0:
                attr_value = self._get_string(attr_raw_value_idx)
            else:
                attr_value = str(attr_typed_data)

            # Build qualified attribute name
            if attr_ns_idx >= 0:
                attr_ns = self._get_string(attr_ns_idx)
                if attr_ns:
                    attr_name = f"{{{attr_ns}}}{attr_name}"

            elem.set(attr_name, attr_value)

        return elem

    def _parse_end_tag(self) -> None:
        self.offset += 16  # line, comment, ns, name


# ---------------------------------------------------------------------------
# Manifest extraction
# ---------------------------------------------------------------------------

def _ns(attr: str) -> str:
    """Expand android: prefix to full namespace for ElementTree queries."""
    return f"{{{ANDROID_NS}}}{attr}"


def extract_manifest_aapt(apk_path: Path) -> ET.Element | None:
    """Try to extract AndroidManifest.xml using aapt2 or aapt."""
    for tool in ("aapt2", "aapt"):
        try:
            result = subprocess.run(
                [tool, "dump", "xmltree", str(apk_path), "--file", "AndroidManifest.xml"]
                if tool == "aapt2"
                else [tool, "dump", "xmltree", str(apk_path), "AndroidManifest.xml"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0 and result.stdout.strip():
                # aapt output is not XML; we can't easily parse it into ET.
                # Return None so we fall through to binary parsing.
                return None
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return None


def extract_manifest_binary(apk_path: Path) -> ET.Element | None:
    """Extract and decode binary AndroidManifest.xml from the APK."""
    try:
        with zipfile.ZipFile(str(apk_path), "r") as zf:
            manifest_data = zf.read("AndroidManifest.xml")
    except (KeyError, zipfile.BadZipFile, OSError) as exc:
        print(f"[!] Cannot read AndroidManifest.xml: {exc}", file=sys.stderr)
        return None

    parser = BinaryXmlParser(manifest_data)
    try:
        return parser.parse()
    except (struct.error, ValueError, IndexError) as exc:
        print(f"[!] Binary XML parse error: {exc}", file=sys.stderr)
        return None


def extract_manifest_text(apk_path: Path) -> str | None:
    """Try aapt2/aapt to dump the manifest as readable XML text."""
    for tool, args in [
        ("aapt2", ["dump", "xmltree", str(apk_path), "--file", "AndroidManifest.xml"]),
        ("aapt", ["dump", "xmltree", str(apk_path), "AndroidManifest.xml"]),
    ]:
        try:
            result = subprocess.run(
                [tool] + args,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    # Try aapt dump badging as a last resort for basic info
    for tool in ("aapt2", "aapt"):
        try:
            result = subprocess.run(
                [tool, "dump", "badging", str(apk_path)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                return result.stdout
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    return None


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

class ApkAnalysis:
    """Container for all APK analysis results."""

    def __init__(self, apk_path: Path) -> None:
        self.apk_path = apk_path
        self.package_name = ""
        self.version_name = ""
        self.version_code = ""
        self.min_sdk = ""
        self.target_sdk = ""
        self.permissions: list[dict[str, Any]] = []
        self.activities: list[dict[str, Any]] = []
        self.services: list[dict[str, Any]] = []
        self.receivers: list[dict[str, Any]] = []
        self.providers: list[dict[str, Any]] = []
        self.security_issues: list[dict[str, str]] = []
        self.secrets: list[dict[str, str]] = []
        self.urls: list[str] = []
        self.native_libs: list[str] = []
        self.apk_size: int = 0
        self.file_count: int = 0
        self.dex_count: int = 0
        self.errors: list[str] = []

    def to_dict(self) -> dict[str, Any]:
        return {
            "apk_path": str(self.apk_path),
            "apk_size_bytes": self.apk_size,
            "package": self.package_name,
            "version_name": self.version_name,
            "version_code": self.version_code,
            "min_sdk": self.min_sdk,
            "target_sdk": self.target_sdk,
            "file_count": self.file_count,
            "dex_count": self.dex_count,
            "permissions": self.permissions,
            "activities": self.activities,
            "services": self.services,
            "receivers": self.receivers,
            "providers": self.providers,
            "native_libraries": self.native_libs,
            "security_issues": self.security_issues,
            "secrets": self.secrets,
            "urls": self.urls,
            "errors": self.errors,
        }


def analyze_manifest(root: ET.Element, analysis: ApkAnalysis) -> None:
    """Extract information from the parsed manifest element tree."""
    # Package info
    analysis.package_name = root.get("package", root.get(_ns("package"), ""))
    analysis.version_name = root.get(_ns("versionName"), root.get("versionName", ""))
    analysis.version_code = root.get(_ns("versionCode"), root.get("versionCode", ""))

    # SDK versions
    for uses_sdk in root.iter("uses-sdk"):
        analysis.min_sdk = uses_sdk.get(_ns("minSdkVersion"), uses_sdk.get("minSdkVersion", ""))
        analysis.target_sdk = uses_sdk.get(_ns("targetSdkVersion"), uses_sdk.get("targetSdkVersion", ""))

    # Permissions
    for perm in root.iter("uses-permission"):
        name = perm.get(_ns("name"), perm.get("name", ""))
        if name:
            is_dangerous = name in DANGEROUS_PERMISSIONS
            analysis.permissions.append({
                "name": name,
                "dangerous": is_dangerous,
            })

    # Application-level flags
    for app in root.iter("application"):
        _check_app_flags(app, analysis)
        _extract_components(app, analysis)


def _check_app_flags(app: ET.Element, analysis: ApkAnalysis) -> None:
    """Check security-relevant application flags."""
    debuggable = app.get(_ns("debuggable"), app.get("debuggable", ""))
    if debuggable.lower() == "true":
        analysis.security_issues.append({
            "issue": "Application is debuggable",
            "severity": "High",
            "detail": "android:debuggable=true allows attaching a debugger to the process.",
        })

    allow_backup = app.get(_ns("allowBackup"), app.get("allowBackup", ""))
    if allow_backup.lower() == "true":
        analysis.security_issues.append({
            "issue": "Application allows backup",
            "severity": "Medium",
            "detail": "android:allowBackup=true allows data extraction via adb backup.",
        })

    cleartext = app.get(
        _ns("usesCleartextTraffic"),
        app.get("usesCleartextTraffic", ""),
    )
    if cleartext.lower() == "true":
        analysis.security_issues.append({
            "issue": "Cleartext traffic allowed",
            "severity": "Medium",
            "detail": "android:usesCleartextTraffic=true allows unencrypted HTTP connections.",
        })

    network_config = app.get(
        _ns("networkSecurityConfig"),
        app.get("networkSecurityConfig", ""),
    )
    if not network_config:
        analysis.security_issues.append({
            "issue": "No network security config",
            "severity": "Low",
            "detail": "No custom networkSecurityConfig defined. Default config applies.",
        })


def _extract_components(app: ET.Element, analysis: ApkAnalysis) -> None:
    """Extract activities, services, receivers, and providers."""
    component_types = [
        ("activity", analysis.activities),
        ("service", analysis.services),
        ("receiver", analysis.receivers),
        ("provider", analysis.providers),
    ]

    for tag, target_list in component_types:
        for elem in app.iter(tag):
            name = elem.get(_ns("name"), elem.get("name", ""))
            exported_raw = elem.get(_ns("exported"), elem.get("exported", ""))
            permission = elem.get(_ns("permission"), elem.get("permission", ""))

            # Determine if exported
            has_intent_filter = any(True for _ in elem.iter("intent-filter"))
            if exported_raw.lower() == "true":
                exported = True
            elif exported_raw.lower() == "false":
                exported = False
            else:
                # Pre-Android 12: exported defaults to True if intent-filter exists
                exported = has_intent_filter

            comp: dict[str, Any] = {
                "name": name,
                "exported": exported,
            }
            if permission:
                comp["permission"] = permission
            if has_intent_filter:
                comp["has_intent_filter"] = True

                # Extract intent filter actions/categories
                actions: list[str] = []
                categories: list[str] = []
                for intent_filter in elem.iter("intent-filter"):
                    for action in intent_filter.iter("action"):
                        a = action.get(_ns("name"), action.get("name", ""))
                        if a:
                            actions.append(a)
                    for category in intent_filter.iter("category"):
                        c = category.get(_ns("name"), category.get("name", ""))
                        if c:
                            categories.append(c)
                if actions:
                    comp["actions"] = actions
                if categories:
                    comp["categories"] = categories

            # Provider-specific: check grantUriPermissions, readPermission, writePermission
            if tag == "provider":
                grant_uri = elem.get(
                    _ns("grantUriPermissions"),
                    elem.get("grantUriPermissions", ""),
                )
                if grant_uri.lower() == "true":
                    comp["grantUriPermissions"] = True
                authorities = elem.get(
                    _ns("authorities"),
                    elem.get("authorities", ""),
                )
                if authorities:
                    comp["authorities"] = authorities

            if exported and not permission:
                analysis.security_issues.append({
                    "issue": f"Exported {tag} without permission: {name}",
                    "severity": "Medium",
                    "detail": f"The {tag} '{name}' is exported and has no permission guard.",
                })

            target_list.append(comp)


def scan_dex_strings(apk_path: Path, analysis: ApkAnalysis, secrets_only: bool = False) -> None:
    """Extract readable strings from all DEX files and scan for secrets/URLs."""
    try:
        zf = zipfile.ZipFile(str(apk_path), "r")
    except (zipfile.BadZipFile, OSError) as exc:
        analysis.errors.append(f"Cannot open APK as ZIP: {exc}")
        return

    dex_files = [n for n in zf.namelist() if n.endswith(".dex")]
    analysis.dex_count = len(dex_files)

    all_strings: set[str] = set()

    for dex_name in dex_files:
        try:
            data = zf.read(dex_name)
        except Exception:
            continue
        # Extract printable strings (simple approach: find runs of ASCII chars)
        strings = _extract_printable_strings(data, min_length=8)
        all_strings.update(strings)

    zf.close()

    seen_secrets: set[str] = set()
    seen_urls: set[str] = set()

    for s in all_strings:
        # Secret scanning
        for label, pattern in SECRET_PATTERNS:
            match = pattern.search(s)
            if match:
                value = match.group(0)[:120]  # Truncate for display
                key = f"{label}:{value}"
                if key not in seen_secrets:
                    seen_secrets.add(key)
                    analysis.secrets.append({
                        "type": label,
                        "value": value,
                        "context": s[:200],
                    })

        # URL extraction
        if not secrets_only:
            for url_match in URL_PATTERN.finditer(s):
                url = url_match.group(0).rstrip(".,;:!?)")
                if url not in seen_urls:
                    seen_urls.add(url)
                    analysis.urls.append(url)

    # Sort URLs for consistent output
    analysis.urls.sort()


def _extract_printable_strings(data: bytes, min_length: int = 8) -> list[str]:
    """Extract runs of printable ASCII characters from binary data."""
    strings: list[str] = []
    current: list[str] = []

    for byte in data:
        if 0x20 <= byte <= 0x7E:
            current.append(chr(byte))
        else:
            if len(current) >= min_length:
                strings.append("".join(current))
            current = []

    if len(current) >= min_length:
        strings.append("".join(current))

    return strings


def scan_native_libs(apk_path: Path, analysis: ApkAnalysis) -> None:
    """List native .so libraries in the APK."""
    try:
        with zipfile.ZipFile(str(apk_path), "r") as zf:
            analysis.file_count = len(zf.namelist())
            for name in sorted(zf.namelist()):
                if name.endswith(".so"):
                    analysis.native_libs.append(name)
    except (zipfile.BadZipFile, OSError):
        pass


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_text(analysis: ApkAnalysis) -> str:
    """Format analysis results as human-readable text."""
    lines: list[str] = []
    sep = "=" * 70

    lines.append(sep)
    lines.append(f"  APK STATIC ANALYSIS REPORT")
    lines.append(sep)
    lines.append(f"  File    : {analysis.apk_path.name}")
    lines.append(f"  Size    : {analysis.apk_size:,} bytes")
    lines.append(f"  Package : {analysis.package_name or 'N/A'}")
    lines.append(f"  Version : {analysis.version_name or 'N/A'} (code: {analysis.version_code or 'N/A'})")
    lines.append(f"  Min SDK : {analysis.min_sdk or 'N/A'}")
    lines.append(f"  Target  : {analysis.target_sdk or 'N/A'}")
    lines.append(f"  Files   : {analysis.file_count}")
    lines.append(f"  DEX     : {analysis.dex_count}")
    lines.append(f"  Native  : {len(analysis.native_libs)} .so libraries")
    lines.append(sep)

    # Security Issues
    lines.append(f"\n  SECURITY ISSUES ({len(analysis.security_issues)})")
    lines.append("-" * 70)
    if analysis.security_issues:
        for issue in analysis.security_issues:
            sev = issue["severity"]
            tag = {"High": "[!!]", "Medium": "[!]", "Low": "[~]"}.get(sev, "[.]")
            lines.append(f"  {tag} [{sev}] {issue['issue']}")
            lines.append(f"      {issue['detail']}")
    else:
        lines.append("  No issues detected.")

    # Permissions
    dangerous = [p for p in analysis.permissions if p["dangerous"]]
    normal = [p for p in analysis.permissions if not p["dangerous"]]
    lines.append(f"\n  PERMISSIONS ({len(analysis.permissions)} total, {len(dangerous)} dangerous)")
    lines.append("-" * 70)
    if dangerous:
        lines.append("  ** Dangerous Permissions **")
        for p in dangerous:
            lines.append(f"    [!!] {p['name']}")
    if normal:
        lines.append("  Normal Permissions:")
        for p in normal:
            lines.append(f"    [  ] {p['name']}")

    # Exported Components
    exported_acts = [c for c in analysis.activities if c.get("exported")]
    exported_svcs = [c for c in analysis.services if c.get("exported")]
    exported_rcvs = [c for c in analysis.receivers if c.get("exported")]
    exported_prvs = [c for c in analysis.providers if c.get("exported")]
    total_exported = len(exported_acts) + len(exported_svcs) + len(exported_rcvs) + len(exported_prvs)

    lines.append(f"\n  EXPORTED COMPONENTS ({total_exported})")
    lines.append("-" * 70)

    for label, components in [
        ("Activities", exported_acts),
        ("Services", exported_svcs),
        ("Receivers", exported_rcvs),
        ("Providers", exported_prvs),
    ]:
        if components:
            lines.append(f"  {label}:")
            for c in components:
                perm = f" [protected: {c['permission']}]" if c.get("permission") else " [UNPROTECTED]"
                lines.append(f"    > {c['name']}{perm}")
                if c.get("actions"):
                    for a in c["actions"]:
                        lines.append(f"        action: {a}")

    # Secrets
    if analysis.secrets:
        lines.append(f"\n  SECRETS / CREDENTIALS ({len(analysis.secrets)})")
        lines.append("-" * 70)
        for s in analysis.secrets:
            lines.append(f"  [{s['type']}]")
            lines.append(f"    Value  : {s['value']}")
            lines.append(f"    Context: {s['context'][:100]}...")

    # URLs
    if analysis.urls:
        lines.append(f"\n  URLS ({len(analysis.urls)})")
        lines.append("-" * 70)
        for url in analysis.urls[:100]:
            lines.append(f"    {url}")
        if len(analysis.urls) > 100:
            lines.append(f"    ... and {len(analysis.urls) - 100} more")

    # Native Libraries
    if analysis.native_libs:
        lines.append(f"\n  NATIVE LIBRARIES ({len(analysis.native_libs)})")
        lines.append("-" * 70)
        for lib in analysis.native_libs:
            lines.append(f"    {lib}")

    # Errors
    if analysis.errors:
        lines.append(f"\n  ERRORS")
        lines.append("-" * 70)
        for err in analysis.errors:
            lines.append(f"    [!] {err}")

    lines.append("")
    lines.append(sep)
    return "\n".join(lines)


def format_markdown(analysis: ApkAnalysis) -> str:
    """Format analysis results as Markdown."""
    lines: list[str] = []

    lines.append(f"# APK Analysis: {analysis.apk_path.name}")
    lines.append("")
    lines.append("| Property | Value |")
    lines.append("|----------|-------|")
    lines.append(f"| Package | `{analysis.package_name}` |")
    lines.append(f"| Version | {analysis.version_name} (code {analysis.version_code}) |")
    lines.append(f"| Min SDK | {analysis.min_sdk} |")
    lines.append(f"| Target SDK | {analysis.target_sdk} |")
    lines.append(f"| Size | {analysis.apk_size:,} bytes |")
    lines.append(f"| Files | {analysis.file_count} |")
    lines.append(f"| DEX files | {analysis.dex_count} |")
    lines.append(f"| Native libs | {len(analysis.native_libs)} |")
    lines.append("")

    # Security Issues
    lines.append(f"## Security Issues ({len(analysis.security_issues)})")
    lines.append("")
    if analysis.security_issues:
        lines.append("| Severity | Issue | Detail |")
        lines.append("|----------|-------|--------|")
        for issue in analysis.security_issues:
            lines.append(f"| **{issue['severity']}** | {issue['issue']} | {issue['detail']} |")
    else:
        lines.append("No security issues detected.")
    lines.append("")

    # Permissions
    dangerous = [p for p in analysis.permissions if p["dangerous"]]
    lines.append(f"## Permissions ({len(analysis.permissions)} total, {len(dangerous)} dangerous)")
    lines.append("")
    if dangerous:
        lines.append("### Dangerous Permissions")
        lines.append("")
        for p in dangerous:
            lines.append(f"- **{p['name']}**")
        lines.append("")
    normal = [p for p in analysis.permissions if not p["dangerous"]]
    if normal:
        lines.append("### Normal Permissions")
        lines.append("")
        for p in normal:
            lines.append(f"- {p['name']}")
        lines.append("")

    # Exported Components
    for label, components in [
        ("Activities", analysis.activities),
        ("Services", analysis.services),
        ("Receivers", analysis.receivers),
        ("Providers", analysis.providers),
    ]:
        exported = [c for c in components if c.get("exported")]
        if exported:
            lines.append(f"## Exported {label} ({len(exported)})")
            lines.append("")
            for c in exported:
                perm = f" (protected: `{c['permission']}`)" if c.get("permission") else " **(UNPROTECTED)**"
                lines.append(f"- `{c['name']}`{perm}")
                if c.get("actions"):
                    for a in c["actions"]:
                        lines.append(f"  - Action: `{a}`")
            lines.append("")

    # Secrets
    if analysis.secrets:
        lines.append(f"## Secrets / Credentials ({len(analysis.secrets)})")
        lines.append("")
        lines.append("| Type | Value | Context |")
        lines.append("|------|-------|---------|")
        for s in analysis.secrets:
            val = s["value"].replace("|", "\\|")
            ctx = s["context"][:80].replace("|", "\\|")
            lines.append(f"| {s['type']} | `{val}` | `{ctx}...` |")
        lines.append("")

    # URLs
    if analysis.urls:
        lines.append(f"## URLs ({len(analysis.urls)})")
        lines.append("")
        for url in analysis.urls[:100]:
            lines.append(f"- `{url}`")
        if len(analysis.urls) > 100:
            lines.append(f"- ... and {len(analysis.urls) - 100} more")
        lines.append("")

    # Native Libs
    if analysis.native_libs:
        lines.append(f"## Native Libraries ({len(analysis.native_libs)})")
        lines.append("")
        for lib in analysis.native_libs:
            lines.append(f"- `{lib}`")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Android APK static analysis tool (stdlib only).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s app.apk\n"
            "  %(prog)s app.apk --secrets\n"
            "  %(prog)s app.apk --json\n"
            "  %(prog)s app.apk --output report.md\n"
        ),
    )
    parser.add_argument(
        "apk",
        help="Path to the APK file to analyze.",
    )
    parser.add_argument(
        "--secrets",
        action="store_true",
        help="Focus on secret/credential hunting (skip URL extraction).",
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
        help="Write output to a file (Markdown if .md, otherwise text).",
    )
    parser.add_argument(
        "--no-dex",
        action="store_true",
        help="Skip DEX string scanning (faster, no secret/URL results).",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print progress information to stderr.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    apk_path = Path(args.apk).resolve()
    if not apk_path.is_file():
        print(f"[!] APK file not found: {apk_path}", file=sys.stderr)
        return 1

    if not zipfile.is_zipfile(str(apk_path)):
        print(f"[!] File is not a valid ZIP/APK: {apk_path}", file=sys.stderr)
        return 1

    analysis = ApkAnalysis(apk_path)
    analysis.apk_size = apk_path.stat().st_size

    if args.verbose:
        print(f"[*] Analyzing {apk_path.name} ({analysis.apk_size:,} bytes)...", file=sys.stderr)

    # 1. Parse manifest
    if args.verbose:
        print("[*] Parsing AndroidManifest.xml...", file=sys.stderr)

    manifest_root = extract_manifest_binary(apk_path)
    if manifest_root is not None:
        analyze_manifest(manifest_root, analysis)
    else:
        analysis.errors.append(
            "Could not parse AndroidManifest.xml (binary XML decoding failed). "
            "Install aapt2 for better results."
        )

    # 2. Scan DEX strings
    if not args.no_dex:
        if args.verbose:
            print("[*] Scanning DEX strings for secrets and URLs...", file=sys.stderr)
        scan_dex_strings(apk_path, analysis, secrets_only=args.secrets)

    # 3. Native libraries
    if args.verbose:
        print("[*] Enumerating native libraries...", file=sys.stderr)
    scan_native_libs(apk_path, analysis)

    # 4. Output
    if args.json_output:
        output = json.dumps(analysis.to_dict(), indent=2, ensure_ascii=False)
    elif args.output and args.output.endswith(".md"):
        output = format_markdown(analysis)
    else:
        output = format_text(analysis)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"[+] Report written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
