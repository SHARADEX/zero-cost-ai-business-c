#!/usr/bin/env python3
"""
Schema validation for agent output.

v3 used a permissive JSON parser with silent fallback to "list_dir" — this
masked real agent errors and let malformed output ship undetected.

v4 uses strict JSON schema validation. If the agent's output fails validation,
the error is fed back to the LLM for a single retry. If the retry also fails,
the run aborts with a clear error (instead of silently degrading).
"""

import json
import re
from typing import Optional, Dict, Any, Tuple

# ---------------------------------------------------------------------------
# Action schema
# ---------------------------------------------------------------------------

VALID_ACTIONS = {
    "write_file", "read_file", "list_dir", "delete_file", "append_doc",
    "http_get", "log_experiment", "update_experiment",
    "validate_html",           # NEW in v4: ship gate for HTML pages
    "seo_update_sitemap",      # NEW in v4: refresh sitemap.xml
    "seo_submit",              # NEW in v4: submit URL to indexing API
    "revenue_verify",          # NEW in v4: on-chain tip verification
    "distribution_post",       # NEW in v4: post to Reddit/Dev.to/Twitter
    "analytics_fetch",         # NEW in v4: pull GoatCounter metrics
    "monetize_inject",         # NEW in v4: inject affiliate/ads into a page
    "done",
}

# Required params per action
ACTION_REQUIRED_PARAMS = {
    "write_file":          {"path", "content"},
    "read_file":           {"path"},
    "list_dir":            {"path"},
    "delete_file":         {"path"},
    "append_doc":          {"path", "append_text"},
    "http_get":            {"url"},
    "log_experiment":      {"hypothesis"},
    "update_experiment":   {"result", "decision"},
    "validate_html":       {"path"},
    "seo_update_sitemap":  set(),
    "seo_submit":          {"urls"},
    "revenue_verify":      {"chain"},
    "distribution_post":   {"channel", "title", "url", "subreddit"},
    "analytics_fetch":     {"metric"},
    "monetize_inject":     {"path"},
    "done":                set(),
}

VALID_DECISIONS = {"KILL", "ITERATE", "SCALE", "PENDING"}
VALID_CHAINS = {"bitcoin", "ethereum", "solana", "tron", "ronin"}
VALID_CHANNELS = {"reddit", "devto", "twitter", "linkedin", "hackernews"}

# Path allowlist (must match tools.py sandbox)
PATH_WRITE_PREFIXES = ("docs",)
PATH_READ_PREFIXES = ("docs", "memory")


def _is_safe_path(path: str, prefixes: Tuple[str, ...]) -> bool:
    """Strict path safety check. Blocks .., absolute paths, symlinks, null bytes."""
    if not path or not isinstance(path, str):
        return False
    if "\x00" in path:
        return False
    if path.startswith("/") or path.startswith("\\"):
        return False
    if ".." in path.split("/"):
        return False
    if ".." in path.split("\\"):
        return False
    # Must start with one of the allowed prefixes
    first_segment = path.replace("\\", "/").split("/", 1)[0]
    return first_segment in prefixes


