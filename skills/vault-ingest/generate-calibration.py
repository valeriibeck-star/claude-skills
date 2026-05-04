#!/usr/bin/env python3
"""Generate calibration.md for /vault-ingest.

Reads current vault state and produces a fresh calibration file the skill
loads in Phase 0. The skill text stays human-edited; this file is data.

Per the Filesystem-as-Feedback for Coding Agents pattern (Lee et al, 2026):
expose prior experience as a navigable artifact rather than burying it
inside the skill prompt.
"""

import os
import re
import glob
import subprocess
import datetime
from pathlib import Path

VAULT = Path.home() / "Vaults" / "second-brain"
SKILL_DIR = Path.home() / ".claude" / "skills" / "vault-ingest"
OUT = SKILL_DIR / "calibration.md"


def sh(cmd, cwd=None):
    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd=cwd, timeout=10
        )
        return r.stdout.strip()
    except Exception:
        return ""


def read(p):
    try:
        return Path(p).read_text()
    except Exception:
        return ""


# --- vault size ---
wiki_files = list((VAULT / "wiki").rglob("*.md"))
raw_files = [p for p in (VAULT / "raw").rglob("*") if p.is_file()]
n_wiki = len(wiki_files)
n_raw = len(raw_files)


# --- MOCs and their vocabulary versions ---
moc_paths = sorted(glob.glob(str(VAULT / "wiki" / "*MOC*.md")))
mocs = []
for p in moc_paths:
    name = Path(p).stem
    txt = read(p)
    fm = re.search(r"^---\n(.*?)\n---", txt, re.DOTALL)
    vv = "?"
    if fm:
        m = re.search(r"vocabulary-version:\s*(\d+)", fm.group(1))
        if m:
            vv = m.group(1)
    has_xdomain = bool(re.search(r"^##\s+Cross-domain references", txt, re.MULTILINE))
    mocs.append((name, vv, has_xdomain))


# --- recent ingests from log.md ---
log = read(VAULT / "wiki" / "log.md")
ingest_re = re.compile(
    r"^## \[(\d{4}-\d{2}-\d{2})\] (ingest|ingest-light) \| (.+?)$",
    re.MULTILINE,
)
ingests = []
for m in ingest_re.finditer(log):
    date, kind, title = m.groups()
    start = m.end()
    nxt = re.search(r"^## \[", log[start:], re.MULTILINE)
    body = log[start : start + nxt.start()] if nxt else log[start:]
    ingests.append({"date": date, "kind": kind, "title": title.strip(), "body": body.strip()})

# stats over thorough ingests
def parse_counts(body):
    """Best-effort extraction of concept / entity counts and new-tag count."""
    out = {"concepts": None, "entities": None, "new_tags": None, "moc_updates": []}
    m = re.search(r"(\d+)\s+(?:new\s+)?concept", body)
    if m:
        out["concepts"] = int(m.group(1))
    m = re.search(r"(\d+)\s+(?:new\s+)?entit", body)
    if m:
        out["entities"] = int(m.group(1))
    # tag flagging — count comma-separated tag tokens after "flagged"
    m = re.search(
        r"flagged[^:]*:\s*([`\w\-,\s]+?)(?:\.|;|$)", body, re.IGNORECASE | re.MULTILINE
    )
    if m:
        tag_blob = m.group(1)
        tags = [t.strip(" `") for t in tag_blob.split(",") if t.strip(" `")]
        out["new_tags"] = len(tags)
    # MOCs touched
    moc_hits = re.findall(r"\[\[([^\]|#]+ MOC)\]\]", body)
    out["moc_updates"] = sorted(set(moc_hits))
    return out


thorough = [i for i in ingests if i["kind"] == "ingest"]
recent = thorough[-10:] if len(thorough) >= 10 else thorough


def avg(lst):
    nums = [x for x in lst if isinstance(x, int)]
    return round(sum(nums) / len(nums), 1) if nums else None


concept_counts = []
entity_counts = []
tag_counts = []
xdomain_count = 0
for ing in recent:
    s = parse_counts(ing["body"])
    if s["concepts"] is not None:
        concept_counts.append(s["concepts"])
    if s["entities"] is not None:
        entity_counts.append(s["entities"])
    if s["new_tags"] is not None:
        tag_counts.append(s["new_tags"])
    if len(s["moc_updates"]) > 1:
        xdomain_count += 1


