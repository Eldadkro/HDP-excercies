# Exponential sampling

## 1. Generate independent exponential random variables

We want to write a function that generates $n$ independent and identically distributed (i.i.d.) random variables

$$
X_1, \ldots, X_n \sim \operatorname{Exp}(\lambda),
$$

where $\lambda > 0$ is the **rate parameter**. For the current experiment, we use $\lambda = 1$.

The probability density function is

$$
f_X(x) =
\begin{cases}
\lambda e^{-\lambda x}, & x \ge 0, \\
0, & x < 0.
\end{cases}
$$

For $\lambda = 1$, this reduces to $f_X(x) = e^{-x}$ for $x \ge 0$. The population mean and variance are

$$
\mathbb{E}[X_i] = \frac{1}{\lambda},
\qquad
\operatorname{Var}(X_i) = \frac{1}{\lambda^2}.
$$

### Function inputs and outputs

**Inputs:**
- $n$: the number of samples (a positive integer).
- $\lambda$: the rate parameter (positive; set to $1$ for this experiment).
- `seed`: an optional random seed, defaulting to `None`. Providing a specific integer seed makes repeated calls with the same inputs reproducible; leaving it as `None` initializes the generator using fresh system entropy.

**Outputs:**
- The vector of samples $(X_1, \ldots, X_n)$.
- Their empirical mean,

$$
\overline{X}_n = \frac{1}{n}\sum_{i=1}^{n} X_i.
$$

### NumPy implementation note

Initialize the generator with `rng = numpy.random.default_rng(seed)`. NumPy's exponential sampler takes a **scale** parameter, not a rate, so generate the samples with `rng.exponential(scale=1 / rate, size=n)`, where `rate` represents $\lambda$.

```python
import numpy as np


def sample_exponential(n, rate=1.0, seed=None):
    rng = np.random.default_rng(seed)
    samples = rng.exponential(scale=1 / rate, size=n)
    return samples, samples.mean()
```

Use `sample_exponential(n, seed=42)` for reproducible samples, or `sample_exponential(n)` for a fresh random initialization. For reported experiments, supply an explicit seed so the results can be reproduced.


## 1.5 plot for multiple n 

1) we want to repeat the experiment above, were we draw exp rvs 
2) we want to do that with n=10:100:10 (from 10 to 100 with jumps of 10, 100 included)
3) we want to create a histogram for each, 
we want to save a markdown with a table of the empirical avarage for each n.
 
4) in addition we want to plot a scatter of the emerical avarage for each n 


## 2. multiple repeats 


1) now we want to repeat (1.5) M = 10^5 times for each n, collect all the results into csv (dont fix the seed so it will be random)
2) collect the empirial avarages for each n, calculate its standard deviation and mean, plot for each n its histogram for the empirical means and write on the plot the mean and std 
3) for each n collect the M sample means, for each empirical avarage clculate the CLT $Z$-score
$$
Z_{n,j} =  \lambda\sqrt{n}\left(\overline{X}_{n,j} - \frac{1}{\lambda}\right),
\qquad j = 1, \ldots, M,
$$

plot the CDF of the Z score as a histogram.