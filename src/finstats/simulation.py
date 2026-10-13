"""Reproducible process simulations with explicit initialization and indexing."""

import numpy as np
from numpy.typing import ArrayLike, NDArray
from ._validation import _sample, _integer, _finite_scalar, _positive_size
from .linear import _coefficients, ar1_unconditional_variance
from .volatility import _parameters, garch11_unconditional_variance


def simulate_ar1(
    phi: float, sigma: float, n: int, mu: float = 0.0, rng=None, *, initial_value=None
) -> NDArray:
    """n Gaussian AR(1) observations with an optional finite initial value.

    sigma is innovation SD, not process SD. Supply a Generator for reproducibility.
    For |phi|<1 the default initial value follows the stationary law; otherwise
    it is mu. An explicit initial_value supports any finite phi.
    """
    phi = _finite_scalar(phi, "phi")
    _positive_size(n)
    mu = _finite_scalar(mu, "mu")
    sigma = _finite_scalar(sigma, "sigma")
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    rng = np.random.default_rng(rng)
    previous = (_finite_scalar(initial_value, "initial_value") if initial_value is not None else
                rng.normal(mu, np.sqrt(ar1_unconditional_variance(phi, sigma**2)))
                if abs(phi)<1 else mu)
    innovations = rng.normal(0, sigma, size=n)
    values = np.empty(n)
    for t in range(n):
        previous = mu + phi * (previous - mu) + innovations[t]
        values[t] = previous
    return values


def simulate_ma(
    theta: ArrayLike, sigma: float, n: int, mu: float = 0.0, rng=None
) -> NDArray:
    """n observations of mu+epsilon_t+sum theta_j*epsilon_(t-j).

    Draw pre-sample Gaussian innovations too, making every returned observation
    follow the stationary finite-MA law. Non-invertible MA processes are valid.
    """
    theta = _coefficients(theta)
    _positive_size(n)
    sigma, mu = _finite_scalar(sigma, "sigma"), _finite_scalar(mu, "mu")
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    rng = np.random.default_rng(rng)
    innovations = rng.normal(0, sigma, size=n + len(theta))
    return mu + np.convolve(innovations, np.r_[1.0, theta], mode="valid")


def simulate_random_walk(
    n: int, sigma: float = 1.0, initial: float = 0.0, rng=None
) -> NDArray:
    """Return (Y_0,...,Y_n), so n increments yield n+1 observations.

    Y_0 is the fixed initial value. differencing returns exactly the n generated
    innovations. Variance at index t is t*sigma**2.
    """
    _positive_size(n)
    sigma, initial = _finite_scalar(sigma, "sigma"), _finite_scalar(initial, "initial")
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    innovations = np.random.default_rng(rng).normal(0, sigma, size=n)
    return np.r_[initial, initial + np.cumsum(innovations)]


def simulate_garch11(
    omega: float,
    alpha: float,
    beta: float,
    n: int,
    rng=None,
    *,
    df: float | None = None,
    initial_variance: float | None = None,
    burn_in: int = 1000,
) -> tuple[NDArray, NDArray]:
    """GARCH(1,1) with optional finite initialization and burn-in.

    Innovations are Gaussian by default. Optional df>2 selects Student-t
    innovations scaled by sqrt((df-2)/df) to have unit variance.

    Below unit persistence the default initial variance is the population variance;
    otherwise it is omega. Burn-in does not guarantee stationary initialization.
    Use burn_in=0 to retain the entire explicitly initialized finite path.
    """
    omega, alpha, beta = _parameters(omega, alpha, beta)
    _positive_size(n)
    rng = np.random.default_rng(rng)
    _integer(burn_in, "burn_in")
    total = n + burn_in
    if df is None:
        innovations = rng.normal(size=total)
    else:
        df = _finite_scalar(df, "df")
        if df <= 2:
            raise ValueError("df must exceed 2 for unit-variance Student-t innovations")
        innovations = rng.standard_t(df, size=total) * np.sqrt((df - 2) / df)
    h = np.empty(total)
    a = np.empty(total)
    h[0] = (_finite_scalar(initial_variance, "initial_variance") if initial_variance is not None
            else garch11_unconditional_variance(omega, alpha, beta) if alpha+beta<1 else omega)
    if h[0] <= 0:
        raise ValueError("initial_variance must be positive")
    a[0] = np.sqrt(h[0]) * innovations[0]
    for t in range(1, total):
        h[t] = omega + alpha * a[t - 1] ** 2 + beta * h[t - 1]
        a[t] = np.sqrt(h[t]) * innovations[t]
    return a[burn_in:], h[burn_in:]


def simulate_arch1(
    omega: float, alpha: float, n: int, rng=None, *, initial_variance=None, burn_in=1000
) -> tuple[NDArray, NDArray]:
    """Gaussian ARCH(1) as the beta=0 variance recursion; see simulate_garch11."""
    return simulate_garch11(omega, alpha, 0.0, n, rng,
                            initial_variance=initial_variance, burn_in=burn_in)


def simulate_ar1_garch11(
    phi: float,
    omega: float,
    alpha: float,
    beta: float,
    n: int,
    mu: float = 0.0,
    rng=None,
    *,
    df: float | None = None,
    initial_value: float | None = None,
    initial_variance: float | None = None,
    burn_in: int = 1000,
) -> tuple[NDArray, NDArray, NDArray]:
    """Return aligned (observations, innovations, conditional variances).

    X_t = mu + phi*(X_(t-1)-mu) + a_t, with Gaussian (default) or unit-variance Student-t (df>2) standardized
    GARCH(1,1) shocks. mu is the equilibrium location, not the recursion
    intercept. Unit/above-unit persistence and nonstationary AR coefficients
    are permitted with finite initial states. Output variance belongs to a_t conditional on the past,
    rather than to the unconditional X_t distribution.

    By default discard 1,000 variance steps and 1,000 mean steps. Set
    burn_in=0 for a path starting at the supplied initial states.
    """
    phi = _finite_scalar(phi, "phi")
    _positive_size(n)
    mu = _finite_scalar(mu, "mu")
    _integer(burn_in, "burn_in")
    burn = burn_in
    shocks, variances = simulate_garch11(omega, alpha, beta, n + burn, rng=rng, df=df,
                                           initial_variance=initial_variance, burn_in=burn_in)
    observations = np.empty(n + burn)
    previous = mu if initial_value is None else _finite_scalar(initial_value, "initial_value")
    for t, shock in enumerate(shocks):
        previous = mu + phi * (previous - mu) + shock
        observations[t] = previous
    return observations[burn:], shocks[burn:], variances[burn:]
