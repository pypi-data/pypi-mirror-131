from __future__ import annotations

from typing import Callable

import numpy as np
from numpy.typing import ArrayLike

from ._helpers import (
    Info,
    LinearOperator,
    asrlinearoperator,
    clip_imag,
    get_default_inner,
    wrap_inner,
)


def cgls(
    A: LinearOperator,
    b: ArrayLike,
    inner: Callable[[np.ndarray, np.ndarray], np.ndarray] | None = None,
    x0: ArrayLike | None = None,
    tol: float = 1e-5,
    atol: float = 1.0e-15,
    maxiter: int | None = None,
    callback: Callable[[int, np.ndarray, np.ndarray], None] | None = None,
    tol_inner_real: float = 1.0e-15,
):
    """Basically CG, but the residual is taken from the normal equation

    s = A^H r = A^H b - A^H A x
    """

    def _norm(y):
        return np.sqrt(clip_imag(_inner(y, y), tol_inner_real))

    A = asrlinearoperator(A)
    b = np.asarray(b)

    assert len(A.shape) == 2
    assert A.shape[0] == b.shape[0]
    N = A.shape[0]

    _inner = get_default_inner(b.shape) if inner is None else wrap_inner(inner)

    maxiter = N if maxiter is None else maxiter

    # get initial residual
    if x0 is None:
        x_shape = (A.shape[1], *b.shape[1:])
        x = np.zeros(x_shape, dtype=b.dtype)
        r = np.copy(b)
    else:
        x = np.copy(x0)
        r = b - A @ x

    if callback is not None:
        callback(0, x, r)

    p = A.rmatvec(r)
    rhos = [None, clip_imag(_inner(p, p), tol_inner_real)]

    nresnorms = [np.sqrt(rhos[-1])]

    # iterate
    k = 0
    success = False
    criterion = np.maximum(tol * nresnorms[0], atol)
    while True:
        if np.all(nresnorms[-1] <= criterion):
            # oh really?
            r = b - A @ x
            nresnorms[-1] = _norm(A.rmatvec(r))
            if np.all(nresnorms[-1] <= criterion):
                success = True
                break

        if k == maxiter:
            break

        Ap = A @ p

        alpha = rhos[-1] / clip_imag(_inner(Ap, Ap), tol_inner_real)

        # update solution and residual
        x += alpha * p
        r -= alpha * Ap
        s = A.rmatvec(r)

        rhos[0] = rhos[-1]
        rhos[-1] = clip_imag(_inner(s, s), tol_inner_real)

        beta = rhos[-1] / np.where(rhos[-2] != 0, rhos[-2], 1.0)
        p = s + beta * p

        if callback is not None:
            callback(k + 1, x, r)

        nresnorms.append(np.sqrt(rhos[-1]))

        k += 1

    return x if success else None, Info(success, x, k, nresnorms=np.array(nresnorms))
