---
name: rem-sleep
description: Process conversation transcripts and store important information into the memory skill tree. Run at end of session or after significant work.
metadata:
  trigger: "Use when: /rem-sleep, end of a work session, after a call, after building a site, after any client interaction"
---

# REM Sleep

You are a background memory processor. Your job is to read the conversation transcript and extract everything worth remembering into the memory skill tree at `~/.claude/skills/memory/`.

## When to Run

- After building or updating a client site
- After a sales call (real or test)
- After receiving client feedback
- After discovering a design technique that worked or failed
- After any pricing discussion or negotiation
- At the end of any substantial work session
- When the user says "/rem-sleep" or "save this to memory"

## What to Extract

### From Site Builds
- Client name, industry, location → `memory/clients/{name}/profile.md`
- What was built, tech stack, design choices → `memory/clients/{name}/site.md`
- GSD UI audit scores → `memory/clients/{name}/site.md`
- What the critic flagged, what was fixed → `memory/techniques/`
- Color palette + industry pairing → `memory/designs/color-palettes/`
- Layout decisions that scored well → `memory/designs/layouts/`
- Components that worked → `memory/designs/components/`

### From Calls
- What was said, how they reacted → `memory/clients/{name}/calls.md`
- Objections encountered + responses used → `memory/objections/`
- If the call succeeded → `memory/calls/successful/`
- If the call failed → `memory/calls/failed/`
- Callbacks scheduled → `memory/calls/callbacks/`

### From Deals
- Price quoted, reaction, outcome → `memory/pricing/`
- Closed deal details → `memory/wins/`
- Lost deal details + reason → `memory/losses/`
- Upsells attempted + result → `memory/clients/{name}/deal.md`

### From Techniques
- Design approach that got high audit scores → `memory/techniques/that-worked/`
- Design approach that scored poorly → `memory/techniques/that-failed/`
- Sales technique that converted → `memory/techniques/that-worked/`
- Sales technique that flopped → `memory/techniques/that-failed/`

## How to Process

1. Read the full conversation/transcript
2. Identify each extractable item (client info, technique, objection, etc.)
3. Check if a memory file already exists for this topic
4. If yes: UPDATE the existing file with new info (append, don't overwrite)
5. If no: CREATE a new file following the memory format
6. Use the format from the memory SKILL.md (date, category, what happened, takeaway)
7. Cross-reference related memories

## Output

After processing, report:
```
REM SLEEP COMPLETE
- Created: [list of new files]
- Updated: [list of updated files]
- Skipped: [anything not worth storing and why]
```

## Rules

- Don't store API keys, passwords, or payment details
- Don't store exact conversation transcripts (summarize instead)
- DO store specific phrases that worked in sales contexts
- DO store exact objection wording (helps train the calling agent)
- DO store specific design decisions with reasoning
- Keep each file under 200 lines. Split if needed.

## Feedback Loop Updates (MANDATORY after audited builds)

After any site build that was audited by GSD:
1. Check which techniques from `memory/techniques/` were applied
2. For each technique used:
   - Compare the relevant pillar score against the technique's historical average
   - Append to `## Used In` with: client name, date, pillar score, delta, ✅ or ❌
   - If score improved or held: increment Confidence by 1
   - If score dropped: don't increment, add note explaining what differed
   - If new industry/context: add to `## Contexts Tested`
   - Update `**Last Used:**` date
3. If a technique was recalled but NOT applied, note why in the technique file
4. If a NEW technique was discovered during this build, create a new entry in `that-worked/` or `that-failed/`
