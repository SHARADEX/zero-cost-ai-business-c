#!/usr/bin/env python3
"""
Daily LLM Budget Management — v4
================================

v3 tracked only request counts per provider. v4 adds:

  1. **Token tracking** — some providers (Groq, SambaNova) throttle on tokens,
     not just requests. We track tokens too.
  2. **Provider health** — if a provider failed N times in the last hour, deprioritize it.
  3. **Pacing** — spread usage across the day based on hour-of-day quota.
  4. **Persistence** — atomic writes (write-then-rename) to avoid corruption.
  5. **Hourly pacing** — never burn >10% of daily budget in a single hour.

Budget file: memory/budget.md (human-readable) + memory/budget.json (machine-readable).
"""

import os
import re
import json
import time
import tempfile
from datetime import datetime, timezone
from typing import Dict, Tuple

BUDGET_MD = os.path.join("memory", "budget.md")
BUDGET_JSON = os.path.join("memory", "budget.json")
HEALTH_JSON = os.path.join("memory", "provider_health.json")

# Conservative daily limits (2026 estimates for free tiers)
DAILY_LIMITS: Dict[str, Dict[str, int]] = {
    # provider: {requests, tokens}
    "groq":        {"requests": 14000, "tokens": 500_000},
    "gemini":      {"requests": 1500,  "tokens": 1_000_000},  # 1500/day, 1M tokens/day free
    "cerebras":    {"requests": 1000,  "tokens": 500_000},
    "sambanova":   {"requests": 500,   "tokens": 500_000},
    "cloudflare":  {"requests": 1000,  "tokens": 200_000},
    "huggingface": {"requests": 500,   "tokens": 200_000},
    "openrouter":  {"requests": 50,    "tokens": 100_000},
}

# Per-hour pacing: never burn more than this fraction of daily budget in one hour
MAX_HOURLY_FRACTION = 0.15

# Provider health: if failures in last 60 min >= this, mark provider as unhealthy
# v4.1: raised from 3 to 10 — a single retry burst (3 models × 3 attempts = 9 failures)
# no longer trips the breaker for a full hour. The breaker should trip on SUSTAINED
# failure, not transient blips. This way one Cloudflare 403 from Groq doesn't block
# all future runs for an hour — the next run will retry Groq fresh.
HEALTH_FAILURE_THRESHOLD = 10
HEALTH_WINDOW_SECONDS = 3600


def _today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _now_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _read_json(path: str, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, IOError):
        return default


def _write_json_atomic(path: str, data):
    """Atomic write: write to temp file, then rename. Prevents corruption."""
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d or ".", prefix=".tmp_", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _default_state() -> Dict:
    today = _today_str()
    return {
        "date": today,
        "last_updated": _now_str(),
        "providers": {
            p: {"requests_used": 0, "tokens_used": 0}
            for p in DAILY_LIMITS
        },
        "hourly_usage": {},  # {"HH": {"requests": N, "tokens": N}}
    }


def _load_state() -> Dict:
    """Load budget state, resetting if it's a new day."""
    state = _read_json(BUDGET_JSON, _default_state())
    today = _today_str()
    if state.get("date") != today:
        state = _default_state()
        _write_json_atomic(BUDGET_JSON, state)
    return state


def _save_state(state: Dict):
    state["date"] = _today_str()
    state["last_updated"] = _now_str()
    _write_json_atomic(BUDGET_JSON, state)
    _write_human_readable(state)


def _write_human_readable(state: Dict):
    """Also write a human-readable .md file for the operator."""
    lines = [
        "# Daily LLM Budget Tracker",
        "",
        f"Date: {state['date']}",
        f"Last Updated: {state['last_updated']}",
        "",
        "## Provider Usage (resets at UTC midnight)",
        "",
        "| Provider | Requests | Tokens |",
        "|----------|----------|--------|",
    ]
    total_req_used = 0
    total_req_limit = 0
    total_tok_used = 0
    total_tok_limit = 0
    for p, limits in DAILY_LIMITS.items():
        used = state["providers"].get(p, {"requests_used": 0, "tokens_used": 0})
        req_used = used.get("requests_used", 0)
        tok_used = used.get("tokens_used", 0)
        req_rem = max(0, limits["requests"] - req_used)
        tok_rem = max(0, limits["tokens"] - tok_used)
        status = "OK" if req_rem > 0 and tok_rem > 0 else "EXHAUSTED"
        lines.append(f"| {p} | {req_used}/{limits['requests']} ({req_rem} rem) [{status}] | {tok_used}/{limits['tokens']} ({tok_rem} rem) |")
        total_req_used += req_used
        total_req_limit += limits["requests"]
        total_tok_used += tok_used
        total_tok_limit += limits["tokens"]
    lines.append("")
    lines.append(f"**TOTAL:** {total_req_used}/{total_req_limit} requests, {total_tok_used}/{total_tok_limit} tokens")
    lines.append("")
    # Hourly usage
    lines.append("## Hourly Usage (UTC)")
    for hour, usage in sorted(state.get("hourly_usage", {}).items()):
        lines.append(f"- {hour}:00 → {usage.get('requests', 0)} req, {usage.get('tokens', 0)} tok")
    lines.append("")
    _write_file(BUDGET_MD, "\n".join(lines))


def _write_file(path, text):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def reset_if_new_day():
    _load_state()  # Side-effect: resets if new day


def get_remaining(provider: str) -> Tuple[int, int]:
    """Returns (remaining_requests, remaining_tokens) for a provider."""
    state = _load_state()
    limits = DAILY_LIMITS.get(provider, {"requests": 0, "tokens": 0})
    used = state["providers"].get(provider, {"requests_used": 0, "tokens_used": 0})
    req_rem = max(0, limits["requests"] - used.get("requests_used", 0))
    tok_rem = max(0, limits["tokens"] - used.get("tokens_used", 0))
    return req_rem, tok_rem