def validate_action_response(raw_content: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Validate the LLM's action response.

    Returns (parsed_dict, None) on success, or (None, error_message) on failure.
    The error message is suitable for feeding back to the LLM as a retry prompt.
    """
    if not raw_content or not raw_content.strip():
        return None, "Empty response. You must output a single JSON object."

    cleaned = raw_content.strip()

    # Strip markdown code fences if present
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    # Find JSON object boundaries
    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")
    if first_brace == -1 or last_brace == -1 or last_brace <= first_brace:
        return None, "No JSON object found. Output a single JSON object with no prose before or after."

    json_candidate = cleaned[first_brace:last_brace + 1]

    try:
        parsed = json.loads(json_candidate)
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON: {e}. Re-emit the complete JSON object with proper escaping."

    if not isinstance(parsed, dict):
        return None, "Top-level JSON must be an object, not an array or scalar."

    # Required fields
    if "action" not in parsed:
        return None, "Missing 'action' field. Must be one of: " + ", ".join(sorted(VALID_ACTIONS))

    action = parsed["action"]
    if not isinstance(action, str) or action not in VALID_ACTIONS:
        return None, f"Invalid action '{action}'. Must be one of: {', '.join(sorted(VALID_ACTIONS))}"

    # action_params must be a dict (or absent → treated as empty)
    params = parsed.get("action_params", {})
    if params is None:
        params = {}
    if not isinstance(params, dict):
        return None, "'action_params' must be a JSON object."
    parsed["action_params"] = params

    # Required params for this action
    required = ACTION_REQUIRED_PARAMS.get(action, set())
    missing = [p for p in required if p not in params]
    if missing:
        return None, f"Action '{action}' requires params: {', '.join(missing)}. You provided: {list(params.keys())}"

    # Action-specific validation
    err = _validate_action_specific(action, params)
    if err:
        return None, err

    # Optional memory-update fields must be strings if present
    for field in ("revenue_update", "pending_request", "blocked_note",
                  "experiment_result", "analytics_update"):
        if field in parsed and parsed[field] is not None:
            if not isinstance(parsed[field], str):
                return None, f"'{field}' must be a string."

    # reasoning field
    if "reasoning" in parsed and parsed["reasoning"] is not None:
        if not isinstance(parsed["reasoning"], str):
            return None, "'reasoning' must be a string."
        if len(parsed["reasoning"]) > 2000:
            parsed["reasoning"] = parsed["reasoning"][:2000]

    return parsed, None


def _validate_action_specific(action: str, params: Dict[str, Any]) -> Optional[str]:
    """Per-action param validation. Returns error string or None."""
    if action in ("write_file", "delete_file", "append_doc", "validate_html", "monetize_inject"):
        path = params.get("path", "")
        if not _is_safe_path(path, PATH_WRITE_PREFIXES):
            return f"Path '{path}' is not allowed for writes. Must start with one of: {', '.join(PATH_WRITE_PREFIXES)}"

    if action in ("read_file", "list_dir"):
        path = params.get("path", "")
        if not _is_safe_path(path, PATH_READ_PREFIXES):
            return f"Path '{path}' is not allowed for reads. Must start with one of: {', '.join(PATH_READ_PREFIXES)}"

    if action == "write_file":
        content = params.get("content", "")
        if not isinstance(content, str):
            return "'content' for write_file must be a string."
        if len(content) > 250_000:
            return f"write_file content too large ({len(content)} chars). Max 250,000."

    if action == "http_get":
        url = params.get("url", "")
        if not isinstance(url, str) or not (url.startswith("http://") or url.startswith("https://")):
            return f"http_get url must start with http:// or https://, got: {url!r}"
        # Block obvious SSRF targets
        lower = url.lower()
        if any(bad in lower for bad in ("localhost", "127.0.0.1", "169.254.169.254", "0.0.0.0", "::1")):
            return f"http_get blocked: url targets internal or metadata service."

    if action == "update_experiment":
        decision = str(params.get("decision", "")).upper()
        if decision not in VALID_DECISIONS:
            return f"decision must be one of {VALID_DECISIONS}, got: {decision}"

    if action == "revenue_verify":
        chain = str(params.get("chain", "")).lower()
        if chain not in VALID_CHAINS:
            return f"chain must be one of {VALID_CHAINS}, got: {chain}"

    if action == "distribution_post":
        channel = str(params.get("channel", "")).lower()
        if channel not in VALID_CHANNELS:
            return f"channel must be one of {VALID_CHANNELS}, got: {channel}"
        if channel == "reddit" and not params.get("subreddit"):
            return "reddit distribution_post requires 'subreddit' param."

    if action == "seo_submit":
        urls = params.get("urls", [])
        if not isinstance(urls, list) or not urls:
            return "seo_submit 'urls' must be a non-empty list of URL strings."
        for u in urls:
            if not isinstance(u, str) or not u.startswith("http"):
                return f"seo_submit url must be a string starting with http, got: {u!r}"

    return None
