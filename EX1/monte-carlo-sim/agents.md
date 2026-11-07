# Agent Instructions

## Project scope

Use `README.MD` as the source of truth. This project estimates the union area of three unit disks with Monte Carlo sampling and visualizes both the geometry and estimator convergence.

## Technology and environment

- Use Python, managed with `uv`.
- Use NumPy for sampling, array operations, membership tests, and cumulative estimates.
- Use Matplotlib for plotting.
- Declare dependencies in `pyproject.toml` and keep `uv.lock` in sync. Do not use global installs or `pip` workflows.
- If the Python project has not been initialized, run `uv init --bare`, then `uv add numpy matplotlib`.
- Install/synchronize the environment with `uv sync`; run scripts with `uv run python <script.py>`.
- Add test tooling only when needed, using `uv add --dev pytest`; run tests with `uv run pytest`.

## Mathematical requirements

- Radius: `R = 1`.
- Disk centers: `(0, 0)`, `(1/2, sqrt(3)/2)`, and `(-1/2, sqrt(3)/2)`.
- Sample independent uniform points in `[-3/2, 3/2] × [-1, 1 + sqrt(3)/2]`.
- Rectangle area: `S = 3 * (2 + sqrt(3)/2)`.
- A point belongs to the union if its squared distance to **any** center is at most `1`. Count overlap points only once.
- For every `k = 1, ..., n`, compute the running area estimate as `S * cumulative_hits[k - 1] / k`.
- Require `n` to be a positive integer; reject invalid inputs clearly.

## Implementation conventions

- Prefer vectorized NumPy operations over Python loops over samples.
- Use `numpy.random.default_rng(seed)` and expose an optional seed for reproducible runs.
- Separate sampling, union membership, estimation, and plotting into small, testable functions.
- Keep computation independent of plotting; avoid running simulations or opening figures on import.
- Use a `main()` entry point guarded by `if __name__ == "__main__":` for executable scripts.
- Keep the implementation simple and focused on the README's scope. Document usage and any new options in `README.MD`.

## Required visualizations

1. Draw the three circle boundaries and sampled points, using distinct colors for points inside and outside the union. Show the enclosing rectangle, use equal axis scaling, and include labels and a legend.
2. Plot the running union-area estimate against iterations `1` through `n`, with labeled axes.

Support saving figures for headless use rather than requiring an interactive display. If scatter points are subsampled for performance, disclose this and still compute estimates using all `n` samples.

## Validation

- Test membership at disk centers, known exterior points, and disk boundaries.
- Check sample shapes and rectangle bounds.
- Check running estimates against a small, manually computed hit sequence.
- Verify estimates remain within `[0, S]` and seeded runs are reproducible.
- Smoke-test figure generation with a noninteractive Matplotlib backend, such as `MPLBACKEND=Agg`.
- Avoid brittle tests requiring a random estimate to equal the exact union area.
