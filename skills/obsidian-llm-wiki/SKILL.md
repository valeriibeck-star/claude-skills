---
name: obsidian-llm-wiki
description: |
  Transform any directory (or Obsidian vault) into a self-maintaining LLM-powered wiki
  using Andrej Karpathy's three-layer knowledge base pattern. Claude reads raw sources
  (articles, transcripts, PDFs, notes, screenshots) and compiles them into an
  interconnected wiki — handling all the bookkeeping so you don't have to.
  Use when asked to "set up my LLM wiki", "ingest this into my wiki", "query my wiki",
  "lint my wiki", or any variant of building/maintaining a personal knowledge base.
  Trigger on: /wiki-setup, /ingest, /wiki-query, /process-inbox, /lint-wiki, /daily-journal.
origin: karpathy-llm-wiki
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
---

# Obsidian LLM Wiki

> Based on Andrej Karpathy's LLM Wiki pattern.
> Original gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

The core insight: maintaining a knowledge base is tedious not because of the thinking
but because of the bookkeeping. LLMs handle bookkeeping effortlessly. You feed raw content;
Claude compiles, cross-references, and maintains the wiki. Result: ~70x more token-efficient
than RAG because knowledge is compiled once, not retrieved per query.

---

## When to Activate

- User wants to build or maintain a personal knowledge base / second brain
- User pastes articles, transcripts, notes and wants them "added to the wiki"
- User asks questions that should be answered from their accumulated knowledge
- User says "ingest this", "add this to my wiki", "what do I know about X"
- User wants to set up Obsidian as a Claude-powered second brain
- Commands: `/wiki-setup`, `/ingest [source]`, `/wiki-query [question]`,
  `/process-inbox`, `/lint-wiki`, `/daily-journal`, `/brain-dump`

---

## Three-Layer Architecture

```
vault/
├── raw/                    ← Layer 1: Immutable sources (YOU write here)
│   ├── articles/
│   ├── transcripts/
│   ├── papers/
│   ├── notes/
│   ├── inbox/              ← Drop quick thoughts here for /process-inbox
│   └── assets/             ← Images, screenshots (set as Obsidian attachment folder)
│
├── wiki/                   ← Layer 2: LLM-maintained wiki (CLAUDE writes here)
│   ├── index.md            ← Master catalog — first file read every session
│   ├── log.md              ← Append-only activity log — never edited, only appended
│   ├── hot.md              ← ~500-word rolling summary of last 3-5 sessions
│   ├── concepts/           ← Cross-source technical/theoretical concepts
│   ├── entities/           ← People, organizations, tools, products
│   ├── sources/            ← Per-source summary pages
│   ├── projects/           ← Active and archived project tracking
│   ├── meetings/           ← Meeting notes → structured pages
│   ├── content/            ← Articles, videos, books consumed
│   └── comparisons/        ← Side-by-side analyses
│
├── outputs/                ← Layer 3: Reports, lint results, exports (CLAUDE writes)
│   └── lint-YYYY-MM-DD.md
│
└── CLAUDE.md               ← Schema: tells Claude how to operate this vault
```

**The single most important rule: Claude NEVER modifies `raw/`. It reads only.**

---

## CLAUDE.md Template (place in vault root)

When setting up a new wiki, create this file:

