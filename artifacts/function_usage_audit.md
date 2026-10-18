# Function usage before simplification

Names are mapped to source, notebook and test references before editing. Private methods are included; name matches can include unrelated local names.

## __init__.py

| Definition | Referenced in |
| --- | --- |

## _validation.py

| Definition | Referenced in |
| --- | --- |
| `_sample` | `src/finstats/simulation.py`, `src/finstats/diagnostics.py`, `src/finstats/fitting.py`, `src/finstats/risk.py`, `src/finstats/empirical.py`, `src/finstats/volatility.py` |
| `_integer` | `src/finstats/simulation.py`, `src/finstats/diagnostics.py`, `src/finstats/linear.py` |
| `_finite_scalar` | `src/finstats/simulation.py`, `src/finstats/linear.py`, `src/finstats/risk.py`, `src/finstats/joint.py`, `src/finstats/volatility.py` |
| `_positive_size` | `src/finstats/simulation.py`, `src/finstats/linear.py`, `src/finstats/volatility.py` |

## arch_models.py

| Definition | Referenced in |
| --- | --- |
| `arch_model` | `tests/test_arch_models.py`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/11_case_study_financial_time_series.ipynb`, `notebooks/09_conditional_volatility_models.ipynb` |
| `constraints` | `tests/test_arch_models.py` |
| `bounds` | `tests/test_arch_models.py`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/09_conditional_volatility_models.ipynb`, `notebooks/08_linear_time_series_models.ipynb` |
| `variance_bounds` | Internal only / no external caller |
| `constraints` | `tests/test_arch_models.py` |
| `bounds` | `tests/test_arch_models.py`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/09_conditional_volatility_models.ipynb`, `notebooks/08_linear_time_series_models.ipynb` |
| `constraints` | `tests/test_arch_models.py` |
| `bounds` | `tests/test_arch_models.py`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/09_conditional_volatility_models.ipynb`, `notebooks/08_linear_time_series_models.ipynb` |

## diagnostics.py

| Definition | Referenced in |
| --- | --- |
| `sample_autocovariance` | `tests/test_timeseries.py`, `notebooks/06_stochastic_processes.ipynb` |
| `sample_autocorrelation` | `tests/test_timeseries.py`, `notebooks/06_stochastic_processes.ipynb` |
| `acf` | `tests/test_timeseries.py`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/11_case_study_financial_time_series.ipynb`, `notebooks/09_conditional_volatility_models.ipynb`, `notebooks/08_linear_time_series_models.ipynb` |
| `ljung_box` | `tests/test_timeseries.py`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/11_case_study_financial_time_series.ipynb`, `notebooks/09_conditional_volatility_models.ipynb`, `notebooks/08_linear_time_series_models.ipynb` |
| `mcleod_li` | `tests/test_volatility.py`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/11_case_study_financial_time_series.ipynb`, `notebooks/09_conditional_volatility_models.ipynb` |
| `standardized_residuals` | `tests/test_volatility.py`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/09_conditional_volatility_models.ipynb` |

## empirical.py

| Definition | Referenced in |
| --- | --- |
| `empirical_cdf` | `tests/test_empirical.py`, `tests/test_nonparametric_risk.py`, `notebooks/04_nonparametric_methods.ipynb`, `notebooks/05_case_study_financial_distribution.ipynb` |
| `empirical_quantile` | `src/finstats/risk.py`, `tests/test_empirical.py`, `tests/test_nonparametric_risk.py`, `notebooks/04_nonparametric_methods.ipynb`, `notebooks/05_case_study_financial_distribution.ipynb` |
| `qq_data` | `tests/test_nonparametric_risk.py`, `notebooks/04_nonparametric_methods.ipynb`, `notebooks/11_case_study_financial_time_series.ipynb`, `notebooks/05_case_study_financial_distribution.ipynb` |
| `evaluate` | `notebooks/09_conditional_volatility_models.ipynb` |

## fitting.py

| Definition | Referenced in |
| --- | --- |
| `fit_distribution` | `tests/test_fitting.py`, `tests/test_univariate_distributions.py`, `notebooks/11_case_study_financial_time_series.ipynb`, `notebooks/05_case_study_financial_distribution.ipynb` |

## joint.py

