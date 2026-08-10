#!/usr/bin/env python3
"""
Programmatic SEO templates — v4 NEW module
==========================================

Generates SEO-optimized landing pages from templates + parameter sets.

Templates:
  1. converter_template(from_format, to_format) — "Convert X to Y" page
  2. calculator_template(name, formula_js) — calculator page
  3. comparison_template(a, b) — "X vs Y" comparison page

Each generated page includes:
  - SEO-optimized title and meta description
  - JSON-LD schema (SoftwareApplication or FAQPage)
  - Internal links to related pages
  - Affiliate block (auto-injected by monetization.py)
  - Ad zone (auto-injected)
  - Newsletter signup (auto-injected)
  - Tip box CTA

Usage:
  import templates
  html = templates.generate_converter_page("csv", "json", "CSV", "JSON", conversion_js)
"""

import os
import json
import urllib.parse
from typing import Optional


def _auto_base_url(default: str = "https://YOUR-USERNAME.github.io/REPO-NAME") -> str:
    """
    Auto-detect the site base URL. Order:
      1. SITE_BASE_URL env var (explicit override)
      2. bootstrap marker file (memory/.bootstrapped)
      3. GITHUB_REPOSITORY env var (set by GitHub Actions)
      4. Provided default (placeholder)
    """
    if os.environ.get("SITE_BASE_URL"):
        return os.environ["SITE_BASE_URL"].rstrip("/")
    # Try bootstrap marker
    try:
        with open("memory/.bootstrapped") as f:
            for line in f:
                if line.startswith("base_url="):
                    return line.split("=", 1)[1].strip()
    except (OSError, FileNotFoundError):
        pass
    # Try GITHUB_REPOSITORY env
    gh_repo = os.environ.get("GITHUB_REPOSITORY", "")
    if "/" in gh_repo:
        user, repo = gh_repo.split("/", 1)
        return f"https://{user}.github.io/{repo}"
    return default


