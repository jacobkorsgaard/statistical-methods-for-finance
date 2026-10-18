from finstats.simulation import simulate_arch1, simulate_garch11
import numpy as np
import pytest
from statsmodels.stats.diagnostic import acorr_ljungbox
from finstats.diagnostics import mcleod_li, standardized_residuals


def test_simulation_reproducibility_and_recursion():
    for function, args in [
        (simulate_arch1, (2, 0.4, 100)),
        (simulate_garch11, (1, 0.1, 0.8, 100)),
    ]:
        a, h = function(*args, rng=606)
        a2, h2 = function(*args, rng=606)
        np.testing.assert_array_equal(a, a2)
        np.testing.assert_array_equal(h, h2)
        assert len(a) == 100 and np.all(h > 0)
        omega, alpha = args[:2]
        beta = 0 if function is simulate_arch1 else args[2]
        np.testing.assert_allclose(h[1:], omega + alpha * a[:-1] ** 2 + beta * h[:-1])
    a, h = simulate_garch11(1, 0, 0, 100, rng=606)
    assert np.all(h == 1)


def test_simulated_population_variance_low_persistence():
    a, h = simulate_arch1(2, 0.2, 50000, rng=604)
    assert abs(np.var(a) - 2.5) < 0.08
    assert abs(h.mean() - 2.5) < 0.05


def test_standardization_and_squared_portmanteau():
    np.testing.assert_allclose(standardized_residuals([2, -3], [2, 1]), [1, -3])
    x = np.random.default_rng(608).normal(size=100)
    ours = mcleod_li(x, 10)
    reference = acorr_ljungbox(x * x, lags=[10]).iloc[0]
    assert ours["statistic"] == pytest.approx(reference.lb_stat)
    assert ours["p_value"] == pytest.approx(reference.lb_pvalue)


@pytest.mark.parametrize(
    "omega,alpha,beta",
    [
        (0, 0.1, 0.8),
        (-1, 0.1, 0.8),
        (1, -0.1, 0.8),
        (1, 0.1, -0.1),
        (np.nan, 0.1, 0.8),
        (1, np.inf, 0.8),
    ],
)
def test_invalid_variance_parameters(omega, alpha, beta):
    with pytest.raises(ValueError):
        simulate_garch11(omega, alpha, beta, 10)


@pytest.mark.parametrize("omega,alpha", [(0, 0.2), (1, -0.1), (1, np.nan)])
def test_invalid_arch_parameters(omega, alpha):
    with pytest.raises(ValueError):
        simulate_arch1(omega, alpha, 10)


@pytest.mark.parametrize("bad", [0, -1, 1.5, True])
def test_invalid_simulation_lengths(bad):
    with pytest.raises(ValueError):
        simulate_garch11(1, 0.1, 0.8, bad)


@pytest.mark.parametrize(
    "a,h",
    [([1], [0]), ([1], [-1]), ([1], [np.nan]), ([1, 2], [1]), ([], []), ([1j], [1])],
)
def test_invalid_standardization(a, h):
    with pytest.raises(ValueError):
        standardized_residuals(a, h)


@pytest.mark.parametrize("initial", [0, -1, np.nan, np.inf])
def test_invalid_initial_variance(initial):
    with pytest.raises(ValueError):
        simulate_garch11(1, 0.1, 0.8, 2, initial_variance=initial)


def test_student_innovations_are_standardized_and_aligned():
    a, h = simulate_garch11(1, 0, 0, 80, rng=42, df=5)
    expected = np.random.default_rng(42).standard_t(5, 1080)[1000:] * np.sqrt(3 / 5)
    np.testing.assert_array_equal(a, expected)
    np.testing.assert_array_equal(h, np.ones(80))
    a, h = simulate_garch11(0.05, 0.05, 0.9, 80, rng=42, df=5)
    np.testing.assert_allclose(h[1:], 0.05 + 0.05 * a[:-1] ** 2 + 0.9 * h[:-1])


@pytest.mark.parametrize("df", [1, 2, np.nan, np.inf])
def test_student_simulation_requires_finite_variance(df):
    with pytest.raises(ValueError):
        simulate_garch11(1, 0, 0, 10, df=df)


@pytest.mark.parametrize("beta", [.8,.9])
def test_simulation_with_unit_or_above_unit_persistence(beta):
    a,h=simulate_garch11(.1,.2,beta,30,rng=91,initial_variance=2.,burn_in=0)
    assert h[0]==2.
    np.testing.assert_allclose(h[1:],.1+.2*a[:-1]**2+beta*h[:-1])
    assert np.isfinite(h).all()
