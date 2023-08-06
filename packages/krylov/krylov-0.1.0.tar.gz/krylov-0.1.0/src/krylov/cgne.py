from numpy.typing import ArrayLike

from ._helpers import Info, LinearOperator, RLinearOperator, asrlinearoperator
from .cg import cg


class A_AH(LinearOperator):
    def __init__(self, A: RLinearOperator):
        assert len(A.shape) == 2
        self.shape = (A.shape[0], A.shape[0])
        self.A = A
        self.dtype = A.dtype

    def __matmul__(self, x: ArrayLike):
        return self.A @ self.A.rmatvec(x)


def cgne(A: RLinearOperator, b: ArrayLike, *args, **kwargs):
    r"""Conjugate Gradient Method on the Normal Equations

    AA^H y = b
    x = A^H y
    """
    A = asrlinearoperator(A)

    sol, info = cg(A_AH(A), b, *args, **kwargs)

    xk = A.rmatvec(info.xk)

    if sol is not None:
        sol = xk

    info = Info(info.success, xk, info.numsteps, info.resnorms, None)
    return sol, info
