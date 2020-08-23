__all__ = ['lib']

__version__ = '0.2.5'

import numpy as np

from mkkm_mr.lib import _check_dims, combine_kernels, kernel_kmeans_iter, calc_objective, update_kernel_weights, \
    normalize_unit_row

EPSILON = 1e-6


def mkkm_mr(K, M, cluster_count, lambda_):  # myregmultikernelclustering
    """
    Clusters given kernels using kernel kmeans
    :param K: kernel matrices of kxnxn
    :param M:
    :param cluster_count:
    :param lambda_:
    :return:
    """
    _check_dims(K, can_2d=False)
    # initialize gamma as equals
    gamma = np.ones(K.shape[0])  # kernel weights
    # noinspection PyTypeChecker
    obj: np.ndarray = None
    # keep as long as this is not the first iteration and there is not a big different finish it
    # PS: we can add an iteration limit here
    while True:
        # normalize gamma with l1
        gamma_sum = np.sum(gamma)
        if gamma_sum > 0:
            gamma = gamma / gamma_sum
        # take weighted kernel average
        K_wavg = combine_kernels(K, gamma)
        H = kernel_kmeans_iter(K_wavg, cluster_count)

        obj_prev = obj
        obj = calc_objective(H, K, M, gamma, lambda_)

        gamma = update_kernel_weights(H, K, M, lambda_)

        if obj_prev is not None and np.abs((obj_prev - obj) / obj_prev) < EPSILON:
            break

    H_normalized = normalize_unit_row(H)
    return H_normalized, gamma, obj
