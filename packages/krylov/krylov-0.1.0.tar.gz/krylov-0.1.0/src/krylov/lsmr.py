"""
D.C.-L. Fong, M.A. Saunders,
LSMR: An iterative algorithm for sparse least-squares problems,
SIAM J. Sci. Comput. 33:5, 2950-2971, published electronically Oct 27, 2011,
<https://arxiv.org/abs/1006.0758>,
<https://doi.org/10.1137/10079687X>
"""
from __future__ import annotations

from typing import Callable

import numpy as np
from numpy.typing import ArrayLike
from scipy.linalg import lapack

from ._helpers import (
    Info,
    LinearOperator,
    asrlinearoperator,
    clip_imag,
    get_default_inner,
    wrap_inner,
)


def lsmr(
    A: LinearOperator,
    b: ArrayLike,
    damp: float = 0.0,
    inner: Callable[[np.ndarray, np.ndarray], np.ndarray] | None = None,
    x0: ArrayLike | None = None,
    tol: float = 1e-5,
    atol: float = 1.0e-15,
    maxiter: int | None = None,
    callback: Callable[[int, np.ndarray, list[np.ndarray], list[np.ndarray]], None]
    | None = None,
    tol_inner_real: float = 1.0e-15,
):
    def _norm(y):
        return np.sqrt(_norm2(y))

    def _norm2(y):
        return clip_imag(_inner(y, y), tol_inner_real)

    A = asrlinearoperator(A)
    b = np.asarray(b)

    assert len(A.shape) == 2
    assert A.shape[0] == b.shape[0]
    N = A.shape[0]

    assert damp >= 0.0

    _inner = get_default_inner(b.shape) if inner is None else wrap_inner(inner)

    maxiter = N if maxiter is None else maxiter

    # get initial residual
    if x0 is None:
        x_shape = (A.shape[1], *b.shape[1:])
        x = np.zeros(x_shape, dtype=b.dtype)
        u = np.copy(b)
    else:
        x = np.copy(x0)
        u = b - A @ x

    beta = _norm(u)
    u /= beta

    v = A.rmatvec(u)
    alpha = _norm(v)
    v /= alpha

    alpha_ = alpha
    zeta_ = alpha * beta

    rho = 1.0
    rho_ = 1.0
    c_ = 1.0
    s_ = 0.0
    h = v.copy()
    h_ = np.zeros_like(h)

    resnorms = [beta]
    # zeta_ changes in-place later, so do a copy here
    nresnorms = [zeta_.copy()]

    if callback is not None:
        callback(0, x, resnorms, nresnorms)

    # values for estimation of ||r||
    beta_dd = beta
    beta_d = 0.0
    rho_d = 1.0
    tau_t = 0.0
    theta_t = 0.0
    zeta = 0.0
    d = 0.0
    anorm2 = alpha ** 2
    anorm = alpha
    acond = 1.0
    max_rbar = 0.0
    min_rbar = np.inf

    lartg = lapack.get_lapack_funcs("lartg", (alpha_, beta))

    # iterate
    k = 0
    success = False
    criterion = np.maximum(tol * resnorms[0], atol)
    while True:
        if np.all(nresnorms[-1] <= criterion):
            # oh really?
            r = b - A @ x
            x_x0 = x if x0 is None else x - x0
            resnorms[-1] = np.sqrt(_norm2(r) + damp ** 2 * _norm2(x_x0))
            nresnorms[-1] = _norm(A.rmatvec(r) - damp ** 2 * x_x0)
            if np.all(nresnorms[-1] <= criterion):
                success = True
                break

        if k == maxiter:
            break

        # continue bidiagonalization
        u = A @ v - alpha * u
        beta = _norm(u)
        u /= beta

        v = A.rmatvec(u) - beta * v
        alpha = _norm(v)
        v /= alpha

        c_hat, s_hat, alpha_hat = lartg(alpha_, damp)
        # Use a plane rotation (Q_i) to turn B_i to R_i.
        rho_old = rho
        c, s, rho = lartg(alpha_hat, beta)
        theta_new = s * alpha
        alpha_ = c * alpha

        # Use a plane rotation (Qbar_i) to turn R_i^T to R_i^bar.
        rho_old_ = rho_
        zeta_old = zeta
        theta_ = s_ * rho
        rho_temp = c_ * rho
        c_, s_, rho_ = lartg(c_ * rho, theta_new)
        zeta = c_ * zeta_
        zeta_ *= -s_

        # Update h, h_hat, x.
        h_ *= -(theta_ * rho / (rho_old * rho_old_))
        h_ += h
        x += (zeta / (rho * rho_)) * h_
        h *= -(theta_new / rho)
        h += v

        # Estimate of ||r||.
        # Apply rotation Qhat_{k,2k+1}.
        beta_acute = c_hat * beta_dd
        beta_check = -s_hat * beta_dd
        # Apply rotation Q_{k,k+1}.
        beta_hat = c * beta_acute
        beta_dd = -s * beta_acute
        # Apply rotation Qtilde_{k-1}.
        # beta_d = beta_d_{k-1} here.
        theta_t_old = theta_t
        c_t, s_t, rho_t = lartg(rho_d, theta_)
        theta_t = s_t * rho_
        rho_d = c_t * rho_
        beta_d = -s_t * beta_d + c_t * beta_hat
        tau_t = (zeta_old - theta_t_old * tau_t) / rho_t
        tau_d = (zeta - theta_t * tau_t) / rho_d
        d = d + beta_check ** 2
        # approximation of sqrt(||b - A @ x|| ** 2 + damp ** 2 * ||x - x0|| ** 2)
        resnorm = np.sqrt(d + (beta_d - tau_d) ** 2 + beta_dd ** 2)
        resnorms.append(resnorm)
        #
        # approximation of ||A.H @ (b - A @ x) - damp ** 2 * (x - x0)||
        arnorm = np.abs(zeta_)
        nresnorms.append(arnorm)

        # estimate ||A||_F
        anorm2 += beta ** 2
        anorm = np.sqrt(anorm2)
        anorm2 += alpha ** 2

        # estimate cond(A)
        max_rbar = max(max_rbar, rho_old_)
        if k > 0:
            min_rbar = min(min_rbar, rho_old_)
        acond = max(max_rbar, rho_temp) / min(min_rbar, rho_temp)

        if callback is not None:
            callback(k + 1, x, resnorms, nresnorms)

        k += 1

    return x if success else None, Info(
        success=success,
        xk=x,
        numsteps=k,
        resnorms=np.array(resnorms),
        nresnorms=np.array(nresnorms),
        anorm=anorm,
        acond=acond,
    )
