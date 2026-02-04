# Traversal Map (v0.2)

## Chosen node order
1. `Q000002`
2. `Q000007`
3. `Q000008`
4. `Q000021`
5. `Q000011`
6. `Q000012`
7. `Q000013`
8. `Q000016`
9. `Q000014`
10. `Q000017`
11. `Q000018`
12. `Q000019`
13. `Q000015`
14. `Q000006`
15. `Q000003`
16. `Q000009`
17. `Q000010`
18. `Q000020`

## Edge sequence used
1. `E000011` (`Q000002 -> Q000007`)
2. `E000004` (`Q000007 -> Q000008`)
3. `E000023` (`Q000008 -> Q000021`, E4 `ledger stability / taxonomy drift`)
4. `E000024` (`Q000021 -> Q000011`, E4 `primitive budget / silent premise`)
5. `E000013` (`Q000011 -> Q000012`)
6. `E000014` (`Q000013 -> Q000016`)
7. `E000015` (`Q000014 -> Q000017`)
8. `E000021` soft adjacency (`Q000011 -> Q000018`)
9. `E000022` (`Q000018 -> Q000019`)
10. `E000016` (`Q000015 -> Q000019`, E4 `local arrow persistence`)
11. `E000018` (`Q000015 -> Q000014`, E4 `constraint-order coupling`)
12. `E000019` (`Q000019 -> Q000017`, E4 `local arrow persistence`)
13. `E000007` (`Q000006 -> Q000003`, E4 `orientation residue`)
14. `E000006` (`Q000003 -> Q000009`, E4 `dimensionless drift`)
15. `E000012` (`Q000009 -> Q000010`)
16. `E000010` (`Q000003 -> Q000010`)
17. `E000005` (`Q000003 -> Q000010`, E4 `observability equivalence class`)
18. `E000017` (`Q000020 -> Q000016`)

## Critical seams
- Method remains procedural unless passed through explicit handoff bridge (`Q000021`, `E000023`, `E000024`).
- E4 bridges (`E000016`, `E000018`, `E000019`) are chart translations, not proofs of identity between claims.
- Soft adjacency (`E000021`) is suggestive only and cannot bear strong inferential weight.
- Physics block constrains detectability classes; it does not derive ontology.
- Intentionality transfer (`E000017`) supports bridge logic, not full cognitive closure.

## Placeholder next nodes (max 5)
- Personal identity continuity test node
- Narrative regress cutoff criterion node
- Handoff failure-mode taxonomy node
- Cross-chart negation stability node
- Search-space bias calibration node