def get_total_remaining() -> Tuple[int, int]:
    """Returns (total_remaining_requests, total_remaining_tokens)."""
    state = _load_state()
    total_req = 0
    total_tok = 0
    for p, limits in DAILY_LIMITS.items():
        used = state["providers"].get(p, {"requests_used": 0, "tokens_used": 0})
        total_req += max(0, limits["requests"] - used.get("requests_used", 0))
        total_tok += max(0, limits["tokens"] - used.get("tokens_used", 0))
    return total_req, total_tok


def get_total_limits() -> Tuple[int, int]:
    return (
        sum(l["requests"] for l in DAILY_LIMITS.values()),
        sum(l["tokens"] for l in DAILY_LIMITS.values()),
    )


def record_usage(provider: str, requests: int = 1, tokens: int = 0):
    """Record usage for a provider."""
    state = _load_state()
    if provider not in state["providers"]:
        state["providers"][provider] = {"requests_used": 0, "tokens_used": 0}
    state["providers"][provider]["requests_used"] += requests
    state["providers"][provider]["tokens_used"] += tokens
    # Hourly tracking
    hour = datetime.now(timezone.utc).strftime("%H")
    if hour not in state["hourly_usage"]:
        state["hourly_usage"] = {h: v for h, v in state.get("hourly_usage", {}).items()
                                  if abs(int(h) - int(hour)) < 24}
        state["hourly_usage"][hour] = {"requests": 0, "tokens": 0}
    state["hourly_usage"][hour]["requests"] = state["hourly_usage"][hour].get("requests", 0) + requests
    state["hourly_usage"][hour]["tokens"] = state["hourly_usage"][hour].get("tokens", 0) + tokens
    _save_state(state)


def get_budget_level() -> str:
    """Returns 'full' | 'high' | 'medium' | 'low' | 'critical' | 'exhausted'."""
    req_rem, tok_rem = get_total_remaining()
    req_limit, tok_limit = get_total_limits()
    if req_limit == 0 or tok_limit == 0:
        return "exhausted"
    req_pct = req_rem / req_limit
    tok_pct = tok_rem / tok_limit
    # Use the more constrained dimension
    pct = min(req_pct, tok_pct)
    if req_rem == 0 or tok_rem == 0:
        return "exhausted"
    elif pct < 0.05:
        return "critical"
    elif pct < 0.20:
        return "low"
    elif pct < 0.50:
        return "medium"
    elif pct < 0.80:
        return "high"
    else:
        return "full"


def get_max_steps_for_budget() -> int:
    """Returns max agentic steps based on budget level."""
    level = get_budget_level()
    return {
        "exhausted": 0,
        "critical":  1,
        "low":       2,
        "medium":    3,
        "high":      4,
        "full":      5,
    }.get(level, 3)


def can_spend_now() -> bool:
    """Hourly pacing check — True if we can spend more this hour."""
    state = _load_state()
    hour = datetime.now(timezone.utc).strftime("%H")
    hourly = state.get("hourly_usage", {}).get(hour, {"requests": 0, "tokens": 0})
    req_limit, tok_limit = get_total_limits()
    hourly_req_cap = req_limit * MAX_HOURLY_FRACTION
    hourly_tok_cap = tok_limit * MAX_HOURLY_FRACTION
    return (hourly.get("requests", 0) < hourly_req_cap
            and hourly.get("tokens", 0) < hourly_tok_cap)


def get_budget_summary() -> str:
    level = get_budget_level()
    req_rem, tok_rem = get_total_remaining()
    req_limit, tok_limit = get_total_limits()
    return (f"{level} | req {req_rem}/{req_limit} | tok {tok_rem}/{tok_limit}")


# ---------------------------------------------------------------------------
# Provider health tracking
# ---------------------------------------------------------------------------

def record_provider_result(provider: str, success: bool, error: str = ""):
    """Record a provider call result for health tracking."""
    health = _read_json(HEALTH_JSON, {"events": []})
    now = time.time()
    # Prune events older than window
    health["events"] = [
        e for e in health.get("events", [])
        if now - e.get("timestamp", 0) < HEALTH_WINDOW_SECONDS
    ]
    health["events"].append({
        "provider": provider,
        "success": success,
        "error": error[:200],
        "timestamp": now,
    })
    _write_json_atomic(HEALTH_JSON, health)


def is_provider_healthy(provider: str) -> bool:
    """A provider is unhealthy if it has >= HEALTH_FAILURE_THRESHOLD failures in last hour."""
    health = _read_json(HEALTH_JSON, {"events": []})
    now = time.time()
    recent = [
        e for e in health.get("events", [])
        if e.get("provider") == provider
        and now - e.get("timestamp", 0) < HEALTH_WINDOW_SECONDS
    ]
    failures = sum(1 for e in recent if not e.get("success"))
    return failures < HEALTH_FAILURE_THRESHOLD


def provider_health_summary() -> Dict[str, Dict]:
    """Returns per-provider health summary for the agent context."""
    result = {}
    for provider in DAILY_LIMITS:
        health = _read_json(HEALTH_JSON, {"events": []})
        now = time.time()
        recent = [
            e for e in health.get("events", [])
            if e.get("provider") == provider
            and now - e.get("timestamp", 0) < HEALTH_WINDOW_SECONDS
        ]
        failures = sum(1 for e in recent if not e.get("success"))
        result[provider] = {
            "healthy": failures < HEALTH_FAILURE_THRESHOLD,
            "recent_calls": len(recent),
            "recent_failures": failures,
        }
    return result