| Definition | Referenced in |
| --- | --- |
| `_series` | `src/finstats/rolling.py` |
| `filter_arma_garch` | `tests/test_timeseries_joint.py` |
| `_filter` | Internal only / no external caller |
| `_wald_inference` | `tests/test_timeseries_joint.py` |
| `fit_arma_garch` | `src/finstats/rolling.py`, `tests/test_timeseries_rolling.py`, `tests/test_timeseries_joint.py`, `notebooks/11_case_study_financial_time_series.ipynb` |
| `params` | `src/finstats/rolling.py`, `src/finstats/fitting.py`, `tests/test_timeseries_joint.py`, `tests/test_arch_models.py`, `tests/test_fitting.py`, `tests/test_univariate_distributions.py`, `notebooks/12_multivariate_time_series_var.ipynb`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/11_case_study_financial_time_series.ipynb`, `notebooks/09_conditional_volatility_models.ipynb`, `notebooks/08_linear_time_series_models.ipynb`, `notebooks/05_case_study_financial_distribution.ipynb` |
| `nobs` | `src/finstats/diagnostics.py`, `tests/test_timeseries_rolling.py`, `tests/test_timeseries_joint.py`, `notebooks/12_multivariate_time_series_var.ipynb`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/11_case_study_financial_time_series.ipynb`, `notebooks/09_conditional_volatility_models.ipynb`, `notebooks/13_cointegration_and_error_correction.ipynb`, `notebooks/08_linear_time_series_models.ipynb` |
| `aic` | `src/finstats/fitting.py`, `tests/test_timeseries_joint.py`, `tests/test_fitting.py`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/11_case_study_financial_time_series.ipynb`, `notebooks/09_conditional_volatility_models.ipynb`, `notebooks/13_cointegration_and_error_correction.ipynb`, `notebooks/08_linear_time_series_models.ipynb`, `notebooks/05_case_study_financial_distribution.ipynb` |
| `bic` | `src/finstats/fitting.py`, `tests/test_timeseries_joint.py`, `tests/test_fitting.py`, `notebooks/12_multivariate_time_series_var.ipynb`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/11_case_study_financial_time_series.ipynb`, `notebooks/09_conditional_volatility_models.ipynb`, `notebooks/13_cointegration_and_error_correction.ipynb`, `notebooks/08_linear_time_series_models.ipynb`, `notebooks/05_case_study_financial_distribution.ipynb` |
| `volatility_order` | `src/finstats/rolling.py`, `tests/test_timeseries_joint.py`, `notebooks/11_case_study_financial_time_series.ipynb` |
| `filter` | `src/finstats/rolling.py`, `tests/test_timeseries_joint.py`, `notebooks/11_case_study_financial_time_series.ipynb` |
| `forecast` | `tests/test_timeseries_rolling.py`, `tests/test_timeseries_joint.py`, `tests/test_arch_models.py`, `notebooks/12_multivariate_time_series_var.ipynb`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/09_conditional_volatility_models.ipynb`, `notebooks/13_cointegration_and_error_correction.ipynb`, `notebooks/08_linear_time_series_models.ipynb` |
| `decode` | Internal only / no external caller |
| `objective` | `src/finstats/multivariate_fit.py`, `src/finstats/multivariate.py`, `tests/test_multivariate_fit.py` |
| `natural_loglikelihood_obs` | Internal only / no external caller |

## linear.py

| Definition | Referenced in |
| --- | --- |
| `_stationary_phi` | Internal only / no external caller |
| `ar1_unconditional_variance` | `src/finstats/simulation.py`, `tests/test_timeseries.py` |
| `ar1_acf` | `tests/test_timeseries.py` |
| `_coefficients` | `src/finstats/simulation.py` |
| `ar_roots` | `tests/test_timeseries.py`, `notebooks/08_linear_time_series_models.ipynb` |
| `is_stationary_ar` | `tests/test_timeseries.py`, `notebooks/08_linear_time_series_models.ipynb` |
| `ar1_forecast` | `tests/test_timeseries.py`, `notebooks/10_joint_mean_volatility_models.ipynb` |
| `ma_roots` | `tests/test_timeseries.py`, `notebooks/08_linear_time_series_models.ipynb` |
| `is_invertible_ma` | `tests/test_timeseries.py`, `notebooks/08_linear_time_series_models.ipynb` |
| `arma_roots` | `tests/test_timeseries.py` |

## multivariate.py

| Definition | Referenced in |
| --- | --- |
| `bivariate_symmetric_laplace_pdf` | `tests/test_multivariate_laplace.py`, `notebooks/02_multivariate_distributions.ipynb` |
| `_parameters` | `src/finstats/simulation.py`, `src/finstats/volatility.py` |
| `multivariate_skew_normal_logpdf` | `tests/test_multivariate_skew_normal.py`, `notebooks/05_case_study_financial_distribution.ipynb` |
| `multivariate_skew_normal_moments` | `tests/test_multivariate_skew_normal.py`, `notebooks/05_case_study_financial_distribution.ipynb` |
| `multivariate_skew_normal_rvs` | `tests/test_multivariate_skew_normal.py` |
| `multivariate_skew_normal_mle` | `tests/test_multivariate_skew_normal.py`, `notebooks/05_case_study_financial_distribution.ipynb` |
| `unpack` | `src/finstats/multivariate_fit.py` |
| `objective` | `src/finstats/multivariate_fit.py`, `src/finstats/joint.py`, `tests/test_multivariate_fit.py` |

## multivariate_fit.py

| Definition | Referenced in |
| --- | --- |
| `multivariate_t_mle` | `tests/test_multivariate_fit.py`, `notebooks/05_case_study_financial_distribution.ipynb` |
| `unpack` | `src/finstats/multivariate.py` |
| `objective` | `src/finstats/multivariate.py`, `src/finstats/joint.py`, `tests/test_multivariate_fit.py` |

## risk.py

| Definition | Referenced in |
| --- | --- |
| `_alpha` | Internal only / no external caller |
| `_location_scale` | Internal only / no external caller |
| `historical_var` | `tests/test_risk.py`, `tests/test_nonparametric_risk.py`, `notebooks/04_nonparametric_methods.ipynb`, `notebooks/11_case_study_financial_time_series.ipynb`, `notebooks/05_case_study_financial_distribution.ipynb` |
| `historical_es` | `tests/test_risk.py`, `tests/test_nonparametric_risk.py`, `notebooks/04_nonparametric_methods.ipynb`, `notebooks/11_case_study_financial_time_series.ipynb`, `notebooks/05_case_study_financial_distribution.ipynb` |
| `gaussian_var` | `src/finstats/rolling.py`, `tests/test_nonparametric_risk.py`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/11_case_study_financial_time_series.ipynb`, `notebooks/09_conditional_volatility_models.ipynb`, `notebooks/01_univariate_distributions.ipynb`, `notebooks/05_case_study_financial_distribution.ipynb` |
| `gaussian_es` | `src/finstats/rolling.py`, `tests/test_nonparametric_risk.py`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/11_case_study_financial_time_series.ipynb`, `notebooks/09_conditional_volatility_models.ipynb`, `notebooks/01_univariate_distributions.ipynb`, `notebooks/05_case_study_financial_distribution.ipynb` |
| `student_t_var` | `src/finstats/rolling.py`, `tests/test_nonparametric_risk.py`, `notebooks/04_nonparametric_methods.ipynb`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/11_case_study_financial_time_series.ipynb`, `notebooks/01_univariate_distributions.ipynb`, `notebooks/05_case_study_financial_distribution.ipynb` |
| `student_t_es` | `src/finstats/rolling.py`, `tests/test_nonparametric_risk.py`, `notebooks/04_nonparametric_methods.ipynb`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/11_case_study_financial_time_series.ipynb`, `notebooks/01_univariate_distributions.ipynb`, `notebooks/05_case_study_financial_distribution.ipynb` |

## rolling.py

| Definition | Referenced in |
| --- | --- |
| `_refit_signature` | Internal only / no external caller |
| `expanding_arma_garch_forecasts` | `tests/test_timeseries_rolling.py`, `notebooks/11_case_study_financial_time_series.ipynb` |
| `checkpoint` | Internal only / no external caller |

## simulation.py

| Definition | Referenced in |
| --- | --- |
| `simulate_ar1` | `tests/test_timeseries.py`, `notebooks/08_linear_time_series_models.ipynb` |
| `simulate_ma` | `tests/test_timeseries.py`, `notebooks/08_linear_time_series_models.ipynb` |
| `simulate_random_walk` | `tests/test_timeseries.py`, `notebooks/07_stationarity_and_nonstationarity.ipynb` |
| `simulate_garch11` | `tests/test_volatility.py`, `tests/test_timeseries_joint.py`, `notebooks/09_conditional_volatility_models.ipynb` |
| `simulate_arch1` | `tests/test_volatility.py`, `notebooks/09_conditional_volatility_models.ipynb` |
| `simulate_ar1_garch11` | `tests/test_timeseries_composite.py`, `notebooks/10_joint_mean_volatility_models.ipynb` |

## volatility.py

| Definition | Referenced in |
| --- | --- |
| `_parameters` | `src/finstats/simulation.py`, `src/finstats/multivariate.py` |
| `arch1_unconditional_variance` | `tests/test_volatility.py` |
| `garch11_unconditional_variance` | `src/finstats/simulation.py`, `tests/test_volatility.py` |
| `garch11_variance_path` | `tests/test_volatility.py` |
| `garch11_forecast` | `tests/test_volatility.py`, `notebooks/10_joint_mean_volatility_models.ipynb`, `notebooks/09_conditional_volatility_models.ipynb` |

