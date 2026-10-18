"""Upper-tail loss measures; alpha is tail probability, not confidence level.

Losses are L=-R. Historical ES integrates the inverse empirical CDF over the
upper alpha tail, including fractional probability mass at its boundary.
"""
from __future__ import annotations
import numpy as np
from numpy.typing import ArrayLike
from scipy import stats
from ._validation import _sample
from ._validation import _finite_scalar
from .empirical import empirical_quantile


def _alpha(alpha: float) -> float:
    alpha = _finite_scalar(alpha, "alpha")
    if not 0 < alpha < 1:
        raise ValueError("alpha must lie strictly between zero and one")
    return alpha


def _location_scale(location: float, scale: float) -> tuple[float, float]:
    location = _finite_scalar(location, "location")
    scale = _finite_scalar(scale, "scale")
    if scale <= 0:
        raise ValueError("scale must be strictly positive")
    return location, scale


def historical_var(losses: ArrayLike, alpha: float = .05) -> float:
    """Return the (1-alpha) generalized-inverse ECDF loss quantile."""
    return empirical_quantile(losses, 1-_alpha(alpha))


def historical_es(losses: ArrayLike, alpha: float = .05) -> float:
    """Return alpha**-1 times the empirical quantile integral from 1-alpha to 1.

    For descending losses, average the largest floor(n*alpha) observations and
    the fractional remainder of the next. Tied boundary losses contribute only
    the mass required to fill the tail. If n*alpha<1, ES is the maximum loss.
    """
    ordered = np.sort(_sample(losses))[::-1]
    tail_mass = ordered.size * _alpha(alpha)
    whole = int(np.floor(tail_mass))
    estimate = float(np.mean(ordered[:whole])) * (whole / tail_mass) if whole else 0.0
    if whole < ordered.size:
        estimate += float(ordered[whole]) * ((tail_mass - whole) / tail_mass)
    return estimate


def gaussian_var(mu: float, sigma: float, alpha: float = .05) -> float:
    """Gaussian LOSS quantile mu+sigma*Phi^{-1}(1-alpha)."""
    mu, sigma = _location_scale(mu, sigma)
    return float(mu+sigma*stats.norm.isf(_alpha(alpha)))


def gaussian_es(mu: float, sigma: float, alpha: float = .05) -> float:
    """Gaussian mean loss conditional on exceeding its VaR."""
    mu, sigma = _location_scale(mu, sigma)
    alpha = _alpha(alpha)
    return float(mu+sigma*stats.norm.pdf(stats.norm.isf(alpha))/alpha)


def student_t_var(location: float, scale: float, df: float, alpha: float = .05) -> float:
    """LOSS quantile for location+scale*T_df; scale is not standard deviation."""
    location, scale = _location_scale(location, scale)
    df = _finite_scalar(df, "df")
    if df <= 0:
        raise ValueError("df must be strictly positive")
    return float(location+scale*stats.t.isf(_alpha(alpha), df))


def student_t_es(location: float, scale: float, df: float, alpha: float = .05) -> float:
    """LOSS ES for location+scale*T_df, requiring df>1 (finite tail mean)."""
    location, scale = _location_scale(location, scale)
    df = _finite_scalar(df, "df")
    if df <= 1:
        raise ValueError("finite Student-t ES requires df > 1")
    alpha = _alpha(alpha)
    q = stats.t.isf(alpha, df)
    return float(location+scale*(df+q*q)/(df-1)*stats.t.pdf(q,df)/alpha)
