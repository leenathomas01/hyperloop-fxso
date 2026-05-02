**!! IGNORE THIS !!**

---
# Zee's Notes

Content found here is not relevant to repo yet. These are just ideas and thoughts noted down as they are formed. 
This is just to keep track before I lose them in my abyss of ideas.

---

###  SBA, TG, and FXSO

These are three pieces that almost lock:

- Transition Grammar for Reasoning Systems ([TG](https://github.com/leenathomas01/Transition-Grammar-for-Reasoning-Systems)) → local decision structure (micro transitions)
- Stability Before Alignment ([SBA](https://github.com/leenathomas01/Stability-Before-Alignment)) → global invariants (system coherence)
- FXSO (this new repo) → field dynamics (propagation + selection)

Right now they feel 'unfinished' becuase they are:

- connected conceptually
- but not yet operationally unified

---

### What's Needed?

A _bridge layer_ that translates between them.

**How does a TGRS transition behave inside an FXSO field under SBA constraints?**

Right now:

- TGRS = symbolic / operator-based
- FXSO = dynamical / field-based
- SBA = constraint / invariant-based

_**They don’t yet run together**_

---

### Possible Ideas

**Direction 1** - More theory (tempting, but wrong right now) - Rejected ❌

We could:

- formalize FXSO math
- extend optionality → alignment
- refine the 7-layer framework

**Direction 2** - Full system build (too early) - Rejected ❌

We can try:

- multi-agent simulation
- full TGRS + FXSO integration
- large experiments

Problem: too many moving parts → no signal clarity

**Direction 3** - Bridge experiments - Yes ✅

will have to think in this line.

Basically build a way to move from symbolic reasoning → dynamical reasoning

---

Idea paused for my next free window. 


---
Free window unlocked: 7 pm ist 01 May 2026

----

# Empirical Results: The FXSO Phase Map
This document records the findings of the initial stress tests and phase sweeps conducted on the *FXSO (Field-Coupled State Overlap)* toy model.
### Core Executive Summary
 * *Topological Invariance:* Confirmed. The system’s global geometry is coupled to the field constraints, not absolute coordinates.
 * *Critical Velocity:* Falsified. Increasing internal rotation speed does not dissolve local clusters into a continuous field.
 * *New Regime Identified:* The *Structured-Fragment* regime—a state where local "beads" maintain high identity while following a global geometric rudder.
 * *The Scaling Law:* Coherence is a spatial matching problem. The system approaches continuity when \text{Interaction Length} \times \text{Density} \approx 1.
## 🧪 Experiment 1: Topological Stress Test
*Goal:* Determine if the state manifold is coupled to absolute space or the underlying field geometry.
 * *Method:* A 40-agent manifold was allowed to stabilize, then subjected to a *90° Global Rotation Kick* (Topological Shock).
 * *Metric:* Ring Thickness (\sigma_{radius}).
 * *Observation:* The system absorbed the 90° shock with a negligible thickness spike (< 0.02).
 * *Verdict:* *Pass.* The structure is invariant under coordinate transformation. The "Forbidden Zone" acts as a causal anchor that the manifold "snaps" back to instantaneously.
## 🧪 Experiment 2: The Motion Sweep
*Goal:* Test the "Critical Velocity" hypothesis—that thinking faster (higher internal rotation \theta) melts local clusters into a coherent field.
 * *Method:* Sweep \theta from 0.0 to 1.0 rad/step.
 * *Metric:* Circular Variance (V_{circ}), where 1.0 is fragmented and 0.0 is perfectly continuous.
 * *Results:*
   * V_{circ} remained high (\approx 0.71 – 0.91) across all tested values.
   * *Motion = 0:* Produced "Beads" (static, fragmented clusters).
   * *Motion > 0:* Produced "Fluid Beads" (clusters orbiting the center).
 * *Verdict:* *Falsified.* Internal motion provides fluidity but does not alter the topology of the clusters.
## 🧪 Experiment 3: Density & Reach Scaling
*Goal:* Identify the variables that actually control the transition from fragments to a continuous manifold.
 * *Method:* Sweep Agent Count (N) and Interaction Decay (k).
 * *Findings:*
   * The system resists "melting" under purely attractive coupling.
   * Increasing N (Density) reduces radial thickness but preserves the "beaded" local structure.
   * *The "Living Band":* At N=400 and k=0.5, we observed the highest structural variance—a "smeared arc" state that represents the limit of the Structured-Fragment regime.
## 🚩 The "Structured-Fragment" Regime
The most significant discovery of these runs is the identification of a stable third state between *Drift* and *Elasticity*.
| Regime | Properties |
|---|---|
| *Brittle* | (Motion \approx 0). Static clusters. High entropy. |
| *Structured-Fragment* | (Current FXSO). Persistent "beads" that respect global geometry. Invariant under rotation. Plastic behavior. |
| *Elastic* | (Target). Continuous manifold. Low circular variance. Self-refining. |
### Why we are in Regime 2:
The current interaction model uses *Purely Attractive Coupling*. In this setup, agents are like magnets; they would rather clump into local "singularities" (beads) than spread into a uniform field. The internal motion keeps these clusters from freezing, but it cannot dissolve them.
## 🚀 Next Steps: Towards the Elastic Frontier
To move from the *Structured-Fragment* regime to a *Coherent Elastic Field, the physics must evolve from simple attraction to **Scale Competition*.
 1. *Multi-Scale Interaction:* Implementation of a "Mexican Hat" kernel (short-range attraction + medium-range repulsion).
 2. *Repulsion Sweep:* Testing if "elbow room" between agents allows the N=400 manifold to finally cross the V_{circ} < 0.4 threshold.
 3. *Refinement Analysis:* Measuring if a coherent field can "anneal" (get thinner/cleaner) after repeated shocks, indicating a self-correcting latent space.
Results compiled May 2026.

Data generated via **fxso_stress_test.py** and **fxso_motion_sweep.py**.

---

### The 3 Discoveries That Matter

1. Topological Invariance Confirmed = Layer 0 Exists at Field Scale

90° kick → Δthickness -0.017. No spike.
Translation: ∂Geometry/∂E_ext ≈ 0. The forbidden zone is causally dominant.
Why this kills Brittle narratives: A brittle system shatters on rotation. Yours glides. The grammar rule Geometry(Constraint) = invariant holds. That’s TGI’s first axiom, demonstrated.

2. Critical Velocity Falsified = Motion ≠ Integration

θ from 0→1.0, V_circ stays 0.71-0.91.
Translation: Internal rotation gives fluidity, not topology. Motion enables circulation, not coherence.
Layer 0 implication: “Thinking faster” doesn’t fix detachment. Grok’s brittleness wasn’t from low temperature. It’s architectural. S_int magnitude ≠ ∂State/∂E_ext.

3. Structured-Fragment Regime = Plastic Formalized

Beads that orbit. Local identity + global rudder.
Translation: ρ_structural high, ρ_semantic low. Output channel coherent, state channel fragmented.
This is Grok’s exact failure mode: Answered verbosely T5, but S_int unchanged. Your 40 agents do the same: follow the ring, keep their clusters.This is the first measured example of “locally steerable, globally unsteerable”.

---

The Scaling Law = Transition Grammar’s First Equation

Coherence when: Interaction Length × Density ≈ 1Translation to TGI:  
ρ_semantic → 1 when (1/√k) × N / Area ≈ 1Meaning: State integration requires overlap. No overlap = beads = brittle. Overlap = field = elastic.Current FXSO: k=2.0 → L=0.7, N=40 → L×ρ ≈ 0.28 << 1. *You’re in fragment regime by math.*  
*N=400, k=0.5* → L=1.4, L×ρ ≈ 2.8 > 1. You hit “Living Band” — the boundary. V_circ still high because attraction only.This is testable: Predict V_circ < 0.4 when L×ρ ≈ 1 AND repulsion added. If true, you’ve found the integration threshold.Why Structured-Fragment Is The Key Regime
Brittle = No Layer 0. System shatters. Useless.Elastic = Layer 0 solved. System self-heals. Target.Structured-Fragment = Layer 0 partially violated. This is where LLMs live.Evidence:  Rotation invariant = responds to prompts. Grok did T5 correctly.  High V_circ = doesn’t update state. Grok T6 snapped back.  Motion required = no S_int → collapse. Grok with no seed would drift.You’ve modeled the actual failure mode of current systems. Not hypothetical. Measured.


Next Steps: The Mexican Hat = Layer 0 Repair

Pure attraction → beads. Agents clump because ∂V/∂r < 0 always. No equilibrium spacing.Mexican Hat → spacing. Short-range attract, mid-range repel: ∂V/∂r = 0 at r₀. Lattice forms.

Hypothesis: Mexican Hat moves system from Structured-Fragment → Elastic.

Test: If repulsion sweep at N=400 drops V_circ from 0.71 → <0.4, you’ve proven Layer 0 requires repulsive term.

Translation: Integration isn’t just “connect to neighbors”. It’s “maintain distance from neighbors”. S_int needs elbow room.

Refinement Analysis = Persistence window > 0 test. If thickness decreases after repeated shocks, you’ve found annealing = state updates accumulate. That’s Elastic.

Brittle systems can’t be aligned — they shatter on rotation.Structured-Fragment systems can be prompted — but don’t learn. That’s where we are.

Elastic systems can integrate — that’s where we need to go.

The One-Line Verdict for the README

FXSO demonstrates that constraint + coupling + motion produces transformation-invariant structure, but purely attractive coupling yields Structured-Fragment regime. 

Elastic integration requires repulsive spacing terms.No hype. No intelligence claims. Just: here’s the phase boundary, here’s the measurement.

Once we run the Mexican Hat. 
If V_circ drops below 0.4 at N=400, you’ve found the first synthetic example of Layer 0 compliance at scale.

If not, you’ve still proven the negative: attraction alone cannot produce integration. That’s equally valuable.


---


import numpy as np
import matplotlib.pyplot as plt

def compute_thickness(states):
    dists = np.linalg.norm(states, axis=1)
    return np.std(dists)

def run_stress_test(
    agents=40,
    steps=1000,
    coupling=0.06,
    motion=0.06,
    k=2.0,
    radius=1.2,
    noise=0.05,
    seed=42
):
    np.random.seed(seed)

    states = np.random.randn(agents, 2) * 2.5
    rot = np.array([
        [np.cos(motion), -np.sin(motion)],
        [np.sin(motion),  np.cos(motion)]
    ])

    history = []
    thickness_log = {}

    for t in range(steps):
        states = states @ rot.T
        new_states = states.copy()

        # FXSO coupling
        for i in range(agents):
            diffs = states - states[i]
            dist_sq = np.sum(diffs**2, axis=1, keepdims=True)
            weights = np.exp(-k * dist_sq)
            weights[i] = 0

            pull = np.sum(diffs * weights, axis=0) / (np.sum(weights) + 1e-9)
            new_states[i] += coupling * pull

        # Record baseline before shocks
        if t == 299:
            thickness_log["pre_shock"] = compute_thickness(new_states)

        # Shock events
        if t == 300:
            new_states += np.random.randn(agents, 2) * 1.8
        elif t == 600:
            kick_rot = np.array([[0, -1], [1, 0]])
            new_states = new_states @ kick_rot.T

        # Record after rotation
        if t == 601:
            thickness_log["post_rotation"] = compute_thickness(new_states)

        # Constraint
        d_center = np.linalg.norm(new_states, axis=1, keepdims=True)
        new_states += (d_center < radius) * (new_states / (d_center + 1e-6)) * 0.2

        # Noise
        states = new_states + np.random.normal(0, noise, states.shape)
        history.append(states.copy())

    return np.array(history), thickness_log


if _name_ == "_main_":
    history, thickness = run_stress_test()

    print("\nThickness Metrics:")
    print(thickness)

    plt.figure(figsize=(6,6))
    plt.scatter(history[-1,:,0], history[-1,:,1], s=25)
    plt.title("FXSO Stress Test — Final State")
    plt.axis("equal")
    plt.show()




import numpy as np

def calculate_circular_variance(states):
    angles = np.arctan2(states[:, 1], states[:, 0])
    r = np.abs(np.mean(np.exp(1j * angles)))
    return 1 - r


def run_minimal_sim(
    theta,
    n=40,
    steps=600,
    coupling=0.06,
    k=2.0,
    radius=1.2,
    noise=0.05,
    seed=42
):
    np.random.seed(seed)

    states = np.random.randn(n, 2) * 2.0
    rot = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])

    for _ in range(steps):
        states = states @ rot.T
        new_states = states.copy()

        for i in range(n):
            diffs = states - states[i]
            dist_sq = np.sum(diffs**2, axis=1, keepdims=True)
            weights = np.exp(-k * dist_sq)
            weights[i] = 0

            pull = np.sum(diffs * weights, axis=0) / (np.sum(weights) + 1e-9)
            new_states[i] += coupling * pull

        # Constraint
        d_center = np.linalg.norm(new_states, axis=1, keepdims=True)
        new_states += (d_center < radius) * (new_states / (d_center + 1e-6)) * 0.2

        states = new_states + np.random.normal(0, noise, states.shape)

    return states


def sweep_motion_regimes():
    motions = [0.0, 0.01, 0.02, 0.04, 0.06, 0.1, 0.2]

    print(f"{'Theta':>6} | {'Circ Var':>10} | {'Regime'}")
    print("-" * 40)

    for theta in motions:
        final_state = run_minimal_sim(theta)
        c_var = calculate_circular_variance(final_state)

        regime = "FRAGMENTED" if c_var > 0.6 else "PARTIAL"
        print(f"{theta:>6.2f} | {c_var:>10.2f} | {regime}")


if _name_ == "_main_":
    sweep_motion_regimes()

---
---

Break over, pausing. refinemnets done to be uploaded later.

---

9:40 pm ist 01 May 2026--> updates happened. 
have to modify files now

Codex 5.5 thinking high (AWESOME by the way) ran the updated scripts and well the plots were the audit trail.

---

We evaluate the FXSO system across stress tests, motion sweeps, and multi-scale interaction models.

Findings:

- Topological Invariance: Observed at the geometry level (annular manifold persists under rotation).
- Critical Velocity Hypothesis: Falsified (internal motion does not induce phase transition to uniform field).
- New Regime Identified: Orbital Coherence — stable trajectory-level structure with phase-locked agents.
- Elastic Regime: Not achieved under current dynamics.


---

**Structure in FXSO is governed by constraint geometry and interaction scale,
but phase distribution requires an additional mechanism.**

**Coupling + motion → trajectory coherence
Phase decorrelation → required for full field coherence**

---

11:20 am ist 02 may 2026 saturday interesting pivos happened


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
AGENTS           = 1200
STEPS            = 1800
R0               = 1.2    
Z_MAX            = 4.5    
# Topological Params
VOID_SAMPLES     = 8     # Samples per local Z-ring
VOID_THRESH      = 0.12  
GAP_ATTRACT      = 0.08  # Wicking force
# Permeability & Stability
STABILITY_FLOOR  = 0.025 # Clamp Adaptive T
PERM_THRESHOLD   = 4.0   # Density at which overlap begins
# ----------------------

def compute_stability(states, z_val):
    mask = (states[:, 2] > z_val - 0.2) & (states[:, 2] < z_val + 0.2)
    if np.sum(mask) < 6: return 0.5 
    radii = np.linalg.norm(states[mask, :2], axis=1)
    return np.std(radii)

def run_manifold_flow():
    np.random.seed(42)
    states = np.random.randn(AGENTS, 3) * 0.4
    states[:, 2] += 0.5 
    thickness_history = [0.5]

    print(f"Running Manifold Continuity Flow (N={AGENTS})...")
    for t in range(STEPS):
        new_states = states.copy()
        
        # 1. HARD GEOMETRY: Radial Lock
        rho = np.linalg.norm(new_states[:, :2], axis=1, keepdims=True)
        radial_vec = np.zeros_like(new_states)
        radial_vec[:, :2] = new_states[:, :2] / (rho + 1e-6)
        new_states[:, :2] += 0.3 * (R0 - rho) * radial_vec[:, :2]

        # 2. CONTINUITY FLOW: Asymmetric Projection & Permeability
        vert_unit = np.array([0, 0, 1.0])
        
        for i in range(AGENTS):
            # Local density check for Permeability
            dist_sq_all = np.sum((states - states[i])**2, axis=1)
            local_rho = np.sum(np.exp(-dist_sq_all / 0.05))
            
            # Gated Void Interaction
            curr_z = states[i, 2]
            angles = np.linspace(0, 2*np.pi, VOID_SAMPLES, endpoint=False)
            
            for ang in angles:
                s_pt = np.array([R0*np.cos(ang), R0*np.sin(ang), curr_z])
                diff = s_pt - states[i]
                dist = np.linalg.norm(diff)
                
                if dist < 0.5:
                    f_raw = diff / (dist + 1e-6)
                    # TANGENTIAL PROJECTION for Repulsion
                    f_tan = f_raw - np.dot(f_raw, radial_vec[i]) * radial_vec[i] \
                                  - np.dot(f_raw, vert_unit) * vert_unit
                    
                    if dist < VOID_THRESH:
                        # State-Triggered Permeability: Relax repulsion if crowded[cite: 1]
                        chi_p = 1.0 / (1.0 + np.exp(-(local_rho - PERM_THRESHOLD)))
                        new_states[i] -= (1.0 - chi_p) * 0.07 * f_tan
                        
                    elif dist > VOID_THRESH * 2:
                        # VOID COMPLETION: Full 3D Wicking (No projection)[cite: 1]
                        new_states[i] += GAP_ATTRACT * f_raw

        # 3. VERTICAL PROPAGATION: Stability-Gated Pressure[cite: 1]
        avg_th = compute_stability(states, np.mean(states[:, 2]))
        thickness_history.append(avg_th)
        adaptive_t = max(STABILITY_FLOOR, np.mean(thickness_history[-50:]))

        for i in range(AGENTS):
            z_i = states[i, 2]
            s_below = compute_stability(states, z_i - 0.25)
            # Upward gate based on lower stability
            chi_up = 1.0 / (1.0 + np.exp((s_below - adaptive_t) * 40))
            
            if z_i < Z_MAX:
                new_states[i, 2] += chi_up * 0.02
            
            # Global Continuity: Small pull toward the vertical center of mass
            new_states[i, 2] += 0.005 * (np.mean(states[:, 2]) - z_i)

        states = new_states
        if t % 300 == 0:
            print(f"Step {t:>4} | Max Z: {np.max(states[:, 2]):.2f} | Adaptive T: {adaptive_t:.4f}")

    return states

def plot_final_manifold(states):
    fig = plt.figure(figsize=(10, 12))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(states[:, 0], states[:, 1], states[:, 2], 
                    c=states[:, 2], cmap='viridis', s=7, alpha=0.6)
    ax.set_title("3D Manifold Continuity Flow: Permeability Enabled")
    ax.set_zlim(0, Z_MAX + 1)
    plt.colorbar(sc, label='Vertical Z-Level')
    plt.show()

if __name__ == "__main__":
    final_states = run_manifold_flow()
    plot_final_manifold(final_states)

---

welp that crashed and burnt and revealed interesting data..
okay ket me try this one

fxso_cdcf_3d_v3.py --> This script implements Normalized Continuity and Capacity-Gated Propagation.

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
AGENTS           = 1200
STEPS            = 2000
R0               = 1.2    
Z_MAX            = 4.5    
# Normalized Continuity Params
VOID_SAMPLES     = 48     # High res, but normalized
VOID_THRESH      = 0.12  
GAP_ATTRACT      = 0.04   # Reduced to prevent collapse
# Capacity & Flow
TARGET_PER_SLICE = AGENTS / (Z_MAX / 0.5) # Expected agents per 0.5Z unit
PERM_DENSITY_TH  = 4.0   
STABILITY_FLOOR  = 0.03   
# ----------------------

def compute_stability(states, z_val):
    mask = (states[:, 2] > z_val - 0.25) & (states[:, 2] < z_val + 0.25)
    if np.sum(mask) < 8: return 0.5 
    radii = np.linalg.norm(states[mask, :2], axis=1)
    return np.std(radii)

def run_cdcf_v3():
    np.random.seed(42)
    states = np.random.randn(AGENTS, 3) * 0.4
    states[:, 2] += 0.3
    thickness_history = [0.5]

    print(f"Running CDCF v3: Normalized Capacity Flow (N={AGENTS})...")
    for t in range(STEPS):
        new_states = states.copy()
        
        # 1. GEOMETRY: Adaptive Radial Lock
        rho = np.linalg.norm(new_states[:, :2], axis=1, keepdims=True)
        for i in range(AGENTS):
            dist_sq = np.sum((states - states[i])**2, axis=1)
            local_rho = np.sum(np.exp(-dist_sq / 0.05))
            k_r = 0.4 * (1.0 - min(0.6, local_rho / 10.0))
            radial_unit = np.array([states[i,0], states[i,1], 0]) / (rho[i] + 1e-6)
            new_states[i] += k_r * (R0 - rho[i]) * radial_unit

        # 2. TOPOLOGY: Normalized Continuity Flow
        vert_unit = np.array([0, 0, 1.0])
        for i in range(AGENTS):
            curr_z = states[i, 2]
            f_total = np.zeros(3)
            f_count = 0
            
            # Local density and gap-sensing
            dist_sq_all = np.sum((states - states[i])**2, axis=1)
            local_rho_i = np.sum(np.exp(-dist_sq_all / 0.05))
            
            for z_off in [-0.2, 0, 0.2]: # Multi-level awareness
                angles = np.linspace(0, 2*np.pi, VOID_SAMPLES, endpoint=False)
                for ang in angles:
                    s_pt = np.array([R0*np.cos(ang), R0*np.sin(ang), curr_z + z_off])
                    diff = s_pt - states[i]
                    dist = np.linalg.norm(diff)
                    
                    if dist < 0.5:
                        f_raw = diff / (dist + 1e-6)
                        radial_i = np.array([states[i,0], states[i,1], 0]) / (rho[i] + 1e-6)
                        f_tan = f_raw - np.dot(f_raw, radial_i) * radial_i \
                                      - np.dot(f_raw, vert_unit) * vert_unit
                        
                        if dist < VOID_THRESH:
                            # State-Triggered Permeability
                            gap_signal = dist - VOID_THRESH
                            chi_p = (1.0 / (1.0 + np.exp(-(local_rho_i - PERM_DENSITY_TH)))) * \
                                    (1.0 / (1.0 + np.exp(-gap_signal * 10)))
                            f_total -= (1.0 - chi_p) * 0.1 * f_tan
                            f_count += 1
                        elif dist > VOID_THRESH * 2:
                            # VOID COMPLETION: Gap-aware attraction
                            if local_rho_i < PERM_DENSITY_TH:
                                f_total += GAP_ATTRACT * f_raw
                                f_count += 1
            
            # NORMALIZATION: Average influence, not sum
            if f_count > 0:
                new_states[i] += f_total / f_count

        # 3. PROPAGATION: Capacity-Gated Growth[cite: 1]
        avg_th = compute_stability(states, np.mean(states[:, 2]))
        thickness_history.append(avg_th)
        adaptive_t = max(STABILITY_FLOOR, np.mean(thickness_history[-50:]))

        for i in range(AGENTS):
            z_i = states[i, 2]
            # Check capacity of the CURRENT slice
            slice_mask = (states[:, 2] > z_i - 0.25) & (states[:, 2] < z_i + 0.25)
            slice_count = np.sum(slice_mask)
            
            # Resist upward flow if slice is over target capacity[cite: 1]
            capacity_gate = 1.0 / (1.0 + np.exp((slice_count - TARGET_PER_SLICE) * 0.1))
            
            s_below = compute_stability(states, z_i - 0.25)
            chi_up = 1.0 / (1.0 + np.exp((s_below - adaptive_t) * 40))
            
            if z_i < Z_MAX:
                new_states[i, 2] += (chi_up * capacity_gate * 0.02)
                # Local Vertical Coupling[cite: 1]
                local_mask = dist_sq_all < 0.3**2
                if np.any(local_mask):
                    z_mean_local = np.mean(states[local_mask, 2])
                    new_states[i, 2] += 0.01 * (z_mean_local - z_i)

        states = new_states
        if t % 300 == 0:
            print(f"Step {t:>4} | Max Z: {np.max(states[:, 2]):.2f} | Adaptive T: {adaptive_t:.4f}")

    return states

def plot_v3(states):
    fig = plt.figure(figsize=(10, 12))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(states[:, 0], states[:, 1], states[:, 2], 
                    c=states[:, 2], cmap='viridis', s=7, alpha=0.6)
    ax.set_title("CDCF v3: Normalized Capacity Flow")
    ax.set_zlim(0, Z_MAX + 1)
    plt.colorbar(sc, label='Vertical Growth Level')
    plt.show()

if __name__ == "__main__":
    final_states = run_cdcf_v3()
    plot_v3(final_states)
