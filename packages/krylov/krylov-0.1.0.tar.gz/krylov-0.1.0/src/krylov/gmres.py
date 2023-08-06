"""
Y. Saad, M. Schultz,
GMRES: a generalized minimal residual algorithm for solving nonsymmetric linear systems,
SIAM J. Sci. and Stat. Comput., 7(3), 856–869, 1986,
<https://doi.org/10.1137/0907058>.

Other implementations:
<https://petsc.org/release/docs/manualpages/KSP/KSPGMRES.html>
"""
from __future__ import annotations

from typing import Callable

import numpy as np
import scipy.linalg
from numpy.typing import ArrayLike

from ._helpers import (
    Identity,
    Info,
    LinearOperator,
    Product,
    assert_correct_shapes,
    clip_imag,
    get_default_inner,
    wrap_inner,
)
from .arnoldi import ArnoldiHouseholder, ArnoldiMGS
from .givens import givens


def multi_matmul(A, b):
    """A @ b for many A, b (i.e., A.shape == (m,n,...), y.shape == (n,...))"""
    return np.einsum("ij...,j...->i...", A, b)


def multi_solve_triangular(A, B):
    """This function calls scipy.linalg.solve_triangular for every single A. A
    vectorized version would be much better here.
    """
    A_shape = A.shape
    a = A.reshape(A.shape[0], A.shape[1], -1)
    b = B.reshape(B.shape[0], -1)
    y = []
    for k in range(a.shape[2]):
        if np.all(b[:, k] == 0.0):
            y.append(np.zeros(b[:, k].shape))
        else:
            y.append(scipy.linalg.solve_triangular(a[:, :, k], b[:, k]))
    y = np.array(y).T.reshape([A_shape[0]] + list(A_shape[2:]))
    return y


def gmres(
    *args,
    restart_size: int | None = None,
    maxiter: int | None = None,
    x0: ArrayLike | None = None,
    **kwargs,
) -> tuple[np.ndarray | None, Info]:
    if restart_size is None:
        return _gmres(*args, maxiter=maxiter, x0=x0, **kwargs)

    total_steps = 0
    info = None
    while True:
        sol, info = _gmres(
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


def _gmres(
    A: LinearOperator,
    b: ArrayLike,
    M: LinearOperator | None = None,
    Ml: LinearOperator | None = None,
    Mr: LinearOperator | None = None,
    inner: Callable | None = None,
    ortho: str = "mgs",
    x0: ArrayLike | None = None,
    tol: float = 1e-5,
    atol: float = 1.0e-15,
    maxiter: int | None = None,
    callback: Callable[[int, np.ndarray, list[np.ndarray]], None] | None = None,
) -> tuple[np.ndarray | None, Info]:

    b = np.asarray(b)
    assert_correct_shapes(A, b, x0)

    n = A.shape[0]
    M = Identity(n) if M is None else M
    Ml = Identity(n) if Ml is None else Ml
    Mr = Identity(n) if Mr is None else Mr

    def _get_xk(y):
        if y is None:
            return x0
        k = arnoldi.iter
        if k > 0:
            yy = multi_solve_triangular(R[:k, :k], y)
            # The last is always 0, so we could skip it, too
            # yk = sum(c * v for c, v in zip(yy, V[:-1]))
            yk = sum(c * v for c, v in zip(yy, arnoldi.V))
            return x0 + Mr @ yk
        return x0

    _inner = get_default_inner(b.shape) if inner is None else wrap_inner(inner)

    maxiter = A.shape[0] if maxiter is None else maxiter

    if x0 is None:
        x0 = np.zeros_like(b)
        Ml_r0 = Ml @ b
    else:
        x0 = np.asarray(x0)
        Ml_r0 = Ml @ (b - A @ x0)

    M_Ml_r0 = M @ Ml_r0
    M_Ml_r0_norm = np.sqrt(clip_imag(_inner(Ml_r0, M_Ml_r0)))

    Ml_A_Mr = Product(Ml, A, Mr)

    resnorms = [M_Ml_r0_norm]

    if callback is not None:
        callback(0, x0, resnorms)

    # initialize Arnoldi
    if ortho.startswith("mgs"):
        num_reorthos = 1 if len(ortho) == 3 else int(ortho[3:])
        arnoldi = ArnoldiMGS(
            Ml_A_Mr,
            Ml_r0,
            num_reorthos=num_reorthos,
            M=M,
            Mv=M_Ml_r0,
            Mv_norm=M_Ml_r0_norm,
            inner=_inner,
        )
    else:
        assert ortho == "householder"
        assert inner is None
        assert isinstance(M, Identity)
        arnoldi = ArnoldiHouseholder(Ml_A_Mr, Ml_r0)

    # Givens rotations:
    G = []
    # QR decomposition of Hessenberg matrix via Givens and R
    dtype = M_Ml_r0.dtype
    R = np.zeros([maxiter + 1, maxiter] + list(b.shape[1:]), dtype=dtype)
    y = np.zeros([maxiter + 1] + list(b.shape[1:]), dtype=dtype)
    # Right-hand side of projected system:
    y[0] = M_Ml_r0_norm
    yk = None
    xk = None

    # iterate Arnoldi
    k = 0
    success = False
    reason = None
    criterion = np.maximum(tol * resnorms[0], atol)
    while True:
        if np.all(resnorms[-1] <= criterion):
            # oh really?
            xk = _get_xk(yk) if xk is None else xk
            Ml_r = Ml @ (b - A @ xk)
            resnorms[-1] = np.sqrt(clip_imag(_inner(Ml_r, M @ Ml_r)))
            if np.all(resnorms[-1] <= criterion):
                success = True
                break

        if k == maxiter:
            reason = "maxiter reached"
            break

        # V is used in _get_xk()
        _, h = next(arnoldi)

        # Copy new column from Arnoldi
        R[: k + 2, k] = h[: k + 2]

        # Apply previous Givens rotations.
        for i in range(k):
            R[i : i + 2, k] = multi_matmul(G[i], R[i : i + 2, k])

        # Compute and apply new Givens rotation.
        g, r = givens(R[k : k + 2, k])
        G.append(g)
        R[k, k] = r
        R[k + 1, k] = 0.0
        y[k : k + 2] = multi_matmul(G[k], y[k : k + 2])

        yk = y[: k + 1]
        resnorm = np.abs(y[k + 1])
        xk = None

        if callback is not None:
            xk = _get_xk(yk) if xk is None else xk
            callback(k + 1, xk, resnorms)

        resnorms.append(resnorm)
        k += 1

    # compute solution if not yet done
    if xk is None:
        xk = _get_xk(y[: arnoldi.iter])

    return xk if success else None, Info(
        success, xk, k, np.array(resnorms), reason=reason
    )
