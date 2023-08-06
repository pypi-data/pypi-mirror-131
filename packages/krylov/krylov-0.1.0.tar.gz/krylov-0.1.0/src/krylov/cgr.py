"""
Yousef Saad,
Iterative methods for sparse linear systems (2nd ed.),
page 194, SIAM.

https://en.wikipedia.org/wiki/Conjugate_residual_method
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


def cgr(
    A: LinearOperator,
    b: ArrayLike,
    M: LinearOperator | None = None,
    x0: ArrayLike | None = None,
    inner: Callable | None = None,
    tol: float = 1e-5,
    atol: float = 1.0e-15,
    maxiter: int | None = None,
    callback: Callable | None = None,
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

    r = M @ r

    _inner = get_default_inner(b.shape) if inner is None else wrap_inner(inner)

    Ar = A @ r
    rAr = _inner(r, Ar)

    resnorms = [_norm(r)]

    if callback is not None:
        callback(0, x, r)

    p = r.copy()
    Ap = Ar.copy()

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

        MAp = M @ Ap
        ApMAp = _inner(Ap, MAp)
        alpha = rAr / np.where(ApMAp != 0.0, ApMAp, 1.0)

        x += alpha * p
        r -= alpha * MAp

        Ar = A @ r
        rAr_old = rAr
        rAr = _inner(r, Ar)
        beta = rAr / np.where(rAr_old != 0.0, rAr_old, 1.0)

        p = r + beta * p
        Ap = Ar + beta * Ap

        if callback is not None:
            callback(k + 1, x, r)

        resnorms.append(_norm(r))

        k += 1

    return x if success else None, Info(success, x, k, np.array(resnorms))
