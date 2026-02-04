# Output Contracts (v0.1)

## A1 Segmenter/Indexer
Must create:
- `pieces/P####.md` for each atomic explanatory piece
- `index/pieces_index.json` mapping piece IDs to transcript anchors
- `index/toc.md` with two TOCs:
  1) chronological (by piece ID order)
  2) topical (grouped by intent tags)

Each `pieces/P####.md` must include:
- Title (short)
- Transcript excerpt (short; quote only what's needed)
- Intent tag: one of {definition, claim, analogy, hypothesis, discriminator, objection, correction, meta-method}
- Dependencies: list of other piece IDs or empty
- Notes: optional

No new claims. No reinterpretation. Just segmentation and light labeling.
