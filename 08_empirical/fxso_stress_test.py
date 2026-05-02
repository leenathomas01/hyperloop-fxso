"""
fxso_stress_test.py — FXSO Topological Stress Test

Tests whether system structure is coupled to constraint geometry
(invariant under coordinate transform) or to absolute coordinates (brittle).

Two shock events:
  t=300: Random noise injection (tests robustness)
  t=600: 90° global rotation kick (tests topological invariance)

Key metric: does thickness spike at t=600, or does the system glide?
  Spike → brittle, structure was coordinate-dependent
  Glide → invariant, structure is geometry-dependent

Produces data for Experiment 1 in 08_empirical/Results.md

Requirements: numpy, matplotlib (optional)
Run: python fxso_stress_test.py
Run kill test: python fxso_stress_test.py --motion 0.0
"""

import numpy as np
import argparse

try:
    import matplotlib.pyplot as plt
    PLOT = True
except ImportError:
    PLOT = False


# --- CONFIGURATION ---
AGENTS           = 40
STEPS            = 1000
COUPLING         = 0.06
DECAY_K          = 2.0
NOISE_LEVEL      = 0.05
INTERNAL_MOTION  = 0.06   # set to 0.0 for kill test (beads vs ring)
FORBIDDEN_RADIUS = 1.2
REPULSION        = 0.2
SEED             = 42
# ----------------------


def compute_thickness(states):
    """Standard deviation of agent distances from origin."""
    return float(np.std(np.linalg.norm(states, axis=1)))


def compute_circular_variance(states):
    """
    Angular dispersion of agents around the manifold.
    V_circ = 1 - |mean(e^{iθ})|

    0 = angularly concentrated (phase-locked, agents clustered)
    1 = angularly distributed (agents spread uniformly around ring)

    Note: low V_circ does NOT mean coherence — it indicates phase-locking.
    """
    angles = np.arctan2(states[:, 1], states[:, 0])
    r = np.abs(np.mean(np.exp(1j * angles)))
    return float(1 - r)


def run_stress_test(
    agents=AGENTS,
    steps=STEPS,
    coupling=COUPLING,
    k=DECAY_K,
    noise=NOISE_LEVEL,
    motion=INTERNAL_MOTION,
    radius=FORBIDDEN_RADIUS,
    repulsion=REPULSION,
    seed=SEED,
):
    np.random.seed(seed)

    states = np.random.randn(agents, 2) * 2.5
    rot = np.array([
        [np.cos(motion), -np.sin(motion)],
        [np.sin(motion),  np.cos(motion)]
    ])

    history      = []
    thickness_log = {}

    print(f"\nFXSO Stress Test (motion={motion})")
    print(f"{'Step':>5} | {'Radius':>8} | {'Thickness':>10} | {'Circ Var':>10} | Event")
    print("-" * 65)

    for t in range(steps):
        # 1. Internal loop
        states = states @ rot.T

        # 2. FXSO field coupling — localized, normalized, no self-interaction
        new_states = states.copy()
        for i in range(agents):
            diffs    = states - states[i]
            dist_sq  = np.sum(diffs**2, axis=1, keepdims=True)
            weights  = np.exp(-k * dist_sq)
            weights[i] = 0
            w_sum    = np.sum(weights) + 1e-9
            pull     = np.sum(diffs * weights, axis=0) / w_sum
            new_states[i] += coupling * pull

        # 3. Constraint: forbidden zone repulsion
        d_center = np.linalg.norm(new_states, axis=1, keepdims=True)
        new_states += (d_center < radius) * (new_states / (d_center + 1e-6)) * repulsion

        # 4. Record baseline before shocks
        if t == 299:
            thickness_log["pre_shock"] = compute_thickness(new_states)

        # 5. Shock events
        event_str = ""
        if t == 300:
            event_str = "RANDOM SHOCK"
            new_states += np.random.randn(agents, 2) * 1.8
        elif t == 600:
            event_str = "90° ROTATION KICK"
            kick_rot   = np.array([[0, -1], [1, 0]])
            new_states = new_states @ kick_rot.T

        # 6. Record post-rotation immediate state
        if t == 601:
            thickness_log["post_rotation"] = compute_thickness(new_states)

        # 7. Noise
        states = new_states + np.random.normal(0, noise, new_states.shape)
        history.append(states.copy())

        # 8. Log
        dists    = np.linalg.norm(states, axis=1)
        r_mean   = float(np.mean(dists))
        r_std    = compute_thickness(states)
        c_var    = compute_circular_variance(states)

        if t % 100 == 0 or event_str:
            print(f"{t:>5} | {r_mean:>8.2f} | {r_std:>10.2f} | {c_var:>10.2f} | {event_str}")

    # Final metrics
    thickness_log["final"]     = compute_thickness(states)
    thickness_log["annealing"] = thickness_log["pre_shock"] - thickness_log["final"]
    # Positive annealing = system tightened under stress (elastic signal)
    # Negative annealing = system diffused (plastic/brittle)

    return np.array(history), thickness_log


