# Parameter restriction removal

Removed on 2026-10-13 from the active library and notebook estimators:

- The joint GARCH softmax persistence ceiling and its numerical multiplier.
- AR stationarity and MA invertibility transformations and filtering checks.
- Numerical boxes on joint-fit AR/MA coordinates, omega, alpha/beta and Student-t degrees of freedom; warm-start clipping.
- Multivariate Student-t degrees-of-freedom bounds and Cholesky scale boxes.
- Multivariate skew-normal shape and Cholesky scale boxes.
- Fixed lognormal shift in fitting; the shift is now estimated.
- Stationarity/invertibility defaults in notebook ARIMA fits. The automatic cross-check now uses a direct exhaustive ARMA grid, removing auto_arima’s additional near-unit-root rejection.
- Persistence, parameter caps and residual-based variance clipping inherited from arch in notebook ARCH/GARCH/constant-variance fits, through `finstats.arch_models.arch_model`.
- The bounded degrees-of-freedom search for notebook 11’s diagnostic Student-t reference.
- Stationarity restrictions on finite-horizon AR forecasts and finite simulations. Simulators accept explicit initial states for nonstationary specifications.

Retained mathematical domains: finite input values, positive scales and variances, positive definite density matrices, nonnegative ARCH/GARCH variance coefficients, positive Student-t df, df>2 for unit-variance innovations, and df>1 for finite Student-t ES. Stationary population variance/ACF functions still require the conditions under which their formulas exist; these do not restrict estimation.

Historical archives are preserved. Active notebook outputs and notebook 11’s rolling cache are regenerated with the revised estimators.

The subsequent [simplification constraint review](statistical_simplification_review.md#arch-constraint-review) documents numerical consequences against standard arch; it retains these constraints unchanged.
