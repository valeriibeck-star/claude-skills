# claude-skills

Portable collection of 284 Claude Code skills collected from Val's Mac Mini. Clone into any project's `.claude/skills/` directory to make them available on any device — including iPhone Claude Code (remote container).

## What's here

```
skills/              ← 284 individual skills, each in its own directory
  agent-eval/
    SKILL.md
  autoplan/
    SKILL.md
  ...
project-skills/      ← project-specific skills (standalone .md files)
  kompozit-erp/
    debug-issue.md
    explore-codebase.md
    refactor-safely.md
    review-changes.md
```

## Usage

### Option A — clone all skills into a project

```bash
cd your-project/
git clone https://github.com/valeriibeck-star/claude-skills .claude/skills
```

### Option B — sparse-checkout only the skills you want

```bash
cd your-project/
mkdir -p .claude/skills
git -C .claude/skills init
git -C .claude/skills remote add origin https://github.com/valeriibeck-star/claude-skills
git -C .claude/skills sparse-checkout init --cone
git -C .claude/skills sparse-checkout set skills/gsd-plan-phase skills/ship skills/review
git -C .claude/skills pull origin main
```

### Option C — clone as a subdirectory, symlink what you need

```bash
git clone https://github.com/valeriibeck-star/claude-skills ~/claude-skills
# then symlink individual skills into your project
ln -s ~/claude-skills/skills/ship /your-project/.claude/skills/ship
```

## Skill categories

| Category | Examples |
|----------|---------|
| **GSD (Get Stuff Done)** | gsd-plan-phase, gsd-execute-phase, gsd-new-project, gsd-debug, gsd-health |
| **Code quality** | review, code-review, security-review, refactoring-patterns, clean-code |
| **Testing** | tdd-workflow, python-testing, kotlin-testing, rust-testing, e2e-testing |
| **Language patterns** | python-patterns, rust-patterns, golang-patterns, kotlin-patterns, swift-concurrency-6-2 |
| **Framework patterns** | django-patterns, laravel-patterns, springboot-patterns, nextjs-turbopack |
| **Design** | ui-ux-pro-max, design-shotgun, microinteractions, refactoring-ui, liquid-glass-design |
| **Business books** | obviously-awesome, crossing-the-chasm, lean-startup, traction-eos, made-to-stick |
| **Product** | jobs-to-be-done, continuous-discovery, mom-test, inspired-product |
| **Agent/AI engineering** | agentic-engineering, agent-eval, autonomous-loops, dispatching-parallel-agents |
| **Browser/QA** | browse, browser-qa, gstack-upgrade, connect-chrome |
| **Workflow** | ship, investigate, freeze, unfreeze, autoplan, retro |

## Notes

- **gstack-dependent skills** (browse, autoplan, canary, ship, etc.) require the [gstack framework](https://github.com/getgstack/gstack) to be installed at `~/.claude/skills/gstack/`. The SKILL.md definitions are included here; install gstack separately for full functionality.
- The `gstack/` directory itself is excluded from this repo (it contains 300MB+ of compiled browser extension and binaries).
- `project-skills/kompozit-erp/` contains project-specific skills for the Kompozit ERP project that use a local code-graph MCP — they won't work outside that project context.
- Skills were collected from `~/.claude/skills/` and `~/.agents/skills/` on macOS (Mac Mini M4).

## Updating

To pull the latest skills from this repo:

```bash
cd .claude/skills  # wherever you cloned this
git pull origin main
```

## Source

Collected by [@valeriibeck-star](https://github.com/valeriibeck-star) on 2026-04-18.
