"""
Generalized conjugate residual method

S.C. Eisenstat, H.C. Elman, and H.C. Schultz.
Variational iterative methods for nonsymmetric systems of linear equations.
SIAM J. Numer. Anal., 20, 1983,
<https://doi.org/10.1137/0720023>.

Other implementations:
https://petsc.org/release/src/ksp/ksp/impls/gcr/gcr.c.html
"""
from __future__ import annotations

from typing import Callable

import numpy as np
from numpy.typing import ArrayLike

from ._helpers import Info, LinearOperator, clip_imag, get_default_inner, wrap_inner


def gcr(
    *args,
    restart_size: int | None = None,
    maxiter: int | None = None,
    x0: ArrayLike | None = None,
    **kwargs,
):
    if restart_size is None:
        return _gcr(*args, maxiter=maxiter, x0=x0, **kwargs)

    total_steps = 0
    info = None
    while True:
        sol, info = _gcr(
            *args,
            maxiter=restart_size
            if maxiter is None
            else min(restart_size, maxiter - total_steps),
            x0=x0 if info is None else info.xk,
            **kwargs,
        )
        total_steps += info.numsteps
        if info.success:
            break

    # override numsteps
    info = Info(info.success, info.xk, total_steps, info.resnorms, info.nresnorms)
    return sol, info


# TODO preconditioner
def _gcr(
    A: LinearOperator,
    b: ArrayLike,
    x0: ArrayLike | None = None,
    inner: Callable[[np.ndarray, np.ndarray], np.ndarray] | None = None,
    tol: float = 1e-5,
    atol: float = 1.0e-15,
    maxiter: int | None = None,
    callback: Callable[[int, np.ndarray, np.ndarray], None] | None = None,
    tol_inner_real: float = 1.0e-15,
):
    def _norm(y):
        return np.sqrt(clip_imag(_inner(y, y), tol_inner_real))

    b = np.asarray(b)

    assert len(A.shape) == 2
    assert A.shape[0] == A.shape[1]
    assert A.shape[1] == b.shape[0]

    if x0 is None:
        x = np.zeros_like(b)
        r = b.copy()
    else:
        x = np.copy(x0)
        r = b - A @ x0

    _inner = get_default_inner(b.shape) if inner is None else wrap_inner(inner)

    if callback is not None:
        callback(0, x, r)

    resnorms = [_norm(r)]

    s = []
    v = []

    k = 0
    success = False
    criterion = np.maximum(tol * resnorms[0], atol)
    while True:
        if np.all(resnorms[-1] <= criterion):
            r = b - A @ x
            resnorms[-1] = _norm(r)
            if np.all(resnorms[-1] <= criterion):
                success = True
                break

        if k == maxiter:
            break

        s.append(r.copy())
        v.append(A @ s[-1])

        # modified Gram-Schmidt
        for i in range(k):
            alpha = _inner(v[-1], v[i])
            v[-1] -= alpha * v[i]
            # ensure As = v
            s[-1] -= alpha * s[i]
        # normalize
        beta = _norm(v[-1])
        v[-1] /= np.where(beta != 0.0, beta, 1.0)
        s[-1] /= np.where(beta != 0.0, beta, 1.0)

        gamma = _inner(b, v[-1])
        x += gamma * s[-1]
        r -= gamma * v[-1]

        if callback is not None:
            callback(k + 1, x, r)

        resnorms.append(_norm(r))

        k += 1

    return x if success else None, Info(success, x, k, np.array(resnorms))
