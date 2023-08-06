from __future__ import annotations

from typing import Callable

try:
    # Python 3.8+
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

import numpy as np
from numpy.typing import ArrayLike

from ._helpers import (
    Identity,
    Info,
    LinearOperator,
    assert_correct_shapes,
    clip_imag,
    get_default_inner,
    wrap_inner,
)


def cg(
    A: LinearOperator,
    b: ArrayLike,
    M: LinearOperator | None = None,
    inner: Callable[[np.ndarray, np.ndarray], np.ndarray] | None = None,
    x0: ArrayLike | None = None,
    tol: float = 1e-5,
    atol: float = 1.0e-15,
    maxiter: int | None = None,
    callback: Callable[[int, np.ndarray, list[np.ndarray]], None] | None = None,
    resnorm_type: Literal["rr"] | Literal["rMr"] | Literal["MrMr"] = "rMr",
    tol_inner_real: float = 1.0e-15,
) -> tuple[np.ndarray | None, Info]:
    r"""Preconditioned CG method.

    The *preconditioned conjugate gradient method* can be used to solve a system of
    linear algebraic equations where the linear operator is self-adjoint and positive
    definite.

    Memory consumption is:

    * 3 vectors or 6 vectors if :math:`M` is used.

    **Caution:** CG's convergence may be delayed significantly due to round-off errors,
    cf. chapter 5.9 in [LieS13]_.
    """

    def _norm(y):
        return np.sqrt(clip_imag(_inner(y, y), tol_inner_real))

    b = np.asarray(b)

    assert_correct_shapes(A, b, x0)

    _inner = get_default_inner(b.shape) if inner is None else wrap_inner(inner)

    n = A.shape[0]
    M = Identity(n) if M is None else M

    maxiter = A.shape[0] if maxiter is None else maxiter

    # get initial residual
    if x0 is None:
        x = np.zeros_like(b)
        r = b.copy()
    else:
        x = np.copy(x0)
        r = b - A @ x

    Mr = M @ r
    rMr = clip_imag(_inner(r, Mr), tol_inner_real)

    if resnorm_type == "rMr":
        resnorm = np.sqrt(rMr)
    elif resnorm_type == "rr":
        resnorm = _norm(r)
    else:
        assert resnorm_type == "MrMr"
        resnorm = _norm(Mr)

    resnorms = [resnorm]

    if callback is not None:
        callback(0, x, resnorms)

    # resulting approximation is x = x0 + yk
    # yk = np.zeros(b.shape, dtype=Mr.dtype)
    # x = None

    # square of the old residual norm
    rhos = [None, rMr]
    p = None

    # iterate
    k = 0
    success = False
    reason = None
    criterion = np.maximum(tol * resnorms[0], atol)
    while True:
        if np.all(resnorms[-1] <= criterion):
            # oh really?
            r = b - A @ x
            if resnorm_type == "rMr":
                resnorms[-1] = np.sqrt(clip_imag(_inner(r, M @ r), tol_inner_real))
            elif resnorm_type == "rr":
                resnorms[-1] = _norm(r)
            else:
                assert resnorm_type == "MrMr"
                resnorms[-1] = _norm(M @ r)

            if np.all(resnorms[-1] <= criterion):
                success = True
                break

        if k == maxiter:
            reason = "maxiter reached"
            break

        # update the search direction
        if k == 0:
            p = np.copy(Mr)
        else:
            omega = rhos[-1] / np.where(rhos[-2] != 0, rhos[-2], 1.0)
            p *= omega
            p += Mr

        Ap = A @ p

        # compute inner product
        pAp = clip_imag(_inner(p, Ap), tol_inner_real)

        # rho / <p, Ap>
        alpha = rhos[-1] / np.where(pAp != 0, pAp, 1.0)

        # update solution and residual
        x += alpha * p
        r -= alpha * Ap

        # apply preconditioner
        Mr = M @ r
        # compute norm and new rho
        rMr = clip_imag(_inner(r, Mr), tol_inner_real)

        rhos = [rhos[-1], rMr]

        if resnorm_type == "rMr":
            resnorm = np.sqrt(rMr)
        elif resnorm_type == "rr":
            resnorm = _norm(r)
        else:
            assert resnorm_type == "MrMr"
            resnorm = _norm(Mr)

        resnorms.append(resnorm)

        if callback is not None:
            callback(k + 1, x, resnorms)

        k += 1

    return x if success else None, Info(
        success, x, k, np.array(resnorms), reason=reason
    )
