# CI_LCG_Project (bootstrap)

This is a local-first, version-control-friendly workspace to turn a long conversation into:
1) atomic explanatory pieces,
2) CI annotations (leaks / invariants / discriminators),
3) an LCG graph bundle,
4) a backlog of follow-on tasks for specialist agents.

## Quick start
1. Paste the full conversation transcript into: `source/conversation.md`
   - Keep it chronological.
   - Do not edit for style; treat it as the immutable source.

2. Run agent A1 (Segmenter/Indexer) using the prompt in:
   - `prompts/A1_segmenter.md`

3. Inspect outputs:
   - `pieces/` for P####.md files
   - `index/pieces_index.json`
   - `index/toc.md`

Once A1 looks good, proceed with A2, A3, A4, A5 (prompts are stubbed here for later).