```markdown
# Wiki Schema

## Structure
- `raw/` — immutable source documents. READ ONLY. Never modify.
- `wiki/` — LLM-generated wiki. You own this entirely. Maintain it.
- `wiki/index.md` — master catalog. Update on every ingest.
- `wiki/log.md` — append-only activity log. Append, never edit.
- `wiki/hot.md` — ~500-word rolling summary of recent sessions. Update each session.
- `outputs/` — reports, exports, lint results.

## Page Frontmatter (required on every wiki page)
---
title: Page Title
type: concept | entity | source-summary | comparison | project | meeting
sources:
  - raw/path/to/source.md
related:
  - "[[related-page-slug]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
tags:
  - domain/subtopic
---

## Naming Conventions
- Filenames: kebab-case (e.g., attention-mechanism.md)
- Cross-references: [[wikilinks]] for all internal links
- Source references: always link back to the raw/ file

## Ingest Rules
1. Read source; identify key concepts, entities, claims
2. Create/update 8-15 wiki pages across concepts/, entities/, sources/
3. Use [!contradiction] callouts for conflicts with existing pages
4. Update wiki/index.md — add new pages, update related pages
5. Append to wiki/log.md: `## [YYYY-MM-DD] ingest | Source Title`
6. Update wiki/hot.md with session summary (~500 words)

## Query Rules
1. Read wiki/index.md first to find relevant pages
2. Read those pages; synthesize answer with [[wikilinks]] citations
3. Answer from wiki content, not from raw/ directly
4. Optionally save valuable answers as new wiki pages

## Lint Rules
Scan for and report:
- Contradictions between pages (flag with confidence levels)
- Orphan pages (no incoming wikilinks)
- Missing pages (referenced via [[wikilink]] but not created)
- Stale claims (superseded by newer sources)
- Duplicate concept coverage across multiple pages
Save results to outputs/lint-YYYY-MM-DD.md
```

---

## Core Workflows

### /wiki-setup — Initialize a new vault

1. Check if `raw/`, `wiki/`, `outputs/` directories exist; create if not
2. Check for `CLAUDE.md`; create from template above if not present
3. Create `wiki/index.md` with empty catalog structure
4. Create `wiki/log.md` with header
5. Create `wiki/hot.md` with initialization note
6. Report: vault is ready, drop files into `raw/` and run `/ingest`

```bash
mkdir -p raw/articles raw/transcripts raw/papers raw/notes raw/inbox raw/assets
mkdir -p wiki/concepts wiki/entities wiki/sources wiki/projects wiki/meetings wiki/content wiki/comparisons
mkdir -p outputs
```

### /ingest [source] — Add content to the wiki

**Input:** a file path in `raw/`, a URL, or pasted content

1. Read `wiki/index.md` to understand existing wiki structure
2. Read `wiki/hot.md` for recent session context
3. Read and process the source material
4. Identify: key concepts, entities (people/tools/orgs), claims, cross-references
5. For each concept/entity: check if a wiki page exists (Grep); update or create
6. Create `wiki/sources/[slug].md` summary page for the source
7. Update all related existing pages with new connections
8. Update `wiki/index.md` — add new pages, update existing entry metadata
9. Append to `wiki/log.md`:
   ```
   ## [YYYY-MM-DD] ingest | [Source Title]
   Pages created: N | Pages updated: M | Source: raw/path/file.md
   ```
10. Update `wiki/hot.md` with session summary

**Target: 8-15 wiki pages created/updated per ingest**

### /wiki-query [question] — Answer from accumulated knowledge

1. Read `wiki/index.md` to identify relevant pages
2. Read those pages (not the raw sources)
3. Synthesize answer with [[wikilink]] citations
4. Flag any gaps: "The wiki has no information on X — ingest a source to add it"
5. Offer to save the answer as a new wiki page if it's non-trivial

### /process-inbox — Classify and integrate quick notes

1. Glob `raw/inbox/` for new files
2. For each file: classify (concept, project note, meeting, idea, reference)
3. Route to appropriate wiki section or create new page
4. Move processed files from `raw/inbox/` to `raw/notes/` (or appropriate subdir)
5. Update `wiki/index.md` and `wiki/log.md`

### /daily-journal — Capture and integrate a daily note

1. Prompt for or accept today's note (freeform text)
2. Save to `raw/notes/YYYY-MM-DD.md`
3. Extract: tasks, decisions, links, people mentioned, projects touched
4. Update relevant project pages, entity pages, create meeting pages if needed
5. Append to `wiki/log.md`

### /brain-dump — Fast capture, sort later

Accepts any freeform content. Saves to `raw/inbox/brain-dump-[timestamp].md`.
Immediately runs `/process-inbox` to classify and integrate.

### /lint-wiki — Health check

1. Read all wiki pages (Glob `wiki/**/*.md`)
2. Build link graph: find all `[[wikilinks]]`, check each target exists
3. Find orphan pages: pages with no incoming links
4. Scan for `[!contradiction]` callouts — list unresolved ones
5. Check for stale `confidence: low` pages older than 30 days
6. Check `wiki/index.md` for missing entries (pages not listed)
7. Save report to `outputs/lint-[YYYY-MM-DD].md`
8. Print summary: N issues found, top 3 to fix

---

## Page Type Formats

### Concept page (`wiki/concepts/[slug].md`)
```markdown
---
title: Concept Name
type: concept
sources:
  - raw/articles/source.md
