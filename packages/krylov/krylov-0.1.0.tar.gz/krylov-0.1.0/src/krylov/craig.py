"""
E.J. Craig,
The N-step iteration procedures,
Journal of Mathematics and Physics, 34(1):64–73, 1955.
<https://doi.org/10.1002/sapm195534164>.

See also:
<https://web.stanford.edu/group/SOL/software/craig/>
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
)


def craig(
    A: LinearOperator,
    b: ArrayLike,
    M: LinearOperator | None = None,
    N: LinearOperator | None = None,
    x0: ArrayLike | None = None,
    tol: float = 1e-5,
    atol: float = 1.0e-15,
    maxiter: int | None = None,
    callback: Callable[[int, np.ndarray, list[np.ndarray]], None] | None = None,
    tol_inner_real: float = 1.0e-15,
    max_acond: float = 1.0e15,
):
    """
    Mimizes

        min_x ||Ax-b||^2_{M^{-1}} + ||M^{-1}x||^2_N

    with M, N being SPD operators. An equivalent system is

        ( M    A ) ( r ) = ( b )
        ( A.H -N ) ( x )   ( 0 )

    """

    def _norm2(y):
        return clip_imag(_inner(y, y), tol_inner_real)

    def _norm(y):
        return np.sqrt(_norm2(y))

    A = asrlinearoperator(A)
    b = np.asarray(b)

    assert len(A.shape) == 2
    assert A.shape[0] == b.shape[0]
    m, n = A.shape

    M = Identity(m) if M is None else M
    N = Identity(n) if N is None else N

    _inner = get_default_inner(b.shape)

    maxiter = N if maxiter is None else maxiter

    # get initial residual
    if x0 is None:
        x_shape = (A.shape[1], *b.shape[1:])
        x = np.zeros(x_shape, dtype=b.dtype)
        r = np.copy(b)
    else:
        x = np.copy(x0)
        assert x.shape[0] == A.shape[1], f"A.shape = {A.shape}, but x.shape = {x.shape}"
        r = b - A @ x

    anorm = 0.0
    acond = 0.0
    xnorm = 0.0

    #  Set beta(1) and u(1) for the bidiagonalization.
    #      beta*u = b.
    v = np.zeros((n, *b.shape[1:]), dtype=r.dtype)
    w = np.zeros((m, *b.shape[1:]), dtype=r.dtype)
    y = np.zeros((m, *b.shape[1:]), dtype=r.dtype)

    beta = _norm(r)
    u = r.copy()

    resnorms = [beta]

    anorm2 = 0.0
    ddnorm = 0.0
    xxnorm = 0.0
    alpha = 1.0
    z = -1.0

    if callback is not None:
        callback(0, x, resnorms)

    # iterate
    k = 0
    success = False
    reason = None
    criterion = np.maximum(tol * resnorms[0], atol)
    while True:
        if np.all(resnorms[-1] <= criterion):
            # oh really?
            r = b - A @ x
            resnorms[-1] = _norm(r)
            if np.all(resnorms[-1] <= criterion):
                success = True
                break

        if k == maxiter:
            reason = "maxiter reached"
            break

        if acond > max_acond:
            reason = f"estimated cond(A) = {acond:e} exceeds max_acond = {max_acond:e}"
            break

        alpha_old = alpha

        assert np.all(beta > 0.0)
        u /= beta

        v *= -beta
        v += A.rmatvec(u)

        alpha2 = _norm2(v)
        alpha = np.sqrt(alpha2)

        if alpha < 1.0e-12:
            reason = f"system Ax=b seems incompatible, alpha = {alpha}"
            break

        assert alpha > 0.0
        v /= alpha

        anorm2 += alpha2
        z *= -(beta / alpha)
        x += z * v

        w *= -beta / alpha_old
        w += u
        y += (z / alpha) * w
        # ddnorm: estimate of norm(inv(A.H @ A))
        ddnorm += _norm2(w) / alpha2

        u *= -alpha
        u += A @ v
        beta = _norm(u)

        anorm2 += beta ** 2
        anorm = np.sqrt(anorm2)
        acond = np.sqrt(ddnorm) * anorm
        xxnorm += z ** 2
        rnorm = np.abs(beta * z)
        xnorm = np.sqrt(xxnorm)

        resnorms.append(rnorm)

        if callback is not None:
            callback(k + 1, x, resnorms)

        k += 1

    return x if success else None, Info(
        success=success,
        reason=reason,
        xk=x,
        numsteps=k,
        resnorms=np.array(resnorms),
        acond=acond,
        anorm=anorm,
        xnorm=xnorm,
    )
