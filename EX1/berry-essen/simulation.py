"""Sample independent exponential random variables."""

import numpy as np


def sample_exponential(n, rate=1.0, seed=None):
    """Return n Exp(rate) samples and their empirical mean.

    An integer seed makes results reproducible; None uses fresh system entropy.
    """
    rng = np.random.default_rng(seed)
    samples = rng.exponential(scale=1 / rate, size=n)
    return samples, samples.mean()
