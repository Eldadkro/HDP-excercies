# Monte Carlo Simulations for Three Circles

We consider three circles of radius $R = 1$ with the following centers:

1. $(0, 0)$
2. $(\cos(\pi/3), \sin(\pi/3)) = (\frac{1}{2}, \frac{\sqrt{3}}{2})$
3. $(-\cos(\pi/3), \sin(\pi/3)) = (-\frac{1}{2}, \frac{\sqrt{3}}{2})$

All three circles are enclosed in the rectangle $[-\frac{3}{2}, \frac{3}{2}] \times [-1, 1 + \frac{\sqrt{3}}{2}]$.

## Monte Carlo Area Estimation

Let $A$, $B$, and $C$ denote the disks enclosed by the three circles. We estimate the area of their union using the indicator function

$$
f(x) = \begin{cases}
1, & x \in A \cup B \cup C, \\
0, & \text{otherwise}.
\end{cases}
$$

Given a positive integer input $n$, sample $n$ independent points uniformly from the enclosing rectangle. Its area is

$$
S = 3\left(2 + \frac{\sqrt{3}}{2}\right).
$$

After iteration $k$, the estimated union area is

$$
\widehat{a}_k = \frac{S}{k}\sum_{i=1}^{k} f(X_i), \qquad k = 1, \ldots, n.
$$

The exact union area is $a = 3\pi/2 + \sqrt{3}$.

## Visualizations

- Plot the three circles and a scatter plot of the sampled points in the rectangle, distinguishing points inside the union from those outside it.
- Plot the running area estimate $\widehat{a}_k$ on the vertical axis against iteration $k$ on the horizontal axis.
- Plot the absolute error $|\widehat{a}_n-a|$ against sample count $n$, with logarithmic scales on both axes and a dashed $1/\sqrt{n}$ reference curve (not an error bound). Also show trailing moving averages of the absolute errors with windows of 10, 100, and 500 samples. Each curve starts at its window size and is omitted for shorter runs. Zero errors are masked because logarithmic axes cannot display zero.

## Usage

Requires Python 3.11+ and `uv`.

```bash
uv sync
uv run python simulation.py 10000 --seed 42
```

The sample count must be a positive integer. The optional nonnegative `--seed` makes runs reproducible. The script prints the final area estimate, saves all three plots as `plots/geometry.png`, `plots/convergence.png`, and `plots/error.png`, and displays them. The `plots/` directory is created automatically relative to the working directory; existing images are overwritten. Use `--output-dir` to choose another directory.

Save figures without an interactive display:

```bash
MPLBACKEND=Agg uv run python simulation.py 10000 --seed 42 --output-dir figures --no-show
```

This writes `figures/geometry.png`, `figures/convergence.png`, and `figures/error.png`. All samples are used for both estimation and plotting; no scatter subsampling is performed.

### Averaging independent simulations

```bash
MPLBACKEND=Agg uv run python simulation.py 10000 --seed 42 --MLE-avg 10 --no-show
```

The optional `--MLE-avg M` flag runs exactly M independent simulations (M must be positive). It adds `plots/error_avg.png`: faint individual absolute-error trajectories, their pointwise mean absolute error, and the asymptotic reference $\sqrt{2a(S-a)/\pi}/\sqrt{n}$ on log–log axes. Despite the flag name, this computes MAE, not maximum likelihood. Errors are averaged after taking absolute values, not before.

The usual three plots show the first run. With this flag, `--seed` reproducibly spawns independent random streams, so the first run differs from the unflagged run with the same seed. Without the flag, behavior is unchanged. The errors array uses memory proportional to M times n.

`simulate_average(n, repeats, seed=None)` returns the first `SimulationResult` and an `(repeats, n)` absolute-errors array. `plot_average_error(errors)` returns a `(figure, axes)` pair.

### Python functions

`simulation.py` provides `sample_points(n, seed=None)`, `union_membership(points)`, and `running_estimates(hits)` as separate computation utilities. `simulate(n, seed=None)` returns a `SimulationResult` containing `points`, `hits`, and `estimates` arrays. Importing the module does not run a simulation or open figures.

`plot_geometry(result)`, `plot_convergence(result)`, and `plot_error(result)` each return a Matplotlib `(figure, axes)` pair without displaying it.

```python
from simulation import simulate, plot_convergence

result = simulate(10000, seed=42)
print(result.estimates[-1])
fig, ax = plot_convergence(result)
fig.savefig("convergence.png")
```

## Tests

```bash
MPLBACKEND=Agg uv run pytest
```
