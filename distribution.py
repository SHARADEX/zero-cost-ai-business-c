#!/usr/bin/env python3
"""
Distribution — v4 NEW module
============================

Posts new content to free distribution channels. Each channel has rate limits
and rules; the module enforces them.

Channels:
  - reddit    — post to /r/webdev, /r/FreeTools, /r/SideProject, /r/JavaScript (rate: 1 per 7 days per subreddit)
  - devto     — cross-post blog articles with canonical_url (rate: 1 per day)
  - twitter   — tweet new tool (rate: 1 per 30 min, free tier)
  - linkedin  — share weekly summary (rate: 1 per week)
  - hackernews — submit only best work (rate: 1 per 14 days)

All credentials come from env vars. If absent, the channel is skipped.
Distribution log is persisted to memory/distribution_log.md.
"""

import os
import json
import urllib.request
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional

DIST_LOG = "memory/distribution_log.md"

# Rate limits in hours per channel
RATE_LIMITS_HOURS = {
    "reddit":       7 * 24,   # 1 post per 7 days per subreddit
    "devto":        24,       # 1 per day
    "twitter":      0.5,      # 1 per 30 min
    "linkedin":     7 * 24,   # 1 per week
    "hackernews":   14 * 24,  # 1 per 2 weeks
}


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


def _append_file(path, text):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(text)


def _now():
    return datetime.now(timezone.utc)


def _can_post(channel: str, subreddit: Optional[str] = None) -> bool:
    """Check rate limit. Returns True if OK to post."""
    log = _read_file(DIST_LOG, "")
    key = f"{channel}/{subreddit}" if subreddit else channel
    cutoff = _now() - timedelta(hours=RATE_LIMITS_HOURS.get(channel, 24))
    for line in log.split("\n"):
        line = line.strip()
        if not line.startswith("- ["):
            continue
        # Format: - [YYYY-MM-DD HH:MM:SS UTC] channel/subreddit | ...
        try:
            ts_str = line[line.index("[")+1:line.index("]")]
            ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S UTC").replace(tzinfo=timezone.utc)
            if ts < cutoff:
                continue
            if f"] {key} |" in line:
                return False
        except (ValueError, IndexError):
            continue
    return True


def _log_post(channel: str, subreddit: Optional[str], title: str, url: str, status: str, error: str = ""):
    ts = _now().strftime("%Y-%m-%d %H:%M:%S UTC")
    key = f"{channel}/{subreddit}" if subreddit else channel
    line = f"- [{ts}] {key} | title='{title[:60]}' | url={url} | status={status}"
    if error:
        line += f" | error={error[:200]}"
    _append_file(DIST_LOG, line + "\n")


