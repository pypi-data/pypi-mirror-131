"""
Sou-Cheng T. Choi, Christopher C. Paige, Michael A. Saunders,
MINRES-QLP: A Krylov subspace method for indefinite or singular symmetric systems,
SIAM J. Sci. Comput., 33(4), 1810–1836, 2011,
<https://doi.org/10.1137/100787921>,
<https://arxiv.org/abs/1003.4042>.

Abstract:
CG, SYMMLQ, and MINRES are Krylov subspace methods for solving symmetric systems of
linear equations. When these methods are applied to an incompatible system (that is, a
singular symmetric least-squares problem), CG could break down and SYMMLQ's solution
could explode, while MINRES would give a least-squares solution but not necessarily the
minimum-length (pseudoinverse) solution. This understanding motivates us to design a
MINRES-like algorithm to compute minimum-length solutions to singular symmetric systems.
MINRES uses QR factors of the tridiagonal matrix from the Lanczos process (where R is
upper-tridiagonal). MINRES-QLP uses a QLP decomposition (where rotations on the right
reduce R to lower-tridiagonal form). On ill-conditioned systems (singular or not),
MINRES-QLP can give more accurate solutions than MINRES. We derive preconditioned
MINRES-QLP, new stopping rules, and better estimates of the solution and residual norms,
the matrix norm, and the condition number.
"""
from __future__ import annotations

from typing import Callable

import numpy as np
from numpy.typing import ArrayLike
from scipy.linalg import lapack

from ._helpers import (
    Identity,
    Info,
    LinearOperator,
    assert_correct_shapes,
    clip_imag,
    get_default_inner,
    wrap_inner,
)


