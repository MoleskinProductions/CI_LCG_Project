# Constellations

Clustering used edge-aware rules: E3 edges were treated as strongest cohesion signals, E4 edges as chart-bridge indicators, and E1 edges as weak similarity only.

## Primary/Secondary Assignment (All Nodes)

| Node | Title | Primary | Secondary | Bridge Node |
|---|---|---|---|---|
| Q000001 | Non-Cessation and Chaos/Order Question | C2_Ontology_Ground_Inversion | C5_Mind_Intentionality | No |
| Q000002 | Formalization Request and Logic Background | C1_CI_Method | C2_Ontology_Ground_Inversion | Yes (E4) |
| Q000003 | Question on Wilson Loops | C3_Physics_Gauge_Detectability | C2_Ontology_Ground_Inversion | Yes (E4) |
| Q000004 | Question About Physical Rules | C2_Ontology_Ground_Inversion | C3_Physics_Gauge_Detectability | No |
| Q000005 | Gravity as the First Force? | C3_Physics_Gauge_Detectability | C2_Ontology_Ground_Inversion | No |
| Q000006 | Magnetism as Initial Distinction? | C3_Physics_Gauge_Detectability | C2_Ontology_Ground_Inversion | Yes (E4) |
| Q000007 | Entry Point Leaks and Actionability Request | C1_CI_Method | C2_Ontology_Ground_Inversion | Yes (E4) |
| Q000008 | Request for Algorithmic Agential Loop | C1_CI_Method | C2_Ontology_Ground_Inversion | Yes (E4) |
| Q000009 | Uniform Rescaling Is Undetectable | C3_Physics_Gauge_Detectability | C2_Ontology_Ground_Inversion | Yes (E4) |
| Q000010 | Requirements for a Good Gauge Theory | C3_Physics_Gauge_Detectability | C2_Ontology_Ground_Inversion | Yes (E4) |
| Q000011 | Inside/Out/Backwards Meaning | C2_Ontology_Ground_Inversion | C1_CI_Method | No |
| Q000012 | Constraint + Order + Memory | C2_Ontology_Ground_Inversion | C1_CI_Method | No |
| Q000013 | Duality as Self-Differentiation | C2_Ontology_Ground_Inversion | C5_Mind_Intentionality | No |
| Q000014 | Ground as Structured Differentiation | C2_Ontology_Ground_Inversion | C3_Physics_Gauge_Detectability | Yes (E4) |
| Q000015 | Gravity as Persistent Self-Relation | C4_Time_Identity | C3_Physics_Gauge_Detectability, C2_Ontology_Ground_Inversion | Yes (E4) |
| Q000016 | Existence as Continual Difference | C2_Ontology_Ground_Inversion | C5_Mind_Intentionality | No |
| Q000017 | Negative Ground Statement | C2_Ontology_Ground_Inversion | C4_Time_Identity | Yes (E4) |
| Q000018 | Division as Irreducible Process | C2_Ontology_Ground_Inversion | C1_CI_Method | No |
| Q000019 | No Global Time Direction | C4_Time_Identity | C3_Physics_Gauge_Detectability | Yes (E4) |
| Q000020 | Intentionality Without Desire | C5_Mind_Intentionality | C2_Ontology_Ground_Inversion | No |

## C1_CI_Method

Method and workflow stabilization cluster for formalization boundaries, entry-point leak control, and ledgered procedure loops. Its center of gravity is operational: keep chart transitions explicit, make discriminator usage auditable, and reduce untyped seam drift.

### Nodes
- Q000002: Formalization Request and Logic Background
- Q000007: Entry Point Leaks and Actionability Request
- Q000008: Request for Algorithmic Agential Loop

### Internal spine edges
- E000011 (E3_DiscriminatorTransfer, w=0.6): Q000002 -> Q000007
- E000002 (E4_ChartBridge, w=0.6): Q000002 -> Q000007
- E000003 (E4_ChartBridge, w=0.6): Q000002 -> Q000008
- E000004 (E4_ChartBridge, w=0.6): Q000007 -> Q000008

