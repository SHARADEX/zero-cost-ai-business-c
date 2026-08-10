#!/usr/bin/env python3
"""
Bootstrap — Zero-Touch Auto-Configuration
==========================================

Runs on first run (and is safe to re-run). Auto-detects the GitHub username/repo
from the GITHUB_REPOSITORY env var (set automatically by GitHub Actions) or from
`git remote get-url origin`, then replaces ALL placeholders in every file.

After bootstrap, the system is FULLY OPERATIONAL with only:
  - GROQ_API_KEY (or any LLM key)
  - GH_PAT
  - GitHub Pages enabled

Everything else — wallet addresses, affiliate codes, analytics, newsletter, ad
network — has a zero-setup fallback so the agent can run profitably from day 1.
The operator can add the optional enhancements later (see memory/blocked.md).

What bootstrap does:
  1. Detects GitHub username + repo name from env or git remote
  2. Derives SITE_BASE_URL = https://{username}.github.io/{repo}
  3. Walks every file under docs/, memory/, prompts/, README.md, *.yml
  4. Replaces:
       YOUR-USERNAME  → actual username
       REPO-NAME      → actual repo name
       YOUR_GC_CODE   → 'skip' (agent uses GitHub Traffic API instead)
       YOUR_NEWSLETTER_SLUG → 'skip' (agent uses mailto: fallback)
       (wallet addresses are NOT auto-replaced — they require operator input)
  5. Writes a marker file memory/.bootstrapped so it doesn't re-run unnecessarily
  6. Logs what was changed to memory/state.md

Idempotent: safe to run multiple times. Only replaces placeholders; leaves real
values alone.
"""

import os
import re
import subprocess
import sys
from datetime import datetime, timezone

MARKER_FILE = "memory/.bootstrapped"

# Placeholders to replace — value is what they get replaced with
PLACEHOLDER_MAP = {
    "YOUR-USERNAME": None,           # filled in by _detect_identity()
    "YOUR_USERNAME": None,           # alternate form (underscores)
    "REPO-NAME": None,
    "REPO_NAME": None,
    "YOUR_GC_CODE": "skip",          # signals "use GitHub Traffic API fallback"
    "YOUR_NEWSLETTER_SLUG": "skip",  # signals "use mailto: fallback"
    "YOUR_REFERRAL_CODE": "",        # signals "no affiliate code yet"
}

# File globs to process (relative to repo root)
TARGETS = [
    "docs/**/*.html",
    "docs/**/*.xml",
    "docs/**/*.txt",
    "docs/**/*.yml",
    "docs/**/*.js",
    "docs/**/*.css",
    "memory/*.md",
    "prompts/*.md",
    "*.md",
    "*.yml",
    ".github/workflows/*.yml",
    "config/*.json",
]

# Files NOT to touch (operator-controlled, or contains intentional placeholders)
SKIP_FILES = {
    "memory/affiliate_links.md",  # agent manages this
    "memory/revenue.md",            # wallet addresses are intentional
    "AUTONOMY.md",                  # documentation
    "CHANGELOG.md",                 # documentation
}

# Wallet address placeholders that should NOT be auto-replaced
# (operator must provide their own)
WALLET_PLACEHOLDERS = [
    "bc1qh3areygq598ntxht0yp5yv87ej7g6aqvw8fl4z",
    "0xd6DFE6b54bF3dBC919Fde57009452fe6bbb0D997",
    "0xAa4E76e5Be5334c0f2Fe0716C42B2FC61D4c150B",
    "2emXSLoziaB5wdC8y48ovbu41agh9PzR5ro8o7kRDUvM",
    "TJxkyJW57Tb8qmvvv5rCh3L2FYssRvWFEv",
]


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _detect_identity():
    """
    Detect GitHub username and repo name. Order of preference:
      1. GITHUB_REPOSITORY env var (set by GitHub Actions, format: "user/repo")
      2. `git remote get-url origin` output (parse from HTTPS or SSH URL)
      3. SITE_BASE_URL env var (parse user.github.io/repo)
    Returns (username, repo_name) or (None, None) if not detectable.
    """
    # 1. GITHUB_REPOSITORY env
    gh_repo = os.environ.get("GITHUB_REPOSITORY", "")
    if "/" in gh_repo:
        user, repo = gh_repo.split("/", 1)
        return user.strip(), repo.strip()

    # 2. git remote
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=5, check=False
        )
        url = result.stdout.strip()
        if url:
            # HTTPS: https://github.com/USER/REPO.git
            m = re.search(r"github\.com[/:]([^/]+)/([^/\.]+?)(?:\.git)?$", url)
            if m:
                return m.group(1), m.group(2)
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    # 3. SITE_BASE_URL
    site = os.environ.get("SITE_BASE_URL", "")
    m = re.match(r"https?://([^.]+)\.github\.io/([^/]+)/?", site)
    if m:
        return m.group(1), m.group(2)

    return None, None


def _walk_target_files():
    """Walk TARGETS globs and yield file paths, skipping SKIP_FILES."""
    import glob
    seen = set()
    for pattern in TARGETS:
        for path in glob.glob(pattern, recursive=True):
            if not os.path.isfile(path):
                continue
            if path in SKIP_FILES:
                continue
            if path in seen:
                continue
            seen.add(path)
            yield path


