import numpy as np
from sklearn.metrics.pairwise import euclidean_distances as EuDist2

import IDEAL_NPU.funs as Funs
from IDEAL_NPU.cluster import AGCI


X, y_true, N, dim, c_true = Funs.load_Agg()

obj = AGCI(X, c_true)
Y = obj.clu(graph_knn=20, km_times=10)

print(Y.shape)

pre = np.array([Funs.precision(y_true=y_true, y_pred=y_pred) for y_pred in Y])
rec = np.array([Funs.recall(y_true=y_true, y_pred=y_pred) for y_pred in Y])
f1 = 2 * pre * rec / (pre + rec)

print("{}".format(pre))
print("{}".format(f1))

# not verified

