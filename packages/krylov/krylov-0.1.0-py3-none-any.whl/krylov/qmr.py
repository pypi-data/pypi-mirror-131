"""
Roland W. Freund, Noël M. Nachtigal,
QMR: a quasi-minimal residual method for non-Hermitian linear systems,
Numerische Mathematik volume 60, pages 315–339 (1991),
<https://doi.org/10.1007/BF01385726>.

https://www.netlib.org/templates/templates.pdf
"""
from __future__ import annotations

from typing import Callable

import numpy as np
from numpy.typing import ArrayLike

from ._helpers import (
    Identity,
    Info,
    LinearOperator,
    asrlinearoperator,
    assert_correct_shapes,
    clip_imag,
    get_default_inner,
    wrap_inner,
)


def qmr(
    A: LinearOperator,
    b: ArrayLike,
    Ml: LinearOperator | None = None,
    Mr: LinearOperator | None = None,
    x0: ArrayLike | None = None,
    inner: Callable[[np.ndarray, np.ndarray], np.ndarray] | None = None,
    tol: float = 1e-5,
    atol: float = 1.0e-15,
    maxiter: int | None = None,
    callback: Callable[[int, np.ndarray, np.ndarray], None] | None = None,
    tol_inner_real: float = 1.0e-15,
):
    def _norm(y):
        return np.sqrt(clip_imag(_inner(y, Ml @ y), tol_inner_real))

    b = np.asarray(b)

    assert_correct_shapes(A, b, x0)

    A = asrlinearoperator(A)

    n = A.shape[0]
    Ml = Identity(n) if Ml is None else asrlinearoperator(Ml)
    Mr = Identity(n) if Mr is None else asrlinearoperator(Mr)

    if x0 is None:
        x = np.zeros_like(b)
        r = b.copy()
    else:
        x = np.array(x0)
        r = b - A @ x0

    _inner = get_default_inner(b.shape) if inner is None else wrap_inner(inner)

    if callback is not None:
        callback(0, x, r)

    resnorms = [_norm(r)]

    v_ = r.copy()
    y = Ml @ v_

    rho = _norm(y)

    # arbitrary choice
    w_ = r.copy()
    z = Mr.rmatvec(w_)

    xi = _norm(z)
    gamma2 = 1.0
    eta = -1.0
    theta2 = 1.0
    epsilon = 1.0

    k = 0
    success = False
    criterion = np.maximum(tol * resnorms[0], atol)
    while True:
        if np.all(resnorms[-1] <= criterion):
            resnorms[-1] = _norm(b - A @ x)
            if np.all(resnorms[-1] <= criterion):
                success = True
                break

        if k == maxiter:
            break

        v = v_ / np.where(rho != 0.0, rho, 1.0)
        y /= np.where(rho != 0.0, rho, 1.0)

        w = w_ / np.where(xi != 0.0, xi, 1.0)
        z /= np.where(xi != 0.0, xi, 1.0)

        delta = _inner(z, y)

        y_ = Mr @ y
        z_ = Ml.rmatvec(z)

        if k == 0:
            p = y_.copy()
            q = z_.copy()
        else:
            delta_epilon = delta / np.where(epsilon != 0.0, epsilon, 1.0)
            p *= -xi * delta_epilon
            p += y_
            q *= -rho * delta_epilon
            q += z_

        p_ = A @ p
        epsilon = _inner(q, p_)
        beta = epsilon / np.where(delta != 0.0, delta, 1.0)

        v_ = p_ - beta * v

        y = Ml @ v_
        rho_old = rho
        rho = _norm(y)

        w_ = A.rmatvec(q) - beta * w

        z = Mr.rmatvec(w_)

        xi = _norm(z)
        gamma2_old = gamma2
        theta2_old = theta2

        gamma2_old_abs_beta2 = gamma2_old * np.abs(beta) ** 2

        theta2 = rho ** 2 / np.where(
            gamma2_old_abs_beta2 != 0.0, gamma2_old_abs_beta2, 1.0
        )
        gamma2 = 1 / (1 + theta2)
        beta_gamma2_old = beta * gamma2_old
        eta *= (
            -rho_old * gamma2 / np.where(beta_gamma2_old != 0.0, beta_gamma2_old, 1.0)
        )

        if k == 0:
            d = eta * p
            s = eta * p_
        else:
            d *= theta2_old * gamma2
            d += eta * p
            s *= theta2_old * gamma2
            s += eta * p_

        x += d
        r -= s

        if callback is not None:
            callback(k + 1, x, r)

        resnorms.append(_norm(r))

        k += 1

    return x if success else None, Info(success, x, k, np.array(resnorms))
