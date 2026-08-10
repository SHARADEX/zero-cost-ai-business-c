# Design Decisions — v4

This document explains *why* v4 is built the way it is, and the trade-offs made.

## Core Philosophy

**v4 is a profit-engineering agent, not an experiment-bot.**

v3's prompt said "experiment freely, kill what doesn't work, double down on what
does." That's a methodology, not a strategy. Without a concrete playbook, the agent
wandered — building random tools, writing random blog posts, never advancing a
coherent revenue plan.

v4 has a **concrete 7-stream revenue playbook** (see REVENUE_PLAYBOOK.md). Every
action the agent takes must advance at least one stream. If an action advances
zero streams, the agent doesn't take it.

## The 7-Stream Revenue Model — Why?

A common mistake in zero-cost side projects is betting on a single revenue stream.
v3 bet on crypto tips. Result: $0.06 total over months of running.

The math: a free tools site with no traffic asking for crypto tips has a conversion
rate of approximately 0.01% (1 in 10,000 visitors) and an average tip of $2. To
make $100/month, you'd need 50,000 visitors/month. That's not impossible, but it's
a single point of failure.

v4 diversifies across 7 streams. Each has different unit economics:

| Stream | Conversion | Average revenue per conversion | Requires |
|--------|-----------|---------------------------------|----------|
| Programmatic SEO | N/A (passive) | $0.10-2 RPM × pageviews | Many long-tail pages |
| Ethical ads | N/A (passive) | $0.10-2 RPM × pageviews | Site traffic |
| Affiliate | 1-3% CTR × 5-20% conversion | $5-100 per signup | Contextual links |
| Crypto tips | 0.01% | $2-10 | Goodwill + crypto literacy |
| GH Sponsors / BMC | 0.05% | $3-25 monthly | Goodwill + credit card |
| Newsletter | 2-5% signup | $0 (deferred) | Email capture |
| Sponsored | N/A | $50-500 per placement | Significant traffic |

The key insight: **streams 1-3 scale with traffic**. Streams 4-5 require visitor
intent to support. Stream 6 builds an audience asset. Stream 7 only activates
after streams 1-6 produce.

By running all 7 in parallel, the agent maximizes revenue per visitor regardless
of the visitor's intent.

## Why Programmatic SEO?

v3 had 8 tool pages and asked the agent to "build more tools." That's slow — each
tool is custom code, takes a full run, and only targets one search query.

v4 ships **template-based programmatic SEO**. The agent can generate dozens of
"X to Y converter" pages per run from the `templates.py` module. Each page targets
a specific long-tail search query ("convert csv to json", "convert yaml to json",
etc.) and earns ad impressions + affiliate clicks passively forever.

The seed ships with 12 converter pages and 6 calculator pages. The agent's job is
to expand this to 100+ over the first month, then keep going.

## Why Strict Output Validation?

v3's parser silently fell back to `list_dir` whenever the agent's JSON was
malformed. This caused two problems:

1. **Silent failures.** The agent thought it was doing useful work (listing dirs)
   when in reality it was stuck in a parsing loop. The operator saw "Step 1: list_dir"
   in every log entry with no explanation.

2. **No pressure on the LLM to be correct.** When failures are silent, there's no
   incentive to fix the root cause. The LLM kept emitting prose before JSON, knowing
   the parser would cope.

v4 enforces strict JSON schema validation:
- Parse fails → return the error to the LLM as a retry prompt (1 retry allowed)
- Retry fails → abort the step (logged to `memory/blocked.md`)
- No silent fallback to `list_dir`

This forces the LLM to either produce correct output or fail loudly. Both outcomes
are visible to the operator.

## Why On-Chain Revenue Verification?

v3's `memory/revenue.md` logged "$0.06 (carried over from prior experiment)" —
but there was no code that actually verified any tip on-chain. The agent was *told*
to verify but had no tool to do so. So it didn't.

v4 ships `revenue.py` with real implementations:
- **Bitcoin**: `blockchain.info/q/addressbalance/<addr>` returns satoshis (free, no key)
- **Ethereum**: `api.etherscan.io/api?module=account&action=balance&address=<addr>` (free, no key)
- **Solana**: `api.mainnet-beta.solana.com` JSON-RPC `getBalance` (free)
- **Tron**: `api.trongrid.io/v1/accounts/<addr>` (free)
- **Ronin**: skipped (no free public API; manual check)

The agent calls `revenue_verify(chain)` and the module:
1. Fetches current balance
2. Compares to last logged balance (stored in `revenue_ledger.json`)
3. Returns delta (in native units + USD)
4. Updates the ledger

Only when delta > 0 does the agent emit a `revenue_update` field, which gets
appended to `memory/revenue.md` as a verified transaction.

This means **revenue in v4 is real, on-chain, verified** — not a number the agent
made up.

## Why Provider Health Circuit Breakers?

v3 retried failed providers up to 2 times per model. If a provider was completely
down (e.g., Groq having an outage), every run burned 2 retries × every model × every
step before falling back to the next provider.

v4 tracks per-provider failure count over a 1-hour window. If a provider fails
≥3 times in the last hour, `is_provider_healthy()` returns False and the provider
is skipped entirely until the window clears.

This means a 1-hour Groq outage costs ~0 LLM calls instead of ~2 × N_models × N_steps
wasted calls.

## Why Hourly Pacing?

v3 ran every 30 minutes (48 runs/day) with up to 5 steps each = max 240 calls/day.
The total daily budget across providers was 18,550 — so budget was "plentiful."

But that's the wrong frame. The issue isn't running out — it's **bursting**. If
the agent runs 5 steps × 5 calls per step at 3am, it might burn 25 calls in 2
minutes, while the rest of the day's 47 runs get nothing.

