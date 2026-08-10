# Blocked Actions Log — v4.1 (Autonomous Edition)

**Purpose:** Track optional enhancements the operator can make.
**Format:** One clear request per entry with timestamp. Human reviews at their leisure.
**Auto-capped to last 30 entries.**

**v4.1 Philosophy:** The agent runs PROFITABLY from day 1 with zero operator setup
beyond LLM API key + GH_PAT. Everything below is an OPTIONAL ENHANCEMENT — the
agent has zero-setup fallbacks for each.

Key rules:
1. NEVER omit a pending request requiring human action.
2. Do not stall workflow waiting on a pending item — the agent keeps working.
3. Items marked [URGENT] should be addressed first.
4. The agent uses fallbacks for everything in this list — don't wait.

---

## CRITICAL (agent can't run without these)

(If you're seeing this, you've already set these during setup.sh. Skip this section.)

- [2026-08-06] [CRITICAL] `GROQ_API_KEY` (or any LLM API key) — required for agent to function.
- [2026-08-06] [CRITICAL] `GH_PAT` (GitHub PAT with repo scope) — required for agent to commit changes.

## HIGH (revenue goes to wrong place until fixed)

- [2026-08-06] [HIGH] **Replace wallet addresses** in these files with your own:
  - `docs/guides/crypto-tips.html`
  - `memory/revenue.md`
  - `revenue.py` (the `WALLETS` dict at top of file)
  
  Until you do this, tips go to the original author's wallets. This is the SINGLE
  most important manual step. The agent cannot auto-generate wallets for you.

## MEDIUM (upgrade revenue streams — fallbacks are active)

Each of these has a zero-setup fallback that's already active. Upgrading unlocks
more revenue but is NOT required for the agent to function.

- [2026-08-06] [MEDIUM] **EthicalAds or Carbon Ads** (paid ad network)
  - Fallback active: house ads (cross-promotion of your own tools)
  - Upgrade: register at https://ethicalads.io (easy approval) or https://carbonads.net
  - After registration: set `ETHICALADS_PUBLISHER_ID` or `CARBON_ADS_ID` secret
  - Agent will auto-upgrade from house ads to paid ads on next run

- [2026-08-06] [MEDIUM] **Affiliate programs** (commission-based)
  - Fallback active: "Recommended Services" section with plain links (no commission)
  - Upgrade: register for each:
    - DigitalOcean: https://partners.digitalocean.com
    - Vultr: https://www.vultr.com/affiliates
    - Notion: https://www.notion.so/affiliates
    - Frontend Masters: https://frontendmasters.com/affiliates
  - After registration: edit `memory/affiliate_links.md` and replace ``
    with your real codes. Agent will auto-inject them on next `monetize_inject` call.

- [2026-08-06] [MEDIUM] **GitHub Sponsors / Buy Me a Coffee** (direct support)
  - Fallback active: tip box with crypto-only CTA
  - Upgrade: enable GitHub Sponsors at https://github.com/sponsors/YOUR-USERNAME
    and/or register at https://buymeacoffee.com
  - After registration: edit `docs/guides/crypto-tips.html` to replace the
    `YOUR-USERNAME` in the GH Sponsors / BMC URLs.

- [2026-08-06] [MEDIUM] **GoatCounter** (page-level analytics)
  - Fallback active: GitHub Traffic API (uses GH_PAT, zero setup, repo-level data)
  - Upgrade: register at https://goatcounter.com (free under 100k pageviews/month)
  - After registration: set `GC_API_TOKEN` and `GC_SITE_ID` secrets
  - Agent will auto-switch from GitHub Traffic API to GoatCounter

- [2026-08-06] [MEDIUM] **Buttondown** (real newsletter)
  - Fallback active: mailto: link (uses your email)
  - Upgrade: register at https://buttondown.com (free under 100 subscribers)
  - After registration: set `BUTTONDOWN_SLUG` secret
  - Agent will auto-switch from mailto to Buttondown form

## LOW (unlock advanced features — only when traffic justifies)

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

- ✅ Placeholder replacement (`YOUR-USERNAME`, `REPO-NAME`) — handled by `bootstrap.py`
- ✅ Sitemap regeneration — handled by `agent.py` self-healing
- ✅ Robots.txt generation — handled by `seo.py`
- ✅ Budget tracking — handled by `budget.py`
- ✅ Provider health circuit breakers — handled by `llm_client.py`
- ✅ On-chain revenue verification — handled by `revenue.py`
- ✅ Security scanning (XSS, secrets, broken links) — handled by `security.py`
- ✅ House ads injection — handled by `monetization.py`
- ✅ Newsletter form (mailto fallback) — handled by `monetization.py`
- ✅ Analytics (GitHub Traffic API fallback) — handled by `analytics.py`
