## Quick start

If you're new to the framework:

1. Start with Experiment 4 (anti-entropy)
2. Then run Experiment 1 (trajectory structure)
3. Then try Experiment 3 (compatibility bandwidth)

These three together test the core claims with minimal setup.

---
# 07 — Minimal Experiments: First Tests

These are not full research programs. They are small, realistic starting points — things someone with a GPU, a few days, and relevant expertise could actually try. The goal is not to prove the framework but to make its key claims legible and testable.

Each experiment is designed to probe one specific claim. Falsification is as useful as confirmation.

---

## Experiment 1 — Do loops create coherent internal trajectories?

**Hypothesis:** Hyperloop's repeated loop passes produce meaningfully differentiated internal representations that evolve in a structured, non-random way across iterations — not just noisy oscillations around a fixed point.

**What this tests:** The foundational claim that agents with internal loops behave as trajectory manifolds rather than static states. If loop iterations produce random or nearly identical representations, the entire trajectory-manifold framing collapses.

**Setup:**
- A pretrained Hyperloop model (or any looped Transformer — the paper's architecture, a Universal Transformer, or a simple weight-tied model)
- Alternatively: train a tiny looped model from scratch on a small dataset (e.g., WikiText-2, a few hours on a single GPU)
- A set of ~500 diverse input prompts

**Procedure:**
1. Run each prompt through the model, extracting the residual stream state after each loop iteration (before the end block)
2. For each prompt, you now have L state vectors (one per loop) — your "trajectory"
3. Compute pairwise cosine similarity between loop states (loop 1 vs 2, 1 vs 3, 2 vs 3, etc.)
4. Compute the **trajectory curvature**: how much direction changes between consecutive loops (angle between successive difference vectors)
5. Compare across: (a) different prompts on the same model, (b) same prompts on looped vs non-looped model of same depth

**Expected signal:**
- Loop states should be meaningfully different (cosine similarity < 1.0, ideally showing a consistent pattern of change)
- Curvature should be non-random — similar prompts should produce similar trajectory shapes
- The Hyperloop paper's Figure 3 already shows lower cross-loop similarity for Hyperloop vs vanilla looped — this experiment asks whether that difference is *structured*, not just noisy

**Failure mode:**
- Loop states are nearly identical (similarity > 0.99) → loops are not doing meaningful work
- Trajectory shapes are random across similar prompts → no coherent manifold structure
- Curvature is indistinguishable from a non-looped model of same depth → internal iteration adds nothing beyond depth

**Note:** The Hyperloop paper already reports representation similarity (Table 8). This experiment goes further by asking about *trajectory structure*, not just pairwise similarity.

---

## Experiment 2 — Can relay vs diffusion regimes be observed?

**Hypothesis:** In a multi-agent system, influence propagation transitions from relay-like (discrete, hop-by-hop) to diffusion-like (continuous, percolating) as overlap between agent internal states increases. This transition is observable as a qualitative change in how perturbations spread.

**What this tests:** The propagation regime model. If no such transition exists — if propagation is always relay-like regardless of overlap — the relay ↔ diffusion framework is not a useful description of these systems.

**Setup:**
- A simple simulation (no LLMs required): N agents, each represented as a vector in R^d
- Each agent has an "internal state" that evolves via a fixed recurrent update (a simple RNN cell or even a linear map)
- Agents interact by mixing their states with neighbors, weighted by cosine similarity (overlap)
- Start with a small perturbation in one agent and track how it spreads

**Procedure:**
1. Initialize N=20 agents with random states in R^64
2. Run for T=50 timesteps. At each step: (a) update each agent's internal state via recurrent map, (b) mix states with neighbors weighted by overlap
3. At t=10, perturb agent 0 by adding a structured signal (a fixed vector)
4. Track the signal's spread: at each subsequent timestep, measure cosine similarity between each agent's state and the original signal
5. **Vary the coupling strength** (the weight given to neighbor states in the mixing step) across runs: low (0.1), medium (0.5), high (0.9)
6. Plot spread as a function of time and agent distance from the perturbation source

**Expected signal:**
- Low coupling → signal decays within 1-2 hops, clear relay structure, signal degrades with each hop
- High coupling → signal spreads to all agents within a few timesteps, gradient rather than discrete front
- A regime transition should be visible somewhere in the middle — a qualitative change in spread dynamics, not just a smooth gradient

**Failure mode:**
- Spread is always relay-like regardless of coupling strength → diffusion regime does not emerge from this mechanism
- Spread is always diffusion-like → the relay regime is not a natural state of these systems
- No clear transition → the relay ↔ diffusion distinction is not a useful model for this type of system

**Extensions:** Replace the simple recurrent map with actual Hyperloop loop iterations. Does increasing loop depth shift the system toward diffusion?

---

## Experiment 3 — Does compatibility bandwidth correlate with generalization?

**Hypothesis:** A pattern's "compatibility bandwidth" — how many distinct contexts it survives without collapsing — is a label-free proxy for generalization. Representations with high compatibility bandwidth should generalize better to held-out tasks.

**What this tests:** Nugget 7. If compatibility bandwidth does not correlate with generalization, it is not a useful construct for anticipatory selection.

**Setup:**
- Any pretrained language model (GPT-2 scale is fine — no large model needed)
- A probing setup: extract intermediate representations for a set of inputs, train linear probes on those representations for multiple tasks
- Tasks: e.g., sentiment, topic, syntactic role, named entity — whatever has small labeled datasets available (SST-2, TREC, CoNLL-2003 subsets)

**Procedure:**
1. Extract representations from a fixed layer for ~1000 inputs
2. For each representation, compute **compatibility bandwidth**: run the representation through N=10 small perturbations (add Gaussian noise at varying scales) and measure how stable the linear probe prediction is across perturbations. Bandwidth = average prediction stability across contexts.
3. Separately, measure generalization: train a probe on 80% of each task's data, test on 20%. This is your ground truth for "does this representation generalize?"
4. Correlate per-example compatibility bandwidth with per-example probe accuracy on held-out data
5. Repeat across multiple layers to see if the correlation is layer-dependent

**Expected signal:**
- Positive correlation between compatibility bandwidth and held-out probe accuracy
- Correlation should be stronger in later layers (where representations are more semantically structured)
- The correlation should hold across multiple tasks, not just one

**Failure mode:**
- No correlation → compatibility bandwidth is not a useful proxy for generalization
- Correlation only holds for one task → the measure is task-specific, not general
- Compatibility bandwidth correlates with representation norm or other trivial properties → it's not measuring what we think it is

**Note:** This experiment uses existing models and existing datasets. No training required beyond small linear probes.

---

## Experiment 4 — Do loops act as anti-entropy mechanisms?

**Hypothesis:** Internal loop iterations in a looped Transformer reduce representational entropy across passes — coherent signals are amplified, incoherent fluctuations suppressed. A looped model should show decreasing entropy in its internal representations across loop iterations, especially for structured inputs vs noise.

**What this tests:** Nugget 9. If loop iterations increase or maintain entropy rather than reducing it, they are not acting as anti-entropy mechanisms — they are just adding compute.

**Setup:**
- A looped Transformer (or simple weight-tied RNN as a proxy)
- Two input sets: (a) natural language sentences (structured), (b) random token sequences (noise)
- ~200 examples of each

**Procedure:**
1. Run each input through the model, extracting the residual stream after each loop iteration
2. For each loop state, compute **representational entropy**: fit a PCA to the batch of states at that loop, measure the explained variance ratio. High entropy = variance spread across many dimensions. Low entropy = variance concentrated in few dimensions.
3. Plot entropy as a function of loop iteration, separately for structured vs noise inputs
4. Also measure **inter-example similarity** at each loop: do structured inputs converge toward similar representations while noise inputs remain scattered?

**Expected signal:**
- Structured inputs: entropy decreases (or concentrates) across loops — representations converge toward coherent attractors
- Noise inputs: entropy remains high or increases — no convergence
- The gap between structured and noise entropy should widen with more loops
- This effect should be stronger in Hyperloop (with hyper-connections) than vanilla looped Transformers

**Failure mode:**
- Entropy decreases equally for structured and noise inputs → loops are just compressing everything, not selectively amplifying coherence
- Entropy increases for all inputs → loops are adding noise, not reducing it
- No difference between looped and non-looped models at same depth → the looping mechanism specifically is not responsible for any observed effect

**Note:** This experiment can be run on a tiny model (even 10M parameters) trained for a short time. The mechanism being tested is architectural, not scale-dependent.

---

## Experiment 5 — Does field-based coupling produce emergent coherence?

**Hypothesis:** Agents interacting via simple overlap-based coupling — with no explicit message passing — can self-organize into coherent shared trajectories under noise and internal dynamics. Coherence is a function of coupling strength relative to noise, not of any pre-programmed coordination.

This is not a synchronization model; agents are not forced into identical states, but may form structured, partially aligned trajectories.

**What this tests:** A minimal instantiation of the FXSO hypothesis: that coupling via shared state space is sufficient to produce coordinated structure without discrete communication. This bridges Experiment 2 (propagation regimes) and Experiment 6 (self-refinement) — it is the most visceral, visualizable entry point in the set. If coherence does not emerge from overlap alone, the field-coupling framing needs additional mechanisms before it can support the rest of the framework.

**Setup:**
- Python with numpy (matplotlib optional but recommended for visualization)
- Agents as 2D vectors evolving under a simple internal transformation (rotation matrix — a minimal proxy for Hyperloop's internal loop)
- A shared coordinate space where proximity determines coupling strength

**Procedure:**
1. Initialize 2–10 agents with random 2D states
2. At each timestep, apply a small fixed rotation to each agent's state (internal loop)
3. For each agent, compute distance-weighted pull toward others — coupling force proportional to proximity, not global averaging
4. Add Gaussian noise at each step (field entropy)
5. Track: trajectory variance, inter-agent distance over time, visual convergence/divergence patterns
6. Vary coupling strength across runs to find the transition between regimes

**Expected signal:**
- A "Goldilocks zone" where coupling overcomes noise but doesn't collapse diversity: agents form coherent but non-identical trajectories
- Emergent shared dynamics that were not pre-programmed — structure arising from overlap alone
- Three visible regimes as coupling increases: drift (no interaction) → coherence (structured alignment) → collapse (single degenerate attractor)

**Failure mode:**
- **Collapse** — agents converge to a single point immediately (coupling too high, relay regime dominates)
- **Drift** — agents never influence each other, wander independently (coupling too low, no field effect)
- **Noise dominance** — no stable structure forms regardless of coupling strength (field-based coupling insufficient without additional mechanisms)

**Interpretation:** If coherence emerges in a specific parameter regime, it supports the claim that field-based interaction can produce structured coordination without message passing. If not, it suggests overlap alone is insufficient and additional mechanisms (constraints, loops, anisotropy) are required — which is itself a useful result.

**Implementation:** See `07_experiments/fxso_toy.py` for a runnable starting point.

```python
import numpy as np

def run_fxso_toy(agents=5, steps=500, coupling=0.02, noise=0.01):
    """
    Minimal FXSO field-coupling simulation.
    
    agents:   number of agents
    steps:    timesteps to run
    coupling: field coupling strength (try 0.005 to 0.1)
    noise:    Gaussian noise scale (field entropy)
    
    Returns final agent states.
    """
    # Initialize agents as random 2D states
    states = np.random.randn(agents, 2)
    
    # Internal loop: small rotation matrix (proxy for Hyperloop iterations)
    theta = 0.05
    rot = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])
    
    trajectory = []
    
    for _ in range(steps):
        # 1. Internal loop transformation
        states = states @ rot.T
        
        # 2. Field coupling — proximity-weighted, not global averaging
        new_states = states.copy()
        for i in range(agents):
            diffs = states - states[i]
            distances = np.linalg.norm(diffs, axis=1, keepdims=True) + 1e-6
            weights = np.exp(-distances)          # proximity decay
            new_states[i] += np.sum(diffs * weights * coupling, axis=0)
        states = new_states
        
        # 3. Noise injection (field entropy)
        states += np.random.normal(0, noise, states.shape)
        
        trajectory.append(states.copy())
    
    return states, np.array(trajectory)


# Quick sweep across coupling strengths
if __name__ == "__main__":
    for c in [0.005, 0.02, 0.05, 0.1]:
        final, traj = run_fxso_toy(agents=5, coupling=c)
        variance = np.var(traj[-100:], axis=1).mean()  # variance over last 100 steps
        spread = np.std(final, axis=0).mean()           # final inter-agent spread
        print(f"coupling={c:.3f} | trajectory_variance={variance:.4f} | final_spread={spread:.4f}")
```

**What to look for when you run it:**
- `coupling=0.005`: agents drift independently (drift regime)
- `coupling=0.02–0.05`: agents orbit together with structure (coherence regime — this is the interesting zone)
- `coupling=0.1+`: agents collapse toward a single point (collapse regime)

Plotting `traj[:, :, 0]` vs `traj[:, :, 1]` for each agent will make the regime transition immediately visible.

---

## Experiment 6 — Does self-refining constraint geometry reduce spurious attractors?

**Hypothesis:** A simple dynamical system where constraints update based on local failure signals will, over time, produce fewer spurious stable states — states that are stable but inconsistent with the intended valid manifold.

**What this tests:** The self-refinement layer. This is the most abstract claim in the framework and the hardest to test in LLMs directly. A simple simulation can probe the core mechanism.

**Setup:**
- A low-dimensional dynamical system (2D or 3D is sufficient for visualization)
- Define a "valid manifold" (e.g., a circle or a simple curve in the space)
- Initialize with random attractors, some on the manifold, some off it (spurious)
- Implement a simple constraint update rule: regions where trajectories repeatedly fail to stabilize get slightly increased dissipation

**Procedure:**
1. Initialize a 2D energy landscape with several basins, some on the valid manifold, some off it
2. Run many random trajectories. Track which basins they fall into.
3. After each batch of trajectories: increase dissipation slightly in basins where trajectories frequently escape or show low transferability (fail to re-enter after small perturbation)
4. Repeat for 50 rounds
5. Measure: (a) fraction of trajectories landing in valid vs spurious basins over time, (b) depth and width of spurious basins over time

**Expected signal:**
- Spurious basins should become shallower and narrower over rounds
- Fraction of trajectories landing in valid basins should increase
- The effect should be stronger than a random baseline (random dissipation changes)
- Valid basins should remain stable or deepen — the update should be selective

**Failure mode:**
- All basins shrink equally → the update rule is not selective, just globally increasing friction
- Valid basins also degrade → the update rule cannot distinguish valid from spurious
- Spurious basins persist despite updates → local failure signals are not sufficient for self-refinement at this timescale

**Note:** Requires no ML infrastructure — Python + numpy only.

---

## Priority order

**If you can only run one, run Experiment 5** (field-coupling toy). It takes under 5 minutes, requires nothing beyond numpy, and makes the core FXSO claim immediately visible. You will see collapse, drift, and coherence as you sweep coupling values.

**Then Experiment 4** (anti-entropy). Tests a concrete architectural claim about loops with minimal ML infrastructure.

**Then Experiment 1** (trajectory coherence). Builds on Experiment 4, tests the foundational claim of the full framework.

**Then Experiment 3** (compatibility bandwidth). Existing models and datasets only — no training — tests the most novel construct.

**Experiments 2 and 6** are best run by someone with simulation expertise, in parallel with the above.

---

## What would count as strong evidence?

The framework gains support if:
- Field-coupled agents self-organize into coherent trajectories in a specific parameter regime (Exp 5)
- Loop iterations show structured, non-random trajectory evolution (Exp 1)
- Representational entropy decreases selectively for structured inputs (Exp 4)
- Compatibility bandwidth correlates with generalization across multiple tasks (Exp 3)

The framework is challenged if:
- Field coupling produces only collapse or drift — no coherence regime exists
- Loop states are redundant or random across iterations
- Entropy reduction is uniform with no selectivity between structured and noise inputs
- Compatibility bandwidth shows no correlation, or correlates with trivial properties like representation norm
---

## What would count as strong evidence?

The framework would gain support if:

- Loop iterations show structured, non-random trajectory evolution (Exp 1)
- Representational entropy decreases selectively for structured inputs (Exp 4)
- Compatibility bandwidth correlates with generalization across tasks (Exp 3)

It would be challenged if:

- Loop states are redundant or random
- Entropy reduction is uniform (no selectivity)
- Compatibility bandwidth shows no correlation or trivial correlation
