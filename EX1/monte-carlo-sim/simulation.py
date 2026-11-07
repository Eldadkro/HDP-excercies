"""Monte Carlo estimation of the union area of three unit disks."""

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np

RADIUS = 1.0
CENTERS = np.array([[0.0, 0.0], [0.5, np.sqrt(3) / 2], [-0.5, np.sqrt(3) / 2]])
LOWER = np.array([-1.5, -1.0])
UPPER = np.array([1.5, 1 + np.sqrt(3) / 2])
RECTANGLE_AREA = float(np.prod(UPPER - LOWER))


@dataclass
class SimulationResult:
    points: np.ndarray
    hits: np.ndarray
    estimates: np.ndarray


def sample_points(n: int, seed: int | None = None) -> np.ndarray:
    """Return n independent uniform points in the enclosing rectangle."""
    if isinstance(n, (bool, np.bool_)) or not isinstance(n, (int, np.integer)) or n <= 0:
        raise ValueError("n must be a positive integer")
    return np.random.default_rng(seed).uniform(LOWER, UPPER, size=(n, 2))


def union_membership(points: np.ndarray) -> np.ndarray:
    """Return one boolean per point; overlaps are counted only once."""
    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or points.shape[1] != 2 or not np.isfinite(points).all():
        raise ValueError("points must be a finite array of shape (n, 2)")
    squared_distances = np.sum((points[:, None, :] - CENTERS) ** 2, axis=2)
    return np.any(squared_distances <= RADIUS**2, axis=1)


def running_estimates(hits: np.ndarray) -> np.ndarray:
    """Convert a nonempty boolean/0–1 hit sequence into running area estimates."""
    hits = np.asarray(hits)
    if hits.ndim != 1 or hits.size == 0 or not np.isin(hits, [0, 1]).all():
        raise ValueError("hits must be a nonempty one-dimensional boolean/0–1 sequence")
    return RECTANGLE_AREA * np.cumsum(hits, dtype=np.int64) / np.arange(1, hits.size + 1)


def simulate(n: int, seed: int | None = None) -> SimulationResult:
    """Sample points and compute all running estimates, without plotting."""
    points = sample_points(n, seed)
    hits = union_membership(points)
    return SimulationResult(points, hits, running_estimates(hits))


def plot_geometry(result: SimulationResult):
    """Plot all sampled points, the circle boundaries, and the rectangle."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, Rectangle

    fig, ax = plt.subplots()
    for mask, color, label in (
        (result.hits, "tab:blue", "Inside union"),
        (~result.hits, "tab:orange", "Outside union"),
    ):
        ax.scatter(*result.points[mask].T, s=5, alpha=0.5, color=color, label=label)
    for i, center in enumerate(CENTERS):
        ax.add_patch(Circle(center, RADIUS, fill=False, color="black", label="Circle boundaries" if i == 0 else None))
    ax.add_patch(Rectangle(LOWER, *(UPPER - LOWER), fill=False, linestyle="--", label="Sampling rectangle"))
    ax.set(xlabel="x", ylabel="y", title=f"Monte Carlo samples (n={len(result.points):,})")
    ax.set_aspect("equal", adjustable="box")
    ax.legend()
    fig.tight_layout()
    return fig, ax


def plot_convergence(result: SimulationResult):
    """Plot running union-area estimates against iteration number."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot(np.arange(1, len(result.estimates) + 1), result.estimates)
    ax.set(xlabel="Iteration k", ylabel="Estimated union area", title="Monte Carlo convergence")
    ax.text(
        0.98, 0.98, f"Final area estimate: {result.estimates[-1]:.6f}",
        transform=ax.transAxes, ha="right", va="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
    )
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig, ax


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int, help="positive number of samples")
    parser.add_argument("--seed", type=int, help="nonnegative random seed")
    parser.add_argument("--output-dir", type=Path, default=Path("plots"), help="directory for geometry.png and convergence.png (default: plots/)")
    parser.add_argument("--no-show", action="store_true", help="do not open interactive figures")
    args = parser.parse_args()
    if args.n <= 0:
        parser.error("n must be a positive integer")
    if args.seed is not None and args.seed < 0:
        parser.error("seed must be nonnegative")
    result = simulate(args.n, args.seed)
    print(f"Estimated union area: {result.estimates[-1]:.6f} ({args.n:,} samples)")

    import matplotlib.pyplot as plt

    geometry, _ = plot_geometry(result)
    convergence, _ = plot_convergence(result)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    geometry.savefig(args.output_dir / "geometry.png", dpi=150)
    convergence.savefig(args.output_dir / "convergence.png", dpi=150)
    if not args.no_show:
        plt.show()
    plt.close(geometry)
    plt.close(convergence)


if __name__ == "__main__":
    main()
