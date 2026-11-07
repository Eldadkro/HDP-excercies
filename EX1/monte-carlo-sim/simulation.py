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
EXACT_AREA = 3 * np.pi / 2 + np.sqrt(3)


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


def plot_error(result: SimulationResult):
    """Plot absolute error against sample count on log–log axes.

    Include trailing 10-, 100-, and 500-sample means using full windows only.
    Zero errors are masked because they cannot be represented on a log scale.
    """
    import matplotlib.pyplot as plt

    errors = np.abs(result.estimates - EXACT_AREA)
    fig, ax = plt.subplots()
    n = np.arange(1, len(errors) + 1)
    ax.loglog(n, np.ma.masked_equal(errors, 0), label="Absolute error")
    ax.loglog(n, 1 / np.sqrt(n), "--", label=r"$1/\sqrt{n}$ reference")
    for window in (10, 100, 500):
        if len(errors) >= window:
            smoothed = np.convolve(errors, np.ones(window) / window, mode="valid")
            ax.loglog(n[window - 1:], np.ma.masked_equal(smoothed, 0),
                      label=f"Absolute error ({window}-sample moving average)")
    ax.legend()
    ax.set(xlabel="Sample count n", ylabel="Absolute area error", title="Monte Carlo error")
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    return fig, ax


def simulate_average(n: int, repeats: int, seed: int | None = None):
    """Return the first run and absolute errors from independent seeded runs."""
    if isinstance(repeats, (bool, np.bool_)) or not isinstance(repeats, (int, np.integer)) or repeats <= 0:
        raise ValueError("repeats must be a positive integer")
    seeds = np.random.SeedSequence(seed).spawn(repeats)
    first = simulate(n, seeds[0])
    errors = np.empty((repeats, n))
    errors[0] = np.abs(first.estimates - EXACT_AREA)
    for i in range(1, repeats):
        errors[i] = np.abs(simulate(n, seeds[i]).estimates - EXACT_AREA)
    return first, errors


def plot_average_error(errors: np.ndarray):
    """Plot individual absolute errors and their pointwise mean on log–log axes."""
    import matplotlib.pyplot as plt

    errors = np.asarray(errors, dtype=float)
    if errors.ndim != 2 or 0 in errors.shape or not np.isfinite(errors).all() or (errors < 0).any():
        raise ValueError("errors must be a nonempty finite nonnegative (runs, samples) array")
    n = np.arange(1, errors.shape[1] + 1)
    fig, ax = plt.subplots()
    for i, run in enumerate(errors):
        ax.loglog(n, np.ma.masked_equal(run, 0), color="gray", alpha=0.2,
                  linewidth=0.7, label="Individual runs" if i == 0 else None)
    ax.loglog(n, np.ma.masked_equal(errors.mean(axis=0), 0), linewidth=2,
              label=f"Mean absolute error ({len(errors)} runs)")
    reference = np.sqrt(2 * EXACT_AREA * (RECTANGLE_AREA - EXACT_AREA) / (np.pi * n))
    ax.loglog(n, reference, "--", label=r"Asymptotic MAE: $\sqrt{2a(S-a)/\pi}/\sqrt{n}$")
    ax.set(xlabel="Sample count n", ylabel="Absolute area error",
           title="Monte Carlo mean absolute error")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    return fig, ax


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int, help="positive number of samples")
    parser.add_argument("--seed", type=int, help="nonnegative random seed")
    parser.add_argument("--output-dir", type=Path, default=Path("plots"), help="directory for geometry.png, convergence.png, and error.png (default: plots/)")
    parser.add_argument("--no-show", action="store_true", help="do not open interactive figures")
    parser.add_argument("--MLE-avg", dest="mle_avg", type=int, metavar="M",
                        help="average absolute errors across M independent simulations; save error_avg.png")
    args = parser.parse_args()
    if args.n <= 0:
        parser.error("n must be a positive integer")
    if args.seed is not None and args.seed < 0:
        parser.error("seed must be nonnegative")
    if args.mle_avg is not None and args.mle_avg <= 0:
        parser.error("--MLE-avg must be a positive integer")
    if args.mle_avg is None:
        result = simulate(args.n, args.seed)
    else:
        result, errors = simulate_average(args.n, args.mle_avg, args.seed)
        print(f"Mean absolute error ({args.mle_avg} runs): {errors[:, -1].mean():.6f}")
    print(f"Estimated union area: {result.estimates[-1]:.6f} ({args.n:,} samples)")

    import matplotlib.pyplot as plt

    geometry, _ = plot_geometry(result)
    convergence, _ = plot_convergence(result)
    error, _ = plot_error(result)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    geometry.savefig(args.output_dir / "geometry.png", dpi=150)
    convergence.savefig(args.output_dir / "convergence.png", dpi=150)
    error.savefig(args.output_dir / "error.png", dpi=150)
    average = None
    if args.mle_avg is not None:
        average, _ = plot_average_error(errors)
        average.savefig(args.output_dir / "error_avg.png", dpi=150)
    if not args.no_show:
        plt.show()
    if average is not None:
        plt.close(average)
    plt.close(geometry)
    plt.close(convergence)
    plt.close(error)


if __name__ == "__main__":
    main()
