# Complexical Induction (CI) — One‑Page Functional Overview  
Version: **v0.1** • Generated: **2026-01-29T00:00:00Z**

## What CI is (in one sentence)
**Complexical Induction (CI)** is a method for navigating hard questions by mapping *where explanations fail* (their **leaks**) and then choosing **discriminators** (tests/transformations) that can shrink the space of viable stories.

---

## The objects CI manipulates

### 1) A *Question*
A well-posed “why / how / what grounds X?” prompt.

### 2) A *Chart* (a description frame)
A representation of the question: equations, causal graphs, narratives, models, metaphors, measurement pipelines, etc.  
CI assumes many disputes are **chart mismatches**, not “facts vs facts.”

### 3) A *Leak*
A structural seam where the current chart fails. CI uses an L1–L6 ladder (you can rename later, but keep the *shape* of the ladder stable):

- **L1 — Definition leak:** key terms not pinned down (category drift).  
- **L2 — Measurement leak:** observation pipeline ambiguous or biased.  
- **L3 — Mechanism leak:** causal mechanism under-specified (missing variables/links).  
- **L4 — Scaling/aggregation leak:** micro↔macro mapping unclear (coarse-graining, emergence).  
- **L5 — Boundary/ground leak:** assumptions about “outside the system” hidden (observer, initial conditions, normativity).  
- **L6 — Underdetermination leak:** multiple incompatible stories fit all current evidence (needs new discriminators).

### 4) An *Invariant*
A constraint that must remain stable across transformations (a “glue key”): conservation laws, robustness targets, symmetries, accountability practices, etc.

### 5) A *Discriminator*
A test or transformation that **splits** the hypothesis space. Common patterns CI likes:
- **intervention**, **ablation**, **orthogonal probe**, **stress ramp**, **ensemble split**, **interface scatter**, **hysteresis**.

---

## How CI functions (the loop)

### Step 0 — Normalize the question
Write the question as:  
**“What must be true for X to be the case, and what would we observe if it weren’t?”**

### Step 1 — Enumerate plausible charts (2–5 is enough)
Example: mathematical model, causal model, narrative model, measurement model.  
Don’t merge them yet.

### Step 2 — Locate leaks per chart
For each chart, identify the dominant leak(s): L1..L6.  
CI payoff comes from being explicit: *“This chart fails here, not everywhere.”*

### Step 3 — Extract invariants
Write 1–3 invariants you refuse to give up without explicit cost.  
These become the graph’s “glue keys.”

### Step 4 — Generate discriminators
Pick 1–3 discriminators that would actually reduce ambiguity.  
A discriminator must be capable of yielding **different expected outcomes** under competing hypotheses/charts.

### Step 5 — Route the next move
CI does not “solve” the question directly. It produces the **next best action**:
- switch charts,
- refine measurement,
- add mechanism variable,
- move to a new regime (stress ramp),
- or admit L6 and propose new data.

### Step 6 — Ledger the update
Record: (question, chart, leaks, invariants, discriminator, outcome).  
CI progresses by accumulating **structured residuals** (what broke, where, and why).

---

## Outputs CI is expected to produce
1. **Leak profile** (what kind of failure this is)  
2. **Chart map** (which frames are in play)  
3. **Invariant set** (what’s being held fixed)  
4. **Discriminator plan** (how to split hypotheses)  
5. **Next action** (what to do in research / writing / simulation)  
6. Optionally: a graph entry for LCG (node + typed edges)

---

## Guardrails (anti-bullsh*t constraints)
- **No leak, no move.** If you can’t name the seam, you’re just riffing.  
- **Discriminators over metaphors.** Metaphor is allowed, but it must cash out into a split.  
- **Declare your chart.** Many arguments fail because charts silently swap mid-sentence.  
- **Don’t confuse compatibility with truth.** Empirical equivalence (L6) is common.

---

## Tiny example (template-level)
**Question:** Why do proteins fold fast despite huge conformational spaces?  
**Charts:** “random search” vs “energy landscape/funnel.”  
**Leak:** random-search chart has L4/L6 leak (wrong scaling + underdetermination).  
**Invariant:** typical fold times cluster within regimes.  
**Discriminator:** stress ramp (temperature/noise schedule) + hysteresis tests.  
**Next move:** simulate/measure folding pathways under ramps; look for funnel signatures vs trap-dominated signatures.

---

## CI in one line
**Name the seam → choose the split → update the ledger → repeat.**
