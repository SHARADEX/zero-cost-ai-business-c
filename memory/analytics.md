# Analytics & Metrics

**Purpose:** Track traffic, conversions, and revenue-adjacent metrics.
**Auto-capped to last 80 entries.**

## How to Measure (Zero-Cost Methods)

- **Page views / visitors**: GoatCounter (free, privacy-respecting, no cookies)
  - Requires GC_API_TOKEN + GC_SITE_ID env vars
  - Script tag embedded on every page
- **GitHub repo stars**: `https://api.github.com/repos/{owner}/{repo}` → `stargazers_count`
- **Wallet balances**: see revenue.md for free API endpoints
- **Tool usage**: GoatCounter events (outbound_click, tip_cta_click)
- **Search Console**: Manual check at search.google.com/search-console

## Current Metrics (initial)

- Stars: 0 (repo not yet public)
- Total page views: 0 (GoatCounter not yet configured)
- Tip conversion rate: N/A (no traffic yet)
- Affiliate clicks: 0
- Newsletter subscribers: 0

## A/B Test Tracking

When the agent runs an A/B test, log the variant and metric here. The GoatCounter
event tracking (in main.js) records outbound_click and tip_cta_click events —
these are the primary conversion signals.

---

(empty — agent will append metric events here)
