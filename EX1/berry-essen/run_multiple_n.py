"""Section 1.5. Run with: uv run python run_multiple_n.py"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from simulation import sample_exponential
from utils import plot_histogram


SAMPLE_SIZES = range(10, 101, 10)
RATE = 1.0
SEED = 42
HISTOGRAM_BINS = 10


def main():
    rng = np.random.default_rng(SEED)
    means = []
    histogram_paths = []

    print(f"Distribution: Exponential(rate={RATE}); population mean: {1 / RATE:g}")
    print(f"Sample sizes: {list(SAMPLE_SIZES)}")
    print(f"Monte Carlo repetitions: 1 independent sample vector per n; seed: {SEED}")
    for n in SAMPLE_SIZES:
        samples, empirical_mean = sample_exponential(n, rate=RATE, seed=rng)
        means.append(empirical_mean)
        path = plot_histogram(
            samples,
            bins=HISTOGRAM_BINS,
            output_path=f"plots/section_1_5_histogram_n_{n}.png",
        )
        histogram_paths.append(path)
        print(f"n={n:3d}: empirical mean={empirical_mean:.6f}; histogram: {path}")

    scatter_path = Path("plots/section_1_5_empirical_means.png")
    fig, ax = plt.subplots()
    ax.scatter(list(SAMPLE_SIZES), means, label="Empirical mean")
    ax.axhline(1 / RATE, color="red", linestyle="--", label="Population mean")
    ax.set_title(f"Exponential(rate={RATE:g}): one sample vector per n")
    ax.set_xlabel("Sample size n")
    ax.set_ylabel("Empirical mean")
    ax.set_xticks(list(SAMPLE_SIZES))
    ax.legend()
    fig.tight_layout()
    fig.savefig(scatter_path, dpi=150)
    plt.close(fig)
    print(f"Scatter plot: {scatter_path}")

    lines = [
        "## 1.5 — Exponential samples across sample sizes",
        "",
        f"Exp(rate={RATE:g}); population mean={1 / RATE:g}; seed={SEED}; "
        "one independent sample vector per n.",
        "",
        "| n | Empirical mean | Histogram |",
        "| ---: | ---: | --- |",
    ]
    for n, mean, path in zip(SAMPLE_SIZES, means, histogram_paths):
        lines.append(f"| {n} | {mean:.6f} | [Plot]({path.as_posix()}) |")
    lines.extend(["", f"![Empirical means by sample size]({scatter_path.as_posix()})", ""])
    results_path = Path("results.md")
    with results_path.open("a") as output:
        if results_path.stat().st_size:
            output.write("\n")
        output.write("\n".join(lines))
    print(f"Results appended to: {results_path}")


if __name__ == "__main__":
    main()
