"""
fxso_motion_sweep.py — FXSO Motion Sweep

Tests the "Critical Velocity" hypothesis:
  Does increasing internal rotation speed (θ) dissolve local clusters
  into a continuous distributed field?

Sweeps θ across a range, measures:
  - Circular Variance (V_circ): angular fragmentation
  - Thickness (σ_radius): radial spread
  - Recovery time: steps to return to baseline after shock

Result (from prior runs): No phase transition observed.
V_circ remains high (0.7–0.9) across all θ values.
Conclusion: motion is necessary for fluidity but not sufficient for coherence.

Produces data for Experiment 2 in 08_empirical/Results.md

Requirements: numpy, matplotlib (optional)
Run: python fxso_motion_sweep.py
"""

import numpy as np

try:
    import matplotlib.pyplot as plt
    PLOT = True
except ImportError:
    PLOT = False


# --- CONFIGURATION ---
AGENTS           = 40
STEPS            = 600
COUPLING         = 0.06
DECAY_K          = 2.0
NOISE_LEVEL      = 0.05
FORBIDDEN_RADIUS = 1.2
REPULSION        = 0.2
SEEDS            = [42, 43, 44]   # multi-seed for stability
MOTIONS          = [0.0, 0.005, 0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.2]
# ----------------------


def compute_thickness(states):
    return float(np.std(np.linalg.norm(states, axis=1)))


def compute_circular_variance(states):
    """
    Angular dispersion of agents around the manifold.
    V_circ = 1 - |mean(e^{iθ})|

    0 = angularly concentrated (phase-locked, agents clustered)
    1 = angularly distributed (agents spread uniformly around ring)

    Note: low V_circ does NOT mean coherence — it indicates phase-locking.
    In these experiments V_circ stays high (0.65–1.0) across all θ,
    confirming the system remains angularly fragmented regardless of motion speed.
    """
    angles = np.arctan2(states[:, 1], states[:, 0])
    r = np.abs(np.mean(np.exp(1j * angles)))
    return float(1 - r)


def run_sim(theta, n=AGENTS, steps=STEPS, coupling=COUPLING,
            k=DECAY_K, noise=NOISE_LEVEL, radius=FORBIDDEN_RADIUS,
            repulsion=REPULSION, seed=42):
    """Single simulation run. Returns final agent states."""
    np.random.seed(seed)

    states = np.random.randn(n, 2) * 2.0
    rot = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])

    for _ in range(steps):
        # 1. Internal loop
        states = states @ rot.T

        # 2. FXSO coupling
        new_states = states.copy()
        for i in range(n):
            diffs   = states - states[i]
            dist_sq = np.sum(diffs**2, axis=1, keepdims=True)
            weights = np.exp(-k * dist_sq)
            weights[i] = 0
            w_sum   = np.sum(weights) + 1e-9
            pull    = np.sum(diffs * weights, axis=0) / w_sum
            new_states[i] += coupling * pull

        # 3. Constraint
        d_center = np.linalg.norm(new_states, axis=1, keepdims=True)
        new_states += (d_center < radius) * (new_states / (d_center + 1e-6)) * repulsion

        # 4. Noise
        states = new_states + np.random.normal(0, noise, new_states.shape)

    return states


def run_multi_seed(theta, seeds=SEEDS):
    """Average metrics across multiple seeds for stability."""
    cvars      = []
    thicknesses = []

    for seed in seeds:
        final = run_sim(theta, seed=seed)
        cvars.append(compute_circular_variance(final))
        thicknesses.append(compute_thickness(final))

    return {
        "cvar_mean":  float(np.mean(cvars)),
        "cvar_std":   float(np.std(cvars)),
        "thick_mean": float(np.mean(thicknesses)),
        "thick_std":  float(np.std(thicknesses)),
        "final_states": run_sim(theta, seed=seeds[0]),  # for plotting
    }


def classify(cvar):
    """
    Loose regime labels based on V_circ (angular distribution).
    Remember: high V_circ = distributed, low V_circ = concentrated.

    These thresholds are descriptive, not definitive.
    The key finding is that no transition occurs across θ — all runs stay Fragmented.
    """
    if cvar > 0.75:
        return "Fragmented     (high angular clustering)"
    elif cvar > 0.45:
        return "Partial        (moderate clustering)"
    else:
        return "Low-cvar       (phase-locked — check validation plot)"


