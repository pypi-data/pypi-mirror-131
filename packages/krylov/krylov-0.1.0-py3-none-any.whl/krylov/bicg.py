"""
H.A. Van der Vorst,
Bi-CGSTAB: A Fast and Smoothly Converging Variant of Bi-CG for the Solution of
Nonsymmetric Linear Systems,
SIAM J. Sci. Stat. Comput. 13 (2): 631–644, 1992,
<https://doi.org/10.1137%2F0913035>

Other implementations:

https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.bicg.html
https://petsc.org/release/src/ksp/ksp/impls/bicg/bicg.c.html#KSPBICG
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
    clip_imag,
    get_default_inner,
    wrap_inner,
)


def bicg(
    A: LinearOperator,
    b: ArrayLike,
    M: LinearOperator | None = None,
    x0: ArrayLike | None = None,
    inner: Callable[[np.ndarray, np.ndarray], np.ndarray] | None = None,
    tol: float = 1e-5,
    atol: float = 1.0e-15,
    maxiter: int | None = None,
    callback: Callable[[int, np.ndarray, np.ndarray], np.ndarray] = None,
    tol_inner_real: float = 1.0e-15,
):
    def _norm(y):
        return np.sqrt(clip_imag(_inner(y, M @ y), tol_inner_real))

    b = np.asarray(b)

    assert len(A.shape) == 2
    assert A.shape[0] == A.shape[1]
    assert A.shape[1] == b.shape[0]

    A = asrlinearoperator(A)
    n = A.shape[0]
    M = Identity(n) if M is None else asrlinearoperator(M)

    _inner = get_default_inner(b.shape) if inner is None else wrap_inner(inner)

    if x0 is None:
        x = np.zeros_like(b)
        r = np.array([b, b.conj()])
    else:
        x = np.copy(x0)
        r = b - A @ x
        r = np.array([r, r.conj()])

    if callback is not None:
        callback(0, x, r)

    # make sure to copy, in case M is the Identity
    p = [(M @ r[0]).copy(), M.rmatvec(r[1]).copy()]

    resnorms = [_norm(r[0])]

    rMr = _inner(r[1], M @ r[0])

    k = 0
    success = False
    criterion = np.maximum(tol * resnorms[0], atol)
    while True:
        if np.all(resnorms[-1] <= criterion):
            # oh really?
            resnorms[-1] = _norm(b - A @ x)
            if np.all(resnorms[-1] <= criterion):
                success = True
                break

        if k == maxiter:
            break

        Ap0 = A @ p[0]
        AHp1 = A.rmatvec(p[1])

        pAp = _inner(p[1], Ap0)
        # same as
        # pAp2 = _inner(AHp1, p[0])

        alpha = rMr / np.where(pAp != 0, pAp, 1.0)

        x += alpha * p[0]

        r[0] -= alpha * Ap0
        r[1] -= alpha.conj() * AHp1

        rMr_old = rMr
        rMr = _inner(r[1], M @ r[0])
        beta = rMr / np.where(rMr_old != 0, rMr_old, 1.0)

        if callback is not None:
            callback(k + 1, x, r)

        resnorms.append(_norm(r[0]))

        p[0] = M @ r[0] + beta * p[0]
        p[1] = M.rmatvec(r[1]) + beta.conj() * p[1]

        k += 1

    return x if success else None, Info(success, x, k, np.array(resnorms))
