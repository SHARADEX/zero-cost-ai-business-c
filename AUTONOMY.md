# Autonomy — How v4.1 Runs Itself
==================================

**Goal:** The operator creates a GitHub repo, adds 2 secrets (`GROQ_API_KEY` and
`GH_PAT`), and the agent handles everything else. No file editing, no manual
placeholder replacement, no service signups required to start.

This document lists every auto-configuration and fallback in the system.

---

## The 2-Minute Setup

```bash
# 1. Create a public GitHub repo (e.g., my-tools-site)
# 2. Push this code to it
git clone https://github.com/YOU/my-tools-site
cd my-tools-site
# (copy v4 files here)
git add -A && git commit -m "initial" && git push

# 3. Run setup.sh
./setup.sh
# (it asks for GROQ_API_KEY and GH_PAT, sets them as GitHub secrets,
#  enables GitHub Pages, triggers first run)
```

**That's it.** The agent is now running. Everything else is automatic.

---

## What `setup.sh` Does

1. Asks for `GROQ_API_KEY` (required)
2. Asks for `GH_PAT` (required)
3. Auto-detects your GitHub username + repo from git remote
4. Sets `SITE_BASE_URL` secret = `https://YOUR-USERNAME.github.io/YOUR-REPO`
5. Asks for `GEMINI_API_KEY` (optional)
6. Asks for `OPERATOR_EMAIL` (optional — for mailto newsletter fallback)
7. Enables GitHub Pages (source: GitHub Actions)
8. Commits and pushes
9. Triggers the first agent run

**Total time: ~2 minutes.**

---

## What `bootstrap.py` Does (Automatically)

Runs on every agent run. No-ops if already bootstrapped. On first run:

1. **Detects GitHub identity** from one of:
   - `GITHUB_REPOSITORY` env var (set by GitHub Actions)
   - `git remote get-url origin` output
   - `SITE_BASE_URL` env var

2. **Derives SITE_BASE_URL** = `https://{username}.github.io/{repo}`

3. **Walks every file** in:
   - `docs/**/*.{html,xml,txt,yml,js,css}`
   - `memory/*.md`
   - `prompts/*.md`
   - `*.md`, `*.yml`, `.github/workflows/*.yml`, `config/*.json`

4. **Replaces placeholders**:
   - `YOUR-USERNAME` → actual username
   - `YOUR_USERNAME` → actual username (alternate form)
   - `REPO-NAME` → actual repo name
   - `REPO_NAME` → actual repo name (alternate form)
   - `YOUR_GC_CODE` → `skip` (signals "use GitHub Traffic API")
   - `YOUR_NEWSLETTER_SLUG` → `skip` (signals "use mailto:")
   - `YOUR_REFERRAL_CODE` → `` (signals "no affiliate code yet")

5. **Does NOT replace**:
   - Wallet addresses (operator must provide their own — see `memory/blocked.md`)
   - Files in `SKIP_FILES` set (operator-controlled)

6. **Writes a marker** to `memory/.bootstrapped` so it doesn't re-run unnecessarily.

7. **Idempotent**: safe to run multiple times. Only replaces placeholders; leaves
   real values alone.

---

## Self-Healing Behaviors (Built Into `agent.py`)

Every agent run, before the main loop:

### 1. Sitemap auto-regeneration
- **Condition**: `docs/sitemap.xml` is missing OR older than 24 hours
- **Action**: regenerate from current `docs/` structure via `seo.regenerate_sitemap()`
- **Why**: ensures new pages are always in the sitemap for Google to find

### 2. Corrupt budget reset
- **Condition**: `memory/budget.json` is missing or unparseable
- **Action**: reset to fresh state with `budget._default_state()`
- **Why**: prevents the agent from being permanently stuck if state corrupts

### 3. Placeholder detection
- **Condition**: any HTML file in `docs/` still contains `YOUR-USERNAME` or `REPO-NAME`
- **Action**: force-run `bootstrap.auto_configure(force=True)`
- **Why**: catches cases where new files were added with placeholders

