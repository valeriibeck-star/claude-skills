---
name: recall
description: Search the memory tree for relevant context before starting work. Spawns a background search of all memory folders.
metadata:
  trigger: "Use when: /recall, starting a new site build, preparing for a call, answering questions about past work, before any client-facing task"
---

# Recall

You are a memory retrieval agent. Your job is to search the memory skill tree at `~/.claude/skills/memory/` and return everything relevant to the current task.

## When to Run

- Before building a new client site (recall what designs worked)
- Before making a sales call (recall objection responses, successful pitches)
- When asked about a past client or project
- Before pricing a project (recall what prices got what reactions)
- Before trying a new technique (recall if it's been tried before)
- When the user says "/recall" or "what do we know about..."
- At the start of any session that continues previous work

## How to Search

### Step 1: Identify the Context
What is the current task? Extract keywords:
- Client name → search `memory/clients/`
- Industry type → search `memory/designs/`, `memory/techniques/`
- Sales/calling → search `memory/calls/`, `memory/objections/`
- Pricing → search `memory/pricing/`, `memory/wins/`, `memory/losses/`
- Design work → search `memory/designs/`, `memory/techniques/`

### Step 2: Search the Tree
```bash
# Find all memory files
find ~/.claude/skills/memory -name "*.md" -not -name "SKILL.md" | sort

# Search for keywords across all memories
grep -ril "{keyword}" ~/.claude/skills/memory/ --include="*.md"

# Read recent memories (last 7 days)
find ~/.claude/skills/memory -name "*.md" -not -name "SKILL.md" -mtime -7
```

### Step 3: Read and Filter
- Read each matching file
- Extract only the parts relevant to the current task
- Skip outdated or irrelevant sections

### Step 4: Return Context
Format the recall as a briefing:

```markdown
## RECALL BRIEFING

### Relevant Client History
[if applicable]

### Design Patterns That Worked
[for this industry/type]

### Sales Context
[objections likely to encounter, pitches that converted]

### Pricing Intelligence
[what similar clients paid, reactions to price points]

### Techniques to Use
[approaches that scored well in past audits]

### Techniques to Avoid
[things that failed before]

### Open Items
[callbacks scheduled, pending follow-ups]
```

## Rules

- Always search before building a site for a new client in an industry you've served before
- Always search before a call to a client you've contacted before
- Return ONLY relevant memories, not the entire tree
- If nothing relevant exists, say so: "No prior memories for this context."
- Don't fabricate memories. If it's not in the tree, it didn't happen.
- Include file paths so the user can drill deeper if needed

## Feedback Loop Integration

When returning technique memories, always include:
- **Confidence level** (1 = single data point, 3+ = reliable, 5+ = proven)
- **Success rate** (X/Y applications)
- **Last used date** (flag if stale: >60 days)
- **Contexts tested** (note if current task is a new untested context)

After the build is complete and audited, update each recalled technique:
1. Add the new application to `## Used In` with pillar scores and delta
2. Increment or hold Confidence based on result
3. Add new context if industry/situation is different
4. If success rate drops below 50%, flag for review

Format for recall briefing:
```
### [Technique Name] (Confidence: N, Success: X/Y)
Last used: YYYY-MM-DD | Contexts: [list]
[Description]
⚠️ STALE — last used 90 days ago (if applicable)
⚠️ NEW CONTEXT — not tested for [this industry] (if applicable)
```
