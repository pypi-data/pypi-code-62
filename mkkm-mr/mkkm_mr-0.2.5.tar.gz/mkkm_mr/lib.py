import warnings

import cvxopt
import numpy as np
import scipy.sparse.linalg
from numpy.linalg import multi_dot


def _check_dims(K, can_2d=True, can_3d=True):
    """
    Checks if dimensions are one of allowed sizes and if not throws an error
    :param K: parameter to check
    :param can_2d: whether or not K can be 2d
    :param can_3d: whether or not K can be 3d
    :return:
    """
    ndims = len(K.shape)
    errs = []
    if can_2d:
        if ndims == 2 and K.shape[0] == K.shape[1]:
            return ndims
        else:
            errs.append('a kernel matrix of size nxn')
    if can_3d:
        if ndims == 3 and K.shape[1] == K.shape[2]:
            return ndims
        else:
            errs.append('kernel matrices of size KxNxN')
    if len(errs) == 0:
        return ndims
    raise ValueError(f'Invalid matrix given: expected {" or ".join(errs)}')


def calM(K):  # calM
    _check_dims(K, can_2d=False)
    n_kernel = K.shape[0]
    HE0 = np.zeros((n_kernel, n_kernel))
    for p in range(n_kernel):
        for q in range(p, n_kernel):
            HE0[p, q] = np.trace(K[p].T @ K[q])
    return (HE0 + HE0.T) - np.diag(np.diag(HE0))


def kernel_centralize(K):  # kcenter
    """
    kcenter - center a kernel matrix

    Reference:
        Shawe-Taylor, Cristianini, 'Kernel Methods for Pattern Analysis',
        Cambridge University Press, 2004, http://www.kernel-methods.net

    Authors: K. Rieck, M. Kloft

    :param K: either a 3 dimensional ndarray of size kxnxn or Kernel Matrix (nxn) where k is number of kernels and n is
        kernel size
    :return: centered kernel matrix
    """
    ndims = _check_dims(K)
    n = K.shape[1]  # for both cases this is n

    if ndims == 3:
        return np.stack([kernel_centralize(Ki) for Ki in K])

    D = np.sum(K, axis=0, keepdims=True) / n
    E = np.sum(D) / n
    J = np.ones((n, 1)) @ D
    _K = K - J - J.T + E * np.ones((n, n))
    return 0.5 * (_K + _K.T) + 1e-12 * np.eye(n)


def kernel_normalize(K):  # knorm
    """
    knorm - normalize a kernel matrix

    Description:
        kn(x,y) = k(x,y) / sqrt(k(x,x) k(y,y))

     $Id: knorm.m,v 1.1 2005/05/30 12:07:21 neuro_cvs Exp $

     Copyright (C) 2005 Fraunhofer FIRST
     Author: Konrad Rieck (rieck@first.fhg.de)
      Modified by Marius Kloft

    :param K: kernel matrix (n x n)
    :return: normalized kernel matrix
    """
    ndims = _check_dims(K)
    if ndims == 3:
        return np.stack([kernel_normalize(Ki) for Ki in K])

    K_diag = np.diag(K).reshape((-1, 1))
    return K / np.sqrt(K_diag @ K_diag.T)


def combine_kernels(K, gamma):  # mycombFun
    """
    Combines kernels with weighted average
    :param K: kxnxn kernel matrices
    :param gamma: k length array or kx1 matrix
    :return:
    """
    _check_dims(K, can_2d=False)
    return sum(Ki * gi for Ki, gi in zip(K, gamma))


def kernel_kmeans_iter(K, cluster_count):  # mykernelkmeans
    """
    simple kernel k-means iteration doesn't include calculation for objective function so faster
    :param K: kxnxn kernel matrices
    :param cluster_count: cluster count
    :return:
    """
    K = (K + K.T) / 2
    _, H = scipy.sparse.linalg.eigs(K, k=cluster_count, which='LR')
    if np.sum(np.iscomplex(H)) > 0:
        warnings.warn('K-Means iteration produced complex numbers with imaginary part')
    return H.real


