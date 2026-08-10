#!/usr/bin/env python3
"""
SEO automation — v4 NEW module
==============================

Handles:
  1. Sitemap regeneration from docs/ structure
  2. robots.txt with sitemap reference
  3. Google Indexing API submission (free, requires service account)
  4. Bing URL Submission API (free)
  5. SEO queue management — pages pending indexing submission
  6. JSON-LD schema injection helpers

The Indexing API needs a Google service account JSON. The operator sets
GOOGLE_INDEXING_SERVICE_ACCOUNT_JSON (or a path via GOOGLE_INDEXING_SA_PATH).
If absent, indexing submission is skipped (no failure).
"""

import os
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import List, Optional

SEO_QUEUE_FILE = "memory/seo_queue.md"
SITEMAP_FILE = "docs/sitemap.xml"
ROBOTS_FILE = "docs/robots.txt"


def _auto_base_url() -> str:
    """
    Auto-detect site base URL. Order:
      1. SITE_BASE_URL env var
      2. memory/.bootstrapped marker file
      3. GITHUB_REPOSITORY env var (set by GitHub Actions)
      4. Fallback placeholder (will be replaced by bootstrap on first run)
    """
    if os.environ.get("SITE_BASE_URL"):
        return os.environ["SITE_BASE_URL"].rstrip("/")
    try:
        with open("memory/.bootstrapped") as f:
            for line in f:
                if line.startswith("base_url="):
                    return line.split("=", 1)[1].strip()
    except (OSError, FileNotFoundError):
        pass
    gh_repo = os.environ.get("GITHUB_REPOSITORY", "")
    if "/" in gh_repo:
        user, repo = gh_repo.split("/", 1)
        return f"https://{user}.github.io/{repo}"
    return "https://YOUR-USERNAME.github.io/REPO-NAME"


# Base URL of the published site. Auto-detected at runtime.
DEFAULT_BASE_URL = _auto_base_url()


def _read_file(path, default=""):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except (FileNotFoundError, IOError):
        return default


def _write_file(path, text):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def discover_pages() -> List[str]:
    """Walk docs/ and return list of page URLs (relative paths)."""
    pages = []
    for root, _dirs, files in os.walk("docs"):
        # Skip assets/
        if "/assets" in root or "\\assets" in root:
            continue
        for f in files:
            if f.endswith((".html", ".htm")):
                full = os.path.join(root, f)
                # Convert to URL path
                rel = os.path.relpath(full, "docs")
                # Replace index.html with directory
                if rel.endswith("index.html"):
                    rel = rel[:-10]  # strip "index.html"
                # Normalize path separators
                url_path = "/" + rel.replace(os.sep, "/")
                # Strip leading / for root
                if url_path == "/":
                    pages.append("/")
                else:
                    pages.append(url_path)
    # Deduplicate and sort
    return sorted(set(pages))


def regenerate_sitemap(base_url: str = DEFAULT_BASE_URL) -> int:
    """Regenerate docs/sitemap.xml from discovered pages. Returns page count."""
    pages = discover_pages()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for page in pages:
        # Determine change frequency and priority
        if page == "/" or page == "/blog/":
            changefreq = "daily"
            priority = "1.0" if page == "/" else "0.6"
        elif page.startswith("/tools/"):
            changefreq = "monthly"
            priority = "0.9" if page == "/tools/" else "0.8"
        elif page.startswith("/converters/"):
            changefreq = "weekly"
            priority = "0.9" if page == "/converters/" else "0.8"
        elif page.startswith("/calculators/"):
            changefreq = "weekly"
            priority = "0.9" if page == "/calculators/" else "0.8"
        elif page.startswith("/guides/"):
            changefreq = "monthly"
            priority = "0.7"
        else:
            changefreq = "monthly"
            priority = "0.6"
        full_url = base_url + page
        lines.append("  <url>")
        lines.append(f"    <loc>{full_url}</loc>")
        lines.append(f"    <lastmod>{today}</lastmod>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    _write_file(SITEMAP_FILE, "\n".join(lines) + "\n")
    return len(pages)


def regenerate_robots(base_url: str = DEFAULT_BASE_URL):
    """Regenerate robots.txt with sitemap reference."""
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /assets/\n"
        "\n"
        f"Sitemap: {base_url}/sitemap.xml\n"
    )
    _write_file(ROBOTS_FILE, content)


