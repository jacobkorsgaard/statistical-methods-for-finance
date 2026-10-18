# Statistical implementation simplification

The notebooks remain the educational reference. This refactor preserves all 14 notebooks present in the working tree (00–11 plus the existing new 12–13), their cell order, markdown, equations, figures, tables, metadata and saved outputs. Existing user changes to README, the API guide and Notebook 02 were preserved. Financial data, estimation assumptions and empirical methods are unchanged.

## Implementation decisions

The [function usage audit](function_usage_audit.md) inventories every function and class method in the original `src/finstats`, with references across notebooks, source and tests. It includes private helpers; name matches are deliberately reported as references rather than claimed as executed calls.

| Module | Decision |
| --- | --- |
| `linear.py` | Removed `ar1_unconditional_variance`, `ar1_acf`, `ar_roots`, `is_stationary_ar`, `ar1_forecast`, `ma_roots`, `is_invertible_ma`, `arma_roots` and their private validators. Notebook 08 calls `np.polynomial.polynomial.polyroots` and statsmodels `ArmaProcess.isstationary` / `.isinvertible`. Notebook 10 evaluates the AR(1) forecast formula directly. Population moments already appear in the mathematical exposition. |
| `volatility.py` | Removed `arch1_unconditional_variance`, `garch11_unconditional_variance`, `garch11_variance_path`, `garch11_forecast` and its private validator. Notebook 09 now displays the GARCH forecast recursion and retains its comparison with arch. Notebook 10 uses arch's fitted forecast API, avoiding duplication. The unused variance-path wrapper needs no replacement; the simulator and joint filter retain their useful aligned recursions. |
| `empirical.py` | ECDF evaluation now uses statsmodels `ECDF(side="right")`, retaining input validation and scalar/array behavior. Inverse-ECDF quantiles already used `np.quantile(method="inverted_cdf")` and remain unchanged. QQ data retains explicit `(i−.5)/n` positions and distribution `ppf`; SciPy `probplot` uses different positions. A trial with `mstats.plotting_positions` exposed tie-order changes and was rejected. |
| `diagnostics.py` | Autocovariance delegates to statsmodels `acovf(demean=True, fft=False, adjusted=..., nlag=...)`; single-lag autocorrelation delegates through the existing statsmodels ACF adapter. Both denominator n−lag and n remain supported, centering uses the full sample mean, and constants remain rejected for correlation diagnostics. Existing `acf`, `acorr_ljungbox`, McLeod–Li summary and residual-standardization contracts remain useful and are retained. |
| `simulation.py` | Retained all six reproducible simulators. Moved only the required coefficient/variance parameter checks here, evaluated initialization variances locally, and removed dependencies on the deleted modules. Random streams, initialization and indexing are unchanged. |
| `fitting.py`, `multivariate.py`, `multivariate_fit.py` | Retained unchanged: fit summaries, nonstandard multivariate models and reusable estimators. |
| `joint.py`, `rolling.py`, `_validation.py` | Retained unchanged: joint estimation/filtering/forecasting, validated expanding-window checkpoints and shared input contracts. |
| `risk.py` | Retained unchanged: loss-tail conventions and analytical finance-specific VaR/ES calculations. |
| `arch_models.py` | Retained unchanged after the constraint review below. |

Dependencies and version requirements are unchanged. No compatibility shims or new statistical abstractions were added. Removed tests of deleted formula APIs; preserved simulation/diagnostic tests and moved MA coefficient validation coverage to simulation. Added tests for full-sample centering, both denominators and endpoint lags, tied QQ positions, and the numerical consequence of arch variance clipping. The full suite changed from 264 to 259 passing cases, with the same existing SciPy lognormal warning.

## arch constraint review

These overrides are **not necessary for ordinary stationary ARCH/GARCH estimation**. They are necessary to preserve the repository's current unrestricted estimation domain and unmodified finite-path variance recursion. Replacing the adapter with standard arch would alter assumptions and may change likelihoods, estimates, forecasts and cached empirical results. No constraint was changed in this refactor.