### External interfaces
- None in current edge set.

## C2_Ontology_Ground_Inversion

Ontology and ground-formation cluster focused on distinction, inversion, division, and the structure of persistence through change. This constellation holds the narrative-to-axiom bridge for non-positivist ground claims and tests whether those claims remain stable under restatement.

### Nodes
- Q000001: Non-Cessation and Chaos/Order Question
- Q000004: Question About Physical Rules
- Q000011: Inside/Out/Backwards Meaning
- Q000012: Constraint + Order + Memory
- Q000013: Duality as Self-Differentiation
- Q000014: Ground as Structured Differentiation
- Q000016: Existence as Continual Difference
- Q000017: Negative Ground Statement
- Q000018: Division as Irreducible Process

### Internal spine edges
- E000013 (E3_DiscriminatorTransfer, w=0.7): Q000011 -> Q000012
- E000014 (E3_DiscriminatorTransfer, w=0.7): Q000013 -> Q000016
- E000015 (E3_DiscriminatorTransfer, w=0.7): Q000014 -> Q000017
- E000001 (E1_SharedLeak, w=0.4): Q000001 -> Q000004
- E000020 (E1_SharedLeak, w=0.4): Q000018 -> Q000013
- E000021 (E1_SharedLeak, w=0.4): Q000011 -> Q000018

### External interfaces
- Touches C3_Physics_Gauge_Detectability via edges E000008; bridge nodes: None.
- Touches C4_Time_Identity via edges E000018, E000019; bridge nodes: Q000014, Q000015, Q000017, Q000019.
- Touches C5_Mind_Intentionality via edges E000017; bridge nodes: None.

## C3_Physics_Gauge_Detectability

Physics-facing detectability cluster around gauge freedom, loop residues, observable admissibility, and measurement-level constraints. It captures which structures survive re-description and which are artifacts of local chart choice.

### Nodes
- Q000003: Question on Wilson Loops
- Q000005: Gravity as the First Force?
- Q000006: Magnetism as Initial Distinction?
- Q000009: Uniform Rescaling Is Undetectable
- Q000010: Requirements for a Good Gauge Theory

### Internal spine edges
- E000010 (E3_DiscriminatorTransfer, w=0.8): Q000003 -> Q000010
- E000012 (E3_DiscriminatorTransfer, w=0.7): Q000009 -> Q000010
- E000005 (E4_ChartBridge, w=0.6): Q000003 -> Q000010
- E000006 (E4_ChartBridge, w=0.6): Q000003 -> Q000009
- E000007 (E4_ChartBridge, w=0.6): Q000006 -> Q000003

### External interfaces
- Touches C2_Ontology_Ground_Inversion via edges E000008; bridge nodes: None.

## C4_Time_Identity

Time-direction and persistence cluster centered on local arrow structure and identity-through-relation in physically loaded settings. Current structure is small but strategically cross-connected to ontology through chart-bridge edges.

### Nodes
- Q000015: Gravity as Persistent Self-Relation
- Q000019: No Global Time Direction

### Internal spine edges
- E000016 (E3_DiscriminatorTransfer, w=0.7): Q000015 -> Q000019

### External interfaces
- Touches C2_Ontology_Ground_Inversion via edges E000018, E000019; bridge nodes: Q000014, Q000015, Q000017, Q000019.

## C5_Mind_Intentionality

Intentionality and agency cluster for directionality without desire-language and narrative-cognitive framing pressure. It is currently represented by a single anchor node and interfaces primarily with ontology via discriminator transfer.

### Nodes
- Q000020: Intentionality Without Desire

### Internal spine edges
- None yet (no internal edges in current graph).

### External interfaces
- Touches C2_Ontology_Ground_Inversion via edges E000017; bridge nodes: None.
