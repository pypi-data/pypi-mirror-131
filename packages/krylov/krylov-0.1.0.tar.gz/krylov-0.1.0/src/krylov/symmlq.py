"""
C.C. Paige and M.A. Saunders,
Solution of sparse indefinite systems of linear equations,
SIAM J. Numer. Anal., 12(4), 617–629,
<https://doi.org/10.1137/0712047>,
<https://web.stanford.edu/group/SOL/software/symmlq/PS75.pdf>.

Other implementations:

https://github.com/PythonOptimizers/pykrylov/blob/master/pykrylov/symmlq/symmlq.py
https://www.netlib.org/linalg/symmlq
https://petsc.org/release/src/ksp/ksp/impls/symmlq/symmlq.c.html
"""
from __future__ import annotations

from typing import Callable

import numpy as np
from numpy.typing import ArrayLike

from ._helpers import (
    Identity,
    Info,
    LinearOperator,
    clip_imag,
    get_default_inner,
    wrap_inner,
)


def symmlq(
    A: LinearOperator,
    b: ArrayLike,
    M: LinearOperator | None = None,
    inner: Callable[[np.ndarray, np.ndarray], np.ndarray] | None = None,
    x0: ArrayLike | None = None,
    tol: float = 1e-5,
    atol: float = 1.0e-15,
    maxiter: int | None = None,
    callback: Callable[[int, np.ndarray, np.ndarray], None] | None = None,
    tol_inner_real: float = 1.0e-15,
):
    b = np.asarray(b)

    assert len(A.shape) == 2
    assert A.shape[0] == A.shape[1]
    assert A.shape[1] == b.shape[0]

    n = A.shape[0]
    M = Identity(n) if M is None else M

    _inner = get_default_inner(b.shape) if inner is None else wrap_inner(inner)

    def _norm(x):
        return np.sqrt(clip_imag(_inner(x, x), tol_inner_real))

    # Need to store two previous values of ceta, c, and s.
    # c[0] is the current c, c[-1] the last, c[-2] the second last.
    ceta = [None, None, 0.0]
    c = [1.0, None, 1.0]
    s = [0.0, None, 0.0]

    u_old = np.zeros_like(b)
    v_old = np.zeros_like(b)

    if x0 is None:
        x = np.zeros_like(b)
        r = b.copy()
    else:
        x = np.copy(x0)
        r = b - A @ x0

    if callback is not None:
        callback(0, x, r)

    resnorms = [_norm(r)]

    Mr = (M @ r).copy()

    rMr = _inner(r, Mr)
    dp = np.sqrt(rMr)

    beta = dp
    beta1 = beta
    s_prod = np.abs(beta1)

    v = r / beta
    u = Mr / beta
    w_bar = u.copy()
    # np_ = _norm(Mr)

    xout = None

    def _get_xout(x, ceta, c):
        # move to the CG point: xc_{k+1}
        ceta_bar = ceta[0] / np.where(c[0] != 0.0, c[0], 1.0e-15)
        return x + ceta_bar * w_bar

    k = 0
    success = False
    criterion = np.maximum(tol * resnorms[0], atol)
    while True:
        if np.all(resnorms[-1] <= criterion):
            xout = _get_xout(x, ceta, c)
            resnorms[-1] = _norm(b - A @ xout)
            if np.all(resnorms[-1] <= criterion):
                success = True
                break

        if k == maxiter:
            xout = _get_xout(x, ceta, c)
            break

        if k > 0:
            v_old = v.copy()
            u_old = u.copy()

            v = r * (1.0 / beta)
            u = Mr * (1.0 / beta)
            # u = Mr / beta

            w = c[0] * w_bar + s[0] * u
            w_bar = -s[0] * w_bar + c[0] * u
            x += ceta[0] * w

            ceta[-2], ceta[-1] = ceta[-1], ceta[0]

        # Lanczos
        r = A @ u

        alpha = _inner(u, r)
        # preconditioning
        Mr = (M @ r).copy()

        r -= alpha * v + beta * v_old
        Mr -= alpha * u + beta * u_old

        beta_old = beta
        rMr = _inner(r, Mr)
        beta = np.sqrt(rMr)

        # QR factorization
        c[-2], c[-1] = c[-1], c[0]
        s[-2], s[-1] = s[-1], s[0]
        gamma_bar = c[-1] * alpha - c[-2] * s[-1] * beta_old
        gamma = np.sqrt(gamma_bar * gamma_bar + beta * beta)
        delta = s[-1] * alpha + c[-2] * c[-1] * beta_old
        epsilon = s[-2] * beta_old

        # Givens rotation [c, -s; s, c]
        c[0] = gamma_bar / gamma
        s[0] = beta / gamma

        if k == 0:
            ceta[0] = beta1 / gamma
        else:
            ceta[0] = -(delta * ceta[-1] + epsilon * ceta[-2]) / gamma

        s_prod *= np.abs(s[0])

        if callback is not None:
            xout = _get_xout(x, ceta, c)
            callback(k + 1, xout, r)

        # TODO norm(r) == np_?
        # np_ = s_prod / np.where(c != 0.0, np.abs(c), 1.0e-15)
        resnorms.append(_norm(r))

        k += 1

    return xout if success else None, Info(success, xout, k, np.array(resnorms))
