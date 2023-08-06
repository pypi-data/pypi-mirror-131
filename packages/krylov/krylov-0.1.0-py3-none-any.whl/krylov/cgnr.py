from numpy.typing import ArrayLike

from ._helpers import Info, LinearOperator, RLinearOperator, asrlinearoperator
from .cg import cg


class AH_A(LinearOperator):
    def __init__(self, A: RLinearOperator):
        assert len(A.shape) == 2
        self.shape = (A.shape[1], A.shape[1])
        self.A = A
        self.dtype = A.dtype

    def __matmul__(self, x):
        return self.A.rmatvec(self.A @ x)


def cgnr(A: LinearOperator, b: ArrayLike, *args, **kwargs):
    r"""Conjugate Gradient Method on the Normal Equations

    A^H A x = A^H b.

    Compare with CGNE where one solves

    AA^H y = b
    x = A^H y
    """
    A = asrlinearoperator(A)
    sol, info = cg(AH_A(A), A.rmatvec(b), *args, **kwargs)
    return sol, Info(info.success, info.xk, info.numsteps, nresnorms=info.resnorms)
