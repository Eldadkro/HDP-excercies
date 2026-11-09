# CLT and Berry–Esseen simulations

## Goal
Use random simulations to study the central limit theorem (CLT) and compare the distribution of standardized sums with the standard normal distribution and the Berry–Esseen bound.

## Environment
- Manage dependencies and the virtual environment with `uv`.
- Use NumPy for sampling and numerical calculations and Matplotlib for plots.
- Run scripts with `uv run python <script>.py`; restore dependencies with `uv sync`.
- Keep `pyproject.toml` and `uv.lock` under version control, not `.venv` or caches.

## Coding style
- These are one-off course simulations, not a reusable library. Keep scripts short, readable, and direct.
- Prefer a few clearly named parameters at the top of each script over CLI frameworks or configuration layers.
- Avoid extensive input validation, defensive checks, elaborate abstractions, and large test suites. Use only lightweight sanity checks when useful.
- Use `numpy.random.default_rng` with an explicit seed for reproducibility.
- Print the parameters and numerical summaries needed to interpret each experiment. Label plots clearly, including axes and legends.
- Generate only plots and printed results needed for the current experiment. Put generated plots in `plots/`.

## Results in Markdown
- Whenever we discuss recording results in Markdown, append them to `results.md`; preserve existing results.
- Put each result under a heading containing its corresponding number from `Deriviation.md` and a short, descriptive title.
- Keep `results.md` compact and simple. Include only the results; omit unnecessary explanation or commentary unless explicitly requested.

## Mathematical conventions
- For iid samples with mean mu and variance sigma^2 > 0, standardize sums as (sum(X_i) - n*mu) / (sigma*sqrt(n)).
- State the sampling distribution, sample size n, and number of Monte Carlo repetitions.
- For Berry–Esseen comparisons, specify the constant C and use C * E[|X - mu|^3] / (sigma^3 * sqrt(n)), assuming a finite third absolute centered moment.
- Distinguish the theoretical CDF error bound from Monte Carlo estimation error. A finite-grid empirical CDF discrepancy is an estimate, not a certified supremum or proof.
- Use known population moments when available; clearly label any estimated moments.