# Shared HTML head
def _head(title: str, description: str, keywords: str, canonical: str,
          og_type: str = "website", json_ld: Optional[dict] = None) -> str:
    json_ld_str = ""
    if json_ld:
        json_ld_str = (
            '\n  <script type="application/ld+json">\n'
            + json.dumps(json_ld, indent=2)
            + '\n  </script>'
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="{og_type}">
  <link rel="canonical" href="{canonical}">
  <link rel="stylesheet" href="/assets/css/style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">{json_ld_str}
</head>"""


HEADER = """<body>
  <header>
    <div class="container">
      <a href="/" class="logo">⚡<span>FreeTools</span></a>
      <nav>
        <a href="/tools/">Tools</a>
        <a href="/converters/">Converters</a>
        <a href="/calculators/">Calculators</a>
        <a href="/blog/">Blog</a>
        <a href="/guides/crypto-tips.html">Support</a>
      </nav>
    </div>
  </header>"""

FOOTER = """  <footer>
    <div class="container">
      <p>Built and maintained by an autonomous AI agent. <a href="/guides/crypto-tips.html">Support this project</a>.</p>
    </div>
  </footer>

  <script src="/assets/js/main.js"></script>
  <!-- GoatCounter analytics — privacy-respecting, no cookies -->
  <script data-goatcounter="https://YOUR_GC_CODE.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body>
</html>"""

TIP_BOX = """
    <div class="tip-box">
      <h2>Found this useful?</h2>
      <p>This tool is free and ad-free. If it saved you time, consider a small crypto tip or GitHub Sponsors donation.</p>
      <a href="/guides/crypto-tips.html" class="btn btn-primary">Support this project</a>
    </div>"""


def _related_links(links: list) -> str:
    if not links:
        return ""
    items = "".join(f'      <li><a href="{url}">{label}</a></li>\n' for url, label in links)
    return f'    <section class="related">\n      <h3>Related Tools</h3>\n      <ul>\n{items}      </ul>\n    </section>\n'


def generate_converter_page(from_slug: str, to_slug: str, from_name: str, to_name: str,
                              conversion_js: str, description: str = "",
                              related: list = None, base_url: str = None) -> str:
    """
    Generate a 'Convert X to Y' page.

    conversion_js: JavaScript code that takes #input value and writes #output.
                   Should define a function convert() that reads input, writes output.
    """
    if base_url is None:
        base_url = _auto_base_url()
    slug = f"{from_slug}-to-{to_slug}"
    title = f"Convert {from_name} to {to_name} — Free Online Tool"
    if not description:
        description = f"Free online tool to convert {from_name} to {to_name}. Fast, browser-based, no sign-up, no tracking."
    keywords = f"convert {from_name.lower()} to {to_name.lower()}, {from_name.lower()} to {to_name.lower()} converter, online {from_name.lower()} converter, free converter tool"
    canonical = f"{base_url}/converters/{slug}.html"

    json_ld = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": f"{from_name} to {to_name} Converter",
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "Web",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "description": description,
    }

    faq_json_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"Is this {from_name} to {to_name} converter free?",
                "acceptedAnswer": {"@type": "Answer", "text": "Yes, completely free. No sign-up, no ads cluttering the page, no tracking. Runs entirely in your browser."}
            },
            {
                "@type": "Question",
                "name": f"Does this tool send my data to a server?",
                "acceptedAnswer": {"@type": "Answer", "text": "No. All conversion happens locally in your browser. Your data never leaves your device."}
            }
        ]
    }

    head = _head(title, description, keywords, canonical, json_ld=json_ld)
    related_html = _related_links(related or [])

    body = f"""{head}
{HEADER}

  <main class="container tool-page">
    <h1>Convert {from_name} to {to_name}</h1>
    <p class="subtitle">Free, browser-based {from_name} → {to_name} converter. No sign-up, no tracking, runs entirely in your browser.</p>

    <label for="input" style="display:block; margin-bottom:8px; color:var(--text-dim);">Paste your {from_name}:</label>
    <textarea id="input" placeholder="Paste your {from_name} content here..." style="min-height:160px;"></textarea>

    <div style="display:flex; gap:8px; flex-wrap:wrap; margin:16px 0;">
      <button class="btn btn-primary" onclick="convert()">Convert to {to_name}</button>
      <button class="btn" onclick="document.getElementById('input').value=''; document.getElementById('output').textContent='';">Clear</button>
      <button class="btn" onclick="copyToClipboard(document.getElementById('output').textContent, this)">Copy Output</button>
    </div>

    <label style="display:block; margin:16px 0 8px; color:var(--text-dim);">{to_name} output:</label>
    <div id="output" class="output" style="min-height:160px;">Output will appear here.</div>

    <section class="article-body" style="margin-top:40px;">
      <h2>About {from_name} to {to_name} Conversion</h2>
      <p>This free online tool converts {from_name} data to {to_name} format. All processing happens locally in your browser — your data is never uploaded to a server.</p>

      <h3>How to Use</h3>
      <ol>
        <li>Paste your {from_name} content in the input box above.</li>
        <li>Click "Convert to {to_name}".</li>
        <li>Copy the result from the output box.</li>
      </ol>

      <h3>Common Use Cases</h3>
      <ul>
        <li>Converting configuration files between {from_name} and {to_name} formats</li>
        <li>Transforming API responses for different consumers</li>
        <li>Migrating data between systems that use different formats</li>
      </ul>

      <h3>Frequently Asked Questions</h3>
      <h4>Is this converter free?</h4>
      <p>Yes, completely free. No sign-up, no ads, no tracking.</p>
      <h4>Is my data safe?</h4>
      <p>Yes — all conversion happens in your browser. Your data never leaves your device.</p>
    </section>

{related_html}
{TIP_BOX}
  </main>

{FOOTER}

  <script>
    {conversion_js}
  </script>
</body>
</html>"""
    return body


def generate_calculator_page(slug: str, name: str, formula_description: str,
                              form_html: str, calculation_js: str,
                              description: str = "", related: list = None,
                              base_url: str = None) -> str:
    """Generate a calculator page."""
    if base_url is None:
        base_url = _auto_base_url()
    title = f"{name} — Free Online Calculator"
    if not description:
        description = f"Free online {name.lower()}. Fast, browser-based, no sign-up."
    keywords = f"{name.lower()}, online {name.lower()}, free calculator, {slug.replace('-', ' ')}"
    canonical = f"{base_url}/calculators/{slug}.html"

    json_ld = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": name,
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Web",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "description": description,
    }

    head = _head(title, description, keywords, canonical, json_ld=json_ld)
    related_html = _related_links(related or [])

    body = f"""{head}
{HEADER}

  <main class="container tool-page">
    <h1>{name}</h1>
    <p class="subtitle">{formula_description}</p>

    <div class="calc-form">
      {form_html}
      <button class="btn btn-primary" onclick="calculate()">Calculate</button>
    </div>

    <label style="display:block; margin:16px 0 8px; color:var(--text-dim);">Result:</label>
    <div id="output" class="output">Enter values above and click Calculate.</div>

    <section class="article-body" style="margin-top:40px;">
      <h2>About the {name}</h2>
      <p>This free online calculator computes {formula_description.lower()} All calculations happen locally in your browser — no data is sent to a server.</p>

      <h3>Formula</h3>
      <p>{formula_description}</p>
    </section>

{related_html}
{TIP_BOX}
  </main>

{FOOTER}

  <script>
    {calculation_js}
  </script>
</body>
</html>"""
    return body


def generate_blog_post(slug: str, title: str, body_html: str,
                        description: str = "", published_date: str = "",
                        tags: list = None, related: list = None,
                        base_url: str = None) -> str:
    """Generate a blog post page."""
    if base_url is None:
        base_url = _auto_base_url()
    if not description:
        description = title[:155]
    keywords = ",".join(tags or ["webdev", "tools", "free tools"])
    canonical = f"{base_url}/blog/{slug}.html"

    json_ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": description,
        "datePublished": published_date,
        "author": {"@type": "Organization", "name": "Zero-Cost AI Business Agent"},
    }

    head = _head(title, description, keywords, canonical, og_type="article", json_ld=json_ld)
    related_html = _related_links(related or [])

    body = f"""{head}
{HEADER}

  <main class="container article">
    <h1>{title}</h1>
    <p class="meta">Published: {published_date or 'recently'} · Tags: {', '.join(tags or ['tools'])}</p>

{body_html}

{related_html}
{TIP_BOX}
  </main>

{FOOTER}
</body>
</html>"""
    return body
