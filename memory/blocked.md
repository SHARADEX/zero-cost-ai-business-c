# Blocked Actions Log — v4.1 (Autonomous Edition)

- [2026-08-06] [LOW] **Google Indexing API** (faster SEO indexing)
  - Fallback active: URLs queued in `memory/seo_queue.md`, submitted when API configured
  - Upgrade: create Google Cloud service account, enable Indexing API, add as owner in Search Console
  - After: set `GOOGLE_INDEXING_SERVICE_ACCOUNT_JSON` secret
  - Without this, Google still indexes pages (just slower — they crawl sitemap.xml)

- [2026-08-06] [LOW] **Bing URL Submission API**
  - Fallback active: URLs queued
  - Upgrade: register at https://www.bing.com/webmasters
  - After: set `BING_API_KEY` secret

- [2026-08-06] [LOW] **Reddit API** (auto-posting to subreddits)
  - Fallback active: agent generates "ready-to-post" content but doesn't post
  - Upgrade: create Reddit app at https://www.reddit.com/prefs/apps
  - After: set `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD`

- [2026-08-06] [LOW] **Dev.to API** (cross-posting blog articles)
  - Fallback active: articles stay on your site only
  - Upgrade: get API key at https://dev.to/settings/extensions
  - After: set `DEVTO_API_KEY` secret

## Auto-managed (no operator action needed)

These are listed for transparency — the agent handles them automatically:

- ✅ Placeholder replacement (`SHARADEX`, `zero-cost-ai-business-c`) — handled by `bootstrap.py`
- ✅ Sitemap regeneration — handled by `agent.py` self-healing
- ✅ Robots.txt generation — handled by `seo.py`
- ✅ Budget tracking — handled by `budget.py`
- ✅ Provider health circuit breakers — handled by `llm_client.py`
- ✅ On-chain revenue verification — handled by `revenue.py`
- ✅ Security scanning (XSS, secrets, broken links) — handled by `security.py`
- ✅ House ads injection — handled by `monetization.py`
- ✅ Newsletter form (mailto fallback) — handled by `monetization.py`
- ✅ Analytics (GitHub Traffic API fallback) — handled by `analytics.py`

[2026-08-10 09:54:46 UTC] LLM call failed at step 1.
All LLM providers failed. Attempts:
FAIL groq/llama-3.3-70b-versatile attempt 1: HTTP 403: error code: 1010

FAIL groq/llama-3.1-8b-instant attempt 1: HTTP 403: error code: 1010

FAIL groq/mixtral-8x7b-32768 attempt 1: HTTP 403: error code: 1010

CIRCUIT_OPEN groq

[2026-08-10 09:55:14 UTC] LLM call failed at step 1.
All configured providers exhausted or unhealthy. Configured: ['groq']. Budget resets at UTC midnight; health resets after 1 hour of no failures.

[2026-08-10 10:19:25 UTC] LLM call failed at step 2.
All LLM providers failed. Attempts:
SKIP groq - unhealthy (circuit breaker)
SKIP gemini - unhealthy (circuit breaker)
FAIL openrouter/openrouter/free attempt 1: object of type 'NoneType' has no len()

[2026-08-10 12:04:52 UTC] Agent output failed validation twice. Last error: No JSON object found. Output a single JSON object with no prose before or after.

[2026-08-10 12:11:09 UTC] LLM call failed at step 2.
All LLM providers failed. Attempts:
SKIP groq - unhealthy (circuit breaker)
SKIP gemini - unhealthy (circuit breaker)
FAIL openrouter/meta-llama/llama-3.2-3b-instruct:free attempt 1: HTTP 404: {"error":{"message":"This model is unavailable for free. The paid version is available now - use this slug instead: meta-llama/llama-3.2-3b-instruct","code":404},"user_id":"user_3HJomoKgwYYqCFDG6t6Kr9fAylq"}
FAIL openrouter/google/gemini-flash-1.5:free attempt 1: HTTP 404: {"error":{"message":"No endpoints

[2026-08-10 12:35:32 UTC] LLM call failed at step 2.
All configured providers exhausted or unhealthy. Configured: ['groq', 'gemini', 'openrouter']. Budget resets at UTC midnight; health resets after 1 hour of no failures.

[2026-08-10 15:09:02 UTC] LLM retry failed at step 1.
All LLM providers failed. Attempts:
FAIL groq/llama-3.3-70b-versatile attempt 1: HTTP 403: error code: 1010

FAIL groq/llama-3.1-8b-instant attempt 1: HTTP 403: error code: 1010

FAIL groq/mixtral-8x7b-32768 attempt 1: HTTP 403: error code: 1010

FAIL gemini/gemini-2.5-flash attempt 1: HTTP 404: {
  "error": {
    "code": 404,
    "message": "This model models/gemini-2.5-flash is no longer available to new users. Please update your code to use a newer model for the latest features and improvemen

[2026-08-10 15:09:02 UTC] LLM call failed at step 2.
All LLM providers failed. Attempts:
FAIL groq/llama-3.3-70b-versatile attempt 1: HTTP 403: error code: 1010

FAIL groq/llama-3.1-8b-instant attempt 1: HTTP 403: error code: 1010

FAIL groq/mixtral-8x7b-32768 attempt 1: HTTP 403: error code: 1010

SKIP gemini - unhealthy (circuit breaker)
SKIP openrouter - budget exhausted

[2026-08-10 15:43:00 UTC] LLM call failed at step 1.
All LLM providers failed. Attempts:
FAIL groq/llama-3.3-70b-versatile attempt 1: HTTP 403: {"error":{"message":"Access denied. Please check your network settings."}}
CIRCUIT_OPEN groq
SKIP gemini - unhealthy (circuit breaker)
SKIP openrouter - budget exhausted

[2026-08-10 18:37:12 UTC] Agent output failed validation twice. Last error: Missing 'action' field. Must be one of: analytics_fetch, append_doc, delete_file, distribution_post, done, http_get, list_dir, log_experiment, monetize_inject, read_file, revenue_verify, seo_submit, seo_update_sitemap, update_experiment, validate_html, write_file

[2026-08-10 18:37:12 UTC] LLM call failed at step 2.
All LLM providers failed. Attempts:
FAIL groq/llama-3.3-70b-versatile attempt 1: HTTP 403: error code: 1010

FAIL groq/llama-3.1-8b-instant attempt 1: HTTP 403: error code: 1010

FAIL groq/mixtral-8x7b-32768 attempt 1: HTTP 403: error code: 1010

FAIL gemini/gemini-2.5-flash attempt 1: HTTP 404: {
  "error": {
    "code": 404,
    "message": "This model models/gemini-2.5-flash is no longer available to new users. Please update your code to use a newer model for the latest features and improvemen
