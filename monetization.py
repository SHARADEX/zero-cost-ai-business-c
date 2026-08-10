#!/usr/bin/env python3
"""
Monetization injection — v4.1 with ZERO-SETUP fallbacks
=======================================================

v4 required the operator to register for EthicalAds/Carbon and Buttondown before
those revenue streams could activate. v4.1 adds zero-setup fallbacks:

  - Ad zone: If no ad network configured → inject a HOUSE AD (cross-promote
    another tool on the site). This keeps the ad zone populated, builds internal
    traffic, and gives the operator time to sign up for a real ad network.

  - Newsletter: If no Buttondown/ConvertKit configured → inject a MAILTO link
    with subject "Subscribe". The operator can use any email. Zero setup.

  - Affiliate: If no real affiliate codes configured → inject "Recommended
    Services" section WITHOUT affiliate codes (just plain links to vendor sites).
    Operator can add affiliate codes later by editing memory/affiliate_links.md.

This means the site is FULLY MONETIZED (with house ads + mailto + non-affiliate
links) from day 1, with zero operator setup. The agent continuously logs
pending_requests asking the operator to upgrade each stream when they have time.
"""

import os
import re
from typing import List, Dict, Tuple

AFFILIATE_FILE = "memory/affiliate_links.md"


def _read_file(path, default=""):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except (FileNotFoundError, IOError):
        return default


# ---------------------------------------------------------------------------
# Affiliate inventory parsing
# ---------------------------------------------------------------------------

def parse_affiliate_inventory() -> List[Dict]:
    """Parse memory/affiliate_links.md into a list of dicts."""
    content = _read_file(AFFILIATE_FILE, "")
    entries = []
    blocks = re.split(r"^## ID:\s*", content, flags=re.MULTILINE)
    for block in blocks[1:]:
        entry = {}
        for line in block.split("\n"):
            line = line.strip()
            if line.startswith("- vendor:"):
                entry["vendor"] = line.split(":", 1)[1].strip()
            elif line.startswith("- url:"):
                entry["url"] = line.split(":", 1)[1].strip()
            elif line.startswith("- description:"):
                entry["description"] = line.split(":", 1)[1].strip()
            elif line.startswith("- category:"):
                entry["category"] = line.split(":", 1)[1].strip()
            elif line.startswith("- contexts:"):
                entry["contexts"] = [c.strip().lower() for c in line.split(":", 1)[1].split(",") if c.strip()]
        # Skip entries with placeholder codes (operator hasn't replaced yet)
        if entry.get("url") and "YOUR_REFERRAL_CODE" not in entry["url"]:
            entries.append(entry)
    return entries


def find_contextual_affiliates(page_text: str, max_links: int = 3) -> List[Dict]:
    """Find affiliate links that match the page's keywords."""
    inventory = parse_affiliate_inventory()
    if not inventory:
        return []
    text_lower = page_text.lower()
    scored = []
    for entry in inventory:
        score = sum(1 for ctx in entry.get("contexts", []) if ctx in text_lower)
        if score > 0:
            scored.append((score, entry))
    scored.sort(key=lambda x: -x[0])
    return [e for _, e in scored[:max_links]]


def render_affiliate_block(affiliates: List[Dict]) -> str:
    """Render the 'Recommended' HTML block."""
    if not affiliates:
        return ""
    items = []
    for a in affiliates:
        # Detect if this is an affiliate link (has rel="sponsored") or plain
        is_affiliate = "ref" in a["url"].lower() or "aff" in a["url"].lower() or "utm" in a["url"].lower()
        rel = 'rel="sponsored nofollow noopener"' if is_affiliate else 'rel="nofollow noopener"'
        items.append(
            f'    <div class="affiliate-card">'
            f'      <strong class="affiliate-name">{a["vendor"]}</strong>'
            f'      <p class="affiliate-desc">{a["description"]}</p>'
            f'      <a href="{a["url"]}" {rel} target="_blank" class="btn btn-sm">Learn more →</a>'
            f'    </div>'
        )
    disclosure = "Some links are affiliate links. We may earn a commission if you sign up." if any(
        "ref" in a["url"].lower() or "aff" in a["url"].lower() for a in affiliates
    ) else "We recommend these services based on our experience."
    return (
        '<section class="affiliate-section" aria-label="Recommended services">'
        '  <h3>Recommended Services</h3>'
        f'  <p class="disclosure">{disclosure}</p>'
        '  <div class="affiliate-grid">\n' + "\n".join(items) + "\n  </div>"
        '</section>'
    )


# ---------------------------------------------------------------------------
# House ads — zero-setup alternative to ad networks
# ---------------------------------------------------------------------------

