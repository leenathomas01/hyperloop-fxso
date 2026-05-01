# Empirical Results: The FXSO Phase Map

This document records findings from stress tests and phase sweeps conducted on the FXSO toy model after adding a central constraint geometry (forbidden zone). It follows the baseline results in `07_experiments/minimal_experiments.md` and extends them into constrained dynamics.

---

## Definitions

- **Thickness (σ_radius):** Standard deviation of agent distances from the constraint center. Low = tight structure. High = diffuse cloud.
- **Circular Variance (V_circ):** Angular dispersion of agents around the manifold. 0 = uniform ring. 1 = fully clustered.
- **Density (ρ):** Agents per unit circumference — ρ = N / (2πR).
- **Interaction Length (λ):** Effective radius of influence from the decay kernel — λ ∝ 1/√k.
- **Annealing Score:** pre_shock_thickness − final_thickness. Positive = system tightened under stress. Negative = system diffused.

---

## Executive Summary

| Finding | Status |
|---------|--------|
| Topological invariance | **Confirmed** |
| Critical velocity hypothesis | **Falsified** |
| Ring attractor formation | **Not achieved** (thick annulus instead) |
| Self-refining dynamics | **Not observed** |
| Structured-Fragment regime | **Identified** — new stable regime between brittle and elastic |
| Governing scaling law | **Proposed** — coherence requires λ × ρ ≈ 1 |

---

## Experiment 1 — Topological Stress Test

**Goal:** Determine whether system structure is coupled to absolute coordinates or to the underlying constraint geometry.

**Setup:** 40 agents, coupling=0.06, motion=0.06, forbidden zone radius=1.2. Two shock events: random noise injection at t=300 (magnitude 1.8), 90° global rotation at t=600.

**Metrics logged:**
- Thickness at t=299 (pre-shock baseline)
- Thickness at t=601 (post-rotation, immediate)
- Final thickness at t=999
- Annealing score (pre_shock − final)

**Results:**

| Metric | Motion=0.06 | Motion=0.0 (Kill Test) |
|--------|-------------|----------------------|
| Baseline thickness (t=299) | 1.45 | 1.21 |
| Post-random shock peak | ~2.1 | ~1.7 |
| Rotation kick Δthickness | −0.017 (glide) | −0.013 (glide) |
| Final thickness (t=999) | 2.27 | 1.56 |
| Annealing score | −0.82 (diffused) | −0.35 (diffused) |
| Kill test result | Rotating annulus | Static beads |

**Findings:**

The 90° rotation was absorbed with near-zero thickness spike in both runs. Green trajectories (post-rotation) closely overlay blue trajectories (post-random shock), confirming the structure is defined in relative space — by distance from the constraint — not by absolute coordinates.

**Verdict: Topological invariance confirmed.** The forbidden zone acts as a causal anchor. The system's geometric class survives coordinate transformation.

Annealing score was negative in both runs — the system diffused rather than tightened under repeated stress. No self-refining dynamics observed.

**Kill test:** Motion=0 produced 6–7 static bead clusters at fixed angular positions (circular variance ≈ 0.82). No continuous ring or circulation. Internal motion is required for global coherence; without it, the system fragments into local minima.

---

## Experiment 2 — Motion Sweep

**Goal:** Test the "Critical Velocity" hypothesis — that increasing internal rotation speed (θ) melts local clusters into a coherent distributed field.

**Setup:** 40 agents, swept θ ∈ [0.0, 1.0], 3–4 seeds per value, 600 steps per run. Metrics: circular variance and thickness at final state.

**Results:**

| θ | Circ Var (mean ± std) | Thickness | Regime |
|---|----------------------|-----------|--------|
| 0.00 | 0.83 ± 0.08 | 0.97 | Fragmented |
| 0.01 | 0.84 ± 0.10 | 0.76 | Fragmented |
| 0.02 | 0.75 ± 0.12 | 0.80 | Fragmented |
| 0.04 | 0.73 ± 0.19 | 0.96 | Fragmented |
| 0.06 | 0.80 ± 0.17 | 1.17 | Fragmented |
| 0.10 | 0.84 ± 0.14 | 1.24 | Fragmented |

V_circ remained high (0.71–0.91) across all tested values. No transition to a distributed or continuous manifold was observed at any rotation speed, including θ = 1.0 rad/step.

**Verdict: Critical velocity hypothesis falsified** (within this formulation).

Internal motion affects the *dynamics* of clusters — beads become fluid rather than static — but does not alter their *topology*. The system consistently forms local attractors regardless of motion speed. Motion is necessary for fluidity but not sufficient for coherence.

**Mechanistic explanation:** Purely attractive local coupling creates local minima faster than rotation can dissolve them. Even at high θ, agents re-cluster between rotational steps because the attraction timescale is shorter than the mixing timescale.

---

## Experiment 3 — Density and Reach Sweep

**Goal:** Identify the actual control variables for the fragmented → coherent transition.

