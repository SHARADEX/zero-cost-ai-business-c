#!/usr/bin/env python3
"""
Multi-provider LLM client — v4
==============================

Improvements over v3:
  1. Token-aware budget tracking (not just request count)
  2. Provider health circuit-breaker (skip failing providers for 1 hour)
  3. Per-model success/failure metrics persisted to disk
  4. Structured-output mode: passes `response_format={"type":"json_object"}` to
     providers that support it, for stricter agent output
  5. Token estimation from response (rough char/4 heuristic when usage stats absent)
  6. Hourly pacing: refuses to call if hourly cap would be exceeded
  7. Better retry logic: 404 → next model, 429 → next provider, 5xx → retry with backoff
"""

import os
import json
import time
import urllib.request
import urllib.error
from typing import Optional, Tuple, List

import budget


# ---------------------------------------------------------------------------
# Fallback model lists (used if dynamic discovery fails)
# ---------------------------------------------------------------------------

FALLBACK_MODELS = {
    "groq": [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
    ],
    "gemini": [
        "gemini-2.0-flash",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash-lite",
    ],
    "cerebras": [
        "llama-3.1-8b-instant",
        "llama3.1-70b",
    ],
    "sambanova": [
        "Meta-Llama-3.1-405B-Instruct",
        "Meta-Llama-3.1-70B-Instruct",
        "Meta-Llama-3.1-8B-Instruct",
    ],
    "cloudflare": [
        "@cf/meta/llama-3.1-8b-instruct",
        "@cf/meta/llama-3-8b-instruct",
    ],
    "huggingface": [
        "meta-llama/Meta-Llama-3-8B-Instruct",
        "mistralai/Mistral-7B-Instruct-v0.3",
        "Qwen/Qwen2.5-7B-Instruct",
    ],
    "openrouter": [
        "openrouter/free",  # alias
    ],
}

DEPRECATED_PATTERNS = [
    "gemini-1.5-",
    "gemini-1.0-",
    "text-bison",
    "chat-bison",
    "gpt-3.5-turbo",
]


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _post_json(url, headers, payload, timeout=45):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _get_json(url, headers, timeout=30):
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _is_deprecated(model_id):
    model_lower = model_id.lower()
    for p in DEPRECATED_PATTERNS:
        if p in model_lower:
            return True
    return False


def _estimate_tokens(text: str) -> int:
    """Rough estimate: ~4 chars per token."""
    return max(1, len(text) // 4)


# ---------------------------------------------------------------------------
# Dynamic model discovery (cached for 24h)
# ---------------------------------------------------------------------------

def _cache_path(provider):
    return os.path.join("memory", "models_cache", f"{provider}.json")


def _read_cache(provider):
    path = _cache_path(provider)
    try:
        with open(path, "r") as f:
            data = json.load(f)
        if time.time() - data.get("timestamp", 0) > 86400:
            return None
        return data.get("models", [])
    except (FileNotFoundError, json.JSONDecodeError, IOError):
        return None


def _write_cache(provider, models):
    path = _cache_path(provider)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump({"timestamp": time.time(), "models": models}, f, indent=2)


def _discover_groq():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return []
    try:
        data = _get_json(
            "https://api.groq.com/openai/v1/models",
            {"Authorization": f"Bearer {api_key}"},
            timeout=15,
        )
        models = [m["id"] for m in data.get("data", [])]
        chat = [m for m in models if any(k in m.lower() for k in ["llama", "mixtral", "gemma"])]
        return [m for m in chat if not _is_deprecated(m)]
    except Exception:
        return []


def _discover_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return []
    try:
        data = _get_json(
            f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}",
            {},
            timeout=15,
        )
        models = []
        for m in data.get("models", []):
            name = m.get("name", "").replace("models/", "")
            methods = m.get("supportedGenerationMethods", [])
            if "generateContent" in methods and not _is_deprecated(name):
                models.append(name)
        return models
    except Exception:
        return []


def _discover_openrouter():
    """OpenRouter has free models that change over time. We use a curated list of
    reliable free models. The 'openrouter/free' alias is flaky (sometimes returns
    no model), so we prefer explicit free model IDs."""
    return [
        "meta-llama/llama-3.2-3b-instruct:free",
        "google/gemini-flash-1.5:free",
        "mistralai/mistral-7b-instruct:free",
        "qwen/qwen-2-7b-instruct:free",
        "openrouter/free",  # alias as last resort
    ]


def _invalidate_openrouter_cache():
    """Clear OpenRouter's cached model list so the new list takes effect."""
    try:
        cache_path = _cache_path("openrouter")
        if os.path.exists(cache_path):
            os.remove(cache_path)
            print("[llm_client] Cleared OpenRouter model cache")
    except Exception:
        pass


