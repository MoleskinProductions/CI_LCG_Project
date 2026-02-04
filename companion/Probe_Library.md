# Probe Library

Each probe references at least one discriminator and one interface variable.

## P-PRB-001 — Formalization Primitive-Budget Audit
- Tied discriminators: `D-CI-001`
- Interface variables: `primitive budget / silent premise`
- Inputs: node context, chart pair (formal/narrative), premise inventory
- Outputs: primitive delta, hidden-premise count, split result
- Pass/Fail:
  - Pass: entailments preserved with no primitive inflation
  - Fail: hidden premise or primitive-count increase required

## P-PRB-002 — Entry Framing Seam Visibility Probe
- Tied discriminators: `D-CI-002`
- Interface variables: `primitive budget / silent premise`
- Inputs: entry framing variants, seam taxonomy
- Outputs: seam-type overlap score, masked-seam count
- Pass/Fail:
  - Pass: seam types remain explicit and stable across entry framings
  - Fail: seam masking or seam-type collapse appears

## P-PRB-003 — Ledger Stability Loop Probe
- Tied discriminators: `D-LCG-001`
- Interface variables: `ledger stability / taxonomy drift`
- Inputs: iterative run snapshots, seam labels per iteration
- Outputs: drift index, class-retention score, split result
- Pass/Fail:
  - Pass: class labels remain stable across loop passes
  - Fail: taxonomy drift accumulates

## P-PRB-004 — Adversarial Taxonomy Robustness Probe
- Tied discriminators: `D-LCG-002`
- Interface variables: `ledger stability / taxonomy drift`
- Inputs: adversarial relabel operations, baseline taxonomy
- Outputs: perturbation sensitivity, explosion score, split result
- Pass/Fail:
  - Pass: seam typing remains stable under adversarial relabeling
  - Fail: drift/explosion under perturbation

## P-PRB-005 — Admissibility Handoff Scatter Probe
- Tied discriminators: `D-BRID-021`
- Interface variables: `primitive budget / silent premise`, `ledger stability / taxonomy drift`
- Inputs: procedure-valid claims, ontology-admissible claims, handoff route
- Outputs: handoff delta matrix, reification flag, split result
- Pass/Fail:
  - Pass: seam visibility preserved through handoff
  - Fail: method outcomes reified as ontology without explicit interface accounting

## P-PRB-006 — Triad Mapping Stability Probe
- Tied discriminators: `D-011-001`, `D-012-001`
- Interface variables: `primitive budget / silent premise`
- Inputs: role-assignment mappings across chart variants
- Outputs: role-consistency score, inseparability check
- Pass/Fail:
  - Pass: role assignment and triad inseparability remain stable
  - Fail: silent role swap or optionalization of triad terms

## P-PRB-007 — Recursive Differentiation Continuity Probe
- Tied discriminators: `D-013-001`, `D-016-001`
- Interface variables: `constraint-order coupling`
- Inputs: recursive articulation depth, closure criteria
- Outputs: recursion persistence index, closure mode classification
- Pass/Fail:
  - Pass: differentiation remains generative without identity freeze
  - Fail: recursion collapses into static closure

## P-PRB-008 — Ground Negation Stability Probe
- Tied discriminators: `D-014-001`, `D-017-001`
- Interface variables: `constraint-order coupling`
- Inputs: negative/positive restatement pairs
- Outputs: reification pressure score, boundary stability score
- Pass/Fail:
  - Pass: ground remains relational/negative under restatement
  - Fail: positive substrate insertion required

## P-PRB-009 — Loop/Closure Residue Probe
- Tied discriminators: `D-PHY-001`
- Interface variables: `loop/closure residue`
- Inputs: chart variants, closure path definitions
- Outputs: residue stability score, chart-removability check
- Pass/Fail:
  - Pass: residue persists across allowed chart rewrites
  - Fail: residue removable by local reparameterization

## P-PRB-010 — Dimensionless Drift Probe
- Tied discriminators: `D-PHY-004`
- Interface variables: `dimensionless drift`
- Inputs: scaled chart variants, ratio channels
- Outputs: drift under scaling, admissibility tag
- Pass/Fail:
  - Pass: ratio-level channels remain stable under scaling
  - Fail: observable shifts under unit scaling

## P-PRB-011 — Observable Equivalence-Class Probe
- Tied discriminators: `D-PHY-005`
- Interface variables: `observability equivalence class`
- Inputs: candidate observable families, chart transforms
- Outputs: equivalence-class membership, admissibility class
- Pass/Fail:
  - Pass: operator family remains stable across equivalent charts
  - Fail: candidate depends on chart-specific coordinates

## P-PRB-012 — Local Arrow Persistence Scatter Probe
- Tied discriminators: `D-TIM-002`, `D-019-001`
- Interface variables: `local arrow persistence`
- Inputs: cross-context chart set, asymmetry channels
- Outputs: persistence scatter matrix, global-orientation dependency flag
- Pass/Fail:
  - Pass: arrow-like asymmetry persists locally across chart shifts
  - Fail: persistence appears only with imposed global orientation
