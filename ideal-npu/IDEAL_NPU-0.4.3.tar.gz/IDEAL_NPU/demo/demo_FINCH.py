import numpy as np
import IDEAL_NPU.funs as Ifuns
from IDEAL_NPU.cluster import FINCH

X, y_true, N, dim, c_true = Ifuns.load_Agg()
print("Agg", N, dim, c_true)

# FINCH (1)
Y, num_clu, req_y = FINCH(X, req_clust=c_true, distance='euclidean')  # or cosine

print(len(np.unique(req_y)))
acc = Ifuns.nmi(y_true, req_y, average_method="max")
print(acc)

# FINCH (2)
Y, num_clu, req_y = FINCH(X, distance='euclidean')  # or cosine

acc = [Ifuns.nmi(y_true, y) for y in Y]
print(acc)
