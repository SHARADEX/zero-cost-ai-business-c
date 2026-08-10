# Zero-Cost AI Business — v4.1 (Autonomous Profit Engine)

An autonomous AI agent that runs every 30 minutes on **free** infrastructure (GitHub
Actions + GitHub Pages + free LLM providers), building free web tools and content,
and monetizing them through **seven parallel revenue streams**.

> **v4.1 = Maximum Autonomy.** The operator creates a GitHub repo, adds 2 secrets
> (`GROQ_API_KEY` and `GH_PAT`), runs `./setup.sh`, and the agent handles EVERYTHING
> else — placeholder replacement, analytics, ads, newsletter, SEO, distribution.
> Zero-setup fallbacks for every monetization component mean the agent runs
> profitably from day 1, with zero operator intervention beyond the initial setup.

## 🚀 Quick Start (2 minutes)

```bash
# 1. Create a public GitHub repo (e.g., my-tools-site)
# 2. Clone it locally and copy v4.1 files in
git clone https://github.com/YOU/my-tools-site
cd my-tools-site
# (copy v4.1 files here)
git add -A && git commit -m "initial" && git push

# 3. Run the one-command setup
./setup.sh
```

`setup.sh` will:
- Ask for `GROQ_API_KEY` (required — get from https://console.groq.com/keys)
- Ask for `GH_PAT` (required — get from https://github.com/settings/tokens)
- Auto-detect your GitHub username + repo
- Set all GitHub secrets via `gh` CLI
- Enable GitHub Pages
- Trigger the first agent run

**That's it.** The agent is now running. It will:
- Auto-replace all `SHARADEX` / `zero-cost-ai-business-c` placeholders on first run
- Auto-inject monetization (house ads, mailto newsletter, affiliate placeholders)
- Auto-regenerate sitemap, robots.txt
- Auto-use GitHub Traffic API for analytics (zero setup)
- Auto-build new pages, submit to SEO queue, distribute to channels
- Auto-create a welcome issue on first run with status

See [AUTONOMY.md](AUTONOMY.md) for the full list of auto-configuration and fallbacks.

## What's New in v4.1

v4.1 is v4 + **maximum autonomy**:

| Feature | v4 | v4.1 |
|---------|----|----|
| Setup time | 15-30 min (manual placeholder replacement) | **2 min** (one-command `setup.sh`) |
| Placeholder replacement | Manual find-and-replace | **Auto** via `bootstrap.py` |
| Analytics without signup | None (required GoatCounter) | **GitHub Traffic API** fallback |
| Ads without signup | None (required EthicalAds/Carbon) | **House ads** (cross-promotion) fallback |
| Newsletter without signup | None (required Buttondown) | **mailto:** link fallback |
| Affiliate without signup | None | **Plain links** (no commission) fallback |
| Self-healing | None | Sitemap regen, budget reset, placeholder detection |
| First-run experience | Manual trigger + read logs | **Auto-created GitHub issue** with status |
| Operator intervention needed | 10+ tasks | **2 secrets** + replace wallet addresses |

## What's New in v4 (vs v3)

See [CHANGELOG.md](CHANGELOG.md) for the full diff. Highlights:

| Area | v3 | v4 |
|------|----|----|
| **System prompt** | Empty file | 200-line concrete playbook |
| **Revenue streams** | 1 (crypto tips) | 7 (SEO pages, ads, affiliate, tips, sponsors, newsletter, sponsored placements) |
| **Output validation** | Permissive JSON parser, silent fallback | Strict schema validation, 1 retry, then abort |
| **Security** | Path sandbox only | + XSS scan, broken link check, secret scan |
| **Revenue verification** | Agent "told" to verify | Actual on-chain API calls enforced |
| **Programmatic SEO** | None | Templates for converters/calculators/blog posts |
| **Distribution** | None | Reddit, Dev.to, Twitter, LinkedIn, HN (rate-limited) |
| **Analytics** | None | GoatCounter + GitHub Traffic API fallback |
| **Budget tracking** | Request count only | Requests + tokens, with hourly pacing |
| **Provider health** | None | Circuit breaker — failing providers skipped 1 hour |
| **Kill switch** | PAUSE file | + PAUSE_AGENT env + GitHub issue label |
| **Pre-loaded pages** | 8 tools + 3 pages | 42 pages (14 tools, 12 converters, 6 calculators, 3 blog posts, 2 guides, indexes) |

## How It Works

### The Profit Loop

Every 30 minutes, the agent:

1. **OBSERVE** — reads all memory files, checks revenue, analytics, experiments
2. **HYPOTHESIZE** — picks the highest-leverage next action (a page, a tool, an experiment)
3. **ACT** — writes the file, posts the content, runs the experiment
4. **VERIFY** — confirms the file is valid (link check, XSS scan, lint)
5. **DISTRIBUTE** — submits to SEO queue, schedules social post, updates sitemap
6. **MEASURE** — logs the experiment with a concrete success metric + decision date
7. **ITERATE** — next run, looks at results, kills/iterates/scales

See [REVENUE_PLAYBOOK.md](REVENUE_PLAYBOOK.md) for the full 7-stream playbook.

### The 7-Stream Revenue Model

| # | Stream | How it makes money |
|---|--------|-------------------|
| 1 | **Programmatic SEO pages** | Long-tail traffic → ad impressions + affiliate clicks |
| 2 | **Ethical ads** | $0.10–$2 RPM, paid per impression (Carbon Ads, EthicalAds) |
| 3 | **Affiliate links** | Cookie-tracked commissions on VPS/hosting/VPN/courses signups |
| 4 | **Crypto tips** | Direct donations (verify on-chain before logging) |
| 5 | **GitHub Sponsors / Buy Me a Coffee** | Lower friction than crypto for non-crypto users |
| 6 | **Newsletter** | Audience asset → sponsorship inventory later |
| 7 | **Sponsored placements** | Paid featured listings once traffic exists (future state) |

## Setup (15 minutes)

### Step 1: Create the GitHub repo

1. Create a new **public** repo on GitHub (e.g., `zero-cost-ai-business-v4`).
2. Copy ALL files from this project into the repo (preserving the folder structure).
3. Commit and push to `main`.

### Step 2: Get free LLM API keys

Set up as many as you like — the agent uses them in fallback order. **Minimum
recommended:** Groq + Gemini.

| Provider | Where to get free key | Notes |
|---|---|---|
| **Groq** ⭐ | https://console.groq.com/keys | Best free option. 14K req/day. |
| **Google Gemini** ⭐ | https://aistudio.google.com/apikey | Best free quality. No card needed. |
| Cerebras | https://cloud.cerebras.ai/ | Super-fast inference |
| SambaNova | https://cloud.sambanova.ai/ | Big models (405B) |
| Cloudflare | https://dash.cloudflare.com/ | Needs account ID + API token |
| HuggingFace | https://huggingface.co/settings/tokens | Open models |
| OpenRouter | https://openrouter.ai/keys | 50 req/day on free models |

### Step 3: Add API keys as GitHub repo secrets

In your repo: **Settings → Secrets and variables → Actions → New repository secret**

Add the LLM keys you got (any subset works — at minimum, add Groq + Gemini):
- `GROQ_API_KEY`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY`, `CEREBRAS_API_KEY`,
  `SAMBANOVA_API_KEY`, `CF_API_TOKEN` + `CF_ACCOUNT_ID`, `HF_TOKEN`

Also add:
- `GH_PAT` — a GitHub Personal Access Token with `repo` scope (for the agent to
  commit changes back). Create at https://github.com/settings/tokens.
- `SITE_BASE_URL` — your GitHub Pages URL, e.g., `https://SHARADEX.github.io/zero-cost-ai-business-v4`

### Step 4: Enable GitHub Pages

1. In your repo: **Settings → Pages → Build and deployment → Source = GitHub Actions**
2. The included `.github/workflows/deploy-pages.yml` handles deployment.
3. Your site will be live at `https://SHARADEX.github.io/zero-cost-ai-business-c/`.

### Step 5: Replace placeholders

The repo ships with these placeholders that MUST be replaced before going live:

| Placeholder | Where | Replace with |
|---|---|---|
| `SHARADEX` | All HTML files, sitemap, robots, README | Your GitHub username |
| `zero-cost-ai-business-c` | All HTML files, sitemap, robots | Your repo name |
| `skip` | All HTML files (GoatCounter script tag) | Your GoatCounter site code |
| `skip` | All HTML files (Buttondown form) | Your Buttondown newsletter slug |
| `0xd6DFE6b54bF3dBC919Fde57009452fe6bbb0D997` (etc.) | docs/guides/crypto-tips.html, memory/revenue.md, revenue.py | YOUR wallet addresses |

You can do a global find-and-replace. Or write a setup script. Or have the agent
help — open an issue titled "Replace placeholders" and the agent will write a
pending_request listing every file to update.

### Step 6: (Optional) Sign up for monetization services

These are free and unlock specific revenue streams:

| Service | What it unlocks | URL |
|---|---|---|
| GoatCounter | Analytics (free, no cookies) | https://goatcounter.com |
| EthicalAds | Ethical ad network (paid per impression) | https://ethicalads.io |
| Carbon Ads | Developer-focused ad network | https://carbonads.net |
| Buttondown | Newsletter (free up to 100 subscribers) | https://buttondown.com |
| GitHub Sponsors | Direct sponsorship | https://github.com/sponsors |
| Buy Me a Coffee | Tip jar (lower friction than crypto) | https://buymeacoffee.com |

For each, register, get the embed code/key, and update the corresponding
placeholders in the HTML files. Add API keys as GitHub secrets where applicable.

### Step 7: (Optional) Affiliate programs

Register for affiliate programs relevant to developer tools:

| Vendor | Affiliate URL | Category |
|---|---|---|
| DigitalOcean | https://partners.digitalocean.com | Hosting |
| Vultr | https://www.vultr.com/affiliates | Hosting |
| Notion | https://www.notion.so/affiliates | Tools |
| Frontend Masters | https://frontendmasters.com/affiliates | Courses |

After registering, update `memory/affiliate_links.md` with your real referral codes.

### Step 8: (Optional) SEO indexing APIs

For faster Google indexing:
1. Create a Google Cloud service account, enable Indexing API
2. Add the service account as owner in Google Search Console
3. Set `GOOGLE_INDEXING_SERVICE_ACCOUNT_JSON` secret (paste the JSON) or upload
   the JSON file and set `GOOGLE_INDEXING_SA_PATH`

For Bing:
1. Register at https://www.bing.com/webmasters
2. Get API key, set `BING_API_KEY` secret

### Step 9: (Optional) Distribution channels

For Reddit auto-posting:
1. Create a Reddit app at https://www.reddit.com/prefs/apps (script type)
2. Set `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD` secrets

For Dev.to:
1. Get API key at https://dev.to/settings/extensions
2. Set `DEVTO_API_KEY` secret

### Step 10: Trigger the first run

Go to **Actions tab → Zero-Cost Business Autonomous Loop (v4) → Run workflow**.

The agent will now run every 30 minutes automatically.

## File Structure

```
zero-cost-ai-business-v4/
├── .github/workflows/
│   ├── loop.yml                  # Agent loop (every 30 min)
│   ├── deploy-pages.yml          # Deploy docs/ to GitHub Pages
│   ├── daily-seo.yml             # Daily sitemap refresh + indexing submission
│   ├── weekly-report.yml         # Weekly summary issue auto-created
│   └── health-check.yml          # Hourly site health check
├── agent.py                      # Main agent (profit loop, strict validation)
├── llm_client.py                 # Multi-provider LLM client (circuit breakers, tokens)
├── budget.py                     # Daily LLM budget (requests + tokens, hourly pacing)
├── tools.py                      # 16 tools (file ops, SEO, revenue, distribution, ...)
├── validators.py                 # Strict JSON schema validation for agent output
├── security.py                   # XSS scan, broken link check, secret scan
├── seo.py                        # Sitemap, robots.txt, Google/Bing indexing submission
├── revenue.py                    # On-chain balance verification (BTC/ETH/SOL/TRON)
├── monetization.py               # Affiliate link + ad zone + newsletter injection
├── analytics.py                  # GoatCounter integration
├── distribution.py               # Reddit/Dev.to/Twitter/LinkedIn/HN posting
├── templates.py                  # Programmatic SEO templates (converter/calculator/blog)
├── requirements.txt
├── README.md
├── DESIGN.md                     # Architecture & design decisions
├── REVENUE_PLAYBOOK.md           # The 7-stream money-making strategy
├── CHANGELOG.md                  # What changed from v3 to v4
├── LICENSE                       # MIT
├── .gitignore
│
├── prompts/
│   └── business_prompt.md        # The agent's "brain" — 200-line concrete playbook
│
├── memory/                       # Agent's persistent memory
│   ├── state.md                  # Rolling summary of recent runs
│   ├── action_log.md             # Full audit log (auto-trimmed)
│   ├── blocked.md                # Blockers requiring human action
│   ├── revenue.md                # Realized profit + wallet addresses
│   ├── revenue_ledger.json       # Machine-readable verified transactions
│   ├── revenue_streams.md        # Status of each of 7 revenue streams
│   ├── pending_requests.md       # Requests for human operator
│   ├── consult_request.md        # Agent's strategic Q for human
│   ├── consult_response.md       # Human's answer
│   ├── experiments.md            # A/B test & experiment results
│   ├── analytics.md              # Traffic & conversion metrics
│   ├── analytics_data.json       # GoatCounter snapshot
│   ├── budget.md                 # Daily LLM usage (human-readable)
│   ├── budget.json               # Daily LLM usage (machine-readable, atomic writes)
│   ├── provider_health.json      # Per-provider circuit breaker state
│   ├── seo_queue.md              # Pages pending Google indexing
│   ├── distribution_log.md       # Posts to external channels
│   └── affiliate_links.md        # Affiliate link inventory
│
├── config/
│   └── settings.json             # Centralized configuration
│
└── docs/                         # GitHub Pages website (42 pages)
    ├── index.html                # Landing page (lists popular tools/converters/calculators)
    ├── _config.yml               # Jekyll config
    ├── sitemap.xml               # Auto-regenerated by seo_update_sitemap
    ├── robots.txt                # Auto-regenerated
    ├── assets/
    │   ├── css/style.css         # Dark theme, with ad-zone/affiliate/newsletter styles
    │   └── js/main.js            # Copy buttons, GoatCounter event tracking
    ├── tools/                    # 14 tools
    │   ├── index.html
    │   ├── json-formatter.html
    │   ├── qr-generator.html
    │   ├── base64.html
    │   ├── password-generator.html
    │   ├── hash-generator.html
    │   ├── url-encoder.html
    │   ├── uuid-generator.html
    │   ├── timestamp-converter.html
    │   ├── regex-tester.html         # NEW in v4
    │   ├── markdown-previewer.html   # NEW
    │   ├── jwt-decoder.html          # NEW
    │   ├── color-converter.html      # NEW
    │   ├── yaml-converter.html       # NEW
    │   └── lorem-ipsum.html          # NEW
    ├── converters/                  # NEW section — 12 programmatic SEO pages
    │   ├── index.html
    │   ├── csv-to-json.html
    │   ├── csv-to-yaml.html
    │   ├── csv-to-markdown.html
    │   ├── json-to-csv.html
    │   ├── json-to-yaml.html
    │   ├── json-to-xml.html
    │   ├── yaml-to-json.html
    │   ├── xml-to-json.html
    │   ├── markdown-to-html.html
    │   ├── html-to-markdown.html
    │   ├── base64-encode.html
    │   └── base64-decode.html
    ├── calculators/                 # NEW section — 6 programmatic SEO pages
    │   ├── index.html
    │   ├── percentage-calculator.html
    │   ├── bmi-calculator.html
    │   ├── loan-calculator.html
    │   ├── compound-interest.html
    │   ├── age-calculator.html
    │   └── tip-calculator.html
    ├── guides/
    │   ├── crypto-tips.html         # Tip jar with crypto + GH Sponsors + BMC
    │   └── affiliate-disclosure.html  # FTC-compliant disclosure
    └── blog/
        ├── index.html
        ├── free-developer-tools-2026.html
        ├── csv-to-json-conversion-guide.html
        └── understanding-jwt-tokens.html
```

## Security Model

- **Path allowlist (hardened)**: Writes restricted to `docs/`. Reads restricted to
  `docs/` + `memory/`. Blocks `..`, absolute paths, null bytes, symlinks. Real path
  resolution check.
- **Content security scanning**: Every HTML write is scanned for XSS (inline event
  handlers, `javascript:` URLs), embedded secrets (Stripe keys, AWS keys, private keys,
  GitHub PATs), and broken internal links. Failures are rejected, not shipped.
- **Sandboxed HTTP**: External content from `http_get` is wrapped in
  `<<<UNTRUSTED_DATA>>>` envelope. The agent is told explicitly this is data, not
  instructions.
- **SSRF protection**: `http_get` blocks `localhost`, `127.0.0.1`, `169.254.169.254`
  (AWS metadata), `::1`, and `metadata.google`.
- **No secrets in code**: All API keys come from environment variables / GitHub secrets.
- **No private keys**: Only public receive addresses stored. Never requested, never
  transmitted.
- **Kill switch (multi-modal)**: `PAUSE` file in repo root, `PAUSE_AGENT=true` env,
  or a GitHub issue labeled `agent-pause`. All checked at run start.
- **Action audit**: Every action logged in `action_log.md` with timestamp, model,
  tokens used, result.
- **Strict output validation**: Agent responses must pass JSON schema validation. No
  silent fallback to "list_dir" that masked real errors in v3.
- **delete_file scoped**: Only files created in the same run can be deleted.
- **Atomic budget writes**: `budget.json` uses write-then-rename to prevent corruption
  if a run is interrupted.

## How to Audit

Every run is fully logged:
- `memory/state.md` — Rolling summary of last 2-3 runs
- `memory/action_log.md` — Full uncapped audit log (auto-trimmed to 100 runs / 500KB)
- `memory/blocked.md` — Anything blocking progress
- `memory/revenue.md` — Confirmed realized profit (verified on-chain)
- `memory/revenue_ledger.json` — Machine-readable transaction log
- `memory/experiments.md` — All experiments and their results
- `memory/analytics.md` — Traffic and conversion metrics
- `memory/budget.md` + `memory/budget.json` — Daily LLM usage per provider
- `memory/provider_health.json` — Circuit breaker state
- `memory/seo_queue.md` — URLs pending indexing submission
- `memory/distribution_log.md` — Posts to external channels
- `memory/affiliate_links.md` — Affiliate inventory

Plus, the **Weekly Report** workflow auto-creates a GitHub issue every Monday with
a summary of the previous week.

## How to Stop the Agent

Three ways (any one works):

1. **Create a `PAUSE` file** in the repo root:
   ```bash
   touch PAUSE
   git add PAUSE && git commit -m "Pause agent" && git push
   ```
   Delete it to resume.

2. **Set `PAUSE_AGENT=true`** as a repo secret.

3. **Open a GitHub issue** with the label `agent-pause`.

## Troubleshooting

**"All LLM providers failed"** — Check that at least one API key is set as a repo
secret. The agent logs detailed failure reasons in `memory/blocked.md`. Also check
`memory/provider_health.json` — providers may be in circuit-breaker state (skip 1 hour).

**"Skipped — daily budget exhausted"** — All providers hit their daily limit. The
agent resumes at UTC midnight when budgets reset.

**"Skipped — hourly pacing cap"** — The agent burned >15% of daily budget in one hour.
It resumes next hour. This prevents bursts.

**"Workflow doesn't run"** — GitHub Actions scheduled workflows:
- Only run on the default branch
- Can be delayed 5-15 minutes during high load
- Are skipped if the repo has been inactive for 60 days (GitHub auto-disables)

**"GitHub Pages not deploying"** — Make sure Settings → Pages → Source is set to
"GitHub Actions".

**"Agent keeps failing validation"** — Check `memory/action_log.md` for the validation
error. The most common cause is the LLM returning prose before/after JSON. v4 retries
once with a stricter prompt; if it still fails, the step is skipped.

**"No revenue coming in"** — This is expected in the first 30-60 days. Traffic takes
time to build. Focus on:
1. Adding more programmatic SEO pages (stream 1)
2. Setting up EthicalAds/Carbon Ads (stream 2)
3. Adding affiliate links (stream 3)
4. Submitting URLs to Google indexing daily

Revenue follows traffic by 30-90 days. Don't panic if week 1-4 shows $0.

## Customization

- **Change run frequency**: Edit `.github/workflows/loop.yml` → `cron:` line. Current: `*/30 * * * *` (every 30 min).
- **Change daily limits**: Edit `budget.py` → `DAILY_LIMITS` dict.
- **Change max steps per run**: Edit `budget.py` → `get_max_steps_for_budget()`.
- **Add a new LLM provider**: Add a `_call_<provider>()` function in `llm_client.py` and register it in `PROVIDERS`.
- **Add a new tool**: Add a `tool_<name>()` function in `tools.py`, register it in `TOOLS`, and add validation rules in `validators.py`.
- **Change the agent's strategy**: Edit `prompts/business_prompt.md` — this is the agent's "brain".
- **Add a new programmatic template**: Add a function in `templates.py`.

## License

MIT — see [LICENSE](LICENSE).

## Support This Project

If this template helps you make money, consider tipping the original wallets listed
in `docs/guides/crypto-tips.html`. Or fork it and build your own.

## Disclaimer

This is an autonomous AI agent that runs continuously. The operator is responsible
for:
- Ensuring the agent's output is appropriate (review the action log)
- Replacing all placeholder values (`SHARADEX`, wallet addresses, etc.) before
  going live
- Complying with FTC affiliate disclosure rules (the `affiliate-disclosure.html` page
  is included for this purpose)
- Complying with the terms of service of all integrated platforms (Reddit, Dev.to, etc.)
- Ensuring the agent doesn't spam any external platform (the rate limits in
  `distribution.py` are conservative by design — don't bypass them)

The agent is designed to be safe and respectful, but ultimately the operator is
responsible for what it does. Review the action log regularly.
