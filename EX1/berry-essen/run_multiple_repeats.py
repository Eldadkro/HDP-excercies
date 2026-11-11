"""Section 2. Run with: uv run python run_multiple_repeats.py"""

import csv
from math import erf, sqrt
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


SAMPLE_SIZES = range(10, 101, 10)
RATE = 1.0
REPETITIONS = 100_000
HISTOGRAM_BINS = 100


def main():
    # Section 2 explicitly requests fresh randomness rather than a fixed seed.
    rng = np.random.default_rng()
    data_dir = Path("data")
    plot_dir = Path("plots")
    data_dir.mkdir(exist_ok=True)
    plot_dir.mkdir(exist_ok=True)
    population_mean = 1 / RATE
    grid = np.linspace(-4, 6, 600)
    normal_cdf = np.array([0.5 * (1 + erf(x / sqrt(2))) for x in grid])
    rows = []
    result_lines = [
        "## 2 — Multiple repeats",
        "",
        f"Exp(rate={RATE:g}); M={REPETITIONS:,} independent repetitions per n; "
        "no fixed seed. Standard deviations use ddof=1.",
        f"Population mean of sample means: {population_mean:g}; "
        "population SD: 1/(rate × √n). Z-scores use population moments.",
        "",
        "| n | Mean of sample means | SD of sample means | Theoretical SD | Mean histogram | Z-score CDF |",
        "| ---: | ---: | ---: | ---: | --- | --- |",
    ]
    print(f"Distribution: Exponential(rate={RATE:g}); n={list(SAMPLE_SIZES)}")
    print(f"M={REPETITIONS:,} independent repetitions per n; no fixed seed")
    print("Z = rate * sqrt(n) * (sample_mean - 1/rate); SD uses ddof=1")

    means_path = data_dir / "section_2_sample_means.csv"
    with means_path.open("w", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["n", "repeat", "sample_mean", "z_score"])
        for n in SAMPLE_SIZES:
            means = rng.exponential(scale=1 / RATE, size=(REPETITIONS, n)).mean(axis=1)
            z_scores = RATE * np.sqrt(n) * (means - population_mean)
            writer.writerows(
                (n, j, mean, z) for j, (mean, z) in enumerate(zip(means, z_scores), 1)
            )
            mean = means.mean()
            std = means.std(ddof=1)
            theoretical_std = 1 / (RATE * np.sqrt(n))
            rows.append((n, REPETITIONS, mean, std, population_mean, theoretical_std))

            histogram_path = plot_dir / f"section_2_sample_means_n_{n}.png"
            fig, ax = plt.subplots()
            ax.hist(means, bins=HISTOGRAM_BINS, density=True, alpha=0.75, label="Sample means")
            ax.axvline(population_mean, color="red", linestyle="--", label="Population mean")
            ax.text(
                0.97, 0.95, f"Observed mean = {mean:.6f}\nObserved SD = {std:.6f}",
                transform=ax.transAxes, ha="right", va="top",
            )
            ax.set(title=f"Exp(rate={RATE:g}) sample means: n={n}, M={REPETITIONS:,}",
                   xlabel="Sample mean", ylabel="Density")
            ax.legend(loc="upper left")
            fig.tight_layout()
            fig.savefig(histogram_path, dpi=150)
            plt.close(fig)

            cdf_path = plot_dir / f"section_2_z_cdf_n_{n}.png"
            fig, ax = plt.subplots()
            # Sort the M Z-scores in ascending order so they can serve as the
            # x-coordinates of the empirical CDF (smallest Z first).
            sorted_z = np.sort(z_scores)
            # For M sorted observations the empirical CDF jumps by 1/M at each
            # point, so the i-th value (i = 1..M) gets cumulative probability i/M.
            # np.arange(1, M+1) yields [1, 2, ..., M]; dividing by M maps it to
            # (0, 1], giving the y-coordinates that pair with sorted_z.
            cumulative_probability = np.arange(1, REPETITIONS + 1) / REPETITIONS
            # Plot the empirical CDF as a step-like curve: x = sorted Z-scores,
            # y = their cumulative probabilities, to compare against N(0, 1).
            ax.plot(sorted_z, cumulative_probability, linewidth=1.5,
                    label="Z-score empirical CDF")
            ax.plot(grid, normal_cdf, "r--", label="Standard normal CDF")
            ax.set(title=f"Standardized exponential means: n={n}, M={REPETITIONS:,}",
                   xlabel="Z = rate × √n × (sample mean − 1/rate)",
                   ylabel="Cumulative probability", ylim=(0, 1.02))
            ax.legend()
            fig.tight_layout()
            fig.savefig(cdf_path, dpi=150)
            plt.close(fig)

            result_lines.append(
                f"| {n} | {mean:.6f} | {std:.6f} | {theoretical_std:.6f} | "
                f"[Plot]({histogram_path.as_posix()}) | [Plot]({cdf_path.as_posix()}) |"
            )
            print(f"n={n:3d}: mean={mean:.6f}, SD={std:.6f}, theoretical SD={theoretical_std:.6f}")

    summary_path = data_dir / "section_2_summary.csv"
    with summary_path.open("w", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["n", "repetitions", "mean_of_sample_means", "sd_of_sample_means",
                         "theoretical_mean", "theoretical_sd"])
        writer.writerows(rows)

    result_lines.extend([
        "", f"[All sample means and Z-scores]({means_path.as_posix()}) · "
        f"[Summary CSV]({summary_path.as_posix()})", "",
    ])
    results_path = Path("results.md")
    with results_path.open("a") as output:
        if results_path.stat().st_size:
            output.write("\n")
        output.write("\n".join(result_lines))
    print(f"Saved {REPETITIONS * len(SAMPLE_SIZES):,} rows to {means_path}")
    print(f"Summary: {summary_path}; 20 plots in {plot_dir}; results appended to {results_path}")


if __name__ == "__main__":
    main()
