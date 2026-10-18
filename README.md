# Statistical Methods for Finance

## Overview

This repository is an educational reference connecting statistical theory with financial applications in Python. It covers financial returns, probability distributions, statistical inference, nonparametric methods, stochastic processes, linear time-series models and conditional volatility. Mathematical explanations are accompanied by visualizations, reproducible simulations and empirical case studies.

The sequence begins with returns as random variables and develops tools for describing expected returns, dispersion and downside risk through Value at Risk (VaR) and Expected Shortfall (ES). It then introduces temporal ordering, conditional expectations and changing volatility. Two case studies apply these ideas to equity and bond returns and to S&P 500 exposure, comparing model estimates with out-of-sample observations. The final theory notebooks extend the sequence to multivariate dynamics, shared stochastic trends and error correction.

The notebooks emphasize assumptions, interpretation and evaluation alongside implementation. Established scientific Python libraries provide standard methods; a focused collection of custom implementations supports selected statistical calculations and reusable analyses.

## Notebooks

Read the notebooks in order for the complete progression, or consult individual topics as references.

Notebooks 12 and 13 are still under development.

| Notebook | Coverage |
| --- | --- |
| [00 — Financial Returns](notebooks/00_financial_returns.ipynb) | Return definitions, losses and probability models |
| [01 — Univariate Distributions](notebooks/01_univariate_distributions.ipynb) | Distributions, moments, quantiles and tail risk |
| [02 — Multivariate Distributions](notebooks/02_multivariate_distributions.ipynb) | Joint, marginal and conditional distributions; linear transformations |
| [03 — Statistical Inference and MLE](notebooks/03_statistical_inference_and_mle.ipynb) | Estimator properties, testing, estimation and model comparison |
| [04 — Nonparametric Methods](notebooks/04_nonparametric_methods.ipynb) | Empirical distributions, KDE, QQ plots and empirical risk |
| [05 — Financial Distribution Case Study](notebooks/05_case_study_financial_distribution.ipynb) | Distribution models for equity and bond returns |
| [06 — Stochastic Processes](notebooks/06_stochastic_processes.ipynb) | Realized time series and population/sample properties |
| [07 — Stationarity and Nonstationarity](notebooks/07_stationarity_and_nonstationarity.ipynb) | Stationarity, ergodicity, noise and stochastic trends |
| [08 — Linear Time-Series Models](notebooks/08_linear_time_series_models.ipynb) | AR, MA and ARIMA; estimation, diagnostics and forecasting |
| [09 — Conditional Volatility Models](notebooks/09_conditional_volatility_models.ipynb) | ARCH/GARCH, diagnostics and conditional risk |
| [10 — Joint Mean–Volatility Models](notebooks/10_joint_mean_volatility_models.ipynb) | Combined estimation, diagnostics and forecasting |
| [11 — Financial Time-Series Case Study](notebooks/11_case_study_financial_time_series.ipynb) | S&P 500 models and expanding-window evaluation |
| [12 — Multivariate Time-Series Models](notebooks/12_multivariate_time_series_var.ipynb) | VAR, stability, Granger predictability, impulse responses and forecasting |
| [13 — Cointegration and Error Correction](notebooks/13_cointegration_and_error_correction.ipynb) | Stochastic trends, cointegration tests, rank, VECM and level forecasts |

## Getting Started

From the repository root, use Python 3.11 or later:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

On Windows, activate with `.venv\Scripts\Activate.ps1`. Open the notebooks in your preferred Jupyter-compatible editor and select this environment as the kernel. Execute cells in order. To execute a notebook from the command line:

```bash
python -m nbconvert --to notebook --execute --inplace notebooks/00_financial_returns.ipynb
```

Empirical examples use fixed local snapshots and require no execution-time downloads; see the [data documentation](data/README.md). Notebook 11 can take longer when regenerating its rolling estimates. Run checks with `python -m pytest`; [test documentation](tests/README.md), the [numerical validation record](artifacts/restructuring_validation.json) and [tested dependency versions](requirements-tested.txt) provide verification details.

## Python Implementations

The `finstats` namespace contains focused reusable functionality, including custom multivariate estimators, joint ARMA–GARCH estimation, expanding-window forecasting, simulations and explicit empirical/risk conventions. Standard distribution, inference and time-series methods use NumPy, SciPy, statsmodels, pmdarima and arch. Elementary AR/MA and volatility formulas live in the notebooks, with direct library calls for roots, estimation and forecasts. Empirical and dependence helpers delegate standard calculations to NumPy/statsmodels while preserving the stated conventions.

Historical ES uses the integrated empirical quantile estimator, including fractional boundary mass and ties; see Notebook 04 and the [ES update and validation](artifacts/expected_shortfall_update.md).

The [simplification review](artifacts/statistical_simplification_review.md) records removed APIs, numerical validation, the retained arch constraint overrides and the historical ES convention at the time of that refactor. The [Python API guide](PYTHON_API.md) documents both custom interfaces and third-party methods, with examples, parameterizations and statistical conventions. The notebooks provide the accompanying mathematical exposition and applications.

## Possible Extensions

These directions extend the existing material:

1. **Stochastic Processes and Trading Strategies:** Model-implied signals, mean reversion and volatility timing, assessed through out-of-sample evaluation.
2. **Multivariate Financial Applications:** Empirical VAR and cointegration studies, with economically motivated variables and out-of-sample evaluation.
3. **Extensions of GARCH:** Asymmetric GARCH models and, potentially, multivariate volatility models.
4. **Bayesian Statistical Methods:** Bayesian estimation of univariate distributions, posterior predictive VaR/ES, Bayesian time-series models and state-space methods.

## References and Further Reading

- George Casella and Roger L. Berger (2002). *Statistical Inference*, second edition. Duxbury.
- David Ruppert and David S. Matteson (2015). [*Statistics and Data Analysis for Financial Engineering: with R Examples*](https://link.springer.com/book/10.1007/978-1-4939-2614-5), second edition. Springer.
- Larry Wasserman (2004). [*All of Statistics: A Concise Course in Statistical Inference*](https://link.springer.com/book/10.1007/978-0-387-21736-9), first edition. Springer.

## Acknowledgements

I am grateful to Professors Stefano Tonellato and Roberto Casarin for strengthening my statistical foundations during my time as a visiting student at Ca' Foscari University of Venice.

A repository license remains to be selected; see [LICENSE](LICENSE).
