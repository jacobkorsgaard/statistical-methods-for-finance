# Empirical expected shortfall update

Historical ES now integrates the empirical quantile function over the upper alpha loss tail. It uses exactly `n*alpha` observations’ worth of probability, including fractional boundary mass and ties. Losses remain `L=-R`; alpha remains the upper-tail probability. VaR and all parametric estimators are unchanged.

Notebook 04 explains the estimator and fractional-tail example; Notebook 05 updates historical predictions, test references and ES comparison scores. Notebook 11 updates its fixed empirical baseline. Notebook 09 adds the retained arch restrictions and their statistical implications, without code or numerical changes. No cells or sections were added or removed.

## Empirical numerical changes

ES values below are in percentage points of initial exposure at alpha=5%. The same training estimates appear in the univariate and joint-marginal tables; equity training ES also supplies Notebook 11’s fixed empirical baseline.

| Sample | Old ES | Integrated ES | Change |
| --- | ---: | ---: | ---: |
| equity_train | 3.151731013 | 3.144634207 | -0.007096806 |
| equity_test | 2.129048722 | 2.117671717 | -0.011377005 |
| bond_train | 0.798132780 | 0.796035446 | -0.002097334 |
| bond_test | 0.792792499 | 0.789692007 | -0.003100492 |

The training tail mass is 75.45 observations (75 full observations plus 0.45 of the boundary); the test mass is 37.6 (37 plus 0.6). Including the next, smaller boundary loss reduces each estimate. Strict exceedance counts and ex-post means above forecast VaR remain valid descriptive diagnostics and were not redefined. The ES table labels now describe tail mass rather than strict tail counts.

The absolute differences between predictions and the common test empirical ES change as follows. Rankings remain unchanged.

| Asset | Description | Old ES difference (pp) | New ES difference (pp) |
| --- | --- | ---: | ---: |
| Equity | Empirical | 1.022682291 | 1.026962489 |
| Equity | Standalone univariate | 1.094149747 | 1.105526752 |
| Equity | Joint-model marginal | 0.783771669 | 0.795148673 |
| Bond | Empirical | 0.005340281 | 0.006343439 |
| Bond | Standalone univariate | 0.054804993 | 0.051704501 |
| Bond | Joint-model marginal | 0.012024678 | 0.008924186 |

Notebook 11’s fixed empirical severity gap (realized strict tail mean minus predicted ES) changes from −0.123230916 to −0.116134110 percentage points. Its VaR counts and fixed Student-t/rolling-model results are unchanged.

## Simulated examples

Notebook 04’s 0.5% tail illustrations change as follows:

| Student-t df | n | Old ES | Integrated ES |
| ---: | ---: | ---: | ---: |
| 2 | 250 | 40.899156576 | 37.351547678 |
| 20 | 250 | 10.509534519 | 10.485491331 |
| 2 | 2500 | 40.375312035 | 39.801276680 |

At n=250 the estimator includes one full loss and one-quarter of the next; at n=2500 it includes twelve full losses and one-half of the next. The old estimator omitted the fractional boundary and renormalized the remaining strict tail.

For the 500-replication 1% ES example, at n=250 the mean estimate changes from 3.465105722 to 3.292570615 and the replication SD from 0.952857521 to 0.824455785. At n=2500 the tail mass is exactly 25; estimates are unchanged apart from floating-point summation roundoff (mean 3.446856584, SD 0.276747444). VaR replications are identical.

## Validation and scope

All 272 tests pass, with the existing SciPy lognormal warning. Tests cover fractional tails, tied boundaries, singleton and constant samples, tails smaller than one observation, negative losses, extremely small alpha, independent numerical integration of NumPy inverse-ECDF quantiles, replication invariance and positive affine changes of units.

Notebooks 04, 05, 09 and 11 execute in fresh Jupyter kernels. Ten affected output cells were regenerated: two in 04, seven in 05 and one in 11. Seven figure outputs change only through the updated ES histogram, risk lines, annotations or ES-dependent plotting limits; the visualizations retain their design. All other displayed outputs and figures in these executions match the saved baseline. Notebook 09’s outputs remain identical.

A before/after capture compares 3,734 numeric entries after code cells; the 96 entries differing beyond rtol=1e-10, atol=1e-12 are ES values, dependent comparison tables or plot coordinates. The [detailed record](expected_shortfall_validation.json) lists those entries and maximum differences. It also records the empirical results above. Repeated names are captured after each cell; these counts do not represent independent experiments.

All other estimators, including `arch_models.py`, remain byte-identical. Data and rolling artifacts remain byte-identical. The validated 752-row rolling cache was reused; these fits were not independently regenerated. The other ten notebooks were not rerun because they do not use historical ES and were not changed. No dependency changes were needed.

The older simplification validation and strict-exceedance ES discussion are retained as historical records, superseded by this update for ES. Sparse empirical tails still carry substantial sampling uncertainty. The pre-existing rolling-cache `hold_back` signature omission and unrestricted GARCH numerical risks remain outside this targeted change.
