# State — Most Recent Summaries

The agent appends a new summary to this file after each run. The last 2-3 summaries
are preserved for continuity; older history lives in `action_log.md`.

## v4.1 = Maximum Autonomy

v4.1 is v4 + autonomous operation. The operator does the bare minimum (2 secrets +
GitHub Pages), and the agent handles everything else:

- **`bootstrap.py`** runs on every agent run. On first run, it auto-detects the
  GitHub username/repo from `GITHUB_REPOSITORY` env var and replaces ALL placeholders
  (`YOUR-USERNAME`, `REPO-NAME`, `skip`, `skip`, etc.) in
  every file. Idempotent — no-ops on subsequent runs.

- **Self-healing** in `agent.py`:
  - Auto-regenerates sitemap if missing or older than 24h
  - Auto-resets `budget.json` if corrupt
  - Auto-detects placeholders in `docs/` and forces re-bootstrap
  - Auto-logs SEO queue buildup

- **Zero-setup fallbacks** for every monetization component:
  - Analytics: GitHub Traffic API (uses GH_PAT, no signup) when GoatCounter not configured
  - Ads: House ads (cross-promote own tools) when no ad network configured
  - Newsletter: mailto: link when no Buttondown configured
  - Affiliate: Plain links (no commission) when no referral codes configured

- **`setup.sh`** — one-command operator setup that handles everything via `gh` CLI

- **`first-run.yml`** workflow — bootstraps on first push, injects monetization,
  regenerates sitemap, auto-creates a welcome issue with status

## Pre-Loaded Assets

42 pages already in `docs/`:
- 14 tools (json-formatter, qr-generator, base64, password-generator, hash-generator,
  url-encoder, uuid-generator, timestamp-converter, regex-tester, markdown-previewer,
  jwt-decoder, color-converter, yaml-converter, lorem-ipsum)
- 12 converters (csv↔json, csv→yaml, csv→markdown, json→csv, json→yaml, json→xml,
  yaml→json, xml→json, markdown→html, html→markdown, base64-encode/decode)
- 6 calculators (percentage, BMI, loan, compound-interest, age, tip)
- 3 blog posts (free developer tools, CSV-to-JSON guide, JWT tokens guide)
- 2 guides (crypto-tips, affiliate-disclosure)
- Landing page + index pages

## First Run Instructions

When the agent first runs, it should:
1. `bootstrap.py` has already auto-replaced all placeholders (check `memory/.bootstrapped`).
2. Read `memory/revenue_streams.md` to see what's pending operator setup.
3. Generate pending_requests for HIGH-priority items (wallet addresses) only —
   fallbacks handle the rest.
4. Run `seo_update_sitemap` to refresh the sitemap with current pages.
5. Run `seo_submit` to submit URLs to Google/Bing indexing (queues if no API key).
6. Generate 3-5 new programmatic SEO pages (converters/calculators).
7. Verify revenue on at least one chain (rotate through chains daily).

## Summary

(initial run pending — agent will populate this on first execution)
