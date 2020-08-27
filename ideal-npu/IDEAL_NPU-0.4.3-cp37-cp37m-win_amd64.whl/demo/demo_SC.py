import numpy as np
from sklearn import metrics
import IDEAL_NPU.funs as Ifuns
from IDEAL_NPU.cluster import SC

data_name = "colon"
X, y_true, N, dim, c_true = Ifuns.load_mat("D:/DATA/" + data_name)

print(data_name, N, dim, c_true)

obj = SC(X, c_true)

knn_list = [10, 20, 30, 40, 50]
acc = np.zeros(len(knn_list))
for i, knn in enumerate(knn_list):
    Y = obj.clu(graph_knn=knn, km_rep=10, km_init="k-means++")
    acc[i] = np.mean([Ifuns.accuracy(y_true, y) for y in Y])

print(acc)
print(np.mean(acc))

# paper: USPS, ACC, 67.52 %
