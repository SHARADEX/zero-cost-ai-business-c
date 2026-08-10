# Changelog — v4

## v4.0.0 (2026-08-06)

Complete rewrite focused on **actually generating revenue** at zero cost.

### Breaking Changes from v3

- `prompts/business_prompt.md` is no longer empty. The agent now follows a concrete
  playbook. If you have a customized prompt, you'll need to merge your changes.
- `tools.py` adds 8 new tools. The agent's response schema is now strictly validated
  — silent fallback to `list_dir` is gone.
- `budget.py` writes both `budget.md` (human-readable) and `budget.json` (machine).
  The JSON file is the source of truth.
- `agent.py` uses `validators.validate_action_response()` instead of the inline
  permissive parser.
- All HTML files now include ad zone, newsletter form, and GoatCounter script.
- Memory directory has 4 new files: `revenue_streams.md`, `seo_queue.md`,
  `distribution_log.md`, `affiliate_links.md`, plus 4 JSON files
  (`budget.json`, `revenue_ledger.json`, `provider_health.json`, `analytics_data.json`).

### New Features

#### Revenue
- **7-stream revenue playbook** — programmatic SEO, ethical ads, affiliate links,
  crypto tips, GH Sponsors/BMC, newsletter, sponsored placements
- **On-chain revenue verification** — actual API calls to blockchain explorers
  (blockchain.info, etherscan, Solana RPC, trongrid)
- **Affiliate link injection** — `monetize_inject` tool auto-injects contextual
  affiliate links based on page keywords
- **GitHub Sponsors + Buy Me a Coffee** integration on tip page

#### SEO
- **Programmatic SEO templates** — `templates.py` module generates converter,
  calculator, and blog post pages from parameter sets
- **Sitemap auto-regeneration** — `seo_update_sitemap` tool walks `docs/` and
  rebuilds `sitemap.xml`
- **Google Indexing API submission** — `seo_submit` tool (requires service account)
- **Bing URL Submission API** — same tool, separate submission
- **SEO queue management** — `memory/seo_queue.md` tracks pending submissions

#### Distribution
- **Reddit posting** — `distribution_post` tool with per-subreddit rate limits
- **Dev.to cross-posting** — with `canonical_url` for SEO
- **Twitter / LinkedIn / Hacker News** — graceful degradation when API not configured

#### Analytics
- **GoatCounter integration** — privacy-respecting, no cookies, no consent banner
- **Event tracking** — outbound clicks, tip CTA clicks (for A/B test measurement)
- **Analytics fetch tool** — agent can pull real metrics to inform decisions

#### Security
- **Strict output validation** — `validators.py` enforces JSON schema; no silent
  fallback. Failed validation → 1 retry → abort step (logged to `blocked.md`)
- **XSS scanner** — `security.py` blocks inline event handlers, `javascript:` URLs,
  non-allowlisted external scripts
- **Secret scanner** — blocks writes containing Stripe keys, AWS keys, GitHub PATs,
  private keys, etc.
- **Broken link checker** — validates internal links resolve to real files in `docs/`
- **Hardened path sandbox** — blocks `..`, absolute paths, null bytes, symlinks;
  resolves real path and verifies it stays inside sandbox
- **SSRF protection** — `http_get` blocks localhost, 127.0.0.1, 169.254.169.254,
  metadata.google, ::1
- **delete_file scoped to same-run files** — prevents the agent from deleting
  pre-existing files

#### Reliability
- **Provider health circuit breakers** — failing providers skipped for 1 hour
- **Hourly budget pacing** — never burns >15% of daily budget in one hour
- **Token-aware budgeting** — tracks both requests AND tokens per provider
- **Atomic file writes** — `budget.json` uses write-then-rename (no corruption on crash)
- **Multi-modal kill switch** — PAUSE file, PAUSE_AGENT env var, or GitHub issue
  labeled `agent-pause`
- **Retry on commit failure** — workflow retries `git push` up to 3 times on network blips
- **Retry on validation failure** — agent gets 1 retry with stricter prompt

#### Tooling
- **16 tools** (up from 8): write_file, read_file, list_dir, delete_file, append_doc,
  http_get, log_experiment, update_experiment, validate_html, seo_update_sitemap,
  seo_submit, revenue_verify, distribution_post, analytics_fetch, monetize_inject, done

#### Content (Pre-loaded Pages)
- **42 pages** (up from 11): 14 tools + 12 converters + 6 calculators + 3 blog posts
  + 2 guides + 5 index pages