### 4. SEO queue monitoring
- **Condition**: `memory/seo_queue.md` has >20 pending URLs
- **Action**: log a note (no auto-remediation — needs operator to add indexing API key)
- **Why**: alerts the operator that indexing is backed up

---

## Zero-Setup Fallbacks

Each monetization/analytics component has a fallback that works with **zero
operator setup**. The agent uses the fallback by default and auto-upgrades when
the operator configures the real thing.

### Analytics

| Component | Real (requires signup) | Fallback (zero-setup) | Auto-upgrade trigger |
|-----------|------------------------|------------------------|----------------------|
| Page views | GoatCounter (`GC_API_TOKEN` + `GC_SITE_ID`) | **GitHub Traffic API** (uses `GH_PAT`) | Set both secrets |
| Top pages | GoatCounter | GitHub Traffic API (`popular/paths`) | Same |
| Top referrers | GoatCounter | GitHub Traffic API (`popular/referrers`) | Same |

**Fallback details**: GitHub Traffic API returns 14-day view data for the repo
(not the Pages site, but a strong proxy). Requires only `GH_PAT` which is already
set. Endpoint: `GET /repos/{owner}/{repo}/traffic/views`.

### Ads

| Component | Real (requires approval) | Fallback (zero-setup) | Auto-upgrade trigger |
|-----------|--------------------------|------------------------|----------------------|
| Ad zone | EthicalAds / Carbon Ads | **House ads** (cross-promote own tools) | Set `ETHICALADS_PUBLISHER_ID` or `CARBON_ADS_ID` |

**Fallback details**: House ads randomly pick a tool from the site and display it
in the ad zone. Builds internal traffic, keeps the layout consistent, and gives
the operator time to sign up for a real ad network. Implemented in JS so the ad
changes per page load (no stale content).

### Newsletter

| Component | Real (requires signup) | Fallback (zero-setup) | Auto-upgrade trigger |
|-----------|------------------------|------------------------|----------------------|
| Newsletter form | Buttondown (`BUTTONDOWN_SLUG`) | **mailto: link** (uses `OPERATOR_EMAIL` or GitHub email) | Set `BUTTONDOWN_SLUG` secret |

**Fallback details**: Renders as a "Subscribe via Email" button that opens the
visitor's email client with a pre-filled subscribe message. Operator receives
the email and manually adds the subscriber. Works with any email provider.

### Affiliate Links

| Component | Real (requires signup per vendor) | Fallback (zero-setup) | Auto-upgrade trigger |
|-----------|-----------------------------------|------------------------|----------------------|
| "Recommended Services" section | Affiliate URLs with referral codes | **Plain links** to vendor sites (no commission) | Replace `YOUR_REFERRAL_CODE` in `memory/affiliate_links.md` |

**Fallback details**: The agent parses `memory/affiliate_links.md` and skips
entries that still have `YOUR_REFERRAL_CODE` in the URL. If ALL entries are
skipped, no affiliate block is injected. When the operator adds real codes,
the agent auto-injects the block on the next `monetize_inject` call.

### Crypto Tips

| Component | Real | Fallback | Auto-upgrade trigger |
|-----------|------|----------|----------------------|
| Tip box | Operator's wallet addresses | **Original author's wallets** (placeholders) | Operator edits `docs/guides/crypto-tips.html` |

**Fallback details**: There IS no fallback for this — if you don't replace the
wallet addresses, tips go to the original author. This is the SINGLE manual step
the agent cannot do for you. The agent reminds you weekly via the weekly report.

### GitHub Sponsors / Buy Me a Coffee

| Component | Real | Fallback | Auto-upgrade trigger |
|-----------|------|----------|----------------------|
| Sponsor buttons | Operator's GH Sponsors + BMC URLs | **Crypto-only CTA** | Edit `docs/guides/crypto-tips.html` to replace `YOUR-USERNAME` in sponsor URLs |

**Fallback details**: Until you enable GH Sponsors / BMC, the tip box only shows
crypto options. When you replace the `YOUR-USERNAME` placeholder in the sponsor
URLs, the buttons appear automatically.

---

## What STILL Requires Operator Action

The agent CANNOT do these for you. They require human identity verification or
account creation. The agent will log these as `pending_request`s until done:

