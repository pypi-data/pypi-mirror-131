"""
Roland W. Freund,
A Transpose-Free Quasi-Minimal Residual Algorithm for Non-Hermitian Linear Systems,
SIAM J. Sci. Comput., 14(2), 470–482, 1993,
<https://doi.org/10.1137/0914029>.

See also:
<https://second.wiki/wiki/algoritmo_tfqmr>
<https://github.com/PythonOptimizers/pykrylov/blob/master/pykrylov/tfqmr/tfqmr.py>
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


def tfqmr(
    A: LinearOperator,
    b: ArrayLike,
    M: LinearOperator | None = None,
    x0: ArrayLike | None = None,
    inner: Callable[[np.ndarray, np.ndarray], np.ndarray] | None = None,
    tol: float = 1e-5,
    atol: float = 1.0e-15,
    maxiter: int | None = None,
    callback: Callable[[int, np.ndarray, list[np.ndarray]], None] | None = None,
    tol_inner_real: float = 1.0e-15,
):
    def _norm(y):
        return np.sqrt(clip_imag(_inner(y, y), tol_inner_real))

    b = np.asarray(b)

    assert_correct_shapes(A, b, x0)

    A = asrlinearoperator(A)

    n = A.shape[0]
    M = Identity(n) if M is None else asrlinearoperator(M)

    if x0 is None:
        x = np.zeros_like(b)
        r = b.copy()
    else:
        x = np.array(x0)
        r = b - A @ x0

    _inner = get_default_inner(b.shape) if inner is None else wrap_inner(inner)

    rho = clip_imag(_inner(r, r), tol_inner_real)
    resnorms = [np.sqrt(rho)]

    if callback is not None:
        callback(0, x, resnorms)

    r0 = np.copy(r)
    u = np.copy(r)
    w = np.copy(r)
    d = np.zeros((n, *b.shape[1:]), dtype=r.dtype)
    alpha = 0.0
    theta = 0.0
    eta = 0.0
    Mu = M @ u
    AMu = A @ Mu
    v = AMu.copy()

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

        if k % 2 == 0:
            # first pass
            alpha = rho / _inner(r0, v)
        else:
            # second pass
            u -= alpha * v
            Mu = M @ u
            AMu = A @ Mu

        w -= alpha * AMu
        d *= theta ** 2 * eta / alpha
        d += Mu
        theta = _norm(w) / resnorms[-1]
        c = 1.0 / np.sqrt(1 + theta ** 2)
        eta = c ** 2 * alpha
        x += eta * d

        resnorms.append(resnorms[-1] * theta * c)

        if k % 2 == 1:
            # second pass updates
            rho_old = rho
            rho = _inner(r0, w)
            beta = rho / rho_old

            # v <- beta * (AMu + beta * v)
            v *= beta
            v += AMu

            # u <- w + beta * u
            u *= beta
            u += w
            Mu = M @ u
            AMu = A @ Mu

            # v <- AMu + beta * v
            v *= beta
            v += AMu

        if callback is not None:
            callback(k + 1, x, resnorms)

        k += 1

    return x if success else None, Info(success, x, k, np.array(resnorms))