**Hypothesis:** Coherence emerges when interaction length (λ) matches average inter-agent spacing along the constraint manifold. Formally: λ × ρ ≈ 1, where ρ = N / (2πR).

**Setup:** Swept N ∈ {40, 100, 400} and k ∈ {2.0, 1.0, 0.5} (lower k = longer reach). Weak global repulsion added (α = 0.025) to prevent trivial collapse. Multi-seed averaging.

**Results:**

| N | k | Thickness | Circ Var | Struct Var | Regime |
|---|---|-----------|----------|------------|--------|
| 40 | 2.0 | 1.21 | 0.93 | 7.4 | Fragmented |
| 100 | 2.0 | 1.00 | 0.84 | 18.5 | Fragmented |
| 400 | 2.0 | 0.95 | 0.93 | 39.6 | Fragmented |
| 40 | 1.0 | 1.11 | 0.93 | 15.3 | Fragmented |
| 100 | 1.0 | 0.96 | 0.79 | 27.0 | Fragmented |
| 400 | 1.0 | 0.68 | 0.93 | 39.1 | Fragmented |
| 40 | 0.5 | 0.50 | 0.84 | 20.9 | Fragmented |
| 100 | 0.5 | 0.39 | 0.57 | 52.9 | Approaching boundary |
| 400 | 0.5 | 0.30 | 0.83 | 90.8 | Highest structure seen |

The bottom-right corner (N=400, k=0.5) showed the richest internal structure (Struct Var ≈ 91), the thinnest annulus (thickness 0.30), and the highest local variation — a "smeared arc" state representing the limit of the current formulation. Circular variance remained high, indicating angular fragmentation persists even as radial coherence improves.

**The governing law, as derived:**

```
Coherence emerges when:
    interaction_length × density_along_manifold ≈ 1

Where:
    λ  = 1/√k          (interaction reach from decay kernel)
    ρ  = N / (2πR)     (agent density along manifold)
    Gap = (2πR) / N    (average inter-agent spacing)

Threshold: λ ≥ Gap
```

The empty space (forbidden zone) is the anchor — it projects agents onto a 1D manifold, making density and reach the relevant spatial scales. Without the constraint, agents exist in 2D and no coherence condition applies.

**Verdict:** The data confirm the direction of the law but do not yet show a clean crossing. The system is at the boundary of the predicted coherent regime but has not crossed it under purely attractive coupling.

---

## The Structured-Fragment Regime

The most significant outcome of these experiments is the identification of a stable intermediate dynamical phase not anticipated in the original framework.

| Regime | Properties | Status |
|--------|-----------|--------|
| **Brittle** | Motion ≈ 0. Static clusters. No global circulation. | Confirmed |
| **Structured-Fragment** | Motion > 0. Fluid beads. Global geometry preserved. Invariant under rotation. | **Identified — this is the current system** |
| **Elastic** | Continuous manifold. Low V_circ. Stable thickness. Survives perturbations. | Not yet reached |

The Structured-Fragment regime is both stable and invariant under perturbation, suggesting it is not a transient artifact but a distinct dynamical phase. The system maintains:
- local identity (beads persist)
- global geometry (annular class survives rotation)
- dynamical fluidity (motion prevents freezing)

This combination is non-trivial. Most constrained systems give you one or two of these properties, not all three simultaneously.

---

## What Was Not Found

These are clean negative results, not gaps:

- **No critical velocity** — motion does not drive a fragmented → coherent transition
- **No self-refining dynamics** — repeated stress diffuses rather than tightens the system
- **No ring attractor** — the system forms a thick annular cloud, not a narrow ring
- **No microstate integration** — geometry-level invariance does not imply state-level coherence

These negatives narrow the conditions required for the elastic regime.

---

## Next Step: Multi-Scale Interaction

Pure attractive coupling cannot produce a continuous distributed phase. The physics must introduce competing forces across scales. The minimal modification is a Mexican Hat (DoG) interaction kernel:

```python
def weights_mhat(dist_sq, k_attract=2.0, k_repel=0.5, r0=1.0, beta=0.3):
    attract = np.exp(-k_attract * dist_sq)
    repel   = -np.exp(-k_repel * (dist_sq - r0)**2)
    return attract + beta * repel
```

**Hypothesis:** With N=400, k_attract=0.5, k_repel=0.2, this produces V_circ < 0.5 and stable thickness — the first entry into the elastic regime.

**Test:** Run at N=400 with the mhat kernel. Apply 90° rotation kick. Measure whether V_circ drops and whether the structure survives the kick. If both: elastic regime demonstrated. If not: coherence requires more than pairwise potentials.

See `fxso_mhat_experiment.py` (to be added) for the implementation.

---

*Results compiled May 2026. Experiments run across Grok, Claude, and Gemini sandboxes with consistent parameter sets. Scripts: `fxso_stress_test.py`, `fxso_motion_sweep.py`.*