def _discover_cerebras():
    api_key = os.environ.get("CEREBRAS_API_KEY")
    if not api_key:
        return []
    try:
        data = _get_json(
            "https://api.cerebras.ai/v1/models",
            {"Authorization": f"Bearer {api_key}"},
            timeout=15,
        )
        models = [m["id"] for m in data.get("data", [])]
        return [m for m in models if not _is_deprecated(m)]
    except Exception:
        return []


def _discover_sambanova():
    api_key = os.environ.get("SAMBANOVA_API_KEY")
    if not api_key:
        return []
    try:
        data = _get_json(
            "https://api.sambanova.ai/v1/models",
            {"Authorization": f"Bearer {api_key}"},
            timeout=15,
        )
        models = [m["id"] for m in data.get("data", [])]
        return [m for m in models if not _is_deprecated(m)]
    except Exception:
        return []


def _discover_cloudflare():
    api_token = os.environ.get("CF_API_TOKEN")
    account_id = os.environ.get("CF_ACCOUNT_ID")
    if not api_token or not account_id:
        return []
    try:
        data = _get_json(
            f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/models/search",
            {"Authorization": f"Bearer {api_token}"},
            timeout=15,
        )
        models = []
        for m in data.get("result", []):
            if m.get("type") == "text-generation":
                name = m.get("name", "")
                if name and not _is_deprecated(name):
                    models.append(name)
        return models
    except Exception:
        return []


def _discover_huggingface():
    return FALLBACK_MODELS.get("huggingface", [])


DISCOVERERS = {
    "groq":        _discover_groq,
    "gemini":      _discover_gemini,
    "openrouter":  _discover_openrouter,
    "cerebras":    _discover_cerebras,
    "sambanova":   _discover_sambanova,
    "cloudflare":  _discover_cloudflare,
    "huggingface": _discover_huggingface,
}


def get_models_for_provider(provider):
    cached = _read_cache(provider)
    if cached:
        return cached
    discoverer = DISCOVERERS.get(provider)
    if discoverer:
        try:
            models = discoverer()
            if models:
                _write_cache(provider, models)
                return models
        except Exception:
            pass
    return FALLBACK_MODELS.get(provider, [])


# ---------------------------------------------------------------------------
# Provider call implementations
# ---------------------------------------------------------------------------

def _extract_chat_content(data, provider_name):
    """
    Safely extract content + tokens from an OpenAI-compatible chat completion
    response (Groq, OpenRouter, Cerebras, SambaNova, HuggingFace all use this shape).

    Returns: (content, tokens)
    Raises:  RuntimeError with a useful message if the response is malformed.
    """
    # Some providers return errors inline (200 OK with error body)
    if data.get("error"):
        err = data["error"]
        if isinstance(err, dict):
            err = err.get("message") or str(err)
        raise RuntimeError(f"{provider_name} returned error: {err}")
    # Missing choices entirely
    choices = data.get("choices")
    if not choices or not isinstance(choices, list):
        msg = data.get("message") or "no choices in response"
        raise RuntimeError(f"{provider_name} returned no choices: {msg}")
    first = choices[0] if isinstance(choices[0], dict) else {}
    msg_obj = first.get("message") or {}
    content = msg_obj.get("content")
    if not content:
        finish = first.get("finish_reason", "unknown")
        raise RuntimeError(f"{provider_name} returned empty content (finish_reason={finish})")
    usage = data.get("usage") or {}
    tokens = usage.get("total_tokens") or _estimate_tokens(content)
    return content, tokens


def _extract_gemini_content(data):
    """Safely extract content from a Gemini response (different shape)."""
    if data.get("error"):
        err = data["error"]
        if isinstance(err, dict):
            err = err.get("message") or str(err)
        raise RuntimeError(f"gemini returned error: {err}")
    candidates = data.get("candidates")
    if not candidates:
        msg = data.get("promptFeedback", {}).get("blockReason") or "no candidates in response"
        raise RuntimeError(f"gemini returned no candidates: {msg}")
    first = candidates[0] if isinstance(candidates[0], dict) else {}
    parts = (first.get("content") or {}).get("parts") or []
    if not parts:
        finish = first.get("finishReason", "unknown")
        raise RuntimeError(f"gemini returned empty content (finishReason={finish})")
    content = parts[0].get("text", "")
    if not content:
        raise RuntimeError("gemini returned empty text in first part")
    usage = data.get("usageMetadata") or {}
    tokens = usage.get("totalTokenCount") or _estimate_tokens(content)
    return content, tokens


