import os
import random
import numpy as np
import scipy.io as sio
import pandas as pd
from scipy import stats

from sklearn import metrics
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import adjusted_rand_score as ari
from sklearn.metrics import adjusted_mutual_info_score as ami_ori
from sklearn.metrics import normalized_mutual_info_score as nmi_ori

from sklearn.metrics.pairwise import euclidean_distances as EuDist2
import time
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans


def get_anchor(X, m, way="random"):
    if way == "kmeans":
        A = KMeans(m, init='random').fit(X).cluster_centers_
    elif way == "kmeans2":
        A = KMeans(m, init='random').fit(X).cluster_centers_
        D = EuDist2(A, X)
        ind = np.argmin(D, axis=1)
        A = X[ind, :]
    elif way == "k-means++":
        A = KMeans(m, init='k-means++').fit(X).cluster_centers_
    elif way == "k-means++2":
        A = KMeans(m, init='k-means++').fit(X).cluster_centers_
        D = EuDist2(A, X)
        A = np.argmin(D, axis=1)

    elif way == "random":
        ids = random.sample(range(X.shape[0]), m)
        A = X[ids, :]
    return A


def precision(y_true, y_pred):
    assert (len(y_pred) == len(y_true))
    N = len(y_pred)
    y_df = pd.DataFrame(data=y_pred, columns=["label"])
    ind_L = y_df.groupby("label").indices
    ni_L = [stats.mode(y_true[ind]).count[0] for yi, ind in ind_L.items()]
    return np.sum(ni_L) / N


def recall(y_true, y_pred):
    re = precision(y_true=y_pred, y_pred=y_true)
    return re


def accuracy(y_true, y_pred):
    y_pred = bestmap(y_true, y_pred)
    acc = metrics.accuracy_score(y_true, y_pred)
    return acc


def ami(y_true, y_pred, average_method="max"):
    ret = ami_ori(labels_true=y_true, labels_pred=y_pred, average_method=average_method)
    return ret


def nmi(y_true, y_pred, average_method="max"):
    ret = nmi_ori(labels_true=y_true, labels_pred=y_pred, average_method=average_method)
    return ret


def load_Agg():
    this_directory = os.path.dirname(__file__)
    data_path = os.path.join(this_directory, "dataset/")
    name_full = os.path.join(data_path + "Agg.mat")
    X, y_true, N, dim, c_true = load_mat(name_full)
    return X, y_true, N, dim, c_true


def load_USPS():
    this_directory = os.path.dirname(__file__)
    data_path = os.path.join(this_directory, "dataset/")
    name_full = os.path.join(data_path + "USPS.mat")
    X, y_true, N, dim, c_true = load_mat(name_full)
    return X, y_true, N, dim, c_true


def load_mat(path):
    data = sio.loadmat(path)
    X = data["X"]
    y_true = data["Y"].astype(np.int32).reshape(-1)
    N, dim, c_true = X.shape[0], X.shape[1], len(np.unique(y_true))
    return X, y_true, N, dim, c_true


def save_mat(name_full, xy):
    sio.savemat(name_full, xy)


def matrix_index_take(X, ind_M):
    assert np.all(ind_M >= 0)

    n, k = ind_M.shape
    row = np.repeat(np.array(range(n), dtype=np.int32), k)
    col = ind_M.reshape(-1)
    ret = X[row, col].reshape((n, k))
    return ret


def matrix_index_assign(X, ind_M, Val):
    n, k = ind_M.shape
    row = np.repeat(np.array(range(n), dtype=np.int32), k)
    col = ind_M.reshape(-1)
    if isinstance(Val, (float, int)):
        X[row, col] = Val
    else:
        X[row, col] = Val.reshape(-1)