The installed arch 8.0.0 implementation was inspected directly. Its symmetric GARCH constraints impose nonnegative coefficients and persistence ≤1; coefficient bounds additionally cap individual alpha/beta at 1, and omega lies between `1e-8*mean(resids**2)` and `10*mean(resids**2)`. Standard Student-t estimation uses df in [2.05,500]. Constant variance has residual-dependent lower/upper bounds. The custom adapter removes those caps, permits unit-variance t df immediately above 2, and disables residual-dependent variance clipping.

[Recorded numerical comparison](arch_constraint_comparison.json), using `np.random.default_rng(83).normal(size=150)` with zero mean and no rescaling:

- At `(omega,alpha,beta)=(.1,.25,.9)`, persistence is 1.15. The standard estimation constraint margin is −0.15; the adapter permits the parameters. Fixed-parameter log likelihood is −249.3839404550383 for both when clipping does not bind. `fix()` bypasses estimation constraints, so this equality does not mean the standard estimator would accept the point.
- At `(.1,2,1.5)`, standard variance clipping limits the largest conditional variance to about 1.82e6, while the explicit recursion reaches 1.14e27. Corresponding fixed log likelihoods are −1083.1129091113216 and −2544.1890580650916. This deliberately explosive finite path isolates the numerical effect of clipping; it is not a proposed empirical model.
- Even a Gaussian fit whose optimum is inside the standard domain follows a slightly different optimizer path: log likelihood −211.86643363670265 with standard arch versus −211.86643367062908 with the adapter. This illustrative comparison does not establish the difference for every empirical fit.

Retaining the overrides also retains their numerical costs: removing bounds and clipping makes overflow and poorly conditioned fits possible; df close to 2 approaches the boundary of unit-variance t standardization. Persistence ≥1 has no finite unconditional variance under the usual unit-variance innovation assumptions, even though finite initialized paths can be computed. GARCH's current omega bound includes zero and can admit degenerate boundary points. These are existing estimation decisions, not changes made here. A future return to standard constraints requires a separate empirical re-estimation and validation decision.

## Historical expected shortfall

Historical ES still averages losses **strictly greater** than the inverse-ECDF VaR. It can exclude tied boundary losses, average a fraction different from alpha of the sample, and fail when no strict exceedance exists. It differs from integrated empirical-quantile ES with fractional boundary mass. Deciding whether to adopt that alternative remains separate; tests continue to protect the current estimator.

## Validation

The [validation record](statistical_simplification_validation.json) reports:

- All 14 notebooks execute in fresh Jupyter kernels; executed copies were written under `/tmp`, never over repository outputs. Notebooks 05 and 11 were rerun after rejecting the tie-sensitive QQ substitution.
- 5,589 numeric scalar/array/table/dictionary entries captured after code cells match executions of the pre-refactor working tree at `rtol=1e-10`, `atol=1e-12`. Repeated names are checked after each cell, so this count is not directly comparable with the historical record's 595 objects.
- Notebook 10 has machine-roundoff differences only: maximum absolute changes 3.33e−16 in innovation variance and 8.88e−16 in return forecast-error variance. arch uses a different floating-point operation order from the former explicit recursion. All other captured numerical entries are bitwise equal. A separate ECDF probe at every order statistic for n=3,7,17,100,1000 found differences up to 1.11e−16: statsmodels constructs probability levels with `linspace`, whereas the previous implementation divided integer counts by n. The right-continuous definition is unchanged. No displayed table or reported result changed.
- Displayed text and tables match the saved notebook outputs after whitespace normalization and exclusion of stderr warnings. Raw stream differences consist of blank-line grouping and statsmodels ADF future-warning presence/kernel paths. Figures and all other saved outputs are structurally identical to the pre-refactor working tree.
- Data files and all Notebook 11 artifacts are byte-identical. Its existing validated 752-row rolling cache was reused; the unchanged estimators and cache signature inputs did not require regenerating those fits.
- The historical `restructuring_validation.json` records the earlier twelve-notebook validation with the same tolerances, but contains no individual numerical baselines and predates the constraint changes recorded in `parameter_constraint_audit.md`. It remains untouched. Current saved outputs and a fresh pre-refactor execution provide the numerical baseline for this change.

`PYTHON_API.md`, README and test documentation describe the resulting interfaces. No commit or publication was performed.
