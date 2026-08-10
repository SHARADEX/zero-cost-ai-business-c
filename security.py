#!/usr/bin/env python3
"""
Security scanning for generated HTML content.

v3 had no content security scanning — the agent could ship XSS vulnerabilities
or broken HTML. v4 ships a scanner that runs before any write_file completes
on .html files.

Checks:
  1. No inline event handlers in user-input paths (onclick="..." from untrusted)
  2. No javascript: URLs in href/src
  3. No <script> with external src from non-allowlisted domains (CSP-style)
  4. No document.cookie / localStorage exfiltration patterns
  5. No private keys / API keys embedded
  6. Basic HTML structure (has <html>, <head>, <body>)
  7. No broken internal links (links to /foo that don't resolve in docs/)
"""

import os
import re
from typing import List, Tuple

# CDN domains allowed for <script src="...">
ALLOWED_SCRIPT_DOMAINS = {
    "cdn.jsdelivr.net",
    "unpkg.com",
    "cdnjs.cloudflare.com",
    "code.jquery.com",
    "ajax.googleapis.com",
    "www.googletagmanager.com",
    "gc.zgo.at",  # GoatCounter
}

# Patterns that suggest an embedded secret
SECRET_PATTERNS = [
    (r"sk_live_[a-zA-Z0-9]{20,}", "Stripe live secret key"),
    (r"sk_test_[a-zA-Z0-9]{20,}", "Stripe test secret key"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----", "Private key block"),
    (r"gh[pousr]_[A-Za-z0-9]{36,}", "GitHub PAT"),
    (r"xox[baprs]-[A-Za-z0-9-]{10,}", "Slack token"),
    (r"AIza[0-9A-Za-z_-]{35}", "Google API key"),
]

# Inline event handler attributes (XSS risk if value comes from user input)
INLINE_EVENT_ATTRS = re.compile(
    r'\s(on[a-z]+)\s*=\s*["\']?[^"\']{0,200}["\']?',
    re.IGNORECASE,
)

# javascript: URL pattern
JS_URL = re.compile(r'(?:href|src)\s*=\s*["\']javascript:', re.IGNORECASE)

# External script src
EXTERNAL_SCRIPT = re.compile(
    r'<script[^>]+src\s*=\s*["\']https?://([^/"\']+)[^"\']*["\']',
    re.IGNORECASE,
)

# Cookie / storage exfil patterns
EXFIL_PATTERNS = [
    re.compile(r"document\.cookie", re.IGNORECASE),
    re.compile(r"localStorage\.getItem", re.IGNORECASE),
    re.compile(r"fetch\s*\(\s*[\'\"]https?://(?!gc\.zgo\.at)", re.IGNORECASE),
]


def scan_html(content: str, repo_root: str = ".", path: str = "") -> Tuple[bool, List[str]]:
    """
    Scan HTML content for security issues.

    Returns (is_safe, list_of_issues).
    is_safe=True means the content can be shipped.
    """
    issues: List[str] = []

    # 1. Inline event handlers — allowed only in static contexts (button onclick="localFn()")
    #    but flag any that contain user-input concatenation patterns
    for m in INLINE_EVENT_ATTRS.finditer(content):
        attr = m.group(1).lower()
        # Get the value
        val_match = re.search(rf'{attr}\s*=\s*["\']([^"\']*)["\']', content[m.start():m.start()+300], re.IGNORECASE)
        if val_match:
            val = val_match.group(1)
            # Block event handlers that build HTML from input
            if any(dangerous in val for dangerous in ("innerHTML", "outerHTML", "document.write", "eval(")):
                issues.append(f"Dangerous inline event handler: {attr}='{val[:60]}' contains DOM manipulation")

    # 2. javascript: URLs — block entirely
    if JS_URL.search(content):
        issues.append("Found javascript: URL — blocked (XSS risk)")

    # 3. External script sources — must be in allowlist
    for m in EXTERNAL_SCRIPT.finditer(content):
        domain = m.group(1).lower()
        if domain not in ALLOWED_SCRIPT_DOMAINS:
            issues.append(f"External script from non-allowlisted domain: {domain}")

    # 4. Exfiltration patterns
    for pattern in EXFIL_PATTERNS:
        m = pattern.search(content)
        if m:
            # Allow localStorage in agent's own logic but flag for review
            ctx = content[max(0, m.start()-50):m.end()+50]
            issues.append(f"Suspicious pattern: {pattern.pattern!r} near: ...{ctx[:100]}...")

    # 5. Secret patterns
    for pattern, label in SECRET_PATTERNS:
        if re.search(pattern, content):
            issues.append(f"Embedded secret detected: {label}")

    # 6. Basic HTML structure (only enforce on full pages, not fragments)
    if content.strip().startswith("<!DOCTYPE") or content.strip().startswith("<html"):
        if "<html" not in content.lower():
            issues.append("Full page missing <html> root")
        if "<head" not in content.lower():
            issues.append("Full page missing <head>")
        if "<body" not in content.lower():
            issues.append("Full page missing <body>")

    # 7. Broken internal links (only check docs/ pages)
    if path.startswith("docs/") and path.endswith(".html"):
        for m in re.finditer(r'href\s*=\s*["\'](/[^"\']+)["\']', content, re.IGNORECASE):
            link = m.group(1)
            # Skip anchor-only and external-looking
            if link.startswith("#") or link.startswith("http"):
                continue
            # Strip query/anchor
            clean = link.split("#")[0].split("?")[0]
            # Resolve relative to docs/
            target = os.path.join("docs", clean.lstrip("/"))
            # Directory index → /foo/ resolves to /foo/index.html
            if clean.endswith("/"):
                target = os.path.join(target, "index.html")
            if not os.path.exists(target):
                issues.append(f"Broken internal link: {link} (resolved to {target})")

    is_safe = len(issues) == 0
    return is_safe, issues


def scan_all_html_in_docs(docs_dir: str = "docs") -> List[Tuple[str, List[str]]]:
    """
    Walk docs/ and scan every HTML file. Returns list of (path, issues).
    """
    results = []
    for root, _dirs, files in os.walk(docs_dir):
        for f in files:
            if f.endswith((".html", ".htm")):
                p = os.path.join(root, f)
                try:
                    with open(p, "r", encoding="utf-8") as fh:
                        content = fh.read()
                    rel_path = os.path.relpath(p, ".")
                    _safe, issues = scan_html(content, repo_root=".", path=rel_path)
                    if issues:
                        results.append((rel_path, issues))
                except Exception as e:
                    results.append((p, [f"scan error: {e}"]))
    return results