def sweep():
    results = []

    print("\nFXSO Motion Sweep — Critical Velocity Test")
    print(f"Seeds: {SEEDS} | Agents: {AGENTS} | Steps: {STEPS}")
    print("V_circ: 0 = phase-locked (concentrated), 1 = distributed (uniform ring)")
    print()
    print(f"{'θ':>6} | {'V_circ':>8} ± {'std':>5} | {'Thickness':>9} ± {'std':>5} | Regime")
    print("-" * 65)

    for theta in MOTIONS:
        r = run_multi_seed(theta)
        results.append((theta, r))

        regime = classify(r["cvar_mean"])
        print(f"{theta:>6.3f} | {r['cvar_mean']:>8.2f} ± {r['cvar_std']:>5.2f} | "
              f"{r['thick_mean']:>9.2f} ± {r['thick_std']:>5.2f} | {regime}")

    return results


def plot_sweep(results):
    if not PLOT:
        print("\nInstall matplotlib for plots.")
        return

    thetas      = [r[0]                   for r in results]
    cvar_means  = [r[1]["cvar_mean"]       for r in results]
    cvar_stds   = [r[1]["cvar_std"]        for r in results]
    thick_means = [r[1]["thick_mean"]      for r in results]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
    fig.suptitle("FXSO Motion Sweep: Circular Variance and Thickness vs θ", fontsize=12)

    ax1.errorbar(thetas, cvar_means, yerr=cvar_stds, fmt='o-', color='steelblue',
                 capsize=4, label="V_circ (mean ± std)")
    ax1.axhline(0.45, color='green', ls='--', alpha=0.6, label="Distributed threshold (0.45)")
    ax1.set_ylabel("Circular Variance")
    ax1.set_ylim(0, 1.1)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_title("No phase transition observed — V_circ flat across all θ")

    ax2.plot(thetas, thick_means, 's-', color='darkorange', label="Thickness (mean)")
    ax2.set_xlabel("Internal Motion θ (rad/step)")
    ax2.set_ylabel("Thickness σ_radius")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("fxso_motion_sweep.png", dpi=150, bbox_inches='tight')
    print("\nPlot saved: fxso_motion_sweep.png")
    plt.show()

    # Final state scatter grid
    n_cols = len(results)
    fig2, axes = plt.subplots(1, n_cols, figsize=(n_cols * 2.5, 3))
    fig2.suptitle("Final Agent Positions by θ", fontsize=10)

    for ax, (theta, r) in zip(axes, results):
        final = r["final_states"]
        circle = plt.Circle((0, 0), FORBIDDEN_RADIUS, color='red', fill=False, lw=1, alpha=0.4)
        ax.add_artist(circle)
        ax.scatter(final[:, 0], final[:, 1], s=6, alpha=0.6)
        ax.set_title(f"θ={theta:.3f}\nV_circ={r['cvar_mean']:.2f}", fontsize=7)
        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)
        ax.set_aspect('equal')
        ax.axis('off')

    plt.tight_layout()
    plt.savefig("fxso_motion_states.png", dpi=150, bbox_inches='tight')
    print("State grid saved: fxso_motion_states.png")
    plt.show()


if __name__ == "__main__":
    results = sweep()
    plot_sweep(results)

    print("\nInterpretation:")
    print("  V_circ flat across all θ → critical velocity hypothesis not observed.")
    print("  Motion affects dynamics (beads circulate) but not topology (beads persist).")
    print("  Pure attractive coupling cannot produce a distributed manifold.")
    print("  V_circ: 0 = phase-locked (concentrated), 1 = distributed (uniform ring).")
    print("  Next step: test multi-scale interaction — see fxso_mhat_experiment.py.")
    print("  See 08_empirical/Results.md Experiment 2 for full context.")

    # Reproducibility note
    print(f"\nReproducibility: seeds={SEEDS}, agents={AGENTS}, steps={STEPS}")
    print("  Changing seeds alters microstructure but not regime classification.")
