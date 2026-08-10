# Revenue Playbook — v4

This is the concrete money-making strategy the agent follows. It's not "experiment
freely" — it's a 7-stream playbook with daily targets, decision criteria, and
escalation rules.

## The 7 Revenue Streams

### Stream 1: Programmatic SEO Pages

**What**: Generate dozens of long-tail SEO landing pages from templates.

**Why it makes money**: Each page targets a specific search query (e.g., "convert
csv to json"). When someone searches that query and lands on your page, they see
ads (stream 2) and affiliate links (stream 3). The page is a permanent traffic
asset that compounds over time.

**How the agent contributes**:
- Use `templates.py` to generate new converter/calculator/comparison pages
- Target long-tail keywords with low competition but real search volume
- Each page must have: SEO title, meta description, canonical URL, JSON-LD schema,
  internal links to 2-3 related pages, affiliate block, ad zone, tip box

**Targets**:
- Month 1: 100+ pages live (current: 42)
- Month 3: 300+ pages
- Month 6: 500+ pages

**How to measure success**:
- Pages indexed in Google Search Console
- Organic search impressions per page (GoatCounter)
- Organic click-through rate (Search Console)

**Decision criteria**:
- If a page gets 0 impressions in 90 days → KILL (delete or noindex)
- If a page gets 1-10 impressions/day → ITERATE (improve content, add internal links)
- If a page gets 10+ impressions/day → SCALE (build related pages targeting similar keywords)

---

### Stream 2: Ethical Ads (Carbon Ads / EthicalAds)

**What**: Developer-focused ad network embedded on every page.

**Why it makes money**: Carbon Ads and EthicalAds pay per impression (RPM model).
Developer-focused ads pay $0.10-$2 RPM. With 10,000 pageviews/month, that's
$1-20/month passive. With 100,000 pageviews/month, $10-200/month.

**Operator setup required**:
1. Register at https://ethicalads.io (easier approval) or https://carbonads.net
   (higher RPM but stricter approval)
2. Get your publisher ID
3. Replace `data-ea-publisher="zerocostai"` in all HTML files with your real ID
4. Or wait — the agent's `monetize_inject` tool can do this in bulk once you
   provide the publisher ID

**How the agent contributes**:
- Ensure every new page has the ad zone div (the `monetize_inject` tool does this)
- Monitor for ad blocker impact (track GoatCounter pageviews vs ad impressions — if
  ratio is too high, the ad code might be broken)
- A/B test ad placement (above content vs sidebar) — log as experiment

**Targets**:
- Month 1: Ad zone on every page, account registered, $0 (no traffic yet)
- Month 3: $5-20/month from ads
- Month 6: $20-100/month from ads

---

### Stream 3: Affiliate Links

**What**: Contextual affiliate links on every page where relevant.

**Why it makes money**: When a visitor clicks an affiliate link and signs up for
the recommended service, we earn a commission. Typical commissions:
- DigitalOcean: $25 per new user
- Vultr: $10-50 per new user
- Notion: 50% of first year's subscription
- Frontend Masters: 15-30% of subscription

Conversion rate is 1-3% CTR × 5-20% conversion = 0.05-0.6% of visitors become
paid signups. With 1,000 relevant visitors/month, that's 0.5-6 signups.

**Operator setup required**:
1. Register for each affiliate program
2. Get your referral code
3. Update `memory/affiliate_links.md` — replace `` placeholders
   with real codes
4. The `monetize_inject` tool will auto-inject the links into relevant pages

**How the agent contributes**:
- Identify new contextual affiliate opportunities (e.g., "regex tester page should
  have a Regex101 affiliate link") and log `pending_request` for the operator to add
- Ensure every page has 1-3 contextual affiliate links via `monetize_inject`
- A/B test CTA copy ("Learn more" vs "Try free" vs "Get $200 credit")

**Targets**:
- Month 1: 5 affiliate partners configured, links injected on relevant pages
- Month 3: First affiliate commission (even $5 is a win)
- Month 6: $50-200/month from affiliates

---

### Stream 4: Crypto Tips

**What**: Direct crypto donations via on-chain tip jar.

**Why it makes money**: Some users prefer to tip in crypto. It's lower-friction
than you'd think — many developers already have a wallet. Average tip is $2-10.

**Operator setup required**:
1. Generate wallet addresses for BTC, ETH, SOL, TRON (and optionally Ronin)
2. **IMPORTANT**: Use dedicated receive-only wallets. Never reuse wallets you
   use for other purposes. The addresses will be public.
3. Update `docs/guides/crypto-tips.html` and `memory/revenue.md` and `revenue.py`
   with your addresses

**How the agent contributes**:
- Verify tips on-chain daily via `revenue_verify(chain)` (rotate through chains)
- Log verified tips to `memory/revenue.md` via the `revenue_update` field
- A/B test tip box placement (above fold vs below, large vs small)

**Targets**:
- Month 1: 1 verified tip (any amount)
- Month 3: 1-2 verified tips per week
- Month 6: $10-50/month from tips

**Critical rule**: NEVER log unverified revenue. Only `revenue_verify` confirms a
tip — agent's "I think someone tipped" doesn't count.

---

### Stream 5: GitHub Sponsors / Buy Me a Coffee

**What**: Lower-friction donation options via credit card.

**Why it makes money**: Many users want to support but don't have crypto. GH
Sponsors and BMC let them tip $3-25 with a credit card. BMC also supports
recurring monthly donations.

**Operator setup required**:
1. Enable GitHub Sponsors at https://github.com/sponsors/YOUR-USERNAME
2. Register at https://buymeacoffee.com
3. Update `docs/guides/crypto-tips.html` — replace `YOUR-USERNAME` in the GH
   Sponsors URL and BMC URL with your real usernames

**How the agent contributes**:
- Ensure every page has a clear CTA to the tip page (already done in templates)
- Test whether "GitHub Sponsors" CTA outperforms "Crypto tip" CTA (log as A/B test)

**Targets**:
- Month 1: Both accounts set up, CTAs live
- Month 3: 1-2 sponsors or BMC supporters
- Month 6: $10-50/month from sponsors

---

### Stream 6: Newsletter

**What**: Email newsletter signup form on every page.

**Why it makes money**: The newsletter itself doesn't directly earn — but it
builds an audience asset. Once you have 100+ subscribers, you can:
- Sell sponsorships ($50-200 per send)
- Promote affiliate products to a warm audience
- Drive recurring traffic to new content

**Operator setup required**:
1. Create a newsletter at https://buttondown.com (free up to 100 subscribers)
2. Get your newsletter slug
3. Update `skip` in all HTML files (the newsletter form action URL)

**How the agent contributes**:
- Ensure every page has the newsletter form (via `monetize_inject`)
- Send weekly newsletters (manually for now — agent writes content, operator sends)
- A/B test form placement (header vs sidebar vs footer)

**Targets**:
- Month 1: Form on every page, 5-10 subscribers
- Month 3: 50-100 subscribers, first sponsor inquiry
- Month 6: 200-500 subscribers, $50-200/sponsorship

---

### Stream 7: Sponsored Tool Placements (Future)

**What**: Paid featured listings on the tools page.

**Why it makes money**: Once you have meaningful traffic (5,000+ pageviews/month
on the tools page), tool vendors will pay $50-500/month to be featured at the top.

**Status**: NOT YET ACTIVE. Don't pursue this until streams 1-6 are producing.
The agent should NOT log pending_requests for this — it's premature.

**When to activate**: After month 6, if streams 1-3 are producing $100+/month
combined.

**Targets**:
- Month 6+: First sponsored placement ($50-200/month)
- Month 12: 2-3 sponsored placements ($200-1000/month)

---

## Daily Targets by Month

| Metric | Month 1 | Month 3 | Month 6 |
|--------|---------|---------|---------|
| Pages live | 100+ | 300+ | 500+ |
| Search impressions/day | 50+ | 500+ | 5,000+ |
| Pageviews/day | 20+ | 200+ | 2,000+ |
| Affiliate clicks/day | 1+ | 5+ | 25+ |
| Newsletter subscribers | 10+ | 100+ | 500+ |
| Verified tips/month | 1+ | 4-8 | 10-20 |
| Total revenue/month | $0-5 | $20-100 | $200-1000 |

## Weekly Review

Every Monday, the **weekly-report.yml** workflow creates a GitHub issue with:
- Revenue (verified on-chain)
- Budget usage (tokens + requests per provider)
- Recent state (last 2-3 run summaries)
- Active experiments (and their decisions)
- Recent distribution posts
- Analytics snapshot

The operator should review this and:
- Kill experiments that have run their course
- Double down on what's working
- Add new experiments based on data

## Escalation Rules

If the agent detects any of these conditions, it should write a `pending_request`
with the appropriate priority:

- **[URGENT]** Site is down (health check failed)
- **[URGENT]** All LLM providers failing for >1 hour
- **[HIGH]** Revenue verification showing balance but no logged transactions
  (means tips are coming in but not being recorded)
- **[HIGH]** Budget exhausted before noon UTC (means usage is bursty —
  investigate which experiment is consuming)
- **[MEDIUM]** 30+ pages pending SEO submission (means indexing API not
  configured or failing)
- **[MEDIUM]** Affiliate links have placeholder codes (means operator hasn't
  registered yet)
- **[LOW]** Newsletter form has placeholder slug
- **[LOW]** No new content in 24 hours (means agent is stuck)

## Anti-Patterns to Avoid

The agent should NEVER:

1. **Generate pages with no SEO value.** Every page must target a real search query.
2. **Spam distribution channels.** Reddit especially — getting banned destroys long-term value.
3. **Log unverified revenue.** Only on-chain confirmed transactions count.
4. **Pursue stream 7 (sponsored) prematurely.** It's a future state.
5. **Bypass rate limits in distribution.py.** They exist for a reason.
6. **Create duplicate or near-duplicate pages.** Google penalizes thin content.
7. **Use black-hat SEO tactics** (link farms, comment spam, keyword stuffing).
8. **Ignore the kill switch.** If PAUSE is set, the agent skips. Period.
9. **Modify prompts/ or .github/ files.** Those are operator-controlled.
10. **Include private keys or secrets** in any file or memory entry.

## The Bottom Line

v3's revenue: $0.06 over months.

v4's target: $20-100/month by month 3, $200-1000/month by month 6.

The difference is:
- **7 streams vs 1**
- **Programmatic SEO (100s of pages) vs 8 hand-built tools**
- **Real on-chain verification vs trust-the-agent**
- **Distribution automation vs build-it-and-they-will-come**
- **Concrete playbook vs "experiment freely"**

If the agent follows this playbook and the operator sets up the pending items in
`memory/blocked.md`, v4 should produce real revenue within 3-6 months.
