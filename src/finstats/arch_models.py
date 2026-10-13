"""arch estimators with density domains only and unrestricted persistence."""

import numpy as np
from arch import arch_model as _arch_model
from arch.univariate import ConstantVariance, GARCH, StudentsT


class GARCHWithoutPersistenceLimit(GARCH):
    """Symmetric ARCH/GARCH without a persistence ceiling or parameter caps."""

    def constraints(self):
        # Nonnegative coefficients preserve variance positivity for all histories.
        count = 1 + self.p + self.q
        return np.eye(count), np.zeros(count)

    def bounds(self, resids):
        return [(0.0, np.inf)] * (1 + self.p + self.q)

    def variance_bounds(self, resids, power=2.0):
        # Do not clip the actual conditional recursion to residual-based boxes.
        return np.tile([0.0, np.inf], (len(resids), 1))


class StudentTWithoutParameterCaps(StudentsT):
    """Unit-variance Student-t: nu>2, with no offset or upper cap."""

    def constraints(self):
        return np.ones((1, 1)), np.array([np.nextafter(2.0, np.inf)])

    def bounds(self, resids):
        return [(np.nextafter(2.0, np.inf), np.inf)]


class ConstantVarianceWithoutParameterCaps(ConstantVariance):
    """Positive constant variance without data-dependent numerical boxes."""

    def constraints(self):
        return np.ones((1, 1)), np.array([np.nextafter(0.0, np.inf)])

    def bounds(self, resids):
        return [(np.nextafter(0.0, np.inf), np.inf)]


def arch_model(*args, **kwargs):
    """Construct the course's symmetric ARCH/GARCH/constant-variance models.

    Uses arch's likelihood, estimation and forecasts with only variance and
    density domains. Supports Gaussian or unit-variance Student-t innovations.
    """
    model = _arch_model(*args, **kwargs)
    volatility = model.volatility
    if isinstance(volatility, GARCH):
        if volatility.o or volatility.power != 2:
            raise ValueError("this helper supports symmetric power-two ARCH/GARCH")
        model.volatility = GARCHWithoutPersistenceLimit(p=volatility.p, q=volatility.q)
    elif isinstance(volatility, ConstantVariance):
        model.volatility = ConstantVarianceWithoutParameterCaps()
    else:
        raise ValueError("this helper supports ARCH, GARCH or constant variance")
    if isinstance(model.distribution, StudentsT):
        model.distribution = StudentTWithoutParameterCaps()
    elif model.distribution.name != "Normal":
        raise ValueError("this helper supports normal or Student-t innovations")
    return model
