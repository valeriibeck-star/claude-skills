# TikTok Content Extraction — Video 3

## Source
- **URL:** https://vm.tiktok.com/ZNRqE718d/
- **Resolved URL:** https://www.tiktok.com/@howard.mov7/video/7630253909973650709
- **Creator:** @howard.mov7 (howard.mov)
- **Posted:** ~April 19, 2026 (3 days ago as of extraction)
- **Engagement:** 4,058 likes · 53 comments · 2,972 bookmarks · 429 shares

## Video Title / On-Screen Text
"Upgrade Harnesses, Not Models"

## Caption / Description
Better models won't fix your agent. . . . Most people are upgrading models… But ignoring the one layer that can change performance by up to 6×. The harness. It controls: - what your model sees - what it remembers - how it behaves. Meta-Harness flips the game by optimizing that layer directly — using full code + execution logs instead of compressed summaries. That's how it beats hand-engineered systems. I'm testing this myself next. Follow @howard.mov7 for the upcoming breakdown. #ai #app #llm #airesearch #tech

## Full Spoken Transcript (from subtitles)
you need this now. most people try to improve their coding agents by upgrading the model, but there's something else that can change performance by up to six times — it's the harness. the code that decides what context the model sees, what it remembers, and what it does next. and almost no one is treating this as a first class problem. a new system called Meta-Harness is a harness for improving harnesses. instead of compressing text like traditional techniques, Meta-Harness stores full source code and logs and then uses an agent to iteratively rewrite the harness. and that alone was enough to beat the best hand-designed systems on coding benchmarks. I'm gonna try this out myself, so follow along for an upcoming guide.

## Hashtags
#ai #app #llm #airesearch #tech

## Topic Summary
The video introduces Meta-Harness, a research system from Stanford (paper: arXiv:2603.28052) that automatically optimizes the "harness" layer around LLM-based coding agents. Rather than upgrading the underlying model, Meta-Harness optimizes the scaffolding code that controls what context the model sees, what it remembers, and how it behaves. The system stores full source code and execution logs (rather than compressed summaries) and uses an agent to iteratively rewrite the harness. This approach achieved up to 6x performance improvements and beat hand-engineered systems on coding benchmarks.

## Key Concepts
- **Harness:** The code wrapper around an LLM that controls context, memory, and behavior
- **Meta-Harness:** An automated system that optimizes harnesses using iterative agent-driven rewriting
- **Core insight:** Changing the harness around a fixed LLM can produce a 6x performance gap on the same benchmark
- **Method:** Uses full source code + execution traces (not compressed summaries) stored in a filesystem, with an agent proposing improved harness versions each iteration

## Extraction Method
- Caption/description: Extracted from page text and `__UNIVERSAL_DATA_FOR_REHYDRATION__` JSON
- Transcript: Fetched from `subtitleInfos` WebVTT endpoint embedded in TikTok page data
- On-screen text: Read from video screenshot
- Metadata: Parsed from page DOM and structured data