#### Workflows
- **loop.yml** — every 30 min (improved with retries, kill switch env var, token tracking)
- **deploy-pages.yml** — same as v3
- **daily-seo.yml** — NEW: daily sitemap refresh + indexing submission
- **weekly-report.yml** — NEW: auto-creates a GitHub issue every Monday with summary
- **health-check.yml** — NEW: hourly check that the site, sitemap, robots, and a tool
  page are all reachable; creates an issue if any check fails

### Documentation
- **README.md** — completely rewritten with setup steps, file structure, security model
- **DESIGN.md** — NEW: explains every design decision and trade-off
- **REVENUE_PLAYBOOK.md** — NEW: the 7-stream money-making strategy with targets
- **CHANGELOG.md** — this file

### Bug Fixes from v3

- **Empty business prompt**: v3's `prompts/business_prompt.md` was an empty file.
  v4's is a 200-line concrete playbook. (This was the single biggest flaw in v3.)
- **Silent parser fallback**: v3's parser silently fell back to `list_dir` on JSON
  parse failure, masking real agent errors. v4 strictly validates and aborts on failure.
- **Unverified revenue**: v3 logged "$0.06 (carried over from prior experiment)" with
  no on-chain verification. v4 has actual API calls to verify tips before logging.
- **No content security**: v3 could ship XSS vulnerabilities or broken HTML. v4 scans
  every HTML write before allowing it.
- **Symlink escape**: v3's path sandbox didn't resolve symlinks, allowing potential
  escape. v4 resolves real paths and verifies they stay inside the sandbox.
- **Single revenue stream**: v3 bet everything on crypto tips. v4 has 7 parallel streams.
- **No distribution**: v3 had no way to post content externally. v4 has 5 channels.
- **No analytics**: v3 had no real metrics. v4 has GoatCounter integration.
- **Bursty budget usage**: v3 could burn the entire daily budget in the first few runs.
  v4 has hourly pacing caps.
- **Provider failures cascade**: v3 retried failed providers, wasting budget. v4 has
  circuit breakers that skip failing providers for 1 hour.

### Migration from v3

If you have a v3 deployment and want to upgrade:

1. **Back up your v3 repo** — `git clone` it locally.
2. **Copy v3's memory files** into v4's `memory/` directory (except `budget.md`,
   `budget.json`, `provider_health.json`, `revenue_ledger.json` — let v4 create fresh).
3. **Manually migrate any custom tools** you added to v3's `tools.py` — they need to
   be re-registered in v4's `tools.py` AND have validation rules added in `validators.py`.
4. **Manually migrate any custom providers** in v3's `llm_client.py` — the function
   signature changed (now returns 3 values: content, provider, tokens).
5. **Replace your v3 prompt** with v4's `prompts/business_prompt.md` (or merge your
   customizations into v4's structure).
6. **Replace placeholders** in v4's HTML files (`YOUR-USERNAME`, `REPO-NAME`,
   `YOUR_GC_CODE`, `YOUR_NEWSLETTER_SLUG`, wallet addresses) with your real values.
7. **Commit and push**. The next cron run will use v4.

### Known Limitations

- **No real backend** — all tools run client-side in the browser. Limits monetization
  to ad/affiliate/tip models. No paid API tier possible without adding a backend.
- **No concurrent writes** — only one agent run at a time (enforced by GitHub Actions
  concurrency group). If you need parallelism, run multiple agents in separate repos.
- **Twitter v2 API requires OAuth 1.0a** — the agent logs a `pending_request` for
  the operator to tweet manually. (Twitter v2 doesn't support simple bearer-token
  posting.)
- **LinkedIn API requires manual OAuth flow** — same as Twitter; manual posting.
- **Hacker News has no submission API** — manual posting required.
- **Ronin chain has no free public API** — revenue verification for Ronin is skipped;
  the agent should log a `pending_request` if a Ronin tip is suspected.

### What's Next (v4.1 ideas)

- A/B test infrastructure with deterministic traffic splitting (cookie-based)
- Multi-language support (i18n) for top-performing pages
- Auto-generate schema markup (FAQ, HowTo, Product) for eligible pages
- Backlink outreach automation (find sites linking to similar tools, suggest adding
  a link to ours)
- Email digest of weekly report (via Buttondown broadcast)
- Server-side rendering via Cloudflare Workers (free tier) for dynamic content
- Browser extension for one of the tools (e.g., a "copy as markdown" browser extension
  that promotes the main site)
