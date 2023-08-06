"""
Christopher C. Paige, Michael A. Saunders,
LSQR: An Algorithm for Sparse Linear Equations and Sparse Least Squares,
ACM Transactions on Mathematical Software,
Volume 8, Issue 1, March 1982, pp 43-71,
<https://doi.org/10.1145/355984.355989>.

<https://web.stanford.edu/group/SOL/software/lsqr/>
<https://petsc.org/release/src/ksp/ksp/impls/lsqr/lsqr.c.html#KSPLSQR>
"""
from __future__ import annotations

from typing import Callable

import numpy as np
from numpy.typing import ArrayLike
from scipy.linalg import lapack

from ._helpers import (
    Info,
    LinearOperator,
    asrlinearoperator,
    clip_imag,
    get_default_inner,
)


def lsqr(
    A: LinearOperator,
    b: ArrayLike,
    damp: float = 0.0,
    x0: ArrayLike | None = None,
    tol: float = 1e-5,
    atol: float = 1.0e-15,
    maxiter: int | None = None,
    callback: Callable[[int, np.ndarray, list[np.ndarray], list[np.ndarray]], None]
    | None = None,
    tol_inner_real: float = 1.0e-15,
):
    def _norm(y):
        return np.sqrt(clip_imag(_inner(y, y), tol_inner_real))

    A = asrlinearoperator(A)
    b = np.asarray(b)

    assert len(A.shape) == 2
    assert A.shape[0] == b.shape[0]
    N = A.shape[0]

    assert damp >= 0.0

    _inner = get_default_inner(b.shape)

    maxiter = N if maxiter is None else maxiter

    # get initial residual
    if x0 is None:
        x_shape = (A.shape[1], *b.shape[1:])
        x = np.zeros(x_shape, dtype=b.dtype)
        u = np.copy(b)
    else:
        x = np.copy(x0)
        assert x.shape[0] == A.shape[1], f"A.shape = {A.shape}, but x.shape = {x.shape}"
        u = b - A @ x

    beta = _norm(u)
    resnorms = [beta]
    u /= beta

    v = A.rmatvec(u)
    alpha = _norm(v)
    v /= alpha

    w = v.copy()

    # anorm = Frobenius norm of A
    anorm = alpha
    anorm2 = alpha ** 2
    acond = None
    arnorm = alpha * beta
    phi_ = beta
    rho_ = alpha
    c = 1.0
    s2 = 0.0
    c2 = -1.0
    z = 0.0
    xnorm = 0.0
    xxnorm = 0.0
    nresnorms = [phi_ * alpha]
    ddnorm = 0.0
    res2 = 0.0

    if callback is not None:
        callback(0, x, resnorms, nresnorms)

    # for the givens rotations
    lartg = lapack.get_lapack_funcs("lartg", (rho_, beta))

    # iterate
    k = 0
    success = False
    criterion = np.maximum(tol * resnorms[0], atol)
    while True:
        if np.all(nresnorms[-1] <= criterion):
            # oh really?
            r = b - A @ x
            xx0 = x if x0 is None else x - x0
            nresnorms[-1] = _norm(A.rmatvec(r) - (damp ** 2) * xx0)
            if np.all(nresnorms[-1] <= criterion):
                success = True
                break

        if k == maxiter:
            break

        # continue bidiagonalization
        u *= -alpha
        u += A @ v
        beta = _norm(u)
        u /= beta

        v *= -beta
        v += A.rmatvec(u)
        alpha = _norm(v)
        v /= alpha

        if damp == 0.0:
            # c1, s1, rho1_ = lartg(rho_, 0.0)
            rho1_ = rho_
            psi = 0.0
        else:
            c1, s1, rho1_ = lartg(rho_, damp)
            psi = s1 * phi_
            phi_ *= c1

        # rho = np.sqrt(rho_ ** 2 + beta ** 2); c = rho_ / rho; s = beta / rho
        c, s, rho = lartg(rho1_, beta)
        theta = s * alpha
        rho_ = -c * alpha
        phi = c * phi_
        phi_ *= s
        tau = s * phi

        dk = w / rho
        ddnorm += clip_imag(_inner(dk, dk))

        # update x, w
        x += (phi / rho) * w
        w *= -theta / rho
        w += v

        # estimate <x, x>
        delta = s2 * rho
        gamma_ = -c2 * rho
        rhs = phi - delta * z
        z_ = rhs / gamma_
        # xnorm is an approximation of ||x - x0||
        xnorm = np.sqrt(xxnorm + z_ ** 2)
        c2, s2, gamma = lartg(gamma_, theta)
        z = rhs / gamma
        xxnorm += z ** 2

        # approximation of the Frobenius-norm of A
        # this uses the old alpha
        anorm2 += beta ** 2 + damp ** 2
        anorm = np.sqrt(anorm2)
        anorm2 += alpha ** 2

        # estimate cond(A)
        acond = anorm * np.sqrt(ddnorm)
        res1 = phi_ ** 2
        res2 += psi ** 2
        # approximation of sqrt(||b - A @ x|| ** 2 + damp ** 2 * ||x - x0|| ** 2)
        resnorm = np.sqrt(res1 + res2)
        # approximation of ||A.H @ (b - A @ x) - damp ** 2 * (x - x0)||
        arnorm = alpha * np.abs(tau)

        resnorms.append(resnorm)
        nresnorms.append(arnorm)

        # The callback can override [n]resnorm with explicit values with, e.g.,
        # resnorms[-1] = 3.14
        if callback is not None:
            callback(k + 1, x, resnorms, nresnorms)

        k += 1

    return x if success else None, Info(
        success=success,
        xk=x,
        numsteps=k,
        resnorms=np.array(resnorms),
        nresnorms=np.array(nresnorms),
        acond=acond,
        anorm=anorm,
        xnorm=xnorm,
    )
