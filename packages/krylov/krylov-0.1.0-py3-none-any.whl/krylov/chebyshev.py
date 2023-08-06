"""
https://www.netlib.org/templates/templates.pdf
"""
from __future__ import annotations

from typing import Callable

import numpy as np
from numpy.typing import ArrayLike

from ._helpers import Identity, Info, LinearOperator, clip_imag, get_default_inner


def chebyshev(
    A: LinearOperator,
    b: ArrayLike,
    eigenvalue_estimates: tuple[float, float],
    M: LinearOperator | None = None,
    x0: ArrayLike | None = None,
    tol: float = 1e-5,
    atol: float = 1.0e-15,
    maxiter: int | None = None,
    callback: Callable[[int, np.ndarray, np.ndarray], np.ndarray] = None,
    tol_inner_real: float = 1.0e-15,
):
    def _norm(y):
        return np.sqrt(clip_imag(_inner(y, y), tol_inner_real))

    b = np.asarray(b)

    assert len(A.shape) == 2
    assert A.shape[0] == A.shape[1]
    assert A.shape[1] == b.shape[0]

    n = A.shape[0]
    M = Identity(n) if M is None else M

    if x0 is None:
        x = np.zeros_like(b)
        r = b.copy()
    else:
        x = np.array(x0)
        r = b - A @ x0

    _inner = get_default_inner(b.shape)

    assert len(eigenvalue_estimates) == 2
    assert eigenvalue_estimates[0] <= eigenvalue_estimates[1]
    lmin, lmax = eigenvalue_estimates

    d = (lmax + lmin) / 2
    c = (lmax - lmin) / 2

    resnorms = [_norm(r)]

    if callback is not None:
        callback(0, x, r)

    alpha = None
    p = None

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

        z = M @ r

        if k == 0:
            p = z.copy()
            alpha = 1.0 / d
        else:
            beta = 0.5 * (c * alpha) ** 2
            if k > 1:
                beta *= 0.5

            alpha = 1.0 / (d - beta / alpha)
            p = z + beta * p

        x += alpha * p
        r -= alpha * (A @ p)

        if callback is not None:
            callback(k + 1, x, r)

        resnorms.append(_norm(r))

        k += 1

    return x if success else None, Info(success, x, k, np.array(resnorms))