def plot_phases(history, radius, motion):
    if not PLOT:
        print("\nInstall matplotlib for trajectory plots.")
        return

    fig, ax = plt.subplots(figsize=(8, 8))

    circle = plt.Circle((0, 0), radius, color='red', fill=False,
                         ls='--', lw=2, alpha=0.4, label="Forbidden Zone")
    ax.add_artist(circle)

    # Phase-coded trajectories
    ax.plot(history[:300,  :, 0], history[:300,  :, 1], color='gray',  alpha=0.1, lw=0.4)
    ax.plot(history[301:600, :, 0], history[301:600, :, 1], color='blue',  alpha=0.2, lw=0.5)
    ax.plot(history[601:,  :, 0], history[601:,  :, 1], color='green', alpha=0.4, lw=0.7)

    ax.scatter(history[-1, :, 0], history[-1, :, 1],
               c='black', s=35, edgecolors='white', zorder=5, label="Final State")

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    ax.legend()
    ax.grid(True, alpha=0.15)
    ax.set_title(f"FXSO Stress Test (motion={motion})\n"
                 f"gray=pre-shock | blue=post-random | green=post-rotation")

    fname = f"fxso_stress_motion_{motion:.2f}.png"
    plt.savefig(fname, dpi=150, bbox_inches='tight')
    print(f"\nPlot saved: {fname}")
    plt.show()


def print_summary(thickness_log, motion):
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Motion (θ):           {motion}")
    print(f"Pre-shock thickness:  {thickness_log.get('pre_shock', 'N/A'):.3f}")
    print(f"Post-rotation (imm):  {thickness_log.get('post_rotation', 'N/A'):.3f}")
    print(f"Final thickness:      {thickness_log.get('final', 'N/A'):.3f}")
    print(f"Annealing score:      {thickness_log.get('annealing', 'N/A'):.3f}  "
          f"({'tightened' if thickness_log.get('annealing', -1) > 0 else 'diffused'})")

    rotation_delta = (thickness_log.get("post_rotation", 0) -
                      thickness_log.get("pre_shock", 0))
    print(f"\nRotation kick Δthickness: {rotation_delta:+.3f}")
    if abs(rotation_delta) < 0.05:
        print("  → Glide: strong topological invariance")
    elif abs(rotation_delta) < 0.15:
        print("  → Moderate disruption: partial invariance (expected result)")
    elif rotation_delta > 0.15:
        print("  → Spike: significant disruption, weaker invariance")
    else:
        print("  → Brittle: structure was coordinate-dependent")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--motion", type=float, default=INTERNAL_MOTION,
                        help="Internal rotation speed (0.0 = kill test)")
    parser.add_argument("--agents", type=int, default=AGENTS)
    parser.add_argument("--seed",   type=int, default=SEED)
    args = parser.parse_args()

    history, thickness_log = run_stress_test(
        motion=args.motion,
        agents=args.agents,
        seed=args.seed,
    )

    print_summary(thickness_log, args.motion)
    plot_phases(history, FORBIDDEN_RADIUS, args.motion)

    print("\nInterpretation:")
    print("  Rotation Δthickness < 0.05 → strong invariance (glide).")
    print("  Rotation Δthickness 0.05–0.15 → partial invariance (expected at these params).")
    print("  Rotation Δthickness > 0.15 → significant disruption.")
    print("  Kill test (--motion 0.0) → expect static beads, no annular circulation.")
    print("  V_circ: 0 = phase-locked (concentrated), 1 = distributed (uniform ring).")
    print("  See 08_empirical/Results.md for full experimental context.")