def _call_groq(messages, model, max_tokens, temperature, json_mode=False):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature}
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    data = _post_json(url, headers, payload, timeout=60)
    content, tokens = _extract_chat_content(data, "groq")
    return content, "groq", tokens


def _call_openrouter(messages, model, max_tokens, temperature, json_mode=False):
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/zero-cost-ai-business-v4",
        "X-Title": "Zero-Cost AI Business Agent v4",
    }
    payload = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature}
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    data = _post_json(url, headers, payload, timeout=60)
    content, tokens = _extract_chat_content(data, "openrouter")
    return content, "openrouter", tokens


def _call_gemini(messages, model, max_tokens, temperature, json_mode=False):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")
    system_text = ""
    contents = []
    for m in messages:
        if m["role"] == "system":
            system_text += m["content"] + "\n"
        elif m["role"] == "user":
            contents.append({"role": "user", "parts": [{"text": m["content"]}]})
        elif m["role"] == "assistant":
            contents.append({"role": "model", "parts": [{"text": m["content"]}]})
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        f"?key={api_key}"
    )
    gen_config = {"maxOutputTokens": max_tokens, "temperature": temperature}
    if json_mode:
        gen_config["responseMimeType"] = "application/json"
    payload = {
        "systemInstruction": {"parts": [{"text": system_text}]} if system_text else None,
        "contents": contents,
        "generationConfig": gen_config,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    data = _post_json(url, {"Content-Type": "application/json"}, payload, timeout=60)
    content, tokens = _extract_gemini_content(data)
    return content, "gemini", tokens


def _call_cerebras(messages, model, max_tokens, temperature, json_mode=False):
    api_key = os.environ.get("CEREBRAS_API_KEY")
    if not api_key:
        raise RuntimeError("CEREBRAS_API_KEY not set")
    url = "https://api.cerebras.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature}
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    data = _post_json(url, headers, payload, timeout=60)
    content, tokens = _extract_chat_content(data, "cerebras")
    return content, "cerebras", tokens


def _call_sambanova(messages, model, max_tokens, temperature, json_mode=False):
    api_key = os.environ.get("SAMBANOVA_API_KEY")
    if not api_key:
        raise RuntimeError("SAMBANOVA_API_KEY not set")
    url = "https://api.sambanova.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature}
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    data = _post_json(url, headers, payload, timeout=90)
    content, tokens = _extract_chat_content(data, "sambanova")
    return content, "sambanova", tokens


def _call_cloudflare(messages, model, max_tokens, temperature, json_mode=False):
    api_token = os.environ.get("CF_API_TOKEN")
    account_id = os.environ.get("CF_ACCOUNT_ID")
    if not api_token or not account_id:
        raise RuntimeError("CF_API_TOKEN or CF_ACCOUNT_ID not set")
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
    headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
    payload = {"messages": messages, "max_tokens": max_tokens, "temperature": temperature}
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    data = _post_json(url, headers, payload, timeout=60)
    # Cloudflare uses a different shape: { "result": { "response": "..." } }
    if not data.get("success", True):
        errors = data.get("errors", [])
        err_msg = errors[0].get("message") if errors else "unknown cloudflare error"
        raise RuntimeError(f"cloudflare returned error: {err_msg}")
    result = data.get("result") or {}
    content = result.get("response")
    if not content:
        raise RuntimeError("cloudflare returned empty response")
    tokens = _estimate_tokens(content)
    return content, "cloudflare", tokens


def _call_huggingface(messages, model, max_tokens, temperature, json_mode=False):
    api_key = os.environ.get("HF_TOKEN")
    if not api_key:
        raise RuntimeError("HF_TOKEN not set")
    url = f"https://api-inference.huggingface.co/models/{model}/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature}
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    data = _post_json(url, headers, payload, timeout=60)
    content, tokens = _extract_chat_content(data, "huggingface")
    return content, "huggingface", tokens


PROVIDERS = [
    ("groq",        "GROQ_API_KEY",        _call_groq),
    ("gemini",      "GEMINI_API_KEY",      _call_gemini),
    ("cerebras",    "CEREBRAS_API_KEY",    _call_cerebras),
    ("sambanova",   "SAMBANOVA_API_KEY",   _call_sambanova),
    ("cloudflare",  "CF_API_TOKEN",        _call_cloudflare),
    ("huggingface", "HF_TOKEN",            _call_huggingface),
    ("openrouter",  "OPENROUTER_API_KEY",  _call_openrouter),
]

MAX_RETRIES_PER_MODEL = 2
RETRY_DELAY_SECONDS = 5


def list_available_providers():
    """Providers with API key configured, budget remaining, AND healthy."""
    budget.reset_if_new_day()
    result = []
    for name, env, _ in PROVIDERS:
        if not os.environ.get(env):
            continue
        req_rem, tok_rem = budget.get_remaining(name)
        if req_rem <= 0 or tok_rem <= 0:
            continue
        if not budget.is_provider_healthy(name):
            continue
        result.append(name)
    return result


def list_configured_providers():
    return [name for name, env, _ in PROVIDERS if os.environ.get(env)]


def call_llm_with_fallback(messages, max_tokens=3000, temperature=0.7, json_mode=True):
    """
    Try every configured provider/model in order until one succeeds.

    v4 improvements:
      - Records health per call
      - Returns token usage for budget tracking
      - Smart retry: 404 → next model, 429 → next provider, 5xx → backoff retry

    Returns: (content, provider_name, tokens_used, attempts_log)
    Raises:  RuntimeError if ALL providers fail or budget exhausted.
    """
    attempts = []
    budget.reset_if_new_day()

    configured = list_configured_providers()
    if not configured:
        raise RuntimeError(
            "No LLM provider API keys found. Set at least one of: "
            "GROQ_API_KEY, GEMINI_API_KEY, OPENROUTER_API_KEY, CEREBRAS_API_KEY, "
            "SAMBANOVA_API_KEY, CF_API_TOKEN+CF_ACCOUNT_ID, HF_TOKEN"
        )

    # Hourly pacing check
    if not budget.can_spend_now():
        raise RuntimeError(
            "Hourly budget pacing cap reached. Agent will resume next hour."
        )

    available = list_available_providers()
    if not available:
        raise RuntimeError(
            f"All configured providers exhausted or unhealthy. "
            f"Configured: {configured}. Budget resets at UTC midnight; "
            f"health resets after 1 hour of no failures."
        )

    for provider_name, env_var, call_fn in PROVIDERS:
        if provider_name not in available:
            if provider_name in configured:
                req_rem, tok_rem = budget.get_remaining(provider_name)
                if req_rem <= 0 or tok_rem <= 0:
                    attempts.append(f"SKIP {provider_name} - budget exhausted")
                elif not budget.is_provider_healthy(provider_name):
                    attempts.append(f"SKIP {provider_name} - unhealthy (circuit breaker)")
            continue

        models = get_models_for_provider(provider_name)
        if not models:
            attempts.append(f"SKIP {provider_name} - no models available")
            continue

        for model in models:
            for attempt in range(1, MAX_RETRIES_PER_MODEL + 1):
                try:
                    content, used_provider, tokens = call_fn(
                        messages, model, max_tokens, temperature, json_mode=json_mode
                    )
                    budget.record_usage(used_provider, requests=1, tokens=tokens)
                    budget.record_provider_result(used_provider, success=True)
                    attempts.append(f"OK {used_provider}/{model} (attempt {attempt}, {tokens} tok)")
                    return content, used_provider, tokens, attempts
                except urllib.error.HTTPError as e:
                    err_body = ""
                    try:
                        err_body = e.read().decode("utf-8", errors="replace")[:300]
                    except Exception:
                        pass
                    err_msg = f"HTTP {e.code}: {err_body}"
                    attempts.append(f"FAIL {provider_name}/{model} attempt {attempt}: {err_msg}")
                    # 404 → model not found, move to next model
                    if e.code == 404:
                        break
                    # 429 → rate limited, move to next provider
                    if e.code == 429:
                        budget.record_provider_result(provider_name, success=False, error="429")
                        break
                    # 5xx → retry with backoff
                    if 500 <= e.code < 600 and attempt < MAX_RETRIES_PER_MODEL:
                        time.sleep(RETRY_DELAY_SECONDS * attempt)
                        continue
                    # Other → record and move on
                    budget.record_provider_result(provider_name, success=False, error=err_msg)
                    break
                except Exception as e:
                    err_msg = str(e)[:200]
                    attempts.append(f"FAIL {provider_name}/{model} attempt {attempt}: {err_msg}")
                    budget.record_provider_result(provider_name, success=False, error=err_msg)
                    if attempt < MAX_RETRIES_PER_MODEL:
                        time.sleep(RETRY_DELAY_SECONDS)
                    break

            if budget.get_remaining(provider_name)[0] <= 0:
                attempts.append(f"BUDGET_EXHAUSTED {provider_name}")
                break
            if not budget.is_provider_healthy(provider_name):
                attempts.append(f"CIRCUIT_OPEN {provider_name}")
                break

    raise RuntimeError("All LLM providers failed. Attempts:\n" + "\n".join(attempts))
