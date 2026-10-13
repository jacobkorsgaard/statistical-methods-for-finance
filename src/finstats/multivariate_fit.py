"""Numerical location/scale Student-t fitting for multivariate observations."""

import numpy as np
from scipy import optimize, stats


def multivariate_t_mle(data, df_starts=(4.0, 10.0, 30.0)):
    """Fit a multivariate t with positive degrees of freedom.

    Rows are observations. Returns location, scale matrix (NOT covariance),
    df, log_likelihood and successful-start diagnostics. Positive definiteness
    is enforced through a Cholesky factor. Standardization improves conditioning.
    Several L-BFGS-B starts reduce, but do not eliminate, local-optimum risk.
    Raises ValueError for invalid/singular samples and RuntimeError if all starts
    fail. Log Cholesky diagonals and log degrees of freedom are unbounded;
    positive scale and df are the density domains. Covariance exists only for df>2.
    """
    if np.iscomplexobj(data):
        raise ValueError("data must be real")
    x = np.asarray(data, dtype=float)
    if x.ndim != 2 or x.shape[1] < 2 or x.shape[0] <= x.shape[1]:
        raise ValueError("need more observations than variables and at least two variables")
    if not np.isfinite(x).all():
        raise ValueError("data must be finite")
    starts = np.asarray(df_starts, dtype=float)
    if starts.ndim != 1 or not starts.size or not np.isfinite(starts).all() or np.any(starts <= 0):
        raise ValueError("df_starts must be positive and finite")
    center, sd = x.mean(axis=0), x.std(axis=0)
    if np.any(sd == 0):
        raise ValueError("sample covariance must be positive definite")
    z = (x-center)/sd
    covariance = np.cov(z, rowvar=False, ddof=0)
    try:
        np.linalg.cholesky(covariance)
    except np.linalg.LinAlgError as error:
        raise ValueError("sample covariance must be positive definite") from error
    k = x.shape[1]
    rows, cols = np.tril_indices(k)
    diagonal = rows == cols

    def unpack(p):
        factor = np.zeros((k, k))
        entries = p[k:-1].copy()
        entries[diagonal] = np.exp(entries[diagonal])
        factor[rows, cols] = entries
        return p[:k], factor @ factor.T, np.exp(p[-1])

    @np.errstate(over="ignore", invalid="ignore", divide="ignore")
    def objective(p):
        mu, scale, df = unpack(p)
        if not np.isfinite(scale).all() or not np.isfinite(df) or df <= 0:
            return 1e100
        try:
            value = -stats.multivariate_t.logpdf(z, loc=mu, shape=scale, df=df).sum()
        except (ValueError, np.linalg.LinAlgError):
            return 1e100
        return float(value) if np.isfinite(value) else 1e100

    candidates, diagnostics = [], []
    for df in starts:
        factor = np.linalg.cholesky(covariance*((df-2)/df if df>2 else 1))
        entries = factor[rows, cols].copy()
        entries[diagonal] = np.log(entries[diagonal])
        initial = np.r_[np.zeros(k), entries, np.log(df)]
        fit = optimize.minimize(objective, initial, method="L-BFGS-B",
                                options={"maxiter": 1500, "ftol": 1e-11})
        ll = -fit.fun - len(x)*np.log(sd).sum()
        diagnostics.append({"start_df": float(df), "success": bool(fit.success),
                            "log_likelihood": float(ll), "message": str(fit.message)})
        if fit.success and np.isfinite(ll) and fit.fun < 1e100:
            candidates.append((ll, fit.x))
    if not candidates:
        raise RuntimeError("all multivariate Student-t optimization starts failed")
    ll, parameters = max(candidates, key=lambda item: item[0])
    mu, scale, df = unpack(parameters)
    return {"location": center+sd*mu, "scale": scale*np.outer(sd, sd),
            "df": float(df), "log_likelihood": float(ll), "starts": diagnostics}
