# Monte Carlo error: CLT, Berry–Esseen, and concentration bounds

## Setup

Let $a$ be the exact union area and $S$ the sampling rectangle's area:

$$
a=\frac{3\pi}{2}+\sqrt3,
\qquad S=3\left(2+\frac{\sqrt3}{2}\right).
$$

For independent uniform samples from the rectangle, define

$$
I_i=\mathbf 1\{X_i\text{ lies in the union}\}.
$$

Then $I_i$ are independent Bernoulli random variables with success probability $p=a/S$. The Monte Carlo estimator is

$$
\widehat a_n=\frac Sn\sum_{i=1}^n I_i.
$$

It is unbiased, and

$$
\operatorname{Var}(\widehat a_n)
=\frac{S^2p(1-p)}n
=\frac{a(S-a)}n.
$$

## Deriving the asymptotic mean absolute error reference

Write $\sigma^2=a(S-a)$. By the central limit theorem (CLT),

$$
\frac{\sqrt n(\widehat a_n-a)}{\sigma}
\xrightarrow{d} Z,\qquad Z\sim N(0,1).
$$

Thus, for large $n$, the error behaves approximately like $\sigma Z/\sqrt n$. A standard normal variable satisfies

$$
\mathbb E|Z|
=\frac{2}{\sqrt{2\pi}}\int_0^\infty z e^{-z^2/2}\,dz
=\sqrt{\frac2\pi}.
$$

Consequently,

$$
\boxed{\mathbb E|\widehat a_n-a|
\sim \sqrt{\frac{2a(S-a)}{\pi}}\,\frac1{\sqrt n}.}
$$

This is the theoretical asymptotic reference plotted alongside the empirical mean absolute error (MAE).

**Technical justification:** convergence in distribution alone does not imply convergence of expectations. Here the normalized errors have second moment exactly one, so their absolute values are uniformly integrable. This justifies convergence of their first absolute moments.

For $M$ independent simulations, the empirical curve is

$$
\operatorname{MAE}_M(n)
=\frac1M\sum_{j=1}^M|\widehat a_n^{(j)}-a|.
$$

It estimates the expected absolute error. Absolute values are taken **before** averaging. A finite number of runs will still produce fluctuations.

## Why use the CLT rather than Berry–Esseen or MGF bounds?

These tools answer different questions.

### CLT: what error should we typically observe?

The CLT gives the limiting shape of the normalized error distribution and, with the moment justification above, the asymptotically correct MAE constant. This makes it useful for a reference curve intended to match average observed performance.

It is not a finite-sample upper bound and does not assert that a single trajectory decreases monotonically.

### Berry–Esseen: how accurate is the normal approximation?

Berry–Esseen strengthens the CLT by quantifying the finite-sample discrepancy between the normalized error's cumulative distribution function and the standard normal CDF $\Phi$:

$$
\sup_x\left|
\Pr\!\left(\frac{\sqrt n(\widehat a_n-a)}{\sigma}\le x\right)
-\Phi(x)\right|
\le
\frac{C\,\mathbb E|I_i-p|^3}{[p(1-p)]^{3/2}\sqrt n},
$$

where $C$ is a universal constant. For Bernoulli variables,

$$
\mathbb E|I_i-p|^3
=p(1-p)^3+(1-p)p^3
=p(1-p)\big[(1-p)^2+p^2\big].
$$

Therefore,

$$
\sup_x\left|
\Pr\!\left(\frac{\sqrt n(\widehat a_n-a)}{\sigma}\le x\right)
-\Phi(x)\right|
\le \frac{C\,[p^2+(1-p)^2]}{\sqrt{np(1-p)}}.
$$

This is useful when asking **how reliable the Gaussian approximation is at a given sample count**. It complements the CLT rather than changing its limiting prediction. Turning this uniform CDF bound into an absolute-moment bound requires additional tail control; integrating a constant CDF error over an unbounded domain does not suffice.

### MGF-based concentration: how unlikely is a large error?

Moment-generating-function (MGF) methods give finite-sample tail bounds. For example, Hoeffding's inequality gives

$$
\Pr(|\widehat a_n-a|\ge t)
\le 2\exp\!\left(-\frac{2nt^2}{S^2}\right).
$$

For a fixed $n$, with probability at least $1-\delta$,

$$
|\widehat a_n-a|
\le S\sqrt{\frac{\log(2/\delta)}{2n}}.
$$

This also exhibits the $n^{-1/2}$ scale, but the constant describes a **confidence bound**, not expected absolute error. Such a curve is generally conservative relative to the MAE. This is a pointwise guarantee for a fixed sample count, not automatically a simultaneous guarantee over all sample counts in a plot.

## An exact alternative: RMSE

No normal approximation is necessary for the root mean squared error. Unbiasedness and the variance calculation give, for every positive integer $n$,

$$
\boxed{\operatorname{RMSE}(n)
=\sqrt{\mathbb E(\widehat a_n-a)^2}
=\frac{\sqrt{a(S-a)}}{\sqrt n}.}
$$

In particular, Cauchy–Schwarz already provides the finite-sample bound

$$
\mathbb E|\widehat a_n-a|
\le \frac{\sqrt{a(S-a)}}{\sqrt n}.
$$

The CLT sharpens this into an asymptotic equivalence with the factor $\sqrt{2/\pi}$.

## What to show in the plot

- Use faint individual absolute-error trajectories to show run-to-run variability.
- Overlay a bold empirical MAE across independent simulations.
- Add the asymptotic MAE reference $\sqrt{2a(S-a)/\pi}/\sqrt n$.
- On log–log axes, the reference has slope $-1/2$.
- Optionally plot $\sqrt n\,\operatorname{MAE}_M(n)$ in a second panel; it should fluctuate around an approximately constant level for sufficiently large $n$ and enough runs.
- If a finite-sample guarantee is the goal, add a clearly labeled concentration bound instead of interpreting the MAE reference as a bound.

Moving averages along a single simulation do not replace averaging independent runs: neighboring running estimates are strongly correlated, and sharp dips can occur when the estimate crosses the exact area. The convergence claim concerns the typical error scale, not monotonic decay along one trajectory.
