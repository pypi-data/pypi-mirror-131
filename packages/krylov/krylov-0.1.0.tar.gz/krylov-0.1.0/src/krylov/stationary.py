from __future__ import annotations

from typing import Callable

import numpy as np
from numpy.typing import ArrayLike
from scipy.linalg import solve_triangular
from scipy.sparse import tril, triu
from scipy.sparse.linalg import spsolve_triangular
from scipy.sparse.linalg.interface import LinearOperator

from ._helpers import Info, clip_imag, get_default_inner


def richardson(*args, omega: float = 1.0, **kwargs):
    return _stationary(lambda r: omega * r, *args, **kwargs)


def jacobi(A, *args, omega: float = 1.0, **kwargs):
    # There's no difference in speed between division and multiplication, so keep D
    # here. <https://gist.github.com/nschloe/7e4cb61dd391b4edbeb10d23038aa98e>
    D = A.diagonal()

    def _update(r):
        return omega * (r.T / D).T

    return _stationary(_update, A, *args, **kwargs)


def gauss_seidel(A, *args, omega: float = 1.0, lower: bool = True, **kwargs):
    def tri_solve_dense(y):
        return omega * solve_triangular(A, y, lower=lower)

    # scipy doesn't accept non-triangular matrices into spsolve_triangular
    # https://github.com/scipy/scipy/issues/14091
    M = tril(A) if lower else triu(A)
    M = M.tocsr()

    def tri_solve_sparse(y):
        return omega * spsolve_triangular(M, y, lower=lower)

    return _stationary(
        tri_solve_dense if isinstance(A, np.ndarray) else tri_solve_sparse,
        A,
        *args,
        **kwargs
    )


def sor(A, *args, omega: float = 1.0, lower: bool = True, **kwargs):
    """x_{k+1} = xk + omega * (D + omega * L)^{-1} r"""
    d_ = A.diagonal() / omega

    if isinstance(A, np.ndarray):
        A_ = A.copy()
        np.fill_diagonal(A_, d_)

        def tri_solve_dense(y):
            return solve_triangular(A_, y, lower=lower)

        return _stationary(tri_solve_dense, A, *args, **kwargs)

    M = tril(A) if lower else triu(A)
    M.setdiag(d_)
    M = M.tocsr()

    def tri_solve_sparse(y):
        return spsolve_triangular(M, y, lower=lower)

    return _stationary(tri_solve_sparse, A, *args, **kwargs)


def ssor(A, *args, omega: float = 1.0, **kwargs):
    """https://en.wikipedia.org/wiki/Successive_over-relaxation

    P = omega / (2 - omega) * (D/omega + L) D^{-1} (D/omega + U)
    x_{k+1} = x_k + P^{-1} r
    """
    d = A.diagonal()

    if isinstance(A, np.ndarray):
        A_ = A.copy()
        np.fill_diagonal(A_, d / omega)

        def solve_dense(y):
            y = solve_triangular(A_, y, lower=True)
            y = (y.T * d).T
            y = solve_triangular(A_, y, lower=False)
            return (2 - omega) / omega * y

        return _stationary(solve_dense, A, *args, **kwargs)

    L = tril(A)
    L.setdiag(d / omega)
    L = L.tocsr()

    U = triu(A)
    U.setdiag(d / omega)
    U = U.tocsr()

    def solve_sparse(y):
        y = spsolve_triangular(L, y, lower=True)
        y = (y.T * d).T
        y = spsolve_triangular(U, y, lower=False)
        return (2 - omega) / omega * y

    return _stationary(solve_sparse, A, *args, **kwargs)


def _stationary(
    update: Callable[[np.ndarray], np.ndarray],
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
    b = np.asarray(b)

    assert len(A.shape) == 2
    assert A.shape[0] == A.shape[1]
    assert A.shape[1] == b.shape[0]

    _inner = get_default_inner(b.shape) if inner is None else inner

    def _norm(y):
        return np.sqrt(clip_imag(_inner(y, y), tol_inner_real))

    if x0 is None:
        x = np.zeros_like(b)
        r = b.copy()
    else:
        x = np.asarray(x0).copy()
        r = b - A @ x

    if callback is not None:
        callback(0, x, r)

    resnorms = [_norm(r)]

    k = 0
    success = False
    criterion = np.maximum(tol * resnorms[0], atol)
    while True:
        if np.all(resnorms[-1] <= criterion):
            success = True
            break

        if k == maxiter:
            break

        x += update(r)
        # TODO check which is faster
        r = b - A @ x
        # r -= A @ update

        if callback is not None:
            callback(k + 1, x, r)

        resnorms.append(_norm(r))

        k += 1

    return x if success else None, Info(success, x, k, np.array(resnorms))
