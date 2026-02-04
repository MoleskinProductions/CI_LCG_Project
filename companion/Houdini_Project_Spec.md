# Houdini Project Spec (CI/LCG Companion)

## Project Goal
Implement a Houdini-native simulation companion where:
- nodes are test contexts,
- discriminators are probes,
- interface variables are channels,
- edges are transfer/translation routes,
- seams are explicit failure artifacts.

No domain-truth claims are produced; outputs are model-family comparison results.

## Concept Model in Houdini
- **Chart**: parameterization mode for a context (e.g., narrative chart, formal chart, loop chart).
- **Probe**: repeatable operator producing structured measurable outputs.
- **Ledger**: persistent record of invariants, probe outcomes, drift, seam flags.
- **Graph View**: cluster view for constellations and edge semantics (E3 transfer, E4 translation, E1 soft).

## Directory Structure

```text
companion/
  houdini_project/
    hip/
      ci_lcg_companion_v01.hip
    hda/
      CI_ChartMode.hda
      CI_ProbeRunner.hda
      CI_TransferEvaluator.hda
      CI_ChartBridge.hda
      CI_LedgerWriter.hda
      CI_SeamFlagger.hda
      CI_GraphOverlay.hda
    config/
      lcg_graph.snapshot.json
      interface_variables.snapshot.json
      probe_registry.json
      chart_modes.json
    data/
      runs/
        <run_id>/
          probe_outputs.json
          transfer_results.json
          seam_flags.json
          ledger_delta.json
    schemas/
      probe_output.schema.json
      ledger_event.schema.json
      seam_flag.schema.json
    reports/
      run_summary.md
      seam_audit.md
```

## HDA / Node List
- `CI_ChartMode`: selects chart parameterization and channel mappings.
- `CI_ProbeRunner`: executes probe set for selected node(s).
- `CI_ChartBridge`: applies E4 reparameterization using one interface variable.
- `CI_TransferEvaluator`: evaluates E3 transfer validity across source/target contexts.
- `CI_SeamFlagger`: classifies failures (drift, silent upgrade, reification, axis collapse).
- `CI_LedgerWriter`: appends standardized ledger events.
- `CI_GraphOverlay`: renders constellations, selected path, seam hotspots.

## Data Formats

### probe_output.schema.json (logical fields)
- `run_id`, `timestamp`, `node_id`, `probe_id`, `discriminator_ids[]`
- `chart_mode`, `interface_variables[]`
- `observable_values{}`
- `split_result` (`pass|fail|inconclusive`)
- `confidence` (0..1)
- `failure_signatures[]`
- `notes`

### ledger_event.schema.json (logical fields)
- `run_id`, `event_id`, `node_id`, `edge_id?`
- `invariant_ids[]`
- `probe_refs[]`
- `channel_drift{interface_variable: value}`
- `seam_flags[]`
- `decision` (`retain|downgrade|review`)

### seam_flag.schema.json (logical fields)
- `flag_id`, `severity`, `scope` (`node|edge|path`)
- `kind` (`silent_upgrade|taxonomy_drift|reification|axis_collapse|nonportable_transfer`)
- `evidence_refs[]`, `trigger_probe_ids[]`

## UX Flows

### Flow 1: Run Probe
1. Select node(s) and chart mode.
2. Select probe set from registry (auto-suggest by discriminator ids).
3. Run and inspect pass/fail + channel-level measurements.
4. Save run artifact.

### Flow 2: Compare Charts
1. Choose source/target chart modes.
2. Select E4 edge or manual interface variable.
3. Execute `CI_ChartBridge` reparameterization.
4. Display translation success and seam flags.

### Flow 3: Evaluate Transfer
1. Select source discriminator probe and target node.
2. Execute transfer evaluator (E3 semantics).
3. Inspect portability constraints and failure signatures.
4. Accept/reject transfer and write ledger delta.

### Flow 4: Seam Audit
1. Filter seam flags by constellation or severity.
2. Open linked probe outputs and edge lineage.
3. Export seam audit report.

## Acceptance Criteria
- Every probe run records at least one discriminator id and one interface variable.
- Every E4 evaluation names exactly one interface variable channel.
- E3 transfer reports include portability status and failure signatures.
- Ledger deltas are append-only and traceable to run artifacts.
- Graph overlay marks E1 as soft adjacency by default.

## Sanity Checks
- Re-run same probe/chart combination -> stable output envelope.
- Adversarial relabeling changes should trigger taxonomy-drift flags.
- Handoff path (`Q000008 -> Q000021 -> Q000011`) must fail if silent ontic upgrade is introduced.
- Transfer evaluation should downgrade to review if source probe is non-transferable.
