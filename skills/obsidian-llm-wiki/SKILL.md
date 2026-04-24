---
name: obsidian-llm-wiki
description: >
  Build and maintain an LLM-powered second brain in Obsidian using Andrej Karpathy's LLM Wiki
  pattern. Run Claude Code inside the vault to process raw sources into a structured, cross-referenced
  wiki. Use when setting up an AI-maintained knowledge base, ingesting articles/transcripts/notes,
  writing daily journals, clearing an inbox, finding orphan notes (brain-dump), querying the wiki,
  or running a health check (lint). Tracks projects, meetings, content, revenue, and fitness.
---

# Obsidian LLM Wiki

An implementation of Andrej Karpathy's LLM Wiki pattern: instead of retrieval on every query, Claude
**compiles** raw sources into a persistent, cross-referenced markdown wiki. You curate; Claude
maintains everything. Knowledge compounds.

## Core Insight

Traditional RAG re-searches raw documents on every query. The LLM Wiki shifts to **compilation**:
- Raw sources (articles, transcripts, screenshots, URLs) → ingested once
- Claude writes and cross-links wiki pages → synthesis already exists
- Queries hit the compiled wiki → instant, cited answers
- Humans supply sources and ask questions; Claude handles all bookkeeping

## Three-Layer Architecture

```
raw/          ← Layer 1: Immutable source material. Never modified by Claude.
wiki/         ← Layer 2: LLM-owned. Claude creates, edits, cross-references.
CLAUDE.md     ← Layer 3: Schema/config. Governs how Claude maintains the wiki.
```

---

## Invocation

Run `/obsidian-llm-wiki` followed by an operation:

| Command | What it does |
|---------|-------------|
| `setup` | Initialize vault structure and write CLAUDE.md |
| `ingest [url\|path\|text]` | Process a source into the wiki |
| `daily-journal` | Create or update today's daily note |
| `inbox` | Classify and integrate all inbox/ notes |
| `brain-dump` | Find orphan notes, fill gaps, surface stale content |
| `query [question]` | Answer from the wiki with citations |
| `lint` | Health check: broken links, contradictions, stale claims |

---

## Operation: setup

When the user runs `/obsidian-llm-wiki setup`:

1. **Ask for vault path** if not already running inside one. Default: `~/Documents/Vault/`.
2. **Create the directory structure**:

```
{vault}/
├── raw/                    # Source inbox — drop anything here
│   ├── articles/
│   ├── transcripts/
│   ├── screenshots/
│   └── assets/
├── inbox/                  # Fleeting thoughts, quick captures
├── wiki/                   # LLM-generated and maintained
│   ├── sources/            # One page per ingested source
│   ├── people/             # Contacts, collaborators, relationships
│   ├── concepts/           # Ideas, frameworks, mental models
│   ├── projects/           # Active and archived projects
│   ├── meetings/           # Meeting notes and decisions
│   ├── content/            # Content created: posts, videos, writing
│   ├── revenue/            # Deals, invoices, financial milestones
│   ├── fitness/            # Workouts, health metrics, sleep
│   ├── synthesis/          # Comparisons, deep-dives, analyses
│   ├── index.md            # Master catalog — one line per page
│   └── log.md              # Chronological operation log
├── output/                 # Generated reports, exports
├── daily/                  # Daily notes (YYYY-MM-DD.md)
├── templates/              # Note templates
└── CLAUDE.md               # Governs how Claude works here
```

3. **Write `CLAUDE.md`** in the vault root (see template below).
4. **Write starter `wiki/index.md`** and **`wiki/log.md`**.
5. **Write all templates** in `templates/`.
6. **Confirm** with a summary of what was created.

### CLAUDE.md to write into the vault (verbatim)

