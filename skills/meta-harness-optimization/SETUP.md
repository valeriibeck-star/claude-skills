# How to Set Up Meta-Harness: Practical Implementation Guide

## What Is Meta-Harness?

Meta-Harness is a system from Stanford IRIS Lab that automatically optimizes the "harness" — the scaffolding code around an LLM agent that controls what context it sees, what it remembers, and how it acts. Instead of swapping in a better model, you optimize the wrapper code itself. The research showed this can produce up to 6x performance differences on the same benchmark with the same model.

**Paper:** "Meta-Harness: End-to-End Optimization of Model Harnesses" (arXiv:2603.28052) by Yoonho Lee, Rohan Nair, Qinyuan Zhang, Kimin Lee, Omar Khattab, and Chelsea Finn.

---

## Prerequisites

Before setting up Meta-Harness, you need:

1. **Python 3.10+** with `uv` package manager installed
2. **Claude Code** (the default proposer agent) — or adapt for another coding agent
3. **An Anthropic API key** (for Claude as the proposer)
4. **A task/benchmark** you want to optimize your agent harness for
5. **Git** for cloning the repository

---

## Step-by-Step Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/stanford-iris-lab/meta-harness.git
cd meta-harness
```

### Step 2: Install Dependencies

```bash
uv sync
```

This installs all Python dependencies using the `uv` package manager. If you don't have `uv`, install it first:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 3: Onboarding — Define Your Domain

The repository ships with an `ONBOARDING.md` file. Start by having your coding assistant (Claude Code) read it:

```bash
claude "Read ONBOARDING.md and help me set up Meta-Harness for my domain"
```

This interactive conversation will produce a `domain_spec.md` file with concrete details for your specific use case — what your task looks like, how evaluation works, and what your initial harness should contain.

### Step 4: Understand the Architecture

Meta-Harness works as an outer optimization loop:

1. **Filesystem as memory:** All prior harness candidates, their source code, execution traces, and evaluation scores live in a directory structure
2. **Proposer agent:** A coding agent (Claude Code by default) reads the entire filesystem and proposes a new harness
3. **Evaluator:** The new harness is tested against your benchmark
4. **Repeat:** Scores and traces are logged, and the proposer sees everything for the next iteration

A typical run evaluates ~60 harnesses over ~20 iterations.

### Step 5: Try a Reference Example

Two reference experiments ship with the repo:

**Option A — Text Classification (simpler start):**
```bash
cd reference_examples/text_classification/
uv sync
# Follow the README in this directory
```

**Option B — Terminal-Bench 2.0 (coding agent scaffold):**
```bash
cd reference_examples/terminal_bench_2/
uv sync
uv run bash scripts/run_eval.sh agents.baseline_kira:AgentHarness full 1 1 -i extract-elf
```

### Step 6: Write Your Own Harness

A harness is Python code that wraps your LLM calls. At minimum it defines:

- **What context to store** — full source code and execution logs (Meta-Harness's key insight: don't compress, store everything)
- **What context to retrieve** — which prior information gets injected into the next prompt
- **What the model does next** — tool selection, output parsing, loop control

Create your initial harness as a Python class (e.g., `AgentHarness`) following the patterns in the reference examples.

### Step 7: Configure the Proposer

The shipped examples use Claude Code as the proposer agent. The proposer:

- Reads the filesystem containing all prior candidates
- Analyzes what worked and what didn't
- Writes a new harness variant
- The system evaluates it and logs results

If you want a different proposer, adapt the `claude_wrapper.py` scripts in the reference examples.

### Step 8: Run the Optimization Loop

```bash
# From your experiment directory
uv run python run_search.py --config your_config.yaml
```

The loop will:
1. Start with your initial harness
2. Have the proposer agent analyze all history and propose improvements
3. Evaluate each new harness on your benchmark
4. Store all traces and scores
5. Repeat for the configured number of iterations

---

## Key Discoveries from the Paper

Things Meta-Harness discovered that you can apply manually even without running the full system:

1. **Environment bootstrapping:** Before the agent loop begins, run a compound shell command to snapshot the sandbox environment (available tools, files, etc.) and inject it into the initial prompt. This eliminates the 2-4 exploratory turns agents typically waste discovering their environment.

2. **Store full source code and logs, not summaries:** Traditional approaches compress context. Meta-Harness showed that keeping full execution traces (up to 10M tokens per step) gives the proposer agent much better signal for improvement.

3. **Treat the harness as a first-class optimization target:** Most teams spend effort on prompt engineering or model upgrades. The harness layer — what the model sees, remembers, and does — has a bigger impact.

---

## Practical Tips

- **Start small:** Begin with the text classification reference example to understand the flow before tackling your own domain
- **Budget for compute:** A full optimization run (~60 harness evaluations) requires significant API calls
- **Version control your harnesses:** Each iteration produces a new harness variant — the filesystem structure handles this, but back it up
- **Read the execution traces:** The most valuable output isn't just the final harness, but understanding *why* certain changes improved performance
- **Apply insights manually:** Even if you don't run the full loop, the discovered patterns (like environment bootstrapping) can be implemented by hand in your existing agent scaffolding

---

## Resources

- **Paper:** https://arxiv.org/abs/2603.28052
- **Project page:** https://yoonholee.com/meta-harness/
- **Official repo:** https://github.com/stanford-iris-lab/meta-harness
- **Terminal-Bench 2.0 artifact:** https://github.com/stanford-iris-lab/meta-harness-tbench2-artifact
- **Community implementation:** https://github.com/SuperagenticAI/metaharness
- **HuggingFace report:** https://huggingface.co/blog/Svngoku/meta-harness-end-to-end-optimization-of-model
- **Source TikTok:** https://www.tiktok.com/@howard.mov7/video/7630253909973650709
