# LCG QA Findings

- (warning) Duplicated discriminator meaning across nodes — Q000001/D-IOB-001, Q000002/D-CI-001, Q000003/D-PHY-001, Q000004/D-IOB-002, Q000005/D-PHY-002, Q000006/D-PHY-003, Q000007/D-CI-002, Q000008/D-LCG-001, Q000009/D-PHY-004, Q000010/D-PHY-005
  Proposed patch: Customize Observable/Split to each node’s chart to avoid identical tests.
- (warning) Redundant E1 with E3 present — Edge E000009
  Proposed patch: Remove E1 or lower weight to 0.2.
- (warning) High weight with short justification — Edge E000005
  Proposed patch: Lower weight to <=0.6 or expand justification with shared invariant/discriminator.
- (warning) High weight with short justification — Edge E000011
  Proposed patch: Lower weight to <=0.6 or expand justification with shared invariant/discriminator.
- (warning) E4 bridge lacks interface/chart reason — Edge E000008
  Proposed patch: Clarify interface variable or downgrade to E1.
- (warning) Boilerplate invariant — Q000001/I-001-001 'Question focus'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000001/I-001-002 'Scope boundary'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000002/I-002-001 'Question focus'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000002/I-002-002 'Scope boundary'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000003/I-003-001 'Question focus'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000003/I-003-002 'Scope boundary'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000004/I-004-001 'Question focus'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000004/I-004-002 'Scope boundary'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000005/I-005-001 'Question focus'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000005/I-005-002 'Scope boundary'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000006/I-006-001 'Question focus'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000006/I-006-002 'Scope boundary'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000007/I-007-001 'Question focus'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000007/I-007-002 'Scope boundary'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000008/I-008-001 'Question focus'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000008/I-008-002 'Scope boundary'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000009/I-009-001 'Constraint statement'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000009/I-009-002 'Allowed/forbidden split'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000010/I-010-001 'Constraint statement'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
- (warning) Boilerplate invariant — Q000010/I-010-002 'Allowed/forbidden split'
  Proposed patch: Replace with chart-specific invariant (loop residue, gauge invariant, rescaling residue).
