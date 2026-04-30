"""
fxso_toy.py — Minimal FXSO Field-Coupling Simulation

Tests whether field-based coupling (overlap-driven, no explicit message passing)
can produce emergent coherence in a population of agents with internal loop dynamics.

Corresponds to Experiment 5 in 07_experiments/minimal_experiments.md

Requirements: numpy, matplotlib (optional)
Run: python fxso_toy.py
"""

import numpy as np

try:
    import matplotlib.pyplot as plt
    PLOT = True
except ImportError:
    PLOT = False
    print("matplotlib not found — running in text-only mode")


def run_fxso_toy(agents=5, steps=500, coupling=0.02, noise=0.01):
    """
    Minimal FXSO field-coupling simulation.

    Each agent is a 2D vector evolving under:
      1. An internal rotation (proxy for Hyperloop loop iterations)
      2. Proximity-weighted coupling toward other agents (field overlap)
      3. Gaussian noise (field entropy)

    Parameters
    ----------
    agents   : number of agents
    steps    : timesteps to run
    coupling : field coupling strength — sweep this to find regime transitions
    noise    : Gaussian noise scale (field entropy)

    Returns
    -------
    final_states : (agents, 2) array of final positions
    trajectory   : (steps, agents, 2) full history
    """
    states = np.random.randn(agents, 2)

    # Internal loop: rotation matrix (small fixed angle)
    theta = 0.05
    rot = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])

    trajectory = []

    for _ in range(steps):
        # 1. Internal loop transformation
        states = states @ rot.T

        # 2. Field coupling — proximity-weighted, no self-interaction
        new_states = states.copy()
        for i in range(agents):
            diffs = states - states[i]
            distances = np.linalg.norm(diffs, axis=1, keepdims=True) + 1e-6
            weights = np.exp(-distances)          # proximity decay: closer = stronger pull
            weights[i] = 0                        # remove self-interaction
            new_states[i] += np.sum(diffs * weights * coupling, axis=0)
        states = new_states

        # 3. Noise injection (field entropy)
        states += np.random.normal(0, noise, states.shape)

        trajectory.append(states.copy())

    return states, np.array(trajectory)


def measure_regime(trajectory):
    """
    Compute summary statistics to characterize the coupling regime.

    Returns
    -------
    dict with:
      trajectory_variance : mean variance over last 100 steps (lower = more stable)
      final_spread        : std of final agent positions (lower = more coherent)
      convergence_rate    : how quickly inter-agent spread decreases
    """
    last = trajectory[-100:]                        # last 100 steps
    tvar = float(np.var(last, axis=1).mean())
    spread = float(np.std(trajectory[-1], axis=0).mean())

    # Convergence rate: compare spread in first vs second half
    mid = len(trajectory) // 2
    early_spread = np.std(trajectory[:mid], axis=1).mean()
    late_spread  = np.std(trajectory[mid:], axis=1).mean()
    convergence  = float(early_spread - late_spread)   # positive = converging

    return {
        "trajectory_variance": tvar,
        "final_spread": spread,
        "convergence_rate": convergence,
    }


def classify_regime(stats, collapse_threshold=0.05, drift_threshold=0.8):
    """
    Heuristic regime classification based on summary statistics.
    """
    if stats["final_spread"] < collapse_threshold:
        return "COLLAPSE  — agents merged into single point"
    elif stats["final_spread"] > drift_threshold:
        return "DRIFT     — agents not influencing each other"
    else:
        return "COHERENCE — structured alignment (interesting zone)"


def sweep(agents=5, steps=500, noise=0.01):
    """
    Sweep coupling strengths and report regime for each.
    """
    couplings = [0.001, 0.005, 0.01, 0.02, 0.05, 0.08, 0.1, 0.15]
    results = []

    print(f"\n{'coupling':>10} | {'traj_var':>10} | {'spread':>8} | {'convergence':>12} | regime")
    print("-" * 80)

    for c in couplings:
        np.random.seed(42)                          # reproducible
        final, traj = run_fxso_toy(agents=agents, steps=steps, coupling=c, noise=noise)
        stats = measure_regime(traj)
        regime = classify_regime(stats)
        results.append((c, stats, regime, traj))
        print(f"{c:>10.3f} | {stats['trajectory_variance']:>10.4f} | "
              f"{stats['final_spread']:>8.4f} | {stats['convergence_rate']:>12.4f} | {regime}")

    return results


def plot_results(results):
    """
    Plot trajectories for three representative coupling values.
    """
    if not PLOT:
        print("\nInstall matplotlib to enable trajectory plots.")
        return

    # Pick three regimes to show
    targets = [results[1], results[4], results[-1]]   # drift, coherence, collapse
    labels  = ["Drift (low coupling)", "Coherence (mid coupling)", "Collapse (high coupling)"]
    colors  = plt.cm.tab10.colors

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("FXSO Field-Coupling: Regime Transitions", fontsize=13)

    for ax, (c, stats, regime, traj), label in zip(axes, targets, labels):
        for agent_idx in range(traj.shape[1]):
            ax.plot(traj[:, agent_idx, 0], traj[:, agent_idx, 1],
                    alpha=0.6, linewidth=0.8, color=colors[agent_idx % 10])
            ax.scatter(*traj[0, agent_idx], marker='o', s=40, color=colors[agent_idx % 10])
            ax.scatter(*traj[-1, agent_idx], marker='*', s=80, color=colors[agent_idx % 10])

        ax.set_title(f"{label}\ncoupling={c:.3f} | spread={stats['final_spread']:.3f}")
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("fxso_regimes.png", dpi=150, bbox_inches='tight')
    print("\nPlot saved to fxso_regimes.png")
    plt.show()


if __name__ == "__main__":
    print("=" * 80)
    print("FXSO Toy Simulation — Regime Sweep")
    print("=" * 80)
    print("\nWhat to look for:")
    print("  DRIFT     = coupling too low, no field effect")
    print("  COHERENCE = field coupling produces structured alignment (target regime)")
    print("  COLLAPSE  = coupling too high, all agents merge")
    print()

    results = sweep(agents=5, steps=500, noise=0.01)
    plot_results(results)

    print("\nInterpretation:")
    print("  Coherence regime indicates field-based coupling can produce structure")
    print("  without explicit messaging — the core FXSO claim in minimal form.")
    print()
    print("Next steps:")
    print("  - Vary noise level: does the coherence regime shrink under higher entropy?")
    print("  - Vary agent count: does coherence persist with more agents?")
    print("  - Replace rotation with actual Hyperloop loop states (Experiment 1 bridge)")
    print("  - See minimal_experiments.md Experiment 5 for full context")