v4 enforces a 15% hourly cap: never burn more than 15% of daily budget in any
1-hour window. This spreads usage evenly across the day, so the agent is always
available, not just at 3am.

## Why Token-Aware Budgeting?

v3 tracked only request counts. But providers throttle on tokens too — especially
Gemini (1M tokens/day free tier) and Groq (500K tokens/day).

v4 tracks both. The `get_budget_level()` function uses the more constrained
dimension (`min(req_pct, tok_pct)`) to decide budget level. This prevents the
agent from running out of tokens while still having requests left (or vice versa).

## Why Atomic Writes for budget.json?

v3 wrote `memory/budget.md` directly. If the agent crashed mid-write (e.g., GitHub
Actions timeout), the file would be truncated or empty. Next run would see an
empty budget, think it was a new day, reset all counts to 0, and burn through
budget again — potentially 2x or 3x the daily limit.

v4's `_write_json_atomic()` writes to a temp file first, then `os.replace()`s
into place. `os.replace()` is atomic on POSIX — either the new file is fully in
place, or the old file is still there. No partial writes.

## Why Multi-Modal Kill Switch?

v3 had one kill switch: `PAUSE` file in repo root. To activate it, the operator
had to `git push` a file. Then wait up to 30 minutes for the next cron run.
That's slow if the agent is doing something destructive.

v4 has three kill switches, all checked at run start:
1. **PAUSE file** — same as v3
2. **PAUSE_AGENT env var** — set as GitHub secret, takes effect immediately on
   next run (no commit needed)
3. **GitHub issue labeled `agent-pause`** — open an issue with this label, agent
   skips runs until it's closed

The GitHub issue approach is the fastest for non-technical operators — they can
pause the agent from the GitHub UI without touching code.

## Why Not More LLM Providers?

v3 had 7 providers. v4 keeps the same 7. Adding more (e.g., Together AI, Mistral,
Cohere trial) is tempting but:
- Each provider adds maintenance burden (model discovery, API quirks, error handling)
- The 7 we have cover ~18,550 requests/day — more than enough for 30-min runs
- More providers = more secrets to manage = more attack surface

7 is the sweet spot. If one provider drops their free tier, we add a replacement
then.

## Why No Database?

This is a **zero-cost** system. Databases cost money (or require setup beyond
GitHub's free tier). All state lives in markdown and JSON files in `memory/`.

Trade-offs:
- ✅ Zero cost, zero setup, zero maintenance
- ✅ Human-readable (operator can `cat memory/state.md` to see what's happening)
- ✅ Version-controlled (every state change is a git commit)
- ❌ No concurrent writes (only one agent run at a time — enforced via `concurrency: group` in workflow)
- ❌ No queries (the agent reads entire files into context)

The concurrency limitation is fine because the agent runs every 30 min and each
run takes 1-5 minutes. Overlap is rare.

## Why No Backend / API?

Same reason: zero-cost. A backend requires:
- A server (costs money, even on free tiers — Vercel/Render free tiers have limits)
- Authentication (more code, more attack surface)
- Database (see above)

By shipping only static HTML on GitHub Pages, we get:
- ✅ Zero cost, zero maintenance
- ✅ Infinite scale (GitHub handles it)
- ✅ No security patches needed
- ❌ No user accounts, no server-side processing, no API

The trade-off is significant: we can't offer paid API access, user-specific
features, or dynamic content. But for a zero-cost side project, this is the
right trade-off. The 7 revenue streams we have all work with static HTML.

## Why GoatCounter (not Google Analytics)?

- **Privacy**: GoatCounter is cookieless. No GDPR consent banner needed.
- **Cost**: Free for small sites (under 100k pageviews/month)
- **Simplicity**: One script tag, no consent mode v2 setup
- **Ethics**: Aligns with the "ethical ads" positioning of the site

Google Analytics 4 is free but requires cookie consent, has a steeper learning
curve, and the data goes to Google. GoatCounter keeps data ownership with us.

## Why Not Make the Agent Smarter (more LLM calls per run)?

v3's max was 5 steps per run. v4 keeps the same max. The temptation is to allow
10-20 steps for "more work per run" — but that:
- Burns budget faster (less pacing)
- Increases the chance of the agent going off-rails (longer context = more drift)
- Doesn't actually do more useful work (the agent can do 5 meaningful things in 5 steps)

5 steps × 48 runs/day = 240 actions/day. That's plenty.

## What Didn't Make It Into v4

- **Email digest of weekly report**: Could use a free service like Buttondown's
  broadcast feature, but adds complexity. The weekly GitHub issue is enough.
- **A/B test infrastructure with deterministic traffic splitting**: Would require
  server-side rendering or JS-based variant selection. Marked as future work.
- **Multi-language support (i18n)**: Would 2x the page count, but only after
  English traffic justifies it.
- **Paid API tier for popular tools**: Requires a backend. Out of scope for
  zero-cost.
- **Browser extension distribution**: Different beast entirely. Skip.

These are deliberate omissions, not oversights. Each would add complexity without
proportional revenue impact at v4's scale.

## Conclusion

v4 is a **profit-engineering system**, not a research project. Every design
decision serves the goal of "actually generating money at zero cost." The
7-stream playbook, strict validation, on-chain verification, and programmatic
SEO are all in service of that goal.

If you're forking this, the most important things to keep are:
1. The 7-stream playbook (don't reduce it to 1-2 streams)
2. Strict output validation (don't go back to silent fallbacks)
3. On-chain revenue verification (don't trust the agent's claims)
4. Programmatic SEO templates (don't go back to 1-page-at-a-time)

Everything else is customizable.
