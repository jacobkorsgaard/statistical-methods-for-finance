import numpy as np
import pytest
from scipy import stats

from finstats.arch_models import arch_model


def test_arch_likelihood_and_forecasts_allow_above_unit_persistence():
    values = np.random.default_rng(83).normal(size=150)
    model = arch_model(values, mean="Zero", vol="GARCH", p=1, q=1, rescale=False)
    params = np.array([.1, .25, .9])
    a, b = model.volatility.constraints()
    assert np.all(a @ params >= b)
    fit = model.fix(params)
    variance = np.asarray(fit.conditional_volatility)**2
    np.testing.assert_allclose(variance[1:], .1+.25*values[:-1]**2+.9*variance[:-1])
    assert fit.loglikelihood == pytest.approx(stats.norm.logpdf(values, scale=np.sqrt(variance)).sum())
    forecasts = fit.forecast(horizon=3).residual_variance.iloc[-1].to_numpy()
    np.testing.assert_allclose(forecasts[1:], .1+1.15*forecasts[:-1])


@pytest.mark.parametrize("df", [2.0001, 600.])
def test_arch_student_t_has_only_unit_variance_density_domain(df):
    values = np.random.default_rng(84).normal(size=100)
    model = arch_model(values, mean="Zero", dist="t", rescale=False)
    a, b = model.distribution.constraints()
    assert np.all(a @ np.array([df]) >= b)
    lo, hi = model.distribution.bounds(values)[0]
    assert lo < df < hi
    assert np.isfinite(model.distribution.loglikelihood(
        [df], values, np.ones(len(values))))


def test_variance_clipping_override_changes_explosive_finite_likelihood():
    from arch import arch_model as standard_arch_model

    values = np.random.default_rng(83).normal(size=150)
    options = dict(mean="Zero", p=1, q=1, rescale=False)
    standard = standard_arch_model(values, **options)
    custom = arch_model(values, **options)
    parameters = np.array([.1, 2., 1.5])
    a, b = standard.volatility.constraints()
    assert np.any(a @ parameters < b)
    # fix() bypasses estimation constraints, isolating the recursion clipping.
    clipped = standard.fix(parameters)
    unclipped = custom.fix(parameters)
    variance = np.asarray(unclipped.conditional_volatility)**2
    np.testing.assert_allclose(variance[1:], .1+2*values[:-1]**2+1.5*variance[:-1])
    assert variance[-1] > 1e20
    assert np.max(clipped.conditional_volatility**2) < 1e8
    assert unclipped.loglikelihood == pytest.approx(
        stats.norm.logpdf(values, scale=np.sqrt(variance)).sum())
    assert abs(unclipped.loglikelihood-clipped.loglikelihood) > 100