# --- source-note body lengths ---
src_dir = VAULT / "wiki" / "sources"
src_paths = sorted(src_dir.glob("*.md"), key=lambda p: p.stat().st_mtime)
recent_srcs = src_paths[-10:]
body_lengths = []
for p in recent_srcs:
    txt = read(p)
    body = re.sub(r"^---\n.*?\n---\n", "", txt, count=1, flags=re.DOTALL)
    body_lengths.append(len(body))


# --- known dangling / orphans / stubs from latest lint ---
lints = sorted(glob.glob(str(VAULT / "output" / "lint-*.md")))
latest_lint = lints[-1] if lints else None
known_dangling = set()
known_thin = []
if latest_lint:
    txt = read(latest_lint)
    # capture wikilinks listed as dangling
    for m in re.finditer(r"`\[\[([^\]|#]+?)\]\]`", txt):
        # heuristic: only count those near "dangl" or "stub" mentions in the same paragraph
        start = max(0, m.start() - 200)
        nearby = txt[start : m.end() + 50].lower()
        if "dangl" in nearby or "stub" in nearby or "convert" in nearby:
            known_dangling.add(m.group(1))


# --- qmd index freshness ---
qmd_status = sh("qmd collection list")
qmd_block = ""
if qmd_status:
    qmd_block = qmd_status
qmd_stale = False
m = re.search(r"wiki .*?\n.*?Files:\s+(\d+)", qmd_status, re.DOTALL)
if m:
    indexed = int(m.group(1))
    if indexed < n_wiki * 0.9:
        qmd_stale = True


# --- jobs/ ---
jobs_files = sorted(glob.glob(str(VAULT / "jobs" / "*.md")))


# --- existing concept and entity filenames for dupe-check hints ---
n_concepts = len(list((VAULT / "wiki" / "concepts").glob("*.md")))
n_entities = len(list((VAULT / "wiki" / "entities").glob("*.md")))
n_sources = len(list(src_dir.glob("*.md")))


# --- emit calibration.md ---
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M %Z").strip()

lines = []
lines.append("---")
lines.append(f"generated-at: {now}")
lines.append(f"vault: {VAULT}")
lines.append("kind: vault-ingest calibration data")
lines.append("---")
lines.append("")
lines.append("# vault-ingest calibration")
lines.append("")
lines.append(
    "Auto-generated by `generate-calibration.py`. The skill (`SKILL.md`) is human-edited "
    "and stable; this file is the data layer the skill reads in Phase 0. "
    "Per the Filesystem-as-Feedback for Coding Agents pattern: prior experience "
    "lives as a navigable artifact, not buried in prompt summaries."
)
lines.append("")
lines.append("## Vault size right now")
lines.append("")
lines.append(f"- `wiki/` files: **{n_wiki}**")
lines.append(f"  - sources: {n_sources}")
lines.append(f"  - concepts: {n_concepts}")
lines.append(f"  - entities: {n_entities}")
lines.append(f"- `raw/` artifacts: {n_raw}")
lines.append("")
lines.append(
    "At this size CLAUDE.md mandates `qmd query` for non-trivial searches. "
    "Filename-only `grep` for concept-dupe detection misses semantic overlaps "
    "(\"Vector Database\" vs \"Vector Store\" — the contract's own example)."
)
lines.append("")
lines.append("## MOCs and vocabulary versions")
lines.append("")
lines.append("| MOC | vocabulary-version | Has Cross-domain references section |")
lines.append("|---|---|---|")
for name, vv, has_x in mocs:
    lines.append(f"| `{name}` | v{vv} | {'yes' if has_x else 'no'} |")
lines.append("")
lines.append(
    "**Routing rule:** when a source touches >1 domain, prefer creating one source note "
    "+ Cross-domain reference entries in *each* relevant MOC. Don't pick one MOC via `--domain` "
    "unless the source is clearly single-domain. Public APIs Catalog (May 4) is the canonical "
    "5-MOC example."
)
lines.append("")
lines.append("## qmd index status")
lines.append("")
lines.append("```")
lines.append(qmd_block or "(qmd not available)")
lines.append("```")
if qmd_stale:
    lines.append("")
    lines.append(
        f"**Index is stale** ({n_wiki} wiki files exist, fewer indexed). "
        f"Before relying on `qmd query` for dupe-check, run `qmd collection update wiki`."
    )