def kng(X, knn, way="gaussian", t="mean", Anchor=0):
    """
    :param X: data matrix of n by d
    :param knn: the number of nearest neighbors
    :param way: one of ["gaussian", "t_free"]
        "t_free" denote the method proposed in :
            "The constrained laplacian rank algorithm for graph-based clustering"
        "gaussian" denote the heat kernel
    :param t: only needed by gaussian, the bandwidth parameter
    :param Anchor: Anchor set, m by d
    :return: A, an sparse matrix (graph) of n by n if Anchor = 0 (default)
    """
    N, dim = X.shape
    if isinstance(Anchor, int):
        # n x n graph
        D = EuDist2(X, X, squared=True)
        ind_M = np.argsort(D, axis=1)
        if way == "gaussian":
            Val = matrix_index_take(D, ind_M[:, 1:(knn+1)])
            if t == "mean":
                t = np.mean(Val)
            elif t == "median":
                t = np.median(Val)
            Val = np.exp(-Val / t)
        elif way == "t_free":
            Val = matrix_index_take(D, ind_M[:, 1:(knn+2)])
            Val = Val[:, knn].reshape((-1, 1)) - Val[:, :knn]
            Val = Val / np.sum(Val, axis=1).reshape(-1, 1)
        A = np.zeros((N, N))
        matrix_index_assign(A, ind_M[:, 1:(knn+1)], Val)
        A = (A + A.T) / 2
    else:
        # n x m graph
        num_anchor = Anchor.shape[0]
        D = EuDist2(X, Anchor, squared=True)  # n x m
        ind_M = np.argsort(D, axis=1)
        if way == "gaussian":
            Val = matrix_index_take(D, ind_M[:, :knn])
            if t == "mean":
                t = np.mean(Val)
            elif t == "median":
                t = np.median(Val)
            Val = np.exp(-Val / t)
        elif way == "t_free":
            Val = matrix_index_take(D, ind_M[:, :(knn+1)])
            Val = Val[:, knn].reshape((-1, 1)) - Val[:, :knn]
            Val = Val / np.sum(Val, axis=1).reshape(-1, 1)
        A = np.zeros((N, num_anchor))
        matrix_index_assign(A, ind_M[:, :knn], Val)

    return A


def kmeans(X, c, rep, init="random", mini_batch=False):
    """
    km = random or k-means++
    """
    Y = np.zeros((rep, X.shape[0]))
    for i in range(rep):
        if mini_batch:
            Y[i, :] = MiniBatchKMeans(n_clusters=c, init=init, n_init=1).fit(X).predict(X)
        else:
            Y[i, :] = KMeans(c, n_init=1, init=init).fit(X).labels_
    return Y


def bestmap(L1, L2):
    """
    bestmap: permute labels of L2 to match L1 as good as possible
    """
    L1 = L1.astype(np.int64)
    L2 = L2.astype(np.int64)
    assert L1.size == L2.size

    Label1 = np.unique(L1)
    nClass1 = Label1.__len__()
    Label2 = np.unique(L2)
    nClass2 = Label2.__len__()

    nClass = max(nClass1, nClass2)
    G = np.zeros((nClass, nClass))
    for i in range(nClass1):
        for j in range(nClass2):
            G[i][j] = np.nonzero((L1 == Label1[i]) * (L2 == Label2[j]))[0].__len__()

    c = linear_sum_assignment(-G.T)[1]
    newL2 = np.zeros(L2.__len__())
    for i in range(nClass2):
        for j in np.nonzero(L2 == Label2[i])[0]:
            if len(Label1) > c[i]:
                newL2[j] = Label1[c[i]]
    return newL2


def normalize_fea(fea, row):
    '''
    if row == 1, normalize each row of fea to have unit norm;
    if row == 0, normalize each column of fea to have unit norm;
    '''

    if 'row' not in locals():
        row = 1

    if row == 1:
        feaNorm = np.maximum(1e-14, np.sum(fea ** 2, 1).reshape(-1, 1))
        fea = fea / np.sqrt(feaNorm)
    else:
        feaNorm = np.maximum(1e-14, np.sum(fea ** 2, 0))
        fea = fea / np.sqrt(feaNorm)

    return fea