def minres_qlp(
    A: LinearOperator,
    b: ArrayLike,
    M: LinearOperator | None = None,
    inner: Callable[[np.ndarray, np.ndarray], np.ndarray] | None = None,
    x0: ArrayLike | None = None,
    tol: float = 1e-5,
    atol: float = 1.0e-15,
    maxiter: int | None = None,
    callback: Callable[[int, np.ndarray, list[np.ndarray]], None] | None = None,
    tol_inner_real: float = 1.0e-15,
    max_acond: float = 1.0e15,
):
    def _norm(y):
        return np.sqrt(clip_imag(_inner(y, y), tol_inner_real))

    b = np.asarray(b)

    assert_correct_shapes(A, b, x0)

    n = A.shape[0]
    M = Identity(n) if M is None else M

    _inner = get_default_inner(b.shape) if inner is None else wrap_inner(inner)

    if x0 is None:
        x = np.zeros_like(b)
        r = b.copy()
    else:
        x = np.copy(x0)
        r = b - A @ x

    # TODO
    resnorms = [0.0]

    if callback is not None:
        callback(0, x, resnorms)

    # for the givens rotations
    lartg = lapack.get_lapack_funcs("lartg", (r,))

    n = len(b)
    r2 = b
    beta1 = _norm(r2)

    r3 = M @ r2
    beta1 = _inner(r3, r2)
    if beta1 < 0:
        raise ValueError('Error: "M" is indefinite!')
    beta1 = np.sqrt(beta1)

    ## Initialize
    flag0 = -2
    flag = -2
    QLPiter = 0
    beta = 0
    tau = 0
    taul = 0
    phi = beta1
    betan = beta1
    gmin = 0
    cs = -1
    sn = 0
    cr1 = -1
    sr1 = 0
    cr2 = -1
    sr2 = 0
    dltan = 0
    eplnn = 0
    gama = 0
    gamal = 0
    gamal2 = 0
    eta = 0
    etal = 0
    etal2 = 0
    vepln = 0
    veplnl = 0
    veplnl2 = 0
    ul3 = 0
    ul2 = 0
    ul = 0
    u = 0
    rnorm = betan
    xnorm = 0
    xl2norm = 0
    Axnorm = 0
    Anorm = 0
    acond = 1
    relres = rnorm / (beta1 + 1e-50)
    x = np.zeros(n)
    w = np.zeros(n)
    wl = np.zeros(n)
    r1 = None
    wl2 = None

    max_xnorm = 1e7
    TranCond = 1e7

    k = 0
    success = False
    criterion = np.maximum(tol * resnorms[0], atol)
    while True:
        # Lanczos
        betal = beta
        beta = betan
        v = r3 / beta
        r3 = A @ v

        if k > 0:
            r3 -= r1 * (beta / betal)

        alpha = np.real(r3.T.dot(v))
        r3 -= r2 * (alpha / beta)
        r1 = r2
        r2 = r3

        if M is None:
            betan = _norm(r3)
            if k == 0:
                if betan == 0:
                    if alpha == 0:
                        flag = 0
                        break
                    else:
                        flag = -1
                        x = b / alpha
                        break
        else:
            r3 = M @ r2
            betan = _inner(r2, r3)
            assert betan > 0.0, "Error: M is indefinite or singular!"
            betan = np.sqrt(betan)

        pnorm = np.sqrt(betal ** 2 + alpha ** 2 + betan ** 2)

        # previous left rotation Q_{k-1}
        dbar = dltan
        dlta = cs * dbar + sn * alpha
        epln = eplnn
        gbar = sn * dbar - cs * alpha
        eplnn = sn * betan
        dltan = -cs * betan
        dlta_QLP = dlta
        # current left plane rotation Q_k
        gamal3 = gamal2
        gamal2 = gamal
        gamal = gama
        cs, sn, gama = lartg(gbar, betan)
        gama_tmp = gama
        taul2 = taul
        taul = tau
        tau = cs * phi
        Axnorm = np.sqrt(Axnorm ** 2 + tau ** 2)
        phi = sn * phi
        # previous right plane rotation P_{k-2,k}
        if k > 1:
            veplnl2 = veplnl
            etal2 = etal
            etal = eta
            dlta_tmp = sr2 * vepln - cr2 * dlta
            veplnl = cr2 * vepln + sr2 * dlta
            dlta = dlta_tmp
            eta = sr2 * gama
            gama = -cr2 * gama
        # current right plane rotation P{k-1,k}
        if k > 0:
            cr1, sr1, gamal = lartg(gamal, dlta)
            vepln = sr1 * gama
            gama = -cr1 * gama

        # update xnorm
        xnorml = xnorm
        ul4 = ul3
        ul3 = ul2
        if k > 1:
            ul2 = (taul2 - etal2 * ul4 - veplnl2 * ul3) / gamal2
        if k > 0:
            ul = (taul - etal * ul3 - veplnl * ul2) / gamal
        xnorm_tmp = np.sqrt(xl2norm ** 2 + ul2 ** 2 + ul ** 2)
        if abs(gama) > np.finfo(np.double).tiny and xnorm_tmp < max_xnorm:
            u = (tau - eta * ul2 - vepln * ul) / gama
            if np.sqrt(xnorm_tmp ** 2 + u ** 2) > max_xnorm:
                u = 0
                flag = 6
        else:
            u = 0
            flag = 9
        xl2norm = np.sqrt(xl2norm ** 2 + ul2 ** 2)
        xnorm = np.sqrt(xl2norm ** 2 + ul ** 2 + u ** 2)

        # update w and x
        # Minres
        if (acond < TranCond) and flag != flag0 and QLPiter == 0:
            wl2 = wl
            wl = w
            w = (v - epln * wl2 - dlta_QLP * wl) / gama_tmp
            if xnorm < max_xnorm:
                x += tau * w
            else:
                flag = 6
        # Minres-QLP
        else:
            QLPiter += 1
            if QLPiter == 1:
                xl2 = np.zeros((n, 1))
                if k > 0:  # construct w_{k-3}, w_{k-2}, w_{k-1}
                    if k > 2:
                        wl2 = gamal3 * wl2 + veplnl2 * wl + etal * w
                    if k > 1:
                        wl = gamal_QLP * wl + vepln_QLP * w
                    w = gama_QLP * w
                    xl2 = x - wl * ul_QLP - w * u_QLP

            if k == 0:
                wl2 = wl
                wl = v * sr1
                w = -v * cr1
            elif k == 1:
                wl2 = wl
                wl = w * cr1 + v * sr1
                w = w * sr1 - v * cr1
            else:
                wl2 = wl
                wl = w
                w = wl2 * sr2 - v * cr2
                wl2 = wl2 * cr2 + v * sr2
                v = wl * cr1 + w * sr1
                w = wl * sr1 - w * cr1
                wl = v
            xl2 = xl2 + wl2 * ul2
            x = xl2 + wl * ul + w * u

        # next right plane rotation P{k-1,k+1}
        gamal_tmp = gamal
        cr2, sr2, gamal = lartg(gamal, eplnn)
        # transfering from Minres to Minres-QLP
        gamal_QLP = gamal_tmp
        # print('gamal_QLP=', gamal_QLP)
        vepln_QLP = vepln
        gama_QLP = gama
        ul_QLP = ul
        u_QLP = u
        ## Estimate various norms
        abs_gama = abs(gama)
        Anorml = Anorm
        Anorm = max([Anorm, pnorm, gamal, abs_gama])
        if k == 0:
            gmin = gama
            gminl = gmin
        elif k > 0:
            gminl2 = gminl
            gminl = gmin
            gmin = min([gminl2, gamal, abs_gama])
        acondl = acond
        acond = Anorm / gmin
        rnorml = rnorm
        relresl = relres
        if flag != 9:
            rnorm = phi
        relres = rnorm / (Anorm * xnorm + beta1)
        rootl = np.sqrt(gbar ** 2 + dltan ** 2)
        Arnorml = rnorml * rootl
        relAresl = rootl / Anorm
        ## See if any of the stopping criteria are satisfied.
        epsx = Anorm * xnorm * np.finfo(float).eps
        if (flag == flag0) or (flag == 9):
            t1 = 1 + relres
            t2 = 1 + relAresl
            if k == maxiter:
                flag = 8  # exit before maxit
            if acond >= max_acond:
                flag = 7  # Huge acond
            if xnorm >= max_xnorm:
                flag = 6  # xnorm exceeded
            if epsx >= beta1:
                flag = 5  # x = eigenvector
            if t2 <= 1:
                flag = 4  # Accurate Least Square Solution
            if t1 <= 1:
                flag = 3  # Accurate Ax = b Solution
            if relAresl <= rtol:
                flag = 2  # Trustful Least Square Solution
            if relres <= rtol:
                flag = 1  # Trustful Ax = b Solution

        if flag == 2 or flag == 4 or flag == 6 or flag == 7:
            # possibly singular
            k = k - 1
            acond = acondl
            rnorm = rnorml
            relres = relresl
        else:
            resvec = np.append(resvec, rnorm)
            Aresvec = np.append(Aresvec, Arnorml)

        k += 1

    return x if success else None, Info(success, x, k, np.array(resnorms))
