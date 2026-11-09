"""Run with: uv run python run_simulation.py"""

from simulation import sample_exponential
from utils import plot_histogram


N = 1_000
RATE = 1.0
SEED = 42  # Set to None for a fresh random initialization.
HISTOGRAM_BINS = 40


def main():
    samples, empirical_mean = sample_exponential(N, rate=RATE, seed=SEED)

    print(f"Distribution: Exponential(rate={RATE})")
    print(f"Number of samples: {N}")
    print("Monte Carlo repetitions: 1 sample vector")
    print(f"Seed: {SEED}")
    print(f"First 10 samples: {samples[:10]}")
    print(f"Empirical mean: {empirical_mean:.6f}")
    print(f"Population mean: {1 / RATE:.6f}")
    print(f"Population variance: {1 / RATE**2:.6f}")

    plot_path = plot_histogram(samples, bins=HISTOGRAM_BINS)
    print(f"Histogram saved to: {plot_path}")


if __name__ == "__main__":
    main()
