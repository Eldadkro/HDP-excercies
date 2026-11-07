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

## Visualizations

- Plot the three circles and a scatter plot of the sampled points in the rectangle, distinguishing points inside the union from those outside it.
- Plot the running area estimate $\widehat{a}_k$ on the vertical axis against iteration $k$ on the horizontal axis.

## Usage

Requires Python 3.11+ and `uv`.

```bash
uv sync
uv run python simulation.py 10000 --seed 42
```

The sample count must be a positive integer. The optional nonnegative `--seed` makes runs reproducible. The script prints the final area estimate, saves both plots as `plots/geometry.png` and `plots/convergence.png`, and displays them. The `plots/` directory is created automatically relative to the working directory; existing images are overwritten. Use `--output-dir` to choose another directory.

Save figures without an interactive display:

```bash
MPLBACKEND=Agg uv run python simulation.py 10000 --seed 42 --output-dir figures --no-show
```

This writes `figures/geometry.png` and `figures/convergence.png`. All samples are used for both estimation and plotting; no scatter subsampling is performed.

### Python functions

`simulation.py` provides `sample_points(n, seed=None)`, `union_membership(points)`, and `running_estimates(hits)` as separate computation utilities. `simulate(n, seed=None)` returns a `SimulationResult` containing `points`, `hits`, and `estimates` arrays. Importing the module does not run a simulation or open figures.

`plot_geometry(result)` and `plot_convergence(result)` each return a Matplotlib `(figure, axes)` pair without displaying it.

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
