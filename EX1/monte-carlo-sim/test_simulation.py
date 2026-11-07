import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

from simulation import (
    CENTERS, LOWER, UPPER, RECTANGLE_AREA,
    sample_points, union_membership, running_estimates, simulate,
    plot_geometry, plot_convergence,
)


def test_membership():
    assert union_membership(CENTERS).all()
    points = [[0, -1], [1.5, np.sqrt(3) / 2], [-1.5, np.sqrt(3) / 2],
              [0, -1.001], [1.5, -1], [10, 10], [0, 0.5]]
    np.testing.assert_array_equal(
        union_membership(points), [True, True, True, False, False, False, True]
    )


def test_samples():
    points = sample_points(1000, seed=42)
    assert points.shape == (1000, 2)
    assert np.all(points >= LOWER)
    assert np.all(points <= UPPER)
    np.testing.assert_array_equal(points, sample_points(1000, seed=42))


@pytest.mark.parametrize("n", [0, -1, 2.5, "10", True, np.bool_(True)])
def test_invalid_sample_count(n):
    with pytest.raises(ValueError, match="positive integer"):
        simulate(n)


def test_running_estimates():
    np.testing.assert_allclose(
        running_estimates([1, 0, 1, 1]), RECTANGLE_AREA * np.array([1, 0.5, 2 / 3, 0.75])
    )


@pytest.mark.parametrize("hits", [[], [[1]], [0, 2], [np.nan]])
def test_invalid_hits(hits):
    with pytest.raises(ValueError):
        running_estimates(hits)


def test_simulation():
    first = simulate(1000, seed=123)
    second = simulate(1000, seed=123)
    assert np.all((first.estimates >= 0) & (first.estimates <= RECTANGLE_AREA))
    np.testing.assert_array_equal(first.points, second.points)
    np.testing.assert_array_equal(first.hits, second.hits)
    np.testing.assert_array_equal(first.estimates, second.estimates)
    assert simulate(1, seed=0).estimates.shape == (1,)


def test_figures(tmp_path):
    result = simulate(50, seed=42)
    for plot, name in [(plot_geometry, "geometry"), (plot_convergence, "convergence")]:
        fig, ax = plot(result)
        path = tmp_path / f"{name}.png"
        fig.savefig(path)
        assert path.stat().st_size > 0
        assert ax.get_xlabel() and ax.get_ylabel()
        plt.close(fig)
