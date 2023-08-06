from __future__ import annotations

from typing import Callable

try:
    # Python 3.8+
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

# from collections import namedtuple


# https://docs.python.org/3/library/typing.html#typing.Protocol
class LinearOperator(Protocol):
    shape: tuple[int, int]
    dtype: np.dtype

    @staticmethod
    def __matmul__(_: ArrayLike) -> np.ndarray:
        ...


class RLinearOperator(LinearOperator):
    @staticmethod
    def rmatvec(_: ArrayLike) -> np.ndarray:
        ...


class Identity(RLinearOperator):
    # lowest possible dtype
    dtype = np.dtype("u1")

    def __init__(self, n: int):
        self.shape = (n, n)

    @staticmethod
    def __matmul__(x: ArrayLike) -> ArrayLike:
        return x

    @staticmethod
    def rmatvec(x: ArrayLike) -> ArrayLike:
        return x


class Product(LinearOperator):
    def __init__(self, *operators):
        self.operators = operators
        self.dtype = np.find_common_type([op.dtype for op in operators], [])
        self.shape = (operators[0].shape[0], operators[-1].shape[1])

    def __matmul__(self, x):
        out = x.copy()
        for op in self.operators[::-1]:
            out = op @ out
        return out


class RLinearOperatorWrapper(RLinearOperator):
    """Provides rmatvec."""

    def __init__(self, array):
        self._array = array
        self._adj_array = None
        self.shape = array.shape
        self.dtype = array.dtype

    def __matmul__(self, x: ArrayLike) -> np.ndarray:
        return self._array @ x

    matvec = __matmul__

    def rmatvec(self, x: ArrayLike) -> np.ndarray:
        """Performs the operation y = A^H @ x."""
        x = np.asarray(x)
        # For dense matrices, caching takes a lot of memory and the below gist analysis
        # suggests that it isn't even that much faster.
        # <https://gist.github.com/nschloe/eb3bd2520cdbb1378c14887d56c031a2>
        # Just use conj().
        if isinstance(self._array, np.ndarray):
            return (self._array.T @ x.conj()).conj()

        # For the rest, just cache the Hermitian matrix
        if self._adj_array is None:
            self._adj_array = self._array.T.conj()
        return self._adj_array @ x


def asrlinearoperator(A: LinearOperator):
    if not hasattr(A, "__matmul__"):
        raise ValueError(f"Unknown linear operator A = {A}")

    if hasattr(A, "rmatvec"):
        return A

    return RLinearOperatorWrapper(A)


@dataclass(frozen=True)
class Info:
    success: bool
    xk: np.ndarray
    numsteps: int
    resnorms: np.ndarray | None = None
    # resnorms of the normalized equations ||A.H (b - Ax)||. Useful for least-squares
    # etc.
    nresnorms: np.ndarray | None = None
    acond: float | None = None
    anorm: float | None = None
    xnorm: float | None = None
    reason: str | None = None


def get_default_inner(b_shape):
    # np.dot is faster than einsum for flat vectors
    # <https://gist.github.com/nschloe/33b3c93b9bc0768394ba9edee1fda2bc>
    def inner_dot(x, y):
        return np.dot(x.conj(), y)

    def inner_einsum(x, y):
        return np.einsum("i...,i...->...", x.conj(), y)

    return inner_dot if len(b_shape) == 1 else inner_einsum


def wrap_inner(inner: Callable) -> Callable:
    # a wrapper to assert correct shape handling

    def _inner(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        assert x.shape == y.shape
        out = inner(x, y)
        if out.shape != x.shape[1:]:
            raise ValueError(
                f"inner(x, y) returned wrong shape! From x.shape = y.shape = {x.shape} "
                + f"expected shape {x.shape[1:]} but got shape {out.shape}"
            )
        return out

    return _inner


# def matrix_2_norm(A):
#     """Computes the max singular value of all matrices of shape (n, n, ...). The result
#     has shape (...).
#     """
#     return np.max(np.linalg.svd(A.T, compute_uv=False).T, axis=0)


def clip_imag(val, tol=0.0):
    val = np.asarray(val)

    if np.issubdtype(val.dtype, np.floating):
        return val

    if np.any(np.abs(val.imag) > tol * (1.0 + np.abs(val))):
        raise ValueError(f"value is not real, val = {val}")
    return val.real


def assert_correct_shapes(A, b, x0, must_be_square=True):
    if len(A.shape) != 2:
        raise ValueError(f"A must have shape (m, n), not {A.shape}")

    if must_be_square:
        if A.shape[0] != A.shape[1]:
            raise ValueError(f"Need square matrix, not A.shape = {A.shape}")

    if A.shape[1] != b.shape[0]:
        raise ValueError(
            "Incompatible right-hand side, "
            + f"A.shape = {A.shape}, b.shape = {b.shape}"
        )

    if x0 is not None:
        if A.shape[1] != b.shape[0]:
            raise ValueError(
                "Incompatible x0, "
                + f"A.shape = {A.shape}, b.shape = {b.shape}, x0.shape = {x0.shape}"
            )
