"""
Christopher C. Paige, Michael A. Saunders:
Solution of sparse indefinite systems of linear equations,
SIAM Journal on Numerical Analysis. Band 12, Nr. 4, 1975,
<https://doi.org/10.1137/0712047>.
"""
from __future__ import annotations

from typing import Callable

import numpy as np
from numpy.typing import ArrayLike
from scipy.linalg import lapack

from ._helpers import (
    Identity,
    Info,
    LinearOperator,
    assert_correct_shapes,
    clip_imag,
    get_default_inner,
    wrap_inner,
)


def minres(
    A: LinearOperator,
    b: ArrayLike,
    Ml: LinearOperator | None = None,
    Mr: LinearOperator | None = None,
    inner: Callable[[np.ndarray, np.ndarray], np.ndarray] | None = None,
    x0: ArrayLike | None = None,
    tol: float = 1e-5,
    atol: float = 1.0e-15,
    maxiter: int | None = None,
    callback: Callable[[int, np.ndarray, list[np.ndarray]], None] | None = None,
    tol_inner_real: float = 1.0e-15,
):
    b = np.asarray(b)

    assert_correct_shapes(A, b, x0)

    n = A.shape[0]
    has_Ml = Ml is not None
    Ml = Identity(n) if Ml is None else Ml
    Mr = Identity(n) if Mr is None else Mr

    _inner = get_default_inner(b.shape) if inner is None else wrap_inner(inner)

    u_old = np.zeros_like(b) if has_Ml else None
    v_old = np.zeros_like(b)
    w = np.zeros_like(b)
    w_old = np.zeros_like(b)

    if x0 is None:
        x = np.zeros_like(b)
        r = b.copy()
    else:
        x = np.copy(x0)
        r = b - A @ (Mr @ x)

    z = Ml @ r

    beta = np.sqrt(clip_imag(_inner(r, z), tol_inner_real))

    resnorm = np.copy(beta)

    resnorms = [resnorm]

    if callback is not None:
        callback(0, x, resnorms)

    eta = beta

    c = 1.0
    c_old = 1.0
    s = 0.0
    s_old = 0.0

    b1 = np.where(beta != 0.0, beta, 1.0)
    v = r / b1
    u = z / b1 if has_Ml else v

    # for the givens rotations
    lartg = lapack.get_lapack_funcs("lartg", (beta,))

    def givens(a, b):
        if isinstance(a, float):
            return lartg(a, b)

        assert len(a) == len(b)
        return np.array([lartg(aa, bb) for aa, bb in zip(a, b)]).T

    k = 0
    success = False
    criterion = np.maximum(tol * resnorms[0], atol)
    while True:
        if np.all(resnorms[-1] <= criterion):
            # oh really?
            rr = b - A @ (Mr @ x)
            zz = Ml @ rr
            resnorms[-1] = np.sqrt(clip_imag(_inner(rr, zz), tol_inner_real))

            if np.all(resnorms[-1] <= criterion):
                success = True
                break

        if k == maxiter:
            break

        # Lanczos
        # `r` is _not_ an approximation to the residual
        r = A @ (Mr @ u)
        alpha = clip_imag(_inner(r, u), tol_inner_real)
        z = Ml @ r
        r -= alpha * v
        r -= beta * v_old
        if has_Ml:
            z -= alpha * u
            z -= beta * u_old

        beta_old = beta
        beta = np.sqrt(clip_imag(_inner(r, z), tol_inner_real))

        # QR
        c_oold = c_old
        c_old = c
        s_oold = s_old
        s_old = s
        #
        rho0 = c_old * alpha - c_oold * s_old * beta_old
        rho2 = s_old * alpha + c_oold * c_old * beta_old
        rho3 = s_oold * beta_old

        # Givens
        c, s, rho1 = givens(rho0, beta)
        # rho1 = np.sqrt(rho0 ** 2 + beta ** 2)
        # c = rho0 / rho1
        # s = beta / rho1

        w_oold = w_old
        w_old = w
        w = u.copy()

        w -= rho2 * w_old
        w -= rho3 * w_oold
        w /= np.where(rho1 != 0.0, rho1, 1.0)

        x += (c * eta) * w

        resnorm = resnorms[-1] * np.abs(s)
        resnorms.append(resnorm)

        eta *= -s

        v_old = v
        b1 = np.where(beta != 0.0, beta, 1.0)
        v = r / b1
        u_old = u if has_Ml else None
        u = z / b1 if has_Ml else v

        if callback is not None:
            callback(k + 1, x, resnorms)

        k += 1

    x = Mr @ x

    return x if success else None, Info(success, x, k, np.array(resnorms))