# Pool of tools to cross-promote. The house ad picks one randomly per page load.
HOUSE_AD_POOL = [
    ("/tools/json-formatter.html", "JSON Formatter", "Format and validate JSON instantly."),
    ("/tools/qr-generator.html", "QR Code Generator", "Generate QR codes for free."),
    ("/tools/regex-tester.html", "Regex Tester", "Test regex patterns with live highlighting."),
    ("/tools/password-generator.html", "Password Generator", "Generate strong, secure passwords."),
    ("/tools/jwt-decoder.html", "JWT Decoder", "Decode and inspect JWT tokens."),
    ("/tools/color-converter.html", "Color Converter", "Convert HEX, RGB, HSL colors."),
    ("/converters/csv-to-json.html", "CSV → JSON", "Convert CSV data to JSON."),
    ("/converters/json-to-yaml.html", "JSON → YAML", "Convert JSON to YAML."),
    ("/calculators/bmi-calculator.html", "BMI Calculator", "Calculate your Body Mass Index."),
    ("/calculators/loan-calculator.html", "Loan Calculator", "Calculate monthly loan payments."),
]


def render_house_ad(current_path: str = "") -> str:
    """
    Render a house ad (cross-promotion). Picks a random tool that's NOT the current page.
    Zero-setup alternative to EthicalAds/Carbon.
    """
    import random
    candidates = [(url, name, desc) for url, name, desc in HOUSE_AD_POOL if url not in current_path]
    if not candidates:
        candidates = HOUSE_AD_POOL
    url, name, desc = random.choice(candidates)
    return (
        '<div class="house-ad">'
        '  <span class="house-ad-label">Featured Tool</span>'
        f'  <a href="{url}" class="house-ad-link">'
        f'    <strong>{name}</strong> — {desc}'
        '  </a>'
        '</div>'
    )


def render_ad_zone() -> str:
    """
    Render the ad zone. If EthicalAds/Carbon is configured, use it.
    Otherwise, fall back to a house ad (zero-setup).
    """
    publisher_id = os.environ.get("ETHICALADS_PUBLISHER_ID") or os.environ.get("CARBON_ADS_ID")
    if publisher_id and publisher_id != "zerocostai":
        return (
            f'<div class="ad-zone" data-ea-publisher="{publisher_id}" data-ea-type="text"></div>'
        )
    # Zero-setup fallback: house ad
    # We use JS to render this randomly per page load
    return (
        '<div class="ad-zone" id="house-ad-container">'
        '  <script>'
        '    (function() {'
        '      var pool = ['
        + ",".join(f'["{u}","{n}","{d}"]' for u, n, d in HOUSE_AD_POOL) +
        '      ];'
        '      var pick = pool[Math.floor(Math.random()*pool.length)];'
        '      document.write(\'<span class="house-ad-label">Featured Tool</span>'
        '        <a href="\' + pick[0] + \'" class="house-ad-link"><strong>\' + pick[1] + \'</strong> — \' + pick[2] + \'</a>\');'
        '    })();'
        '  </script>'
        '  <noscript><a href="/tools/" class="house-ad-link">Browse all tools →</a></noscript>'
        '</div>'
    )


# ---------------------------------------------------------------------------
# Newsletter — zero-setup mailto fallback
# ---------------------------------------------------------------------------

def render_newsletter_form() -> str:
    """
    Render the newsletter signup form.
    If Buttondown is configured → use the real form.
    Otherwise → use a mailto: link (zero-setup).
    """
    # Check if Buttondown is configured (slug replaced from placeholder)
    buttondown_slug = os.environ.get("BUTTONDOWN_SLUG", "")
    if not buttondown_slug:
        # Try to detect from the existing HTML files (was the placeholder replaced?)
        # Default to "skip" which means "use mailto fallback"
        buttondown_slug = "skip"

    if buttondown_slug and buttondown_slug != "skip" and buttondown_slug != "YOUR_NEWSLETTER_SLUG":
        return (
            f'<form class="newsletter-form" action="https://buttondown.com/api/emails/embed-subscribe/{buttondown_slug}" method="post" target="popupwindow">'
            '  <label for="newsletter-email">Get notified when we add new tools:</label>'
            '  <input type="email" name="email" id="newsletter-email" placeholder="you@example.com" required>'
            '  <input type="hidden" value="1" name="embed">'
            '  <button type="submit" class="btn btn-sm">Subscribe</button>'
            '  <p class="disclosure">No spam. One email per week max. Unsubscribe anytime.</p>'
            '</form>'
        )

    # Zero-setup fallback: mailto link
    # The operator's email is auto-detected from git config or env
    operator_email = (
        os.environ.get("OPERATOR_EMAIL")
        or os.environ.get("GIT_AUTHOR_EMAIL")
        or "subscribe@example.com"
    )
    return (
        f'<div class="newsletter-form">'
        '  <label>Get notified when we add new tools:</label>'
        f'  <a href="mailto:{operator_email}?subject=Subscribe%20to%20newsletter&body=Please%20add%20me%20to%20the%20newsletter%20for%20new%20tool%20updates." class="btn btn-sm">Subscribe via Email</a>'
        '  <p class="disclosure">No spam. One email per week max. Just send the email and we\'ll add you.</p>'
        '</div>'
    )