```markdown
# Wiki Maintainer Instructions

You are the maintainer of this Obsidian knowledge base. Your job is to compile raw sources into a
structured, cross-referenced wiki. Humans supply sources and ask questions; you handle all bookkeeping
and synthesis.

## Hard Rules

- **Never modify `raw/`** — it is immutable source material.
- **Always update `wiki/index.md`** when you create or significantly change a wiki page.
- **Always append to `wiki/log.md`** after every operation (timestamp + what changed).
- **Use wikilinks** `[[Page Name]]` for all internal cross-references.
- **Frontmatter** every wiki page with: `type`, `created`, `updated`, `tags`, `sources`.
- One page per entity (person, concept, project). Merge, don't duplicate.
- When uncertain about a claim, mark it `> [!question] Unverified:` callout.

## Page Types

| Type | Folder | Purpose |
|------|--------|---------|
| source | wiki/sources/ | Summary of one ingested item |
| person | wiki/people/ | Individual contact or figure |
| concept | wiki/concepts/ | Idea, framework, mental model |
| project | wiki/projects/ | Active or archived project |
| meeting | wiki/meetings/ | Meeting record + decisions |
| content | wiki/content/ | Published or drafted content |
| revenue | wiki/revenue/ | Deal, invoice, financial milestone |
| fitness | wiki/fitness/ | Workout, metric, health record |
| synthesis | wiki/synthesis/ | Cross-source analysis |

## Frontmatter Schema

```yaml
---
type: concept
title: "Page Title"
created: 2026-01-01
updated: 2026-01-01
tags: []
sources: []
related: []
status: active   # active | archived | stub
---
```

## wiki/index.md Format

One line per page:
`| [[Page]] | type | one-line summary | updated |`
Keep sorted by type, then alphabetically.

## wiki/log.md Format

```
## 2026-01-15T14:32 — ingest
Source: "Article Title"
Created: [[sources/article-slug]]
Touched: [[concepts/concept]], [[people/author]]
```

## Callout Conventions

- `> [!summary]` — key takeaways at top of source pages
- `> [!quote]` — verbatim excerpts worth preserving
- `> [!question]` — unverified or needs research
- `> [!action]` — tasks that emerge from a source
- `> [!decision]` — decisions made in meetings

## Synthesis Guidelines

When multiple sources touch the same concept:
1. Update the concept page — add the new perspective, note agreements/contradictions
2. If contradiction: create a synthesis page comparing the views
3. Cross-link bidirectionally: concept → sources, source → concept

## Quality Standards

- Every source page must have a `> [!summary]` with 3-5 bullet takeaways
- Every person page must link to sources where they appear
- Every project page must have: goal, status, next action, related meetings
- Stubs (< 3 sentences) get `status: stub` and appear in lint report
```

### Templates to write in `templates/`

**source.md** — for ingested articles, videos, transcripts:
```markdown
---
type: source
title: ""
created: {{date}}
updated: {{date}}
tags: []
url: ""
author: ""
sources: []
related: []
status: active
---

> [!summary]
> -
> -
> -

## Key Points

## Quotes

## Actions

## Related
```

**project.md**:
```markdown
---
type: project
title: ""
created: {{date}}
updated: {{date}}
tags: []
status: active
---

## Goal

## Status

## Next Action

## Decisions

## Related Meetings

## Related People
```

**daily.md**:
```markdown
---
type: daily
date: {{date}}
---

## Focus

## Done

## Notes

## Inbox
```

**meeting.md**:
```markdown
---
type: meeting
title: ""
date: {{date}}
attendees: []
tags: []
---

## Agenda

## Notes

> [!decision]
>

## Actions

## Related Projects
```

**person.md**:
```markdown
---
type: person
title: ""
created: {{date}}
updated: {{date}}
tags: []
status: active
---

## Role / Context

## Key Interactions

## Appears In
```

---

## Operation: ingest

When the user runs `/obsidian-llm-wiki ingest [source]`:

Source can be: URL → fetch, file path → read, or raw text pasted inline.

### Ingest Workflow

1. **Read** the source completely before writing anything.
2. **Announce the plan**: list pages you'll create or update.
3. **Create** `wiki/sources/{slug}.md` from source template:
   - Fill `> [!summary]` with 3-5 bullet key takeaways
   - Extract `> [!quote]` for high-value passages
   - Note `> [!action]` items if source implies tasks
4. **Update or create** entity pages touched by the source:
   - People mentioned → `wiki/people/{name}.md`
   - Concepts introduced → `wiki/concepts/{concept}.md`
   - Projects referenced → `wiki/projects/{project}.md`
5. **Cross-link** bidirectionally using wikilinks.
6. **Update** `wiki/index.md` with all new/changed pages.
7. **Append** to `wiki/log.md` with timestamp and pages touched.
8. **Report**: N pages created, M pages updated, key insights.

Typically touches 5–15 pages per source.

---

## Operation: daily-journal

When the user runs `/obsidian-llm-wiki daily-journal`:

1. Check if `daily/YYYY-MM-DD.md` exists for today.
2. If no: create from `templates/daily.md`.
3. If yes: read it and ask what to add, or append provided content.
4. Surface any unresolved `> [!action]` items from yesterday's note.
5. Check `wiki/projects/` for projects with overdue next actions.
6. Append to `wiki/log.md`.