related:
  - "[[related-concept]]"
  - "[[entity-name]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high
tags:
  - domain/subtopic
---

# Concept Name

One-paragraph definition.

## Key Claims
- Claim one (source: [[source-summary-page]])
- Claim two

## Connections
Links to related concepts and why they're related.

## Open Questions
Things the wiki doesn't yet know about this concept.
```

### Entity page (`wiki/entities/[slug].md`)
For people, tools, organizations, products. Same frontmatter schema.

### Source summary (`wiki/sources/[slug].md`)
Per-source distillation: what it says, key claims, concepts introduced,
entities mentioned, confidence assessment.

---

## index.md Structure

```markdown
# Wiki Index
Last updated: YYYY-MM-DD | Pages: N | Sources ingested: M

## Concepts (N)
- [[attention-mechanism]] — self-attention in transformers (2024-01-15, 3 sources)
- [[retrieval-augmented-generation]] — RAG vs compiled wiki tradeoffs (2024-01-10, 1 source)

## Entities (N)
- [[andrej-karpathy]] — AI researcher, LLM Wiki author (2024-01-15)
- [[obsidian]] — knowledge management tool used in this setup (2024-01-10)

## Sources (N)
- [[karpathy-llm-wiki-gist]] — original LLM Wiki pattern (ingested 2024-01-15)

## Projects (N)
## Meetings (N)
## Content (N)
```

---

## log.md Format

Append-only. Never edit existing entries.

```markdown
# Activity Log

## [2024-01-15] ingest | Karpathy LLM Wiki Gist
Pages created: 8 | Pages updated: 3 | Source: raw/articles/karpathy-llm-wiki.md

## [2024-01-15] query | What is the difference between RAG and compiled wikis?
Answer saved: wiki/concepts/rag-vs-compiled-wiki.md

## [2024-01-16] lint | 4 issues found
Report: outputs/lint-2024-01-16.md
```

---

## Obsidian Integration Tips

- Set `raw/assets/` as your attachment folder in Obsidian settings
- Install: **Dataview** (query metadata), **Obsidian Git** (auto-sync), **Templater**
- Enable wikilinks in Obsidian settings (default on)
- Run Claude Code with the vault folder as working directory
- Open vault in Obsidian — watch wiki pages appear in real-time as Claude writes

---

## Design Principles

1. **Compile once, query many.** Wiki pages are pre-synthesized — not retrieved raw per query.
2. **raw/ is immutable.** Claude reads, never writes.
3. **index.md is the entry point.** Read it first, every session.
4. **log.md is the audit trail.** Append only.
5. **hot.md is the session bridge.** ~500 words of recent context for fast cold-start.
6. **8-15 pages per ingest.** Full update across all related pages, not just a summary.
7. **Contradictions are first-class.** Flag with `[!contradiction]`, don't silently overwrite.
8. **Confidence degrades.** Stale unverified content drops from `high` to `low`, not deleted.
9. **The wiki is the product. Chat is the interface.**