def kernel_kmeans_iter_with_obj(K, cluster_count):  # mykernelkmeans
    """
    Not in use left for reference, includes calculation for objective function
    simple kernel k-means iteration
    :param K: kxnxn kernel matrices
    :param cluster_count: cluster count
    :return:
    """
    K = (K + K.T) / 2
    _, H = scipy.sparse.linalg.eigs(K, k=cluster_count, which='LR')
    obj = np.trace(multi_dot([H.T, K, H])) - np.trace(K)
    if np.sum(np.iscomplex(H)) > 0:
        warnings.warn('K-Means iteration produced complex numbers with imaginary part')
    return H.real, obj


def calc_objective(T, K, H0, gamma0, lambda_):  # calObj
    """
    Calculates objective
    :param T:
    :param K:
    :param H0:
    :param gamma0:
    :param lambda_:
    :return:
    """
    _check_dims(K, can_2d=False)

    # multi_dot optimizes multiple kernel multiplications
    f = [np.trace(Ki) - np.trace(multi_dot([T.T, Ki, T])) for Ki in K]

    return 0.5 * multi_dot([gamma0.T, (lambda_ * H0 + 2 * np.diag(f)), gamma0])


def quadprog(H, f, L=None, k=None, Aeq=None, beq=None, lb=None, ub=None):
    """
    Reference:
    https://github.com/nolfwin/cvxopt_quadprog

    Input: Numpy arrays, the format follows MATLAB quadprog function: https://www.mathworks.com/help/optim/ug/quadprog.html
    Output: Numpy array of the solution

    :param H:
    :param f:
    :param L:
    :param k:
    :param Aeq:
    :param beq:
    :param lb:
    :param ub:
    :return:
    """
    _check_dims(H, can_3d=False)
    n_var = H.shape[1]

    if np.sum(np.iscomplex(H)) > 0:
        raise ValueError('H vector contains complex values')

    P = cvxopt.matrix(H.real, tc='d')
    q = cvxopt.matrix(f, tc='d')

    if L is not None or k is not None:
        assert (k is not None and L is not None)
        if lb is not None:
            L = np.vstack([L, -np.eye(n_var)])
            k = np.vstack([k, -lb])

        if ub is not None:
            L = np.vstack([L, np.eye(n_var)])
            k = np.vstack([k, ub])

        L = cvxopt.matrix(L, tc='d')
        k = cvxopt.matrix(k, tc='d')

    if Aeq is not None or beq is not None:
        assert (Aeq is not None and beq is not None)
        Aeq = cvxopt.matrix(Aeq, tc='d')
        beq = cvxopt.matrix(beq, tc='d')

    sol = cvxopt.solvers.qp(P, q, L, k, Aeq, beq)

    return np.array(sol['x'])


def update_kernel_weights(H, K, HE0, lambda_):  # updatekernelweightsV2
    _check_dims(K, can_2d=False)
    k, n = K.shape[:2]

    U0 = np.eye(n) - H @ H.T
    ZH = np.stack([np.trace(Ki @ U0) for Ki in K])

    H = lambda_ * HE0 + 2 * np.diag(ZH)
    f = np.zeros((k, 1))
    Aeq = np.ones((k, 1)).T
    beq = 1
    lb = np.zeros((k, 1))
    ub = np.ones((k, 1))

    gamma = quadprog(H, f, Aeq=Aeq, beq=beq, lb=lb, ub=ub)  # solve for given kernels
    gamma[gamma < 1e-6] = 0  # ignore small numbers
    gamma = gamma / np.sum(gamma)  # normalize
    return gamma


def normalize_unit_row(H):
    """
    Normalizes given matrix rows by converting rows to unit vectors
    :param H:
    :param k:
    :return:
    """
    _div = np.linalg.norm(H, axis=1, keepdims=True)
    _div[_div == 0] = 1
    return H / _div
