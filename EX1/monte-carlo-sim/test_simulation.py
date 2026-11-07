import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

from simulation import (
    CENTERS, LOWER, UPPER, RECTANGLE_AREA, EXACT_AREA,
    sample_points, union_membership, running_estimates, simulate,
    plot_geometry, plot_convergence, plot_error, simulate_average, plot_average_error,
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


def test_error_plot():
    result = simulate(50, seed=42)
    result.estimates[0] = EXACT_AREA
    fig, ax = plot_error(result)
    assert ax.get_xscale() == ax.get_yscale() == "log"
    line = ax.lines[0]
    np.testing.assert_array_equal(line.get_xdata(), np.arange(1, 51))
    reference = ax.lines[1]
    np.testing.assert_array_equal(reference.get_xdata(), np.arange(1, 51))
    np.testing.assert_allclose(reference.get_ydata(), 1 / np.sqrt(np.arange(1, 51)))
    smoothed = ax.lines[2]
    np.testing.assert_array_equal(smoothed.get_xdata(), np.arange(10, 51))
    expected = [np.mean(np.abs(result.estimates[i - 9:i + 1] - EXACT_AREA))
                for i in range(9, 50)]
    np.testing.assert_allclose(smoothed.get_ydata(), expected)
    assert ax.get_legend() is not None
    errors = line.get_ydata()
    assert np.ma.getmaskarray(errors)[0]
    np.testing.assert_allclose(errors[1:], np.abs(result.estimates[1:] - EXACT_AREA))
    plt.close(fig)


@pytest.mark.parametrize("n", [1, 9, 10, 99, 100, 499, 500, 600])
def test_error_plot_short_runs(n):
    result = simulate(n, seed=42)
    fig, ax = plot_error(result)
    windows = [window for window in (10, 100, 500) if window <= n]
    assert len(ax.lines) == 2 + len(windows)
    errors = np.abs(result.estimates - EXACT_AREA)
    for line, window in zip(ax.lines[2:], windows):
        np.testing.assert_array_equal(line.get_xdata(), np.arange(window, n + 1))
        expected = [errors[i - window + 1:i + 1].mean()
                    for i in range(window - 1, n)]
        np.testing.assert_allclose(line.get_ydata(), expected)
    plt.close(fig)


def test_average_error(tmp_path):
    first, errors = simulate_average(50, 10, seed=42)
    assert errors.shape == (10, 50)
    np.testing.assert_allclose(errors[0], np.abs(first.estimates - EXACT_AREA))
    np.testing.assert_array_equal(errors, simulate_average(50, 10, seed=42)[1])
    assert not np.array_equal(errors[0], errors[1])
    fig, ax = plot_average_error(errors)
    assert ax.get_xscale() == ax.get_yscale() == "log"
    np.testing.assert_allclose(ax.lines[10].get_ydata(), errors.mean(axis=0))
    reference = np.sqrt(2 * EXACT_AREA * (RECTANGLE_AREA - EXACT_AREA)
                        / (np.pi * np.arange(1, 51)))
    np.testing.assert_allclose(ax.lines[11].get_ydata(), reference)
    fig.savefig(tmp_path / "error_avg.png")
    plt.close(fig)


@pytest.mark.parametrize("repeats", [0, -1, True, 1.5])
def test_invalid_repeats(repeats):
    with pytest.raises(ValueError, match="positive integer"):
        simulate_average(50, repeats)


def test_figures(tmp_path):
    result = simulate(50, seed=42)
    for plot, name in [(plot_geometry, "geometry"), (plot_convergence, "convergence"), (plot_error, "error")]:
        fig, ax = plot(result)
        path = tmp_path / f"{name}.png"
        fig.savefig(path)
        assert path.stat().st_size > 0
        assert ax.get_xlabel() and ax.get_ylabel()
        plt.close(fig)
