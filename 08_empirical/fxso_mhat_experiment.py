"""
fxso_mhat_experiment.py — FXSO Mexican Hat Kernel Experiment

Tests whether multi-scale interaction (short-range attraction + medium-range
repulsion) can push the system from the Structured-Fragment regime into the
Elastic regime — a continuous, stable, rotation-invariant manifold.

The core hypothesis:
  Pure attractive coupling → persistent fragmentation (beads)
  Competing interaction scales → possible distributed coherence

The Mexican Hat (Difference of Gaussians) kernel:
  w(d²) = exp(-k_a * d²) - β * exp(-k_r * (d² - r0)²)

  where:
    k_a = short-range attraction decay
    k_r = medium-range repulsion decay
    r0  = distance at which repulsion peaks
    β   = relative strength of repulsion

  Effect: agents attract at short range, repel at medium range, ignore at long range.
  This prevents bead collapse while maintaining local cohesion.

Target: N=400, k_a=0.5, k_r=0.2, r0=0.8
  Hypothesis: V_circ < 0.5 AND stable thickness AND survives 90° kick
  → first entry into elastic regime

If it works:  elastic regime achieved via force balance, not parameter tuning
If it fails:  elastic regime requires memory, phase structure, or non-pairwise terms

Produces data for next section of 08_empirical/Results.md

Requirements: numpy, matplotlib (optional)
Run: python fxso_mhat_experiment.py
"""

import numpy as np

try:
    import matplotlib.pyplot as plt
    PLOT = True
except ImportError:
    PLOT = False


# --- CONFIGURATION ---
AGENTS           = 400
STEPS            = 800
COUPLING         = 0.06
NOISE_LEVEL      = 0.04
INTERNAL_MOTION  = 0.06
FORBIDDEN_RADIUS = 1.2
REPULSION        = 0.2
SEED             = 42

# Mexican Hat kernel parameters
K_ATTRACT        = 0.5    # short-range attraction (lower = longer reach)
K_REPEL          = 0.2    # medium-range repulsion
R0               = 0.8    # distance at which repulsion peaks
BETA             = 0.3    # repulsion strength relative to attraction
# ----------------------


def compute_thickness(states):
    return float(np.std(np.linalg.norm(states, axis=1)))


def compute_circular_variance(states):
    angles = np.arctan2(states[:, 1], states[:, 0])
    r = np.abs(np.mean(np.exp(1j * angles)))
    return float(1 - r)


def weights_mhat(dist_sq, k_attract=K_ATTRACT, k_repel=K_REPEL,
                 r0=R0, beta=BETA):
    """
    Mexican Hat (DoG) interaction kernel.

    Short-range attraction + medium-range repulsion.
    Negative weights = true repulsion (agents push away at medium range).
    This creates preferred spacing — the key difference from pure attraction.

    Note: do NOT clip to zero. Clipping turns repulsion into "weaker attraction"
    and removes the spacing force needed to reach the elastic regime.
    """
    attract = np.exp(-k_attract * dist_sq)
    repel   = beta * np.exp(-k_repel * (dist_sq - r0**2)**2)
    return attract - repel  # true multi-scale competition, no clipping


def run_mhat_experiment(
    agents=AGENTS,
    steps=STEPS,
    coupling=COUPLING,
    noise=NOISE_LEVEL,
    motion=INTERNAL_MOTION,
    radius=FORBIDDEN_RADIUS,
    repulsion=REPULSION,
    seed=SEED,
    apply_rotation_kick=True,
):
    np.random.seed(seed)

    states = np.random.randn(agents, 2) * 2.0
    rot = np.array([
        [np.cos(motion), -np.sin(motion)],
        [np.sin(motion),  np.cos(motion)]
    ])

    history      = []
    thickness_log = {}

    print(f"\nFXSO Mexican Hat Experiment")
    print(f"N={agents} | k_attract={K_ATTRACT} | k_repel={K_REPEL} | r0={R0} | β={BETA}")
    print(f"{'Step':>5} | {'Radius':>8} | {'Thickness':>10} | {'Circ Var':>10} | Event")
    print("-" * 65)

    for t in range(steps):
        # 1. Internal loop
        states = states @ rot.T

        # 2. FXSO coupling with Mexican Hat kernel
        new_states = states.copy()
        for i in range(agents):
            diffs   = states - states[i]
            dist_sq = np.sum(diffs**2, axis=1, keepdims=True)
            weights = weights_mhat(dist_sq)
            weights[i] = 0
            w_sum   = np.sum(weights) + 1e-9
            pull    = np.sum(diffs * weights, axis=0) / w_sum
            new_states[i] += coupling * pull

        # 3. Constraint
        d_center = np.linalg.norm(new_states, axis=1, keepdims=True)
        new_states += (d_center < radius) * (new_states / (d_center + 1e-6)) * repulsion

        # 4. Record baseline
        if t == 399:
            thickness_log["pre_kick"] = compute_thickness(new_states)
            thickness_log["pre_kick_cvar"] = compute_circular_variance(new_states)

        # 5. Rotation kick (if enabled)
        event_str = ""
        if apply_rotation_kick and t == 400:
            event_str = "90° ROTATION KICK"
            kick_rot   = np.array([[0, -1], [1, 0]])
            new_states = new_states @ kick_rot.T

        if t == 401:
            thickness_log["post_kick"] = compute_thickness(new_states)

        # 6. Noise
        states = new_states + np.random.normal(0, noise, new_states.shape)
        history.append(states.copy())

        # 7. Log
        dists  = np.linalg.norm(states, axis=1)
        r_mean = float(np.mean(dists))
        r_std  = compute_thickness(states)
        c_var  = compute_circular_variance(states)

        if t % 100 == 0 or event_str:
            print(f"{t:>5} | {r_mean:>8.2f} | {r_std:>10.2f} | {c_var:>10.2f} | {event_str}")

    thickness_log["final"]           = compute_thickness(states)
    thickness_log["final_cvar"]      = compute_circular_variance(states)
    thickness_log["annealing"]       = thickness_log.get("pre_kick", 0) - thickness_log["final"]
    thickness_log["kick_delta"]      = (thickness_log.get("post_kick", 0) -
                                        thickness_log.get("pre_kick", 0))

    return np.array(history), thickness_log


