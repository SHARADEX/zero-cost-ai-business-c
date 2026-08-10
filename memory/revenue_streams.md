# Revenue Streams Status — v4

Tracks each of the 7 parallel revenue streams. Agent reviews this every run to decide
which stream needs attention.

| # | Stream | Status | Target (Month 1) | Current | Next Action |
|---|--------|--------|------------------|---------|-------------|
| 1 | Programmatic SEO pages | Active | 100+ pages live | 42 (initial seed) | Add 10 converters + 10 calculators per run until 200+ |
| 2 | Ethical ads (Carbon/EthicalAds) | Pending operator signup | $0.10–$2 RPM | $0 | Operator must register at ethicalads.io or carbonads.net |
| 3 | Affiliate links | Pending operator signup | 5+ affiliate partners | 0 | Operator must register for: DigitalOcean, Vultr, Notion, etc. |
| 4 | Crypto tips | Active | 1 verified tip/week | $0 | Verify weekly via revenue_verify tool |
| 5 | GitHub Sponsors / BMC | Pending operator signup | 2 sponsors/month | $0 | Operator must enable GH Sponsors + Buy Me a Coffee |
| 6 | Newsletter (Buttondown) | Pending operator signup | 50 subscribers/month | 0 | Operator must create newsletter, replace skip |
| 7 | Sponsored tool placements | Future | (after streams 1–6 produce) | $0 | Not yet — too early |

## Notes

- Streams marked "Pending operator signup" require human action. The agent should
  write a `pending_request` for each that hasn't been set up, every 24 hours, until done.
- Stream 1 (programmatic SEO) is the highest leverage right now — each page is a
  permanent traffic asset that compounds. The agent should generate as many as possible.
- Stream 7 is intentionally deferred. Don't pursue sponsored placements until organic
  traffic justifies it.