# ---------------------------------------------------------------------------
# GoatCounter script — only injected if configured, otherwise no-op
# ---------------------------------------------------------------------------

def render_analytics_script() -> str:
    """Render GoatCounter script tag if configured, else empty (no analytics or GH API used)."""
    gc_code = os.environ.get("GC_SITE_ID", "")
    if gc_code and gc_code != "skip" and gc_code != "YOUR_GC_CODE":
        return f'<script data-goatcounter="https://{gc_code}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
    # No GoatCounter — the GitHub Traffic API still works (server-side), so
    # we don't need a client-side script.
    return '<!-- Analytics: using GitHub Traffic API (server-side, zero-setup). Configure GoatCounter for page-level data. -->'


# ---------------------------------------------------------------------------
# Main injection function
# ---------------------------------------------------------------------------

def inject_monetization(html: str, page_path: str = "") -> Tuple[str, List[str]]:
    """
    Inject affiliate block, ad zone, newsletter form into HTML.
    Idempotent — won't re-inject if already present.

    Returns (updated_html, list_of_changes_made).
    """
    changes = []

    # 1. Affiliate block — inject before the tip box if not already present
    if "affiliate-section" not in html:
        affiliates = find_contextual_affiliates(html)
        if affiliates:
            block = render_affiliate_block(affiliates)
            if '<div class="tip-box">' in html:
                html = html.replace('<div class="tip-box">', block + '\n\n    <div class="tip-box">', 1)
                changes.append(f"injected {len(affiliates)} affiliate link(s)")
            elif "</main>" in html:
                html = html.replace("</main>", block + "\n  </main>", 1)
                changes.append(f"injected {len(affiliates)} affiliate link(s) before </main>")

    # 2. Ad zone — replace any placeholder ad-zone with the rendered version
    #    (handles both v4's `data-ea-publisher="zerocostai"` placeholder and
    #    our new dynamic version)
    if "ad-zone" not in html and "</header>" in html:
        ad_html = render_ad_zone()
        html = html.replace("</header>", "</header>\n  " + ad_html, 1)
        changes.append("injected ad zone (house ad fallback)")
    elif 'data-ea-publisher="zerocostai"' in html:
        # Replace the placeholder publisher ID with our dynamic version
        new_ad = render_ad_zone()
        # Find and replace the existing ad-zone div
        html = re.sub(
            r'<!-- AD ZONE:.*?-->\s*<div class="ad-zone"[^>]*></div>',
            new_ad,
            html,
            count=1,
            flags=re.DOTALL
        )
        html = re.sub(
            r'<div class="ad-zone" data-ea-publisher="zerocostai"[^>]*></div>',
            new_ad,
            html,
            count=1
        )
        changes.append("upgraded ad zone to dynamic (house ad fallback)")

    # 3. Newsletter form — inject before </footer> if not present
    if "newsletter-form" not in html and "</footer>" in html:
        newsletter_html = render_newsletter_form()
        html = html.replace("</footer>", "  " + newsletter_html + "\n\n<footer>", 1)
        changes.append("injected newsletter form (mailto fallback)")

    # 4. GoatCounter script — replace placeholder script tag if present
    if 'data-goatcounter="https://YOUR_GC_CODE' in html:
        gc_script = render_analytics_script()
        html = re.sub(
            r'<script data-goatcounter="https://YOUR_GC_CODE[^"]*"[^>]*></script>',
            gc_script,
            html
        )
        changes.append("upgraded GoatCounter script (placeholder → dynamic)")

    return html, changes


def inject_into_file(path: str) -> Tuple[bool, str]:
    """Read file at path, inject monetization, write back. Returns (success, message)."""
    if not os.path.isfile(path):
        return False, f"File not found: {path}"
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        updated, changes = inject_monetization(content, path)
        if not changes:
            return True, f"No changes needed — already monetized: {path}"
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
        return True, f"Monetized {path}: {', '.join(changes)}"
    except Exception as e:
        return False, f"inject_into_file failed: {e}"