def print_verdict(log):
    print("\n" + "=" * 55)
    print("VERDICT")
    print("=" * 55)
    print(f"Pre-kick thickness:   {log.get('pre_kick', 'N/A'):.3f}")
    print(f"Pre-kick V_circ:      {log.get('pre_kick_cvar', 'N/A'):.3f}")
    print(f"Kick Δthickness:      {log.get('kick_delta', 'N/A'):+.3f}")
    print(f"Final thickness:      {log.get('final', 'N/A'):.3f}")
    print(f"Final V_circ:         {log.get('final_cvar', 'N/A'):.3f}")
    print(f"Annealing score:      {log.get('annealing', 'N/A'):.3f}")

    print()
    print("V_circ note: 0 = angularly concentrated (phase-locked), 1 = uniformly distributed.")
    print("Note: Low V_circ does NOT mean coherence — it indicates phase-locking.")
    print()

    cvar  = log.get("final_cvar", 1.0)
    thick = log.get("final", 99)
    kick  = abs(log.get("kick_delta", 99))

    # Elastic: thin band AND angularly distributed (high V_circ)
    # Orbital Coherent: thin band AND angularly concentrated (low V_circ)
    # Fragmented: thick band regardless of V_circ

    if thick < 0.3 and cvar > 0.7:
        print("✅ ELASTIC REGIME: Continuous uniform manifold.")
        print("   Low thickness + high V_circ = phase-decorrelated ring.")
    elif thick < 0.3 and cvar < 0.3:
        print("🔄 ORBITAL COHERENCE: Stable annular trajectory, phase-locked.")
        print("   Low thickness + low V_circ = agents share orbit but are angularly concentrated.")
        print("   This is NOT elastic. To reach elastic, add phase decorrelation.")
    elif thick < 0.5:
        print("⚠️  APPROACHING BOUNDARY: Moderate radial coherence.")
        print(f"   thickness={thick:.3f}, V_circ={cvar:.3f}")
        print("   Check validation plots to classify regime.")
    else:
        print("❌ STILL FRAGMENTED: Thick cloud, no coherent manifold.")
        print(f"   thickness={thick:.3f} — try larger N, lower k_attract, or higher beta.")


def plot_result(history, radius):
    if not PLOT:
        print("\nInstall matplotlib for plots.")
        return

    fig, ax = plt.subplots(figsize=(7, 7))
    circle = plt.Circle((0, 0), radius, color='red', fill=False,
                         ls='--', lw=2, alpha=0.4, label="Forbidden Zone")
    ax.add_artist(circle)

    # Final 200 steps
    for i in range(history.shape[1]):
        ax.plot(history[-200:, i, 0], history[-200:, i, 1], alpha=0.3, lw=0.5)

    ax.scatter(history[-1, :, 0], history[-1, :, 1],
               s=4, c='black', alpha=0.6, label="Final positions")

    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_aspect('equal')
    ax.legend()
    ax.grid(True, alpha=0.2)
    ax.set_title(f"FXSO Mexican Hat (N={AGENTS}, k_a={K_ATTRACT}, β={BETA})")

    plt.savefig("fxso_mhat_result.png", dpi=150, bbox_inches='tight')
    print("\nPlot saved: fxso_mhat_result.png")
    plt.show()


if __name__ == "__main__":
    history, log = run_mhat_experiment()
    print_verdict(log)
    plot_result(history, FORBIDDEN_RADIUS)

    print("\nNext steps if still fragmented:")
    print("  - Increase β (repulsion strength) toward 0.5")
    print("  - Reduce K_ATTRACT to extend reach further (try 0.3)")
    print("  - Increase N toward 800–1000")
    print("  - Try medium-range repulsion in the constraint zone as well")
    print("\nSee 08_empirical/Results.md for experimental context.")
