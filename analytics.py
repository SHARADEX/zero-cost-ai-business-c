#!/usr/bin/env python3
"""
Analytics — v4 with ZERO-SETUP fallback
=======================================

v4 originally required GoatCounter (operator signup). v4.1 adds GitHub Traffic API
as a zero-setup fallback. Now the agent has real traffic data from day 1, without
any operator configuration.

Priority:
  1. GoatCounter (if GC_API_TOKEN + GC_SITE_ID configured) — page-level data
  2. GitHub Traffic API (if GH_PAT configured) — repo-level data, 14-day window
  3. Empty data (if neither configured) — agent logs a pending_request

GitHub Traffic API endpoints (all free, all use GH_PAT which we already have):
  - GET /repos/{owner}/{repo}/traffic/views          — 14-day view data
  - GET /repos/{owner}/{repo}/traffic/clones         — 14-day clone data
  - GET /repos/{owner}/{repo}/traffic/popular/referrers — top referrers
  - GET /repos/{owner}/{repo}/traffic/popular/paths    — top paths in repo

Note: GitHub Traffic API measures traffic to the GitHub REPO, not the Pages site.
But it's a strong proxy — anyone visiting the repo is likely also visiting the
Pages site. And it requires ZERO operator setup.
"""

import os
import json
import urllib.request
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional

ANALYTICS_FILE = "memory/analytics.md"
ANALYTICS_JSON = "memory/analytics_data.json"


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


def _read_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, IOError):
        return default


def _write_json(path, data):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ---------------------------------------------------------------------------
# GoatCounter (preferred, requires signup)
# ---------------------------------------------------------------------------

def _gc_get(endpoint: str, params: Dict = None) -> Optional[dict]:
    token = os.environ.get("GC_API_TOKEN")
    site = os.environ.get("GC_SITE_ID")
    if not token or not site:
        return None
    base = f"https://{site}.goatcounter.com/api/v0"
    url = base + endpoint
    if params:
        qs = "&".join(f"{k}={v}" for k, v in params.items())
        url += "?" + qs
    try:
        req = urllib.request.Request(
            url,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"[analytics] GoatCounter API error: {e}")
        return None


def _gc_fetch(metric: str) -> Optional[dict]:
    """Fetch from GoatCounter. Returns None if not configured or fails."""
    end = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    start = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
    if metric == "summary":
        return _gc_get("/stats/total", {"start": start, "end": end})
    elif metric == "top-pages":
        return _gc_get("/stats/pages", {"start": start, "end": end})
    elif metric == "top-referrers":
        return _gc_get("/stats/referrers", {"start": start, "end": end})
    return None


# ---------------------------------------------------------------------------
# GitHub Traffic API (zero-setup fallback — uses GH_PAT we already have)
# ---------------------------------------------------------------------------

def _gh_repo_identity():
    """Returns (owner, repo) for the GitHub API call."""
    # 1. GITHUB_REPOSITORY env (set by GitHub Actions)
    gh_repo = os.environ.get("GITHUB_REPOSITORY", "")
    if "/" in gh_repo:
        owner, repo = gh_repo.split("/", 1)
        return owner.strip(), repo.strip()
    # 2. bootstrap marker file
    if os.path.exists("memory/.bootstrapped"):
        try:
            with open("memory/.bootstrapped") as f:
                for line in f:
                    if line.startswith("username="):
                        owner = line.split("=", 1)[1].strip()
                    elif line.startswith("repo="):
                        repo = line.split("=", 1)[1].strip()
                if owner and repo:
                    return owner, repo
        except (OSError, UnboundLocalError):
            pass
    # 3. Try git remote
    try:
        import subprocess, re
        r = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=5, check=False
        )
        url = r.stdout.strip()
        m = re.search(r"github\.com[/:]([^/]+)/([^/\.]+?)(?:\.git)?$", url)
        if m:
            return m.group(1), m.group(2)
    except Exception:
        pass
    return None, None


def _gh_get(endpoint: str) -> Optional[dict]:
    """GET request to GitHub API using GH_PAT."""
    token = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN")
    if not token:
        return None
    owner, repo = _gh_repo_identity()
    if not owner or not repo:
        return None
    url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
    try:
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "User-Agent": "ZeroCostAI/4.1",
            },
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"[analytics] GitHub Traffic API error: {e}")
        return None


