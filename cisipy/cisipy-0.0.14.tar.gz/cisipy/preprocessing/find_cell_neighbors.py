import numpy as np
from scipy.sparse import save_npz, load_npz, csr_matrix
from scipy.spatial import distance

CellMasks = load_npz('%s/%s/segmented/cell_masks.npz' % (args.mask_basepath,tissue))
FP_mask = glob.glob(os.path.join(args.mask_basepath,tissue,'segmented','DAPI.tiff'))
n = imageio.imread(FP_mask[0]).shape
CellCentroids = []
for cell in CellMasks:
	rows,cols = np.unravel_index(cell.indices,n)
	avg_r = np.average(rows)
	avg_c = np.average(cols)
	CellCentroids.append((avg_r,avg_c))

CellCentroids = np.array(CellCentroids)
CellDist = distance.squareform(distance.pdist(CellCentroids))
thresh = 80
CellNeighbors = csr_matrix((CellDist + np.eye(CellCentroids.shape[0])*1e9 < thresh))