lines.append("")
lines.append("## Recent thorough-ingest shape (calibration baseline)")
lines.append("")
lines.append(f"Last {len(recent)} thorough ingests in `wiki/log.md`:")
lines.append("")
lines.append("| Date | Title | Concepts | Entities | New tags flagged | MOCs touched |")
lines.append("|---|---|---|---|---|---|")
for ing in recent:
    s = parse_counts(ing["body"])
    title = ing["title"][:50]
    c = s["concepts"] if s["concepts"] is not None else "?"
    e = s["entities"] if s["entities"] is not None else "?"
    t = s["new_tags"] if s["new_tags"] is not None else "?"
    m = ", ".join(s["moc_updates"]) if s["moc_updates"] else "?"
    lines.append(f"| {ing['date']} | {title} | {c} | {e} | {t} | {m} |")
lines.append("")
lines.append("**Aggregate stats over the recent ingests above:**")
lines.append("")
if concept_counts:
    lines.append(
        f"- Concepts per ingest — avg {avg(concept_counts)}, "
        f"range {min(concept_counts)}–{max(concept_counts)}"
    )
if entity_counts:
    lines.append(
        f"- Entities per ingest — avg {avg(entity_counts)}, "
        f"range {min(entity_counts)}–{max(entity_counts)}"
    )
if tag_counts:
    lines.append(
        f"- New tags flagged per ingest — avg {avg(tag_counts)}, "
        f"range {min(tag_counts)}–{max(tag_counts)}"
    )
if body_lengths:
    lines.append(
        f"- Source-note body length (chars) — avg "
        f"{int(sum(body_lengths)/len(body_lengths))}, "
        f"range {min(body_lengths)}–{max(body_lengths)}"
    )
lines.append(
    f"- Cross-domain ingests (touched >1 MOC): {xdomain_count} of {len(recent)}"
)
lines.append("")
lines.append(
    "**How to use:** when presenting the Phase 4 write plan, surface whether the "
    "proposal is *within* or *outside* these ranges. Don't enforce — anchor."
)
lines.append("")
lines.append("## Known dangling-link targets (from latest lint)")
lines.append("")
if latest_lint:
    lines.append(f"Source: `{Path(latest_lint).relative_to(VAULT)}`")
    lines.append("")
    if known_dangling:
        lines.append(
            "Wikilinks already documented as dangling/stub-deferred. **Do not "
            "auto-create stubs**; if your closeout payload would link to one of "
            "these, convert to plain text per [[Vault Ingestion Contract]]:"
        )
        lines.append("")
        for d in sorted(known_dangling):
            lines.append(f"- `[[{d}]]`")
    else:
        lines.append("No dangling-link inventory parsed from latest lint report.")
else:
    lines.append("No lint report found in `output/`.")
lines.append("")
lines.append("## Operating contract files")
lines.append("")
if jobs_files:
    lines.append("CLAUDE.md mandates reading these before non-trivial tasks:")
    lines.append("")
    for j in jobs_files:
        rel = Path(j).relative_to(VAULT)
        lines.append(f"- `{rel}`")
else:
    lines.append("No `jobs/` directory found in vault.")
lines.append("")
lines.append("## Drift watch (skill vs vault)")
lines.append("")
skill_mtime = (SKILL_DIR / "SKILL.md").stat().st_mtime
skill_age_days = (datetime.datetime.now().timestamp() - skill_mtime) / 86400
lines.append(f"- SKILL.md last touched: {skill_age_days:.1f} days ago")
lines.append(
    "- If this exceeds ~30 days, run `/audit-vault-ingest` (when built) "
    "to draft a proposed SKILL.md revision against observed practice."
)
lines.append("")
lines.append("---")
lines.append("")
lines.append("*Regenerate by running:*")
lines.append("")
lines.append("```bash")
lines.append("python3 ~/.claude/skills/vault-ingest/generate-calibration.py")
lines.append("```")

OUT.write_text("\n".join(lines) + "\n")
print(f"Wrote {OUT}")
print(f"  vault wiki files: {n_wiki}, raw: {n_raw}")
print(f"  ingests parsed: {len(ingests)} (thorough: {len(thorough)})")
print(f"  MOCs: {len(mocs)}")
print(f"  known dangling targets: {len(known_dangling)}")
print(f"  qmd stale: {qmd_stale}")
