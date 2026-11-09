"""Plotting utilities for the simulations."""

from pathlib import Path

import matplotlib.pyplot as plt


def plot_histogram(samples, bins=40, output_path="plots/histogram.png"):
    """Save a histogram of the original sample values."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots()
    ax.hist(samples, bins=bins, edgecolor="black", alpha=0.75)
    ax.set_title(f"Histogram of samples (n={len(samples):,})")
    ax.set_xlabel("Sample value X")
    ax.set_ylabel("Count")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path
