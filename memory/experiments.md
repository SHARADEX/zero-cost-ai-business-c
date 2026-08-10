# Experiments Log

**Purpose:** Track A/B tests, content experiments, and revenue strategy results.
**Rule:** Every experiment must have a hypothesis, a result, and a decision (kill/iterate/scale).
**Auto-capped to last 40 entries.**

## Experiment Types

- `standard` — general experiment
- `ab_test` — A/B test with control + variant
- `seo` — SEO experiment (page count, keyword targeting, internal linking)
- `revenue` — revenue stream experiment (ad placement, CTA copy, affiliate angle)

## Template

```
[YYYY-MM-DD HH:MM UTC]
TYPE: <standard|ab_test|seo|revenue>
HYPOTHESIS: ...
SETUP: ...
PREDICTION: ...
DECISION_DATE: YYYY-MM-DD
STATUS: RUNNING
RESULT: (pending)
DECISION: (pending)
```

The agent uses `log_experiment` to start a new experiment and `update_experiment`
to record the result.

---

## Initial Experiments to Queue (suggested for first run)

These are hypotheses the agent should consider logging as experiments:

1. **seo**: Adding 100 long-tail converter pages increases organic search traffic by 500% in 90 days.
2. **ab_test**: Placing the tip box above the fold (vs below) increases tip CTR by 30%.
3. **ab_test**: "GitHub Sponsors" CTA outperforms "Crypto tip" CTA by 2x in non-crypto audiences.
4. **revenue**: Carbon Ads placement above content earns more RPM than sidebar placement.
5. **seo**: Cross-linking between converters (e.g., csv-to-json → json-to-csv) reduces bounce rate by 15%.
