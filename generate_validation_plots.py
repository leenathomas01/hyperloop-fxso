"""
Generate regime-validation plots for the FXSO empirical scripts.

The goal is diagnostic evidence, not presentation polish:
- stress-test recovery and stability after shocks
- raw motion-sweep regime metrics across seeds
- Mexican Hat continuity and final radial concentration
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
from pathlib import Path

import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
EMPIRICAL = ROOT / "08_empirical"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


stress = load_module("fxso_stress_test", EMPIRICAL / "fxso_stress_test.py")
motion = load_module("fxso_motion_sweep", EMPIRICAL / "fxso_motion_sweep.py")
mhat = load_module("fxso_mhat_experiment", EMPIRICAL / "fxso_mhat_experiment.py")


def quiet_call(func, *args, **kwargs):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        return func(*args, **kwargs)


def thickness_series(history: np.ndarray, compute_thickness) -> np.ndarray:
    return np.array([compute_thickness(states) for states in history])


def add_event_lines(ax):
    ax.axvline(300, color="crimson", linestyle="--", linewidth=1.2, label="t=300 random shock")
    ax.axvline(600, color="purple", linestyle="--", linewidth=1.2, label="t=600 rotation kick")


def plot_stress_validation():
    runs = [
        ("motion=0.06", {"motion": stress.INTERNAL_MOTION, "seed": stress.SEED}),
        ("motion=0.00 kill test", {"motion": 0.0, "seed": stress.SEED}),
    ]

    fig, ax = plt.subplots(figsize=(10, 5.8))
    summaries = []

    for label, kwargs in runs:
        history, log = quiet_call(stress.run_stress_test, **kwargs)
        thickness = thickness_series(history, stress.compute_thickness)
        times = np.arange(len(thickness))

        ax.plot(times, thickness, linewidth=1.0, label=label)

        post_rotation = thickness[650:]
        post_mean = float(np.mean(post_rotation))
        post_std = float(np.std(post_rotation))
        ax.hlines(
            post_mean,
            650,
            len(thickness) - 1,
            linestyles=":",
            linewidth=1.2,
            alpha=0.8,
        )

        summaries.append(
            {
                "label": label,
                "pre_shock": log["pre_shock"],
                "post_rotation": log["post_rotation"],
                "final": log["final"],
                "rotation_delta": log["post_rotation"] - log["pre_shock"],
                "post_mean": post_mean,
                "post_std": post_std,
            }
        )

    add_event_lines(ax)
    ax.set_title("FXSO Stress Test: thickness recovery after perturbations")
    ax.set_xlabel("time step")
    ax.set_ylabel("thickness: std(radius)")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="upper right")

    note = "\n".join(
        f"{s['label']}: rotation delta={s['rotation_delta']:+.3f}, "
        f"post-650 mean={s['post_mean']:.3f} +/- {s['post_std']:.3f}"
        for s in summaries
    )
    ax.text(
        0.01,
        0.02,
        note,
        transform=ax.transAxes,
        fontsize=8,
        va="bottom",
        ha="left",
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.8, "edgecolor": "0.8"},
    )

    out = ROOT / "fxso_validation_stress_thickness.png"
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out, summaries


def plot_motion_validation():
    rows = []
    for seed in motion.SEEDS:
        for theta in motion.MOTIONS:
            final = motion.run_sim(theta, seed=seed)
            rows.append(
                {
                    "seed": seed,
                    "theta": theta,
                    "cvar": motion.compute_circular_variance(final),
                    "thickness": motion.compute_thickness(final),
                }
            )

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.5, 7), sharex=True)

    for seed in motion.SEEDS:
        seed_rows = [row for row in rows if row["seed"] == seed]
        seed_rows.sort(key=lambda row: row["theta"])
        thetas = [row["theta"] for row in seed_rows]
        cvars = [row["cvar"] for row in seed_rows]
        thicknesses = [row["thickness"] for row in seed_rows]
        ax1.plot(thetas, cvars, marker="o", linewidth=1.0, label=f"seed {seed}")
        ax2.plot(thetas, thicknesses, marker="o", linewidth=1.0, label=f"seed {seed}")

    ax1.axhline(0.75, color="0.45", linestyle=":", linewidth=1.0, label="fragmented guide")
    ax1.set_title("FXSO Motion Sweep: raw circular variance by theta")
    ax1.set_ylabel("V_circ")
    ax1.set_ylim(0, 1.05)
    ax1.grid(True, alpha=0.25)
    ax1.legend(loc="lower right")

    ax2.set_title("FXSO Motion Sweep: raw thickness by theta")
    ax2.set_xlabel("theta (rad/step)")
    ax2.set_ylabel("thickness: std(radius)")
    ax2.grid(True, alpha=0.25)
    ax2.legend(loc="upper left")

    out = ROOT / "fxso_validation_motion_sweep_raw.png"
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out, rows


def plot_mhat_validation():
    history, log = quiet_call(mhat.run_mhat_experiment)
    final = history[-1]
    last = history[-200:]
    final_radii = np.linalg.norm(final, axis=1)
    final_angles = np.arctan2(final[:, 1], final[:, 0])

    fig, axes = plt.subplots(1, 4, figsize=(19, 4.8))
    traj_ax, scatter_ax, radius_ax, angle_ax = axes

    circle_kwargs = {"color": "crimson", "fill": False, "linestyle": "--", "linewidth": 1.5, "alpha": 0.55}

    traj_ax.add_artist(plt.Circle((0, 0), mhat.FORBIDDEN_RADIUS, **circle_kwargs))
    for agent_idx in range(last.shape[1]):
        traj_ax.plot(last[:, agent_idx, 0], last[:, agent_idx, 1], alpha=0.22, linewidth=0.45)
    traj_ax.set_title("Last 200-step trajectory overlay")
    traj_ax.set_aspect("equal")
    traj_ax.set_xlim(-4, 4)
    traj_ax.set_ylim(-4, 4)
    traj_ax.grid(True, alpha=0.18)

    scatter_ax.add_artist(plt.Circle((0, 0), mhat.FORBIDDEN_RADIUS, **circle_kwargs))
    scatter_ax.scatter(final[:, 0], final[:, 1], s=8, alpha=0.75, color="black")
    scatter_ax.set_title(
        f"Final state: thickness={log['final']:.3f}, V_circ={log['final_cvar']:.3f}"
    )
    scatter_ax.set_aspect("equal")
    scatter_ax.set_xlim(-4, 4)
    scatter_ax.set_ylim(-4, 4)
    scatter_ax.grid(True, alpha=0.18)

    radius_ax.hist(final_radii, bins=28, color="steelblue", edgecolor="white", alpha=0.85)
    radius_ax.axvline(mhat.FORBIDDEN_RADIUS, color="crimson", linestyle="--", linewidth=1.5, label="forbidden radius")
    radius_ax.axvline(float(np.mean(final_radii)), color="black", linestyle=":", linewidth=1.3, label="mean radius")
    radius_ax.set_title("Final radius distribution")
    radius_ax.set_xlabel("radius")
    radius_ax.set_ylabel("agent count")
    radius_ax.grid(True, axis="y", alpha=0.25)
    radius_ax.legend()

    angle_ax.hist(final_angles, bins=28, color="darkorange", edgecolor="white", alpha=0.85)
    angle_ax.set_title("Final angular distribution")
    angle_ax.set_xlabel("angle (radians)")
    angle_ax.set_ylabel("agent count")
    angle_ax.grid(True, axis="y", alpha=0.25)

    fig.suptitle(
        "FXSO Mexican Hat validation: annular trajectory, compact final phase",
        fontsize=12,
    )
    out = ROOT / "fxso_validation_mhat_regime.png"
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out, log


def main():
    stress_out, stress_summary = plot_stress_validation()
    motion_out, motion_rows = plot_motion_validation()
    mhat_out, mhat_log = plot_mhat_validation()

    print("Generated validation plots:")
    print(f"- {stress_out}")
    print(f"- {motion_out}")
    print(f"- {mhat_out}")
    print()
    print("Stress summary:")
    for row in stress_summary:
        print(
            f"- {row['label']}: rotation_delta={row['rotation_delta']:+.3f}, "
            f"post_mean={row['post_mean']:.3f}, post_std={row['post_std']:.3f}"
        )
    print()
    print(
        "Motion sweep raw ranges: "
        f"V_circ={min(r['cvar'] for r in motion_rows):.3f}..{max(r['cvar'] for r in motion_rows):.3f}, "
        f"thickness={min(r['thickness'] for r in motion_rows):.3f}..{max(r['thickness'] for r in motion_rows):.3f}"
    )
    print()
    print(
        "Mexican Hat summary: "
        f"final_thickness={mhat_log['final']:.3f}, "
        f"final_V_circ={mhat_log['final_cvar']:.3f}, "
        f"kick_delta={mhat_log['kick_delta']:+.3f}"
    )


if __name__ == "__main__":
    main()
