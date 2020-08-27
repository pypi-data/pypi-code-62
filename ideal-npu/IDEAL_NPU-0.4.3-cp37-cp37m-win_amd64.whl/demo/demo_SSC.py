import numpy as np
import IDEAL_NPU.funs as Ifuns
from IDEAL_NPU.cluster import SSC

data_name = "USPS"
X, y_true, N, dim, c_true = Ifuns.load_mat("D:/DATA/" + data_name)
print(data_name, N, dim, c_true)

obj = SSC(X=X, c_true=c_true)
Y = obj.clu(km_rep=10, way="NJW")
# print(obj.time)
# print(obj.ref)

acc = np.array([Ifuns.accuracy(y_true, y) for y in Y])
print(acc)
print(np.mean(acc))


# paper: USPS, ACC, 67.52 %