def _gh_fetch(metric: str) -> Optional[dict]:
    """Fetch from GitHub Traffic API. Returns None if not configured or fails."""
    if metric == "summary":
        data = _gh_get("traffic/views")
        if data is None:
            return None
        # Reshape to match GoatCounter-ish summary
        return {
            "source": "github_traffic_api",
            "total_views": data.get("count", 0),
            "total_uniques": data.get("uniques", 0),
            "daily": [
                {"date": d.get("timestamp", "")[:10],
                 "views": d.get("count", 0),
                 "uniques": d.get("uniques", 0)}
                for d in data.get("views", [])
            ],
        }
    elif metric == "top-pages":
        data = _gh_get("traffic/popular/paths")
        if data is None:
            return None
        return {
            "source": "github_traffic_api",
            "pages": [
                {"path": p.get("path", ""), "views": p.get("count", 0), "uniques": p.get("uniques", 0)}
                for p in data
            ],
        }
    elif metric == "top-referrers":
        data = _gh_get("traffic/popular/referrers")
        if data is None:
            return None
        return {
            "source": "github_traffic_api",
            "referrers": [
                {"referrer": r.get("referrer", ""), "views": r.get("count", 0), "uniques": r.get("uniques", 0)}
                for r in data
            ],
        }
    return None


# ---------------------------------------------------------------------------
# Unified fetch — tries GoatCounter, falls back to GitHub Traffic API
# ---------------------------------------------------------------------------

def fetch_metrics(metric: str = "summary") -> dict:
    """
    Fetch analytics metrics. metric can be:
      - "summary": total views, unique visitors
      - "top-pages": top pages by views (last 7 days)
      - "top-referrers": top referring sites

    Returns dict with 'source' field indicating where the data came from:
      - "goatcounter" — page-level data from the Pages site
      - "github_traffic_api" — repo-level data (proxy for Pages traffic)
      - "none" — no analytics source configured
    """
    # Try GoatCounter first (preferred — page-level data)
    gc_data = _gc_fetch(metric)
    if gc_data is not None:
        gc_data["source"] = "goatcounter"
        return gc_data

    # Fall back to GitHub Traffic API (zero-setup)
    gh_data = _gh_fetch(metric)
    if gh_data is not None:
        return gh_data

    # No analytics source available
    return {
        "source": "none",
        "error": "No analytics configured. Set GC_API_TOKEN+GC_SITE_ID for GoatCounter, or ensure GH_PAT is set for GitHub Traffic API fallback."
    }


def record_event(name: str, payload: Dict = None):
    """Record a metric event to memory/analytics.md."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"- [{ts}] {name}"
    if payload:
        line += " | " + " | ".join(f"{k}={v}" for k, v in payload.items())
    existing = _read_file(ANALYTICS_FILE, "# Analytics & Metrics\n\n")
    lines = existing.split("\n")
    lines.append(line)
    if len(lines) > 250:
        lines = lines[:5] + lines[-245:]
    _write_file(ANALYTICS_FILE, "\n".join(lines) + "\n")


def get_top_pages(days: int = 7) -> List[Dict]:
    """Returns top pages by views in last N days (from cached snapshot)."""
    data = _read_json(ANALYTICS_JSON, {"top_pages": []})
    return data.get("top_pages", [])


def update_analytics_snapshot():
    """Pull latest metrics and persist locally. Used by daily-seo workflow."""
    summary = fetch_metrics("summary")
    top_pages = fetch_metrics("top-pages")
    top_referrers = fetch_metrics("top-referrers")
    snapshot = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "top_pages": top_pages,
        "top_referrers": top_referrers,
    }
    _write_json(ANALYTICS_JSON, snapshot)
    source = summary.get("source", "unknown")
    record_event("analytics_snapshot", {
        "source": source,
        "views": summary.get("total_views", 0) if source == "github_traffic_api" else "n/a",
    })
    return snapshot


def is_configured():
    """Returns (has_goatcounter, has_github_traffic_fallback)."""
    has_gc = bool(os.environ.get("GC_API_TOKEN") and os.environ.get("GC_SITE_ID"))
    has_gh = bool(os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN"))
    return has_gc, has_gh
