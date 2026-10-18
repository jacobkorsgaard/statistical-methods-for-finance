# Tests

Run `python -m pytest` from the repository root. Tests are offline and use fixed seeds.

| Files | Coverage |
| --- | --- |
| `test_multivariate_fit.py`, `test_multivariate_skew_normal.py` | Custom MLEs, density/moment agreement, optimizer diagnostics and invalid samples |
| `test_multivariate_laplace.py` | Mixture density, radial mass, second moments, marginals, Jacobian and center singularity |
| `test_timeseries_joint.py` | Joint likelihoods, causal filtering, forecasts, lag orders, parameter constraints and inference |
| `test_timeseries_rolling.py` | Refitting without look-ahead, warm starts, checkpoints and cache invalidation |
| `test_timeseries.py`, `test_volatility.py`, `test_timeseries_composite.py` | Aligned simulations, seed reproducibility, population moments, input contracts and diagnostics |
| `test_nonparametric_risk.py`, `test_empirical.py`, `test_risk.py` | ECDF/QQ positions, inverse-ECDF quantiles, analytical risk, integrated empirical ES, fractional boundary mass and ties |
| `test_descriptive.py`, `test_distributions.py`, `test_multivariate.py`, `test_inference.py`, `test_returns.py` | Mathematical identities and notebook calculations now expressed through NumPy/SciPy; finite-sample interval coverage |
| `test_univariate_distributions.py`, `test_fitting.py` | SciPy distribution conventions and the shared fit-summary interface |
| `test_data_snapshots.py` | Snapshot checksums, schemas, periods, calendars and units |
| `test_api_guide.py` | Executes the Python guide examples in their documented order |

The restructuring retains tests for unique implementations and statistical conventions. Tests of deleted elementary wrappers' validation and plotting adapters are not retained as compatibility promises. Shared current input contracts remain covered through custom estimators, empirical methods, risk, diagnostics and simulations.

All twelve notebooks were also executed against saved pre-restructuring numerical baselines, checking the captured numerical arrays, scalars and tables at relative tolerance `1e-10`, absolute tolerance `1e-12`. Markdown explanations, cell order, section hierarchy, data and saved figures are preserved. Notebook 11's source-signature change triggered a genuine recalculation of its 752 expanding-window forecasts; the forecast CSV remained numerically unchanged.

The statistical simplification additionally checks full-sample autocovariance centering at both endpoint lags and both denominators, and distinct QQ positions for tied observations. Obsolete tests for removed elementary formula APIs were deleted; MA coefficient validation remains covered through simulation. No dependencies were added or removed. See the [current validation](../artifacts/statistical_simplification_validation.json) and [review](../artifacts/statistical_simplification_review.md); the twelve-notebook restructuring record above is historical.

The subsequent [expected-shortfall update](../artifacts/expected_shortfall_update.md) validates the integrated empirical quantile estimator against numerical integration, including ties, fractional and sub-observation tails, constant samples, negative losses, replication invariance and changes of units. Its affected notebook outputs supersede the earlier strict-exceedance ES results.
