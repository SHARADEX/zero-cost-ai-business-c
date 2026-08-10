# Affiliate Link Inventory

Format for each entry:

```
## ID: <unique-id>
- vendor: <vendor name>
- url: <affiliate link>
- description: <short description for the user>
- category: hosting | vpn | courses | tools | other
- contexts: <comma-separated keywords — page is eligible if it matches any>
```

The `monetize_inject` tool reads this file and matches page keywords to affiliate contexts.
Pages with no matching affiliates skip the affiliate block (no forced links).

---

## ID: digitalocean
- vendor: DigitalOcean
- url: https://m.do.co/c/YOUR_REFERRAL_CODE
- description: $200 free credit for new users. Great for VPS hosting.
- category: hosting
- contexts: hosting, vps, server, deploy, cloud, ssh, docker, kubernetes, droplet

## ID: vultr
- vendor: Vultr
- url: https://www.vultr.com/?ref=YOUR_REFERRAL_CODE
- description: $100 free credit for new users. Global VPS hosting.
- category: hosting
- contexts: hosting, vps, server, deploy, cloud

## ID: notion
- vendor: Notion
- url: https://www.notion.so/?r=YOUR_REFERRAL_CODE
- description: All-in-one workspace. Free for personal use.
- category: tools
- contexts: notes, productivity, workspace, markdown, database, kanban

## ID: vercel
- vendor: Vercel
- url: https://vercel.com/?utm_source=YOUR_REFERRAL_CODE
- description: Deploy frontend apps free. Best-in-class Next.js hosting.
- category: hosting
- contexts: deploy, hosting, nextjs, react, frontend, serverless

## ID: frontendmasters
- vendor: Frontend Masters
- url: https://frontendmasters.com/?utm_source=YOUR_REFERRAL_CODE
- description: Deep, expert-led courses on JavaScript, React, CSS.
- category: courses
- contexts: courses, learning, javascript, react, css, webdev, tutorial

---

## Operator Setup Required

Before any affiliate links go live, the operator MUST:
1. Register for each affiliate program above.
2. Replace `YOUR_REFERRAL_CODE` in each URL with the actual code.
3. Commit the changes.

Until then, `monetize_inject` will inject links with placeholder codes — these still
work structurally but won't earn commission. The agent should write a `pending_request`
every 24 hours until this is done.

## Adding New Affiliates

The agent can add new affiliate entries to this file using `append_doc` (path:
`memory/affiliate_links.md`). However, the URL must come from the operator (the agent
shouldn't make up affiliate URLs — they won't be tracked). Workflow:

1. Agent identifies a contextual affiliate opportunity (e.g., "this regex tester page
   should have a Regex101 affiliate link").
2. Agent writes a `pending_request`: "Operator: please register for Regex101 affiliate
   program and add the URL to memory/affiliate_links.md with contexts: regex, pattern, regular expression".
3. Operator adds the entry.
4. Agent's next `monetize_inject` call picks it up automatically.
