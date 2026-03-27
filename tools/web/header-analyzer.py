#!/usr/bin/env python3
"""
HTTP Security Header Analyzer
AI-RedTeam-Toolkit | Authorized Security Testing Only

Analyzes HTTP response headers for security misconfigurations, missing
protections, and information leaks. Provides grading (A-F) and remediation.

Features:
  - Checks all critical security headers (HSTS, CSP, X-Frame-Options, etc.)
  - Detects information leak headers (Server, X-Powered-By, X-AspNet-Version)
  - CORS misconfiguration analysis
  - Security grade calculation (A-F)
  - Remediation recommendations for each finding
  - JSON output mode for automation

Usage:
  python3 header-analyzer.py https://target.com
  python3 header-analyzer.py https://target.com --json
  python3 header-analyzer.py https://target.com --check-cors --origin https://evil.com
  python3 header-analyzer.py https://target.com --timeout 15 --follow-redirects

No external dependencies required - stdlib only.
"""

import argparse
import json
import ssl
import sys
import time
import urllib.error
import urllib.request
from typing import Optional
from http.client import HTTPResponse

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

VERSION = "1.0.0"

BANNER = r"""
    ╦ ╦┌─┐┌─┐┌┬┐┌─┐┬─┐  ╔═╗┌┐┌┌─┐┬ ┬ ┬┌─┐┌─┐┬─┐
    ╠═╣├┤ ├─┤ ││├┤ ├┬┘  ╠═╣│││├─┤│ └┬┘┌─┘├┤ ├┬┘
    ╩ ╩└─┘┴ ┴─┴┘└─┘┴└─  ╩ ╩┘└┘┴ ┴┴─┘┴ └─┘└─┘┴└─
    AI-RedTeam-Toolkit | HTTP Security Headers v{version}
    ─────────────────────────────────────────────────
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
    WHITE = "\033[97m"

    @classmethod
    def disable(cls):
        for attr in ["RESET", "BOLD", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "GRAY", "WHITE"]:
            setattr(cls, attr, "")


# Severity levels
SEVERITY_CRITICAL = "CRITICAL"
SEVERITY_HIGH = "HIGH"
SEVERITY_MEDIUM = "MEDIUM"
SEVERITY_LOW = "LOW"
SEVERITY_INFO = "INFO"

SEVERITY_COLORS = {
    SEVERITY_CRITICAL: "RED",
    SEVERITY_HIGH: "RED",
    SEVERITY_MEDIUM: "YELLOW",
    SEVERITY_LOW: "BLUE",
    SEVERITY_INFO: "GRAY",
}

# Points deducted per severity (from a base of 100)
SEVERITY_DEDUCTIONS = {
    SEVERITY_CRITICAL: 25,
    SEVERITY_HIGH: 15,
    SEVERITY_MEDIUM: 8,
    SEVERITY_LOW: 4,
    SEVERITY_INFO: 0,
}


# ──────────────────────────────────────────────────────────────────────────────
# Header check definitions
# ──────────────────────────────────────────────────────────────────────────────


def check_hsts(headers: dict) -> dict:
    """Check HTTP Strict-Transport-Security header."""
    value = headers.get("strict-transport-security")
    result = {
        "header": "Strict-Transport-Security",
        "value": value,
        "present": value is not None,
    }

    if not value:
        result["status"] = "MISSING"
        result["severity"] = SEVERITY_HIGH
        result["description"] = "HSTS header is missing. The site does not enforce HTTPS connections."
        result["remediation"] = (
            "Add header: Strict-Transport-Security: max-age=31536000; includeSubDomains; preload"
        )
        return result

    issues = []
    # Check max-age
    if "max-age=" in value.lower():
        try:
            max_age_str = value.lower().split("max-age=")[1].split(";")[0].strip()
            max_age = int(max_age_str)
            if max_age < 31536000:
                issues.append(f"max-age is {max_age} (less than 1 year / 31536000)")
            if max_age == 0:
                issues.append("max-age=0 effectively disables HSTS")
        except (ValueError, IndexError):
            issues.append("Could not parse max-age value")
    else:
        issues.append("max-age directive is missing")

    if "includesubdomains" not in value.lower():
        issues.append("includeSubDomains directive missing")

    if issues:
        result["status"] = "MISCONFIGURED"
        result["severity"] = SEVERITY_MEDIUM
        result["issues"] = issues
        result["description"] = "HSTS header present but has configuration issues."
        result["remediation"] = (
            "Recommended: Strict-Transport-Security: max-age=31536000; includeSubDomains; preload"
        )
    else:
        result["status"] = "OK"
        result["severity"] = SEVERITY_INFO
        result["description"] = "HSTS header is properly configured."

    return result


def check_csp(headers: dict) -> dict:
    """Check Content-Security-Policy header."""
    value = headers.get("content-security-policy")
    report_only = headers.get("content-security-policy-report-only")

    result = {
        "header": "Content-Security-Policy",
        "value": value,
        "present": value is not None,
    }

    if not value:
        if report_only:
            result["status"] = "REPORT_ONLY"
            result["severity"] = SEVERITY_MEDIUM
            result["value"] = report_only
            result["description"] = "CSP is in report-only mode, not enforced."
            result["remediation"] = (
                "Move from Content-Security-Policy-Report-Only to Content-Security-Policy to enforce the policy."
            )
        else:
            result["status"] = "MISSING"
            result["severity"] = SEVERITY_HIGH
            result["description"] = "No Content-Security-Policy header. The site is vulnerable to XSS and data injection attacks."
            result["remediation"] = (
                "Implement a CSP. Start with: Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'self'"
            )
        return result

    issues = []
    val_lower = value.lower()

    # Dangerous directives
    if "unsafe-inline" in val_lower:
        issues.append("'unsafe-inline' allows inline scripts/styles (XSS risk)")
    if "unsafe-eval" in val_lower:
        issues.append("'unsafe-eval' allows eval() and similar (XSS risk)")
    if "data:" in val_lower and "script-src" in val_lower.split("data:")[0].rsplit(";", 1)[-1]:
        issues.append("data: URI in script-src allows script injection")

    # Wildcard sources
    if "script-src" in val_lower:
        script_directive = ""
        for directive in value.split(";"):
            if "script-src" in directive.lower():
                script_directive = directive
                break
        if " * " in f" {script_directive} " or script_directive.strip().endswith(" *"):
            issues.append("Wildcard (*) in script-src allows loading scripts from any origin")

    if "default-src" not in val_lower and "script-src" not in val_lower:
        issues.append("Neither default-src nor script-src defined")

    if issues:
        result["status"] = "WEAK"
        result["severity"] = SEVERITY_MEDIUM
        result["issues"] = issues
        result["description"] = "CSP is present but has weaknesses that could be exploited."
        result["remediation"] = (
            "Remove 'unsafe-inline' and 'unsafe-eval'. Use nonce-based or hash-based CSP instead. "
            "Avoid wildcard sources in script-src."
        )
    else:
        result["status"] = "OK"
        result["severity"] = SEVERITY_INFO
        result["description"] = "Content-Security-Policy header is present."

    return result


def check_x_frame_options(headers: dict) -> dict:
    """Check X-Frame-Options header."""
    value = headers.get("x-frame-options")
    result = {
        "header": "X-Frame-Options",
        "value": value,
        "present": value is not None,
    }

    if not value:
        result["status"] = "MISSING"
        result["severity"] = SEVERITY_MEDIUM
        result["description"] = "X-Frame-Options not set. The site may be vulnerable to clickjacking."
        result["remediation"] = (
            "Add header: X-Frame-Options: DENY (or SAMEORIGIN if framing from same origin is needed). "
            "Also consider using CSP frame-ancestors directive."
        )
        return result

    val_upper = value.strip().upper()
    if val_upper in ("DENY", "SAMEORIGIN"):
        result["status"] = "OK"
        result["severity"] = SEVERITY_INFO
        result["description"] = f"X-Frame-Options is set to {val_upper}."
    elif val_upper.startswith("ALLOW-FROM"):
        result["status"] = "DEPRECATED"
        result["severity"] = SEVERITY_LOW
        result["description"] = "ALLOW-FROM is deprecated and not supported by modern browsers."
        result["remediation"] = "Use CSP frame-ancestors directive instead of ALLOW-FROM."
    else:
        result["status"] = "INVALID"
        result["severity"] = SEVERITY_MEDIUM
        result["description"] = f"Invalid X-Frame-Options value: {value}"
        result["remediation"] = "Set to DENY or SAMEORIGIN."

    return result


def check_x_content_type_options(headers: dict) -> dict:
    """Check X-Content-Type-Options header."""
    value = headers.get("x-content-type-options")
    result = {
        "header": "X-Content-Type-Options",
        "value": value,
        "present": value is not None,
    }

    if not value:
        result["status"] = "MISSING"
        result["severity"] = SEVERITY_MEDIUM
        result["description"] = "X-Content-Type-Options not set. The browser may MIME-sniff responses, leading to XSS."
        result["remediation"] = "Add header: X-Content-Type-Options: nosniff"
        return result

    if value.strip().lower() == "nosniff":
        result["status"] = "OK"
        result["severity"] = SEVERITY_INFO
        result["description"] = "X-Content-Type-Options is properly set to nosniff."
    else:
        result["status"] = "INVALID"
        result["severity"] = SEVERITY_MEDIUM
        result["description"] = f"Unexpected value: {value}. Expected 'nosniff'."
        result["remediation"] = "Set to: X-Content-Type-Options: nosniff"

    return result


def check_referrer_policy(headers: dict) -> dict:
    """Check Referrer-Policy header."""
    value = headers.get("referrer-policy")
    result = {
        "header": "Referrer-Policy",
        "value": value,
        "present": value is not None,
    }

    if not value:
        result["status"] = "MISSING"
        result["severity"] = SEVERITY_LOW
        result["description"] = "Referrer-Policy not set. Full URL referrer may leak sensitive data in query strings."
        result["remediation"] = (
            "Add header: Referrer-Policy: strict-origin-when-cross-origin (or no-referrer for maximum privacy)"
        )
        return result

    safe_policies = [
        "no-referrer", "same-origin", "strict-origin",
        "strict-origin-when-cross-origin", "no-referrer-when-downgrade",
    ]
    unsafe_policies = ["unsafe-url"]

    val_lower = value.strip().lower()
    # May contain multiple comma-separated fallback values
    policies = [p.strip() for p in val_lower.split(",")]

    if any(p in unsafe_policies for p in policies):
        result["status"] = "UNSAFE"
        result["severity"] = SEVERITY_MEDIUM
        result["description"] = "Referrer-Policy set to 'unsafe-url' leaks the full URL as referrer."
        result["remediation"] = "Change to: Referrer-Policy: strict-origin-when-cross-origin"
    elif any(p in safe_policies for p in policies):
        result["status"] = "OK"
        result["severity"] = SEVERITY_INFO
        result["description"] = f"Referrer-Policy is set to: {value}"
    else:
        result["status"] = "UNKNOWN"
        result["severity"] = SEVERITY_LOW
        result["description"] = f"Unrecognized Referrer-Policy value: {value}"
        result["remediation"] = "Use a standard value: strict-origin-when-cross-origin"

    return result


def check_permissions_policy(headers: dict) -> dict:
    """Check Permissions-Policy (formerly Feature-Policy) header."""
    value = headers.get("permissions-policy")
    legacy = headers.get("feature-policy")
    result = {
        "header": "Permissions-Policy",
        "value": value or legacy,
        "present": value is not None or legacy is not None,
    }

    if not value and not legacy:
        result["status"] = "MISSING"
        result["severity"] = SEVERITY_LOW
        result["description"] = (
            "Permissions-Policy not set. Browser features (camera, microphone, geolocation) "
            "are not restricted."
        )
        result["remediation"] = (
            "Add header: Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()"
        )
        return result

    if legacy and not value:
        result["status"] = "DEPRECATED"
        result["severity"] = SEVERITY_LOW
        result["description"] = "Using deprecated Feature-Policy header instead of Permissions-Policy."
        result["remediation"] = "Migrate from Feature-Policy to Permissions-Policy header."
        return result

    result["status"] = "OK"
    result["severity"] = SEVERITY_INFO
    result["description"] = "Permissions-Policy header is present."
    return result


def check_x_xss_protection(headers: dict) -> dict:
    """Check X-XSS-Protection header."""
    value = headers.get("x-xss-protection")
    result = {
        "header": "X-XSS-Protection",
        "value": value,
        "present": value is not None,
    }

    if not value:
        result["status"] = "MISSING"
        result["severity"] = SEVERITY_INFO  # Deprecated header, CSP is preferred
        result["description"] = (
            "X-XSS-Protection not set. This header is deprecated in modern browsers, "
            "but can provide defense-in-depth for older ones."
        )
        result["remediation"] = (
            "For legacy browser support: X-XSS-Protection: 0 (disable to avoid side-channel attacks) "
            "or rely on CSP instead."
        )
        return result

    val = value.strip()
    if val == "0":
        result["status"] = "DISABLED"
        result["severity"] = SEVERITY_INFO
        result["description"] = (
            "X-XSS-Protection explicitly disabled. This is the recommended setting for modern browsers "
            "when CSP is in place, as the XSS auditor can introduce vulnerabilities."
        )
    elif val.startswith("1"):
        if "mode=block" in val:
            result["status"] = "ENABLED_BLOCK"
            result["severity"] = SEVERITY_INFO
            result["description"] = "X-XSS-Protection enabled with mode=block."
        else:
            result["status"] = "ENABLED"
            result["severity"] = SEVERITY_LOW
            result["description"] = (
                "X-XSS-Protection enabled without mode=block. Without block mode, "
                "the browser may still render the page with modifications, which "
                "can sometimes be exploited."
            )
            result["remediation"] = "Set to: X-XSS-Protection: 1; mode=block (or 0 with CSP)"
    else:
        result["status"] = "UNKNOWN"
        result["severity"] = SEVERITY_LOW
        result["description"] = f"Unexpected X-XSS-Protection value: {value}"

    return result


def check_cache_control(headers: dict) -> dict:
    """Check Cache-Control for sensitive pages."""
    value = headers.get("cache-control")
    pragma = headers.get("pragma")
    result = {
        "header": "Cache-Control",
        "value": value,
        "present": value is not None,
    }

    if not value:
        result["status"] = "MISSING"
        result["severity"] = SEVERITY_LOW
        result["description"] = "No Cache-Control header. Sensitive data may be cached by proxies or browsers."
        result["remediation"] = (
            "For sensitive pages: Cache-Control: no-store, no-cache, must-revalidate, private"
        )
        return result

    val_lower = value.lower()
    if "no-store" in val_lower:
        result["status"] = "OK"
        result["severity"] = SEVERITY_INFO
        result["description"] = "Cache-Control includes no-store."
    elif "private" in val_lower:
        result["status"] = "PARTIAL"
        result["severity"] = SEVERITY_INFO
        result["description"] = "Cache-Control is set to private but does not include no-store."
    elif "public" in val_lower:
        result["status"] = "PUBLIC"
        result["severity"] = SEVERITY_LOW
        result["description"] = (
            "Cache-Control is set to public. Sensitive responses should not use public caching."
        )
        result["remediation"] = "For sensitive pages: Cache-Control: no-store, no-cache, must-revalidate, private"
    else:
        result["status"] = "OK"
        result["severity"] = SEVERITY_INFO
        result["description"] = f"Cache-Control: {value}"

    return result


# ──────────────────────────────────────────────────────────────────────────────
# Information leak checks
# ──────────────────────────────────────────────────────────────────────────────

INFO_LEAK_HEADERS = {
    "server": {
        "name": "Server",
        "severity": SEVERITY_LOW,
        "description": "Server header reveals web server software and version.",
        "remediation": "Remove or minimize the Server header. Avoid disclosing version numbers.",
    },
    "x-powered-by": {
        "name": "X-Powered-By",
        "severity": SEVERITY_LOW,
        "description": "X-Powered-By reveals the technology stack (e.g., PHP, ASP.NET, Express).",
        "remediation": "Remove the X-Powered-By header entirely.",
    },
    "x-aspnet-version": {
        "name": "X-AspNet-Version",
        "severity": SEVERITY_MEDIUM,
        "description": "X-AspNet-Version discloses the exact .NET framework version.",
        "remediation": "Remove this header. In web.config: <httpRuntime enableVersionHeader=\"false\" />",
    },
    "x-aspnetmvc-version": {
        "name": "X-AspNetMvc-Version",
        "severity": SEVERITY_MEDIUM,
        "description": "X-AspNetMvc-Version discloses the ASP.NET MVC version.",
        "remediation": "Remove this header. Add MvcHandler.DisableMvcResponseHeader = true in Application_Start.",
    },
    "x-generator": {
        "name": "X-Generator",
        "severity": SEVERITY_LOW,
        "description": "X-Generator reveals the CMS or framework used.",
        "remediation": "Remove the X-Generator header.",
    },
    "via": {
        "name": "Via",
        "severity": SEVERITY_INFO,
        "description": "Via header reveals proxy/gateway information.",
        "remediation": "Consider removing if it reveals internal infrastructure details.",
    },
    "x-runtime": {
        "name": "X-Runtime",
        "severity": SEVERITY_LOW,
        "description": "X-Runtime reveals server-side processing time (timing oracle).",
        "remediation": "Remove the X-Runtime header to prevent timing-based information disclosure.",
    },
}


def check_info_leaks(headers: dict) -> list:
    """Check for information leakage headers."""
    findings = []
    for header_key, info in INFO_LEAK_HEADERS.items():
        value = headers.get(header_key)
        if value:
            findings.append({
                "header": info["name"],
                "value": value,
                "present": True,
                "status": "LEAK",
                "severity": info["severity"],
                "description": info["description"],
                "remediation": info["remediation"],
            })
    return findings


# ──────────────────────────────────────────────────────────────────────────────
# CORS check
# ──────────────────────────────────────────────────────────────────────────────


def check_cors(headers: dict, cors_origin: Optional[str] = None) -> dict:
    """Analyze CORS configuration."""
    acao = headers.get("access-control-allow-origin")
    acac = headers.get("access-control-allow-credentials")
    acam = headers.get("access-control-allow-methods")
    acah = headers.get("access-control-allow-headers")

    result = {
        "header": "CORS (Access-Control-Allow-Origin)",
        "value": acao,
        "present": acao is not None,
    }

    if not acao:
        result["status"] = "NOT_SET"
        result["severity"] = SEVERITY_INFO
        result["description"] = "No CORS headers present (cross-origin requests will be blocked by default)."
        return result

    issues = []

    # Wildcard origin
    if acao.strip() == "*":
        if acac and acac.lower() == "true":
            issues.append("CRITICAL: Access-Control-Allow-Origin: * with Access-Control-Allow-Credentials: true is a severe misconfiguration")
            result["severity"] = SEVERITY_CRITICAL
        else:
            issues.append("Wildcard (*) origin allows any domain to read responses")
            result["severity"] = SEVERITY_MEDIUM

    # Reflected origin
    if cors_origin and acao.strip() == cors_origin:
        issues.append(f"Origin '{cors_origin}' was reflected back - potential origin reflection vulnerability")
        if acac and acac.lower() == "true":
            issues.append("Combined with credentials: true, this allows any origin to read authenticated responses")
            result["severity"] = SEVERITY_CRITICAL
        else:
            result["severity"] = SEVERITY_HIGH

    # Null origin
    if acao.strip().lower() == "null":
        issues.append("Access-Control-Allow-Origin: null can be exploited via sandboxed iframes")
        result["severity"] = SEVERITY_HIGH

    if issues:
        result["status"] = "MISCONFIGURED"
        result["issues"] = issues
        result["description"] = "CORS configuration has security issues."
        result["remediation"] = (
            "Restrict Access-Control-Allow-Origin to specific trusted origins. "
            "Never reflect arbitrary Origin headers. Avoid using wildcard with credentials."
        )
    else:
        result["status"] = "OK"
        result["severity"] = SEVERITY_INFO
        result["description"] = f"CORS header set to: {acao}"

    # Add credential info
    if acac:
        result["allow_credentials"] = acac

    return result


# ──────────────────────────────────────────────────────────────────────────────
# HTTP request
# ──────────────────────────────────────────────────────────────────────────────


def fetch_headers(
    url: str,
    timeout: int = 10,
    follow_redirects: bool = True,
    cors_origin: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> dict:
    """Fetch HTTP headers from a URL. Returns dict with response info."""
    # Build request
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", user_agent or "Mozilla/5.0 (HeaderAnalyzer/1.0)")
    req.add_header("Accept", "text/html,application/xhtml+xml,*/*")

    if cors_origin:
        req.add_header("Origin", cors_origin)

    # SSL context (allow self-signed for pentesting)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Custom opener
    if follow_redirects:
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
    else:
        # Disable redirect following
        class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None

        opener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=ctx),
            NoRedirectHandler,
        )

    try:
        response = opener.open(req, timeout=timeout)
        status_code = response.getcode()
        raw_headers = dict(response.headers)
        final_url = response.geturl()
        response.close()
    except urllib.error.HTTPError as e:
        # We still get headers from error responses
        status_code = e.code
        raw_headers = dict(e.headers)
        final_url = url
    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to connect to {url}: {e.reason}")
    except Exception as e:
        raise ConnectionError(f"Request failed: {e}")

    # Normalize header names to lowercase for consistent lookup
    headers_lower = {}
    headers_original = {}
    for key, value in raw_headers.items():
        headers_lower[key.lower()] = value
        headers_original[key] = value

    return {
        "url": url,
        "final_url": final_url,
        "status_code": status_code,
        "headers": headers_lower,
        "headers_original": headers_original,
        "redirected": final_url != url,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Grading
# ──────────────────────────────────────────────────────────────────────────────


def calculate_grade(findings: list) -> tuple:
    """Calculate security grade from findings. Returns (grade, score, breakdown)."""
    score = 100
    breakdown = []

    for finding in findings:
        severity = finding.get("severity", SEVERITY_INFO)
        status = finding.get("status", "")

        if status in ("OK", "NOT_SET") and severity == SEVERITY_INFO:
            continue

        deduction = SEVERITY_DEDUCTIONS.get(severity, 0)
        if deduction > 0:
            header_name = finding.get("header", "unknown")
            score -= deduction
            breakdown.append({
                "header": header_name,
                "severity": severity,
                "deduction": deduction,
                "reason": finding.get("status", "issue"),
            })

    score = max(0, score)

    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 65:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"

    return grade, score, breakdown


GRADE_COLORS = {
    "A": "GREEN",
    "B": "GREEN",
    "C": "YELLOW",
    "D": "YELLOW",
    "F": "RED",
}


# ──────────────────────────────────────────────────────────────────────────────
# Analysis orchestrator
# ──────────────────────────────────────────────────────────────────────────────


def analyze(
    url: str,
    timeout: int = 10,
    follow_redirects: bool = True,
    check_cors_flag: bool = False,
    cors_origin: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> dict:
    """Run full header analysis. Returns structured results."""
    # Fetch
    response_info = fetch_headers(
        url,
        timeout=timeout,
        follow_redirects=follow_redirects,
        cors_origin=cors_origin if check_cors_flag else None,
        user_agent=user_agent,
    )
    headers = response_info["headers"]

    # Security header checks
    security_findings = [
        check_hsts(headers),
        check_csp(headers),
        check_x_frame_options(headers),
        check_x_content_type_options(headers),
        check_referrer_policy(headers),
        check_permissions_policy(headers),
        check_x_xss_protection(headers),
        check_cache_control(headers),
    ]

    # CORS check
    cors_finding = None
    if check_cors_flag:
        cors_finding = check_cors(headers, cors_origin)
        security_findings.append(cors_finding)

    # Info leak checks
    info_leak_findings = check_info_leaks(headers)

    # All findings for grading
    all_findings = security_findings + info_leak_findings

    # Grade
    grade, score, grade_breakdown = calculate_grade(all_findings)

    return {
        "url": response_info["url"],
        "final_url": response_info["final_url"],
        "status_code": response_info["status_code"],
        "redirected": response_info["redirected"],
        "headers_original": response_info["headers_original"],
        "security_findings": security_findings,
        "info_leak_findings": info_leak_findings,
        "cors_finding": cors_finding,
        "grade": grade,
        "score": score,
        "grade_breakdown": grade_breakdown,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Output: JSON
# ──────────────────────────────────────────────────────────────────────────────


def output_json(results: dict):
    """Output results as JSON."""
    output = {
        "url": results["url"],
        "final_url": results["final_url"],
        "status_code": results["status_code"],
        "redirected": results["redirected"],
        "grade": results["grade"],
        "score": results["score"],
        "security_headers": [],
        "information_leaks": [],
        "grade_breakdown": results["grade_breakdown"],
        "response_headers": results["headers_original"],
    }

    for f in results["security_findings"]:
        entry = {
            "header": f["header"],
            "value": f.get("value"),
            "present": f["present"],
            "status": f["status"],
            "severity": f["severity"],
            "description": f.get("description", ""),
        }
        if "remediation" in f:
            entry["remediation"] = f["remediation"]
        if "issues" in f:
            entry["issues"] = f["issues"]
        output["security_headers"].append(entry)

    for f in results["info_leak_findings"]:
        output["information_leaks"].append({
            "header": f["header"],
            "value": f["value"],
            "severity": f["severity"],
            "description": f["description"],
            "remediation": f["remediation"],
        })

    print(json.dumps(output, indent=2))


# ──────────────────────────────────────────────────────────────────────────────
# Output: Pretty terminal
# ──────────────────────────────────────────────────────────────────────────────


def _severity_colored(severity: str) -> str:
    """Get colored severity string."""
    color_name = SEVERITY_COLORS.get(severity, "GRAY")
    color_code = getattr(Color, color_name, Color.RESET)
    return f"{color_code}{severity}{Color.RESET}"


def _status_icon(status: str) -> str:
    """Get status icon."""
    if status == "OK":
        return f"{Color.GREEN}[+]{Color.RESET}"
    elif status == "MISSING":
        return f"{Color.RED}[-]{Color.RESET}"
    elif status in ("MISCONFIGURED", "WEAK", "UNSAFE", "LEAK", "INVALID", "DEPRECATED"):
        return f"{Color.YELLOW}[!]{Color.RESET}"
    elif status in ("ENABLED", "ENABLED_BLOCK", "DISABLED", "REPORT_ONLY", "PARTIAL", "PUBLIC", "NOT_SET"):
        return f"{Color.BLUE}[~]{Color.RESET}"
    else:
        return f"{Color.GRAY}[?]{Color.RESET}"


def output_pretty(results: dict):
    """Output results in formatted terminal output."""
    # Connection info
    print(f"\n{Color.CYAN}[*] Target Analysis{Color.RESET}")
    print(f"{Color.GRAY}{'─' * 65}{Color.RESET}")
    print(f"  URL         : {results['url']}")
    if results["redirected"]:
        print(f"  Redirected  : {Color.YELLOW}{results['final_url']}{Color.RESET}")
    print(f"  Status Code : {results['status_code']}")

    # Grade
    grade = results["grade"]
    score = results["score"]
    grade_color = getattr(Color, GRADE_COLORS.get(grade, "GRAY"), Color.RESET)
    print(f"\n{Color.CYAN}[*] Security Grade{Color.RESET}")
    print(f"{Color.GRAY}{'─' * 65}{Color.RESET}")

    # Grade display box
    grade_bar = ""
    filled = int(score / 5)  # 20 char bar
    empty = 20 - filled
    if score >= 80:
        bar_color = Color.GREEN
    elif score >= 50:
        bar_color = Color.YELLOW
    else:
        bar_color = Color.RED
    grade_bar = f"{bar_color}{'█' * filled}{Color.GRAY}{'░' * empty}{Color.RESET}"

    print(f"\n  Grade: {grade_color}{Color.BOLD}  {grade}  {Color.RESET}  Score: {grade_color}{score}/100{Color.RESET}")
    print(f"  {grade_bar}")

    if results["grade_breakdown"]:
        print(f"\n  {Color.GRAY}Deductions:{Color.RESET}")
        for item in results["grade_breakdown"]:
            print(f"    -{item['deduction']:2d} pts  {item['header']:30s}  [{_severity_colored(item['severity'])}]")

    # Security headers
    print(f"\n{Color.CYAN}[*] Security Headers{Color.RESET}")
    print(f"{Color.GRAY}{'─' * 65}{Color.RESET}")

    for finding in results["security_findings"]:
        icon = _status_icon(finding["status"])
        header_name = finding["header"]
        status = finding["status"]
        value = finding.get("value", "")

        print(f"\n  {icon} {Color.BOLD}{header_name}{Color.RESET}")
        print(f"      Status   : {status}")
        if value:
            # Truncate long values
            display_val = value if len(str(value)) < 80 else str(value)[:77] + "..."
            print(f"      Value    : {Color.GRAY}{display_val}{Color.RESET}")
        print(f"      Severity : {_severity_colored(finding['severity'])}")
        if "description" in finding:
            print(f"      Detail   : {finding['description']}")
        if "issues" in finding:
            for issue in finding["issues"]:
                print(f"      {Color.YELLOW}  -> {issue}{Color.RESET}")
        if "remediation" in finding and finding.get("status") != "OK":
            print(f"      {Color.GREEN}Fix    : {finding['remediation']}{Color.RESET}")

    # Info leaks
    if results["info_leak_findings"]:
        print(f"\n{Color.CYAN}[*] Information Leakage{Color.RESET}")
        print(f"{Color.GRAY}{'─' * 65}{Color.RESET}")

        for finding in results["info_leak_findings"]:
            print(f"\n  {Color.YELLOW}[!]{Color.RESET} {Color.BOLD}{finding['header']}{Color.RESET}: {Color.RED}{finding['value']}{Color.RESET}")
            print(f"      Severity : {_severity_colored(finding['severity'])}")
            print(f"      Detail   : {finding['description']}")
            print(f"      {Color.GREEN}Fix    : {finding['remediation']}{Color.RESET}")
    else:
        print(f"\n{Color.CYAN}[*] Information Leakage{Color.RESET}")
        print(f"{Color.GRAY}{'─' * 65}{Color.RESET}")
        print(f"  {Color.GREEN}[+] No information leak headers detected{Color.RESET}")

    # Raw headers
    print(f"\n{Color.CYAN}[*] All Response Headers{Color.RESET}")
    print(f"{Color.GRAY}{'─' * 65}{Color.RESET}")
    for key, value in results["headers_original"].items():
        display_val = value if len(str(value)) < 60 else str(value)[:57] + "..."
        print(f"  {Color.GRAY}{key}: {display_val}{Color.RESET}")

    print()


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="header-analyzer",
        description="HTTP Security Header Analyzer - AI-RedTeam-Toolkit",
        epilog="For authorized security testing only.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("url", help="Target URL to analyze (e.g. https://example.com)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    parser.add_argument("--no-banner", action="store_true", help="Suppress banner")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds (default: 10)")
    parser.add_argument(
        "--follow-redirects", action="store_true", default=True,
        help="Follow HTTP redirects (default: true)",
    )
    parser.add_argument(
        "--no-follow-redirects", action="store_true",
        help="Do not follow HTTP redirects",
    )
    parser.add_argument("--check-cors", action="store_true", help="Perform CORS configuration check")
    parser.add_argument("--origin", default="https://evil.com", help="Origin header for CORS check (default: https://evil.com)")
    parser.add_argument("--user-agent", help="Custom User-Agent string")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Handle color
    if args.no_color or not sys.stdout.isatty():
        Color.disable()

    # Banner
    if not args.no_banner and not args.json:
        print(f"{Color.CYAN}{BANNER}{Color.RESET}")

    # Validate URL
    url = args.url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        print(f"{Color.YELLOW}[!] No scheme specified, assuming https://{Color.RESET}")
        url = "https://" + url

    follow = args.follow_redirects and not args.no_follow_redirects

    if not args.json:
        print(f"{Color.CYAN}[*] Fetching headers from {url}...{Color.RESET}")

    try:
        results = analyze(
            url=url,
            timeout=args.timeout,
            follow_redirects=follow,
            check_cors_flag=args.check_cors,
            cors_origin=args.origin,
            user_agent=args.user_agent,
        )
    except ConnectionError as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"{Color.RED}[!] {e}{Color.RESET}")
        return 1
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"{Color.RED}[!] Unexpected error: {e}{Color.RESET}")
        return 1

    # Output
    if args.json:
        output_json(results)
    else:
        output_pretty(results)

    # Exit code based on grade
    grade = results["grade"]
    if grade in ("A", "B"):
        return 0
    elif grade in ("C", "D"):
        return 0  # Warnings but not failures
    else:
        return 1  # Grade F


if __name__ == "__main__":
    sys.exit(main() or 0)