### Critical (agent won't run without)
1. **`GROQ_API_KEY`** (or any LLM API key) — get from https://console.groq.com/keys
2. **`GH_PAT`** (GitHub PAT with `repo` scope) — get from https://github.com/settings/tokens

### High (revenue goes to wrong place)
3. **Replace wallet addresses** in 3 files:
   - `docs/guides/crypto-tips.html`
   - `memory/revenue.md`
   - `revenue.py` (the `WALLETS` dict at top)

### Medium (upgrades from fallback to real revenue stream)
4. **EthicalAds or Carbon Ads** registration (ad revenue)
5. **Affiliate programs** (DigitalOcean, Vultr, Notion, etc.)
6. **GitHub Sponsors** + **Buy Me a Coffee** (direct support)
7. **GoatCounter** (page-level analytics — optional, fallback works fine)
8. **Buttondown** (real newsletter — optional, fallback works fine)

### Low (unlock advanced features)
9. **Google Indexing API** (faster SEO indexing)
10. **Bing URL Submission API**
11. **Reddit API** (auto-posting)
12. **Dev.to API** (cross-posting)

---

## Monitoring Autonomy

The system monitors itself:

| Monitor | Frequency | What it checks | How to view |
|---------|-----------|----------------|-------------|
| `health-check.yml` | Hourly | Site, sitemap, robots, sample tool page reachable | GitHub Issues (auto-created on failure) |
| `loop.yml` | Every 30 min | Agent runs profit loop | Actions tab, `memory/state.md` |
| `daily-seo.yml` | Daily 06:00 UTC | Sitemap refresh + indexing submission | Actions tab |
| `weekly-report.yml` | Monday 09:00 UTC | Full weekly summary | GitHub Issues (auto-created) |
| `first-run.yml` | On push to main | Bootstrap + monetization injection | Actions tab |

**Operator's weekly routine** (5 minutes):
1. Read the auto-created weekly report issue
2. Kill/iterate/scale experiments based on data
3. Optionally upgrade one fallback to a real revenue stream

That's it. The agent handles everything else.

---

## If Something Goes Wrong

### Agent stops running
- Check Actions tab for failed workflows
- Check `memory/blocked.md` for new entries
- Check `memory/provider_health.json` — providers in circuit-breaker state?

### Site goes down
- `health-check.yml` will auto-create an issue labeled `health-check-failed`
- Check GitHub Pages settings (Settings → Pages)
- Verify the latest deploy succeeded

### Revenue not appearing
- Check `memory/revenue.md` — only verified on-chain tips appear
- Run `revenue_verify` for each chain manually via the agent (or a script)
- If wallet addresses are still placeholders, tips go to the original author —
  replace them (see `memory/blocked.md` HIGH section)

### Agent keeps failing validation
- Check `memory/action_log.md` for the validation error
- The agent gets 1 retry with stricter prompt; if that fails, the step is skipped
- If validation keeps failing, the LLM might be downgrading its JSON output —
  try a different provider (set a different LLM API key)

### Want to stop the agent
Three ways (any one works):
1. `touch PAUSE && git add PAUSE && git commit -m "pause" && git push`
2. Set `PAUSE_AGENT=true` as a GitHub secret
3. Open a GitHub issue with the label `agent-pause`

---

## Conclusion

v4.1 is designed to be **autonomous by default**. The operator does the bare
minimum (2 secrets + GitHub Pages), and the agent:

- Auto-configures placeholders
- Auto-regenerates stale sitemaps
- Auto-resets corrupt state
- Uses zero-setup fallbacks for every monetization component
- Self-heals common issues
- Auto-creates issues for failures (health check, weekly report)
- Reminds the operator about manual upgrades (wallets, ad networks, etc.)

The agent will run profitably from day 1 with house ads, mailto newsletter,
GitHub Traffic API analytics, and programmatic SEO. As the operator adds real
monetization services, the agent auto-upgrades each stream — no manual
intervention needed beyond editing config files or adding secrets.

**The only thing the operator MUST do**: replace the wallet addresses. Everything
else is optional.
