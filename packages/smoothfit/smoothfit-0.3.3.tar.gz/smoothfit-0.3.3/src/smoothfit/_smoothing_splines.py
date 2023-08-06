import numpy as np
from numpy.typing import ArrayLike
from scipy.sparse import spdiags


def smoothing_splines(x: ArrayLike, y: ArrayLike, lmbda: float):
    # check out
    # https://en.wikipedia.org/wiki/Smoothing_spline#Derivation_of_the_cubic_smoothing_spline
    x = np.asarray(x)
    y = np.asarray(y)

    assert len(x) == len(y)
    n = len(x)

    # build finite difference matrix with "no" boundary conditions
    assert np.all(x[:-1] < x[1:])
    h = x[1:] - x[:-1]

    diags = [
        np.concatenate([1 / h[:-1], [0.0, 0.0]]),
        np.concatenate([[0.0], -1 / h[1:] - 1 / h[:-1], [0.0]]),
        np.concatenate([[0.0, 0.0], 1 / h[1:]]),
    ]
    # D = spdiags(diags, [-1, 0, 1], n, n)
    D = spdiags(diags, [0, 1, 2], n - 2, n)

    # mass matrix
    diags = [h[1:] / 6, (h[1:] + h[:-1]) / 3, h[:-1] / 6]
    M = spdiags(diags, [-1, 0, 1], n - 2, n - 2)

    # compute mu from
    # (I + lmbda * D.T M^{-1} D) mu = y
    # solve directly for now
    D = D.toarray()
    M = M.toarray()
    I = np.eye(n, n)
    mu = np.linalg.solve(I + lmbda * (D.T @ np.linalg.inv(M) @ D), y)

    print(mu)

    return mu
