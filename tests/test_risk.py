"""Empirical ES integrates the inverse ECDF, including boundary mass."""

import numpy as np
import pytest
from scipy.integrate import quad
from finstats.risk import historical_var, historical_es


@pytest.mark.parametrize("losses,alpha,expected", [
    ([1, 2, 3, 4, 5], .2, 5),
    ([1, 2, 3, 4, 5], .3, (5 + .5*4)/1.5),
    ([0, 1, 2, 2, 5], .5, (5 + 2 + .5*2)/2.5),
    ([1, 1, 1], .05, 1),
    ([7], .05, 7),
    ([0, 1, 2, 3, 4], .01, 4),
    ([-5, -3, -1], .5, (-1 - .5*3)/1.5),
    ([1e-100, 2e-100], np.nextafter(0., 1.), 2e-100),
])
def test_empirical_es_tail_mass(losses, alpha, expected):
    assert historical_es(losses, alpha) == pytest.approx(expected, rel=1e-14, abs=0)
    assert historical_es(losses, alpha) >= historical_var(losses, alpha)


@pytest.mark.parametrize("alpha", [.01, .2, .3, .5, .93, np.nextafter(1., 0.)])
def test_es_matches_integrated_numpy_inverse_ecdf(alpha):
    losses = np.array([4., -2., 1., 4., 7., 0., 4.])
    lower = 1-alpha
    points = np.arange(1, len(losses))/len(losses)
    integral = quad(lambda u: np.quantile(losses, u, method="inverted_cdf"),
                    lower, 1, points=points[points > lower], epsabs=1e-12)[0]
    expected = integral/alpha
    assert historical_es(losses, alpha) == pytest.approx(expected)
    assert historical_es(losses[::-1], alpha) == pytest.approx(expected)
    assert historical_es(np.tile(losses, 3), alpha) == pytest.approx(expected)
    assert historical_es(3*losses+2, alpha) == pytest.approx(3*expected+2)
