---
name: memory
description: Long-term memory storage for the website redesign business. Organized as a branching folder tree. Go deeper for more specific context.
metadata:
  trigger: Always loaded. This is persistent memory across all sessions.
---

# Memory

This skill IS your long-term memory. Every folder is a category. Every file is a memory. Go deeper for specifics.

## Structure

```
memory/
├── clients/              # One folder per client
│   └── {client-name}/
│       ├── profile.md    # Business info, contact, status
│       ├── site.md       # What was built, versions, scores
│       ├── calls.md      # Call log, what was said, outcome
│       └── deal.md       # Price, payment status, upsells
├── designs/
│   ├── color-palettes/   # What palettes work for which industries
│   ├── layouts/          # Layout patterns that convert
│   └── components/       # Components that got positive reactions
├── calls/
│   ├── successful/       # Calls that led to sales — what worked
│   ├── failed/           # Calls that bombed — what went wrong
│   └── callbacks/        # Scheduled callbacks with context
├── objections/           # Every objection heard + best response
├── wins/                 # Closed deals — full story
├── losses/               # Lost deals — why, what to change
├── techniques/
│   ├── that-worked/      # Design/sales techniques with positive results
│   └── that-failed/      # Things tried that didn't work
└── pricing/              # Price points tested, reactions, conversion data
```

## Rules

1. **One memory per file.** Don't dump everything in one doc.
2. **Name files descriptively.** `titan-plumbing-first-call.md` not `call1.md`.
3. **Include dates.** Every memory gets a date stamp.
4. **Include outcome.** Every memory ends with what happened as a result.
5. **Be honest.** Log failures as clearly as successes. That's how you learn.
6. **Cross-reference.** If a call memory relates to a client, note the client folder path.

## How to Write a Memory

```markdown
# [Title]
**Date:** YYYY-MM-DD
**Category:** [client | design | call | objection | technique | pricing]
**Related:** [path to related memories]

## What Happened
[The facts]

## What Worked / What Failed
[Analysis]

## Takeaway
[One sentence lesson]
```