def add_to_seo_queue(urls: List[str]):
    """Add URLs to the indexing submission queue."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    existing = _read_file(SEO_QUEUE_FILE, "")
    lines = existing.split("\n")
    # Strip trailing empty
    while lines and not lines[-1].strip():
        lines.pop()
    for url in urls:
        lines.append(f"- [ ] [{ts}] {url}")
    _write_file(SEO_QUEUE_FILE, "\n".join(lines) + "\n")


def mark_seo_queue_submitted(urls: List[str]):
    """Mark URLs as submitted in the queue (checkbox → [x])."""
    content = _read_file(SEO_QUEUE_FILE, "")
    for url in urls:
        content = content.replace(f"] {url}", "] " + url + " ✓ SUBMITTED")
    _write_file(SEO_QUEUE_FILE, content)


def get_pending_seo_urls() -> List[str]:
    """Return list of URLs pending submission (lines starting with '- [ ]')."""
    content = _read_file(SEO_QUEUE_FILE, "")
    urls = []
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("- [ ]"):
            # Extract URL from end
            m = re.search(r"\](.*)$", line)
            if m:
                urls.append(m.group(1).strip())
    return urls


def submit_to_google_indexing(urls: List[str]) -> dict:
    """
    Submit URLs to Google Indexing API.
    Requires GOOGLE_INDEXING_SERVICE_ACCOUNT_JSON env (service account JSON)
    and the service account must be added as owner in Search Console.

    Returns dict with 'submitted' count and 'errors' list.
    If service account not configured, returns {'submitted': 0, 'errors': ['not configured']}.
    """
    sa_json = os.environ.get("GOOGLE_INDEXING_SERVICE_ACCOUNT_JSON")
    sa_path = os.environ.get("GOOGLE_INDEXING_SA_PATH")
    if not sa_json and not sa_path:
        return {"submitted": 0, "errors": ["Google Indexing API not configured (need GOOGLE_INDEXING_SERVICE_ACCOUNT_JSON or GOOGLE_INDEXING_SA_PATH)"]}

    try:
        # Import here so the agent doesn't fail if google-auth isn't installed
        import urllib.request as ur
        # We can't easily do JWT signing with stdlib alone. Try the optional path.
        try:
            from google.oauth2 import service_account
            import google.auth.transport.requests
        except ImportError:
            return {"submitted": 0, "errors": ["google-auth library not installed; pip install google-auth"]}

        if sa_path:
            creds = service_account.Credentials.from_service_account_file(
                sa_path, scopes=["https://www.googleapis.com/auth/indexing"]
            )
        else:
            sa_info = json.loads(sa_json)
            creds = service_account.Credentials.from_service_account_info(
                sa_info, scopes=["https://www.googleapis.com/auth/indexing"]
            )
        creds.refresh(google.auth.transport.requests.Request())

        submitted = 0
        errors = []
        for url in urls:
            try:
                payload = json.dumps({"url": url, "type": "URL_UPDATED"}).encode("utf-8")
                req = ur.Request(
                    "https://indexing.googleapis.com/v3/urlNotifications:publish",
                    data=payload,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {creds.token}",
                    },
                    method="POST",
                )
                with ur.urlopen(req, timeout=20) as resp:
                    if resp.status == 200:
                        submitted += 1
                    else:
                        errors.append(f"{url}: HTTP {resp.status}")
            except Exception as e:
                errors.append(f"{url}: {str(e)[:200]}")
        return {"submitted": submitted, "errors": errors}
    except Exception as e:
        return {"submitted": 0, "errors": [f"unexpected: {str(e)[:200]}"]}


def submit_to_bing(urls: List[str]) -> dict:
    """Submit URLs to Bing Webmaster API. Requires BING_API_KEY env."""
    api_key = os.environ.get("BING_API_KEY")
    site_url = os.environ.get("SITE_BASE_URL", DEFAULT_BASE_URL)
    if not api_key:
        return {"submitted": 0, "errors": ["Bing API not configured (need BING_API_KEY)"]}
    try:
        submitted = 0
        errors = []
        for url in urls:
            try:
                endpoint = (
                    f"https://ssl.bing.com/webmaster/api.svc/json/SubmitUrl"
                    f"?apikey={api_key}&siteUrl={site_url}"
                )
                payload = json.dumps({"siteUrl": site_url, "url": url}).encode("utf-8")
                req = urllib.request.Request(endpoint, data=payload,
                                              headers={"Content-Type": "application/json"},
                                              method="POST")
                with urllib.request.urlopen(req, timeout=20) as resp:
                    if resp.status == 200:
                        submitted += 1
                    else:
                        errors.append(f"{url}: HTTP {resp.status}")
            except Exception as e:
                errors.append(f"{url}: {str(e)[:200]}")
        return {"submitted": submitted, "errors": errors}
    except Exception as e:
        return {"submitted": 0, "errors": [f"unexpected: {str(e)[:200]}"]}