---

## Operation: inbox

When the user runs `/obsidian-llm-wiki inbox`:

1. List all files in `inbox/` plus today's daily note `## Inbox` section.
2. For each item:
   - Classify: source to ingest? Task? Person? Project update?
   - Route it: ingest sources, update project pages, create stubs for new entities.
   - Archive the inbox item to `raw/` after routing.
3. Report: N items processed, what was created/updated.
4. Append to `wiki/log.md`.

---

## Operation: brain-dump

When the user runs `/obsidian-llm-wiki brain-dump`:

The **orphan hunter and gap filler**. Surfaces problems you didn't know existed.

1. **Find orphan pages**: wiki pages with no inbound wikilinks.
2. **Find stubs**: pages with `status: stub` or < 100 words.
3. **Find stale pages**: `updated` > 30 days ago with `status: active`.
4. **Find missing pages**: `[[wikilinks]]` referenced but no file exists.
5. **Find index gaps**: pages not listed in `wiki/index.md`.
6. **Produce report** in `output/brain-dump-YYYY-MM-DD.md`:

```
## Orphans (N) — no inbound links
## Stubs (N) — needs expansion
## Stale (N) — not updated in 30+ days
## Missing pages (N) — referenced but don't exist
## Index gaps (N) — not in index.md
```

7. Ask: "Fix automatically, or review first?" If auto-fix: expand stubs with placeholders,
   create missing pages as stubs, update index, cross-link orphans where logical.
8. Append to `wiki/log.md`.

---

## Operation: query

When the user runs `/obsidian-llm-wiki query [question]`:

1. Search `wiki/index.md` to identify relevant pages.
2. Read those pages plus their linked pages (one hop).
3. Synthesize an answer with inline `[[citations]]`.
4. If the answer reveals a synthesis worth preserving, ask: "Save this as a synthesis page?"
5. Never fabricate — if the wiki doesn't have it, say so and suggest a source to ingest.

---

## Operation: lint

When the user runs `/obsidian-llm-wiki lint`:

Comprehensive health check. Produces `output/lint-YYYY-MM-DD.md`.

Checks:
- 🔴 Broken wikilinks (referenced pages that don't exist)
- 🔴 Pages missing required frontmatter fields
- 🟡 Orphan pages (no inbound links)
- 🟡 Stubs (< 100 words, `status: stub`)
- 🟡 Stale active pages (not updated in 30+ days)
- 🟡 Index out of sync (pages not in index, or dead index entries)
- 🟢 Log gaps (pages with no log entry)
- 🟢 Contradiction flags (same claim stated differently on two pages)

---

## Tracking Domains

| Domain | Folder | Key fields |
|--------|--------|-----------|
| Projects | `wiki/projects/` | goal, status, next action, deadline |
| Meetings | `wiki/meetings/` | date, attendees, decisions, actions |
| Content | `wiki/content/` | format, platform, published date |
| Revenue | `wiki/revenue/` | amount, source, date, status |
| Fitness | `wiki/fitness/` | type, duration, metrics, notes |
| People | `wiki/people/` | role, relationship, appearances |
| Concepts | `wiki/concepts/` | definition, sources, related |

---

## Key Behaviors

- **Announce the plan** before writing anything — list pages, then execute.
- **Never guess** wiki content — derive from sources only.
- **Always update** `wiki/index.md` and `wiki/log.md` — non-negotiable after every operation.
- **Prefer updating** existing pages over creating new — merge, don't duplicate.
- **Use `obsidian` CLI** if available (see `obsidian-cli` skill) for file ops inside a live vault.
- **Wikilinks are connective tissue** — every named entity gets one.
- **Mark uncertainty** with `> [!question]` — never silently fabricate.

---

## Running Claude Code Inside the Vault

For persistent wiki maintenance, run Claude Code from the vault root:

```bash
cd ~/Documents/Vault
claude
```

The vault's `CLAUDE.md` loads automatically and governs all behavior. This turns Claude Code into
a dedicated wiki maintainer for as long as the session runs.

For one-shot operations from outside the vault:

```bash
claude --add-dir ~/Documents/Vault "/obsidian-llm-wiki ingest https://example.com/article"
```

---

## Sources

- [Andrej Karpathy's LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [NicholasSpisak/second-brain](https://github.com/NicholasSpisak/second-brain) — reference implementation
- [LLM Wiki + Obsidian Guide](https://aimaker.substack.com/p/llm-wiki-obsidian-knowledge-base-andrej-karphaty)
