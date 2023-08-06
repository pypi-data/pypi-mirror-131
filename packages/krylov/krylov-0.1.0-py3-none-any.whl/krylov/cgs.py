"""
Peter Sonneveld,
CGS: A fast Lanczos-Type Solver for Nonsymmetric Linear Systems,
SIAM J. Sci. Stat. Comput.,
10(1):36-52, 1989,
<https://doi.org/10.1137/0910004>.

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
    clip_imag,
    get_default_inner,
    wrap_inner,
)


def cgs(
    A: LinearOperator,
    b: ArrayLike,
    M: LinearOperator | None = None,
    x0: ArrayLike | None = None,
    inner: Callable[[np.ndarray, np.ndarray], np.ndarray] | None = None,
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

    def _norm(y):
        return np.sqrt(clip_imag(_inner(y, M @ y), tol_inner_real))

    if x0 is None:
        x = np.zeros_like(b)
        r0 = b.copy()
    else:
        x = np.array(x0)
        assert x.shape[0] == A.shape[1], f"A.shape = {A.shape}, but x.shape = {x.shape}"
        r0 = b - A @ x

    # common but arbitrary choice:
    rp = r0

    r = r0.copy()

    if callback:
        callback(0, x, r)

    resnorms = [_norm(r)]

    rho = 1.0
    alpha = None

    p = np.zeros_like(b)
    q = np.zeros_like(b)

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

        rho_old = rho
        rho = _inner(rp, r)

        # TODO break-down for rho==0?

        beta = rho / np.where(rho_old != 0.0, rho_old, 1.0)
        u = r + beta * q
        p = u + beta * (q + beta * p)

        v = A @ (M @ p)

        s = _inner(rp, v)
        alpha = rho / np.where(s != 0.0, s, 1.0)

        q = u - alpha * v

        u_ = M @ (u + q)

        x += alpha * u_
        r -= alpha * (A @ u_)

        if callback:
            callback(k + 1, x, r)

        resnorms.append(_norm(r))

        k += 1

    return x if success else None, Info(success, x, k, np.array(resnorms))