def post_to_reddit(subreddit: str, title: str, url: str) -> Dict:
    """
    Submit a link post to a subreddit.
    Requires REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD env.
    """
    if not _can_post("reddit", subreddit):
        return {"status": "skipped", "error": "Rate limit — already posted to this subreddit recently"}

    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    username = os.environ.get("REDDIT_USERNAME")
    password = os.environ.get("REDDIT_PASSWORD")

    if not all([client_id, client_secret, username, password]):
        _log_post("reddit", subreddit, title, url, "skipped", "credentials not configured")
        return {"status": "skipped", "error": "Reddit credentials not configured"}

    try:
        # 1. Get OAuth token
        auth_url = "https://www.reddit.com/api/v1/access_token"
        import base64
        auth_str = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        payload = f"grant_type=password&username={username}&password={password}".encode()
        req = urllib.request.Request(
            auth_url, data=payload,
            headers={
                "Authorization": f"Basic {auth_str}",
                "User-Agent": f"ZeroCostAI/4.0 by /u/{username}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            tok_data = json.loads(r.read().decode())
        access_token = tok_data.get("access_token")
        if not access_token:
            _log_post("reddit", subreddit, title, url, "error", "no access token")
            return {"status": "error", "error": "Failed to get access token"}

        # 2. Submit link
        submit_url = "https://oauth.reddit.com/api/submit"
        body = f"kind=link&sr=/r/{subreddit}&title={urllib.parse.quote(title)}&url={urllib.parse.quote(url)}"
        req = urllib.request.Request(
            submit_url, data=body.encode(),
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": f"ZeroCostAI/4.0 by /u/{username}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            result = json.loads(r.read().decode())

        if result.get("json", {}).get("errors"):
            err = str(result["json"]["errors"])
            _log_post("reddit", subreddit, title, url, "error", err)
            return {"status": "error", "error": err}
        _log_post("reddit", subreddit, title, url, "ok")
        return {"status": "ok", "result": result}
    except Exception as e:
        _log_post("reddit", subreddit, title, url, "error", str(e))
        return {"status": "error", "error": str(e)[:300]}


def post_to_devto(title: str, body_markdown: str, canonical_url: str = "", tags: list = None) -> Dict:
    """Cross-post an article to dev.to. Requires DEVTO_API_KEY env."""
    if not _can_post("devto"):
        return {"status": "skipped", "error": "Rate limit — already posted today"}
    api_key = os.environ.get("DEVTO_API_KEY")
    if not api_key:
        _log_post("devto", None, title, canonical_url, "skipped", "DEVTO_API_KEY not set")
        return {"status": "skipped", "error": "DEVTO_API_KEY not set"}
    try:
        payload = json.dumps({
            "article": {
                "title": title,
                "body_markdown": body_markdown,
                "published": True,
                "canonical_url": canonical_url or None,
                "tags": tags or ["webdev", "tools"],
            }
        }).encode()
        req = urllib.request.Request(
            "https://dev.to/api/articles",
            data=payload,
            headers={"api-key": api_key, "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            result = json.loads(r.read().decode())
        _log_post("devto", None, title, canonical_url, "ok")
        return {"status": "ok", "url": result.get("url")}
    except Exception as e:
        _log_post("devto", None, title, canonical_url, "error", str(e))
        return {"status": "error", "error": str(e)[:300]}


def post_to_twitter(text: str) -> Dict:
    """Tweet. Requires TWITTER_BEARER_TOKEN or TWITTER_CONSUMER_KEY etc."""
    if not _can_post("twitter"):
        return {"status": "skipped", "error": "Rate limit — too soon since last tweet"}
    bearer = os.environ.get("TWITTER_BEARER_TOKEN")
    if not bearer:
        _log_post("twitter", None, text[:60], "", "skipped", "Twitter credentials not set")
        return {"status": "skipped", "error": "Twitter API v2 needs OAuth 1.0a user context — manual setup required"}
    # Twitter v2 tweet endpoint requires OAuth 1.0a user context, which is complex
    # with stdlib only. Log a pending_request and let human do it.
    _log_post("twitter", None, text[:60], "", "skipped", "Twitter v2 needs oauthlib — logged as pending")
    return {"status": "skipped", "error": "Twitter v2 requires OAuth1 — log pending_request for human"}


def post_to_linkedin(text: str, url: str = "") -> Dict:
    """Share on LinkedIn. Requires LINKEDIN_ACCESS_TOKEN env."""
    if not _can_post("linkedin"):
        return {"status": "skipped", "error": "Rate limit — already posted this week"}
    token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    if not token:
        _log_post("linkedin", None, text[:60], url, "skipped", "LINKEDIN_ACCESS_TOKEN not set")
        return {"status": "skipped", "error": "LINKEDIN_ACCESS_TOKEN not set"}
    # LinkedIn API v2 shares — requires WIM_SOCIAL scope
    _log_post("linkedin", None, text[:60], url, "skipped", "LinkedIn API requires manual OAuth flow")
    return {"status": "skipped", "error": "LinkedIn requires manual OAuth setup"}


def submit_to_hackernews(title: str, url: str) -> Dict:
    """Submit to Hacker News. HN doesn't have a public submission API.
    Operator must do this manually. We log a pending_request."""
    if not _can_post("hackernews"):
        return {"status": "skipped", "error": "Rate limit — already submitted in last 14 days"}
    _log_post("hackernews", None, title, url, "pending_human", "HN has no submission API — manual")
    return {"status": "pending_human", "error": "HN has no public submission API. Operator must submit manually at https://news.ycombinator.com/submit"}


def distribution_post(channel: str, title: str, url: str,
                       subreddit: str = "", body_markdown: str = "",
                       canonical_url: str = "", tags: list = None) -> Dict:
    """Dispatch to the right channel."""
    channel = channel.lower()
    if channel == "reddit":
        if not subreddit:
            return {"status": "error", "error": "reddit requires subreddit"}
        return post_to_reddit(subreddit, title, url)
    elif channel == "devto":
        return post_to_devto(title, body_markdown, canonical_url=canonical_url, tags=tags)
    elif channel == "twitter":
        return post_to_twitter(f"{title} — {url}")
    elif channel == "linkedin":
        return post_to_linkedin(f"{title} — {url}", url)
    elif channel == "hackernews":
        return submit_to_hackernews(title, url)
    else:
        return {"status": "error", "error": f"Unknown channel: {channel}"}


# Need urllib.parse for quote
import urllib.parse
