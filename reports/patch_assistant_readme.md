# Patch Assistant Readme

`tools/ci_patch_assistant.py` generates guided graph patch artifacts from persisted task suggestions.

## Inputs
- `lcg/lcg_graph.json`
- `houdini_package/output/ledger/task_suggestions.jsonl`
- `reports/interface_variables.md`

## Outputs
- `patches/PATCH-*.json` (machine patch)
- `patches/PATCH-*.md` (human explanation)
- `lcg/lcg_graph.patched.json` (default patched copy)

## Safety
By default, canonical graph is not modified.
Use `--apply` only when ready to overwrite `lcg/lcg_graph.json`.

## Usage
```bash
python tools/ci_patch_assistant.py --list --last-n 20
python tools/ci_patch_assistant.py --task-id TASK-001
python tools/ci_patch_assistant.py --index 1
python tools/ci_patch_assistant.py --task-id TASK-001 --apply
```

## Supported patch classes
- Node discriminator stub adds
- Edge E3/E4 reclassification (with sane weights)
- Interface variable binding additions
- Edge schema hygiene (`tags`, `evidence_refs`) additions

## Acceptance check
- JSON patch + markdown explainer created under `patches/`
- `lcg/lcg_graph.patched.json` written
- Canonical graph untouched unless `--apply` is set
