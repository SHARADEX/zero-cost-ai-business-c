# Distribution Log — Posts to External Channels

Tracks every post the agent makes to Reddit, Dev.to, Twitter, LinkedIn, Hacker News.

Each entry: `- [YYYY-MM-DD HH:MM:SS UTC] channel/subreddit | title='...' | url=... | status=ok|error|skipped|pending_human`

## Rate Limits (enforced by distribution.py)

| Channel | Rate |
|---------|------|
| reddit (per subreddit) | 1 post / 7 days |
| devto | 1 post / 24 hours |
| twitter | 1 post / 30 minutes |
| linkedin | 1 post / 7 days |
| hackernews | 1 post / 14 days |

## Subreddit Rules (READ BEFORE POSTING)

- /r/webdev — Allows tool showcases; requires self-post with description; no pure link drops
- /r/SideProject — Welcomes new tool launches; self-post preferred
- /r/FreeTools — Designed for free tool sharing; direct links OK
- /r/JavaScript — For JS-specific tools only; high bar for quality
- /r/programming — High bar, no spam; only post genuinely novel tools

## Log

(empty — agent will append on each post)