def _replace_in_file(path, replacements):
    """
    Replace placeholders in a file. Returns (was_changed, num_replacements).
    Skips wallet address placeholders — those are operator-controlled.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except (OSError, UnicodeDecodeError):
        return False, 0

    original = content
    count = 0

    for old, new in replacements.items():
        if new is None:
            continue
        if old not in content:
            continue
        # Don't touch wallet addresses
        if old in WALLET_PLACEHOLDERS:
            continue
        # Count occurrences
        n = content.count(old)
        if n > 0:
            content = content.replace(old, new)
            count += n

    if content == original:
        return False, 0

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True, count
    except OSError:
        return False, 0


def auto_configure(force=False):
    """
    Main entry point. Auto-configures the system on first run.

    If force=False and memory/.bootstrapped exists, returns early.
    If force=True, re-runs regardless (useful after operator changes things).

    Returns dict with summary: {username, repo, base_url, files_changed, replacements}
    """
    if not force and os.path.exists(MARKER_FILE):
        return {
            "skipped": True,
            "reason": "already bootstrapped (force=True to re-run)"
        }

    username, repo = _detect_identity()
    if not username or not repo:
        return {
            "skipped": True,
            "reason": "could not detect GitHub identity (no GITHUB_REPOSITORY env, no git remote, no SITE_BASE_URL)"
        }

    base_url = f"https://{username}.github.io/{repo}"

    # Build replacement map
    replacements = dict(PLACEHOLDER_MAP)
    replacements["YOUR-USERNAME"] = username
    replacements["YOUR_USERNAME"] = username
    replacements["REPO-NAME"] = repo
    replacements["REPO_NAME"] = repo

    # Walk files and replace
    files_changed = []
    total_replacements = 0
    for path in _walk_target_files():
        changed, count = _replace_in_file(path, replacements)
        if changed:
            files_changed.append({"path": path, "replacements": count})
            total_replacements += count

    # Write marker file
    os.makedirs(os.path.dirname(MARKER_FILE), exist_ok=True)
    with open(MARKER_FILE, "w", encoding="utf-8") as f:
        f.write(_now() + "\n")
        f.write(f"username={username}\n")
        f.write(f"repo={repo}\n")
        f.write(f"base_url={base_url}\n")
        f.write(f"files_changed={len(files_changed)}\n")
        f.write(f"total_replacements={total_replacements}\n")

    # Also update the SITE_BASE_URL in env for downstream tools (only in current process)
    os.environ["SITE_BASE_URL"] = base_url
    os.environ["DETECTED_USERNAME"] = username
    os.environ["DETECTED_REPO"] = repo

    return {
        "skipped": False,
        "username": username,
        "repo": repo,
        "base_url": base_url,
        "files_changed": files_changed,
        "total_replacements": total_replacements,
    }


def is_bootstrapped():
    """Returns True if bootstrap has been run."""
    return os.path.exists(MARKER_FILE)


def get_detected_base_url():
    """Returns the auto-detected base URL, or None."""
    if os.path.exists(MARKER_FILE):
        try:
            with open(MARKER_FILE, "r") as f:
                for line in f:
                    if line.startswith("base_url="):
                        return line.split("=", 1)[1].strip()
        except OSError:
            pass
    # Try fresh detection
    username, repo = _detect_identity()
    if username and repo:
        return f"https://{username}.github.io/{repo}"
    return os.environ.get("SITE_BASE_URL", "")


def needs_operator_input():
    """
    Returns list of things that still need operator input (cannot be auto-configured).
    These are the ONLY things the operator must do manually.
    """
    needs = []

    # Wallet addresses — operator must provide their own
    # (we ship placeholder addresses that match the original v3, but tips sent there
    # go to the original author. Operator MUST replace these.)
    needs.append({
        "item": "Wallet addresses in docs/guides/crypto-tips.html, memory/revenue.md, revenue.py",
        "why": "Crypto tips sent to the placeholder addresses go to the original author, not you.",
        "priority": "HIGH",
        "auto_fallback": "Agent will still run, but revenue from tips goes to wrong wallet."
    })

    # LLM API keys
    if not any(os.environ.get(k) for k in [
        "GROQ_API_KEY", "GEMINI_API_KEY", "OPENROUTER_API_KEY",
        "CEREBRAS_API_KEY", "SAMBANOVA_API_KEY", "CF_API_TOKEN", "HF_TOKEN"
    ]):
        needs.append({
            "item": "At least one LLM API key (GROQ_API_KEY recommended)",
            "why": "Agent can't run without an LLM.",
            "priority": "CRITICAL",
            "auto_fallback": "None — agent will exit."
        })

    # GH_PAT
    if not os.environ.get("GH_PAT"):
        needs.append({
            "item": "GH_PAT (GitHub Personal Access Token with repo scope)",
            "why": "Agent needs this to commit changes back to the repo.",
            "priority": "CRITICAL",
            "auto_fallback": "None — agent runs but changes aren't persisted."
        })

    return needs


if __name__ == "__main__":
    # Run as standalone script (for setup.sh or manual operator use)
    result = auto_configure(force="--force" in sys.argv)
    if result.get("skipped"):
        print(f"Bootstrap skipped: {result.get('reason')}")
    else:
        print(f"Bootstrap complete:")
        print(f"  Username: {result['username']}")
        print(f"  Repo: {result['repo']}")
        print(f"  Base URL: {result['base_url']}")
        print(f"  Files changed: {len(result['files_changed'])}")
        print(f"  Total replacements: {result['total_replacements']}")
        print()
        needs = needs_operator_input()
        if needs:
            print("Still needs operator input:")
            for n in needs:
                print(f"  [{n['priority']}] {n['item']}")
                print(f"      Why: {n['why']}")
                if n.get("auto_fallback"):
                    print(f"      Fallback: {n['auto_fallback']}")
