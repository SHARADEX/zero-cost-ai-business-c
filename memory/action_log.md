# Action Log (Full Audit Trail)

**Purpose:** Uncapped log of every agent run. Auto-trimmed to last 100 runs when
it exceeds 500KB.
**Format:** Each entry shows timestamp, model, budget, tokens used, steps taken,
and full reasoning.

In v4, each entry also includes **token usage** per step — for cost analysis and
provider performance comparison.

---
## Run 2026-08-10 09:54:46 UTC
**Model:** unknown
**Budget:** full
**Steps taken:** 0
**Tokens used:** 0

**Steps:**


**Run Summary:**
  - Stopped: LLM failed at step 1.
---
## Run 2026-08-10 09:55:14 UTC
**Model:** unknown
**Budget:** full
**Steps taken:** 0
**Tokens used:** 0

**Steps:**


**Run Summary:**
  - Stopped: LLM failed at step 1.
---
## Run 2026-08-10 10:19:25 UTC
**Model:** openrouter
**Budget:** full
**Steps taken:** 1
**Tokens used:** 10655

**Steps:**
  Step 1: action=seo_submit | tokens=10655 | result=SEO submit complete. Google: 0/7 submitted (errors: 1). Bing: 0/7 submitted (errors: 1). URLs added to queue regardless.

**Run Summary:**
  - Step 1: seo_submit (OK) — SEO submit complete. Google: 0/7 submitted (errors: 1). Bing: 0/7 submitted (err
  - Stopped: LLM failed at step 2.
---
