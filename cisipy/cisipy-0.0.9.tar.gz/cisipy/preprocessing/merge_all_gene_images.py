import numpy as np
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import cm
import imageio

f = open('../../Training/Data/37genes.txt')
Genes = [line.strip() for line in f]
f.close()

GeneGroups = {'Excitatory': ['Slc17a7','Rorb','Paqr8','Deptor','Foxp2','Tle4','Rgs12','Stard8','Cux2','Sulf1'],
				'Inhibitory': ['Gad1','Vip','Parm1','Sst','Grin3a','Pvalb','Ndnf','Fgf13'],
				'Astrocytes': ['Gja1','F3','Prex2'],
				'Microglia': ['Ctss','Csf1r','Hmha1'],
				'Oligodendrocytes': ['Olig1','Vcan','Olig2'],
				'OPCs': ['Pdgfra','Mog'],
				'Endothelial': ['Flt1','Xdh','Id1'],
				'SMC': ['Vtn','Colec12'],
				'Other glia': ['Pdgfd','Id3','Ly86']}

colors = cm.get_cmap('gist_ncar',len(Genes)+8)
Colors = np.zeros([len(Genes),3])
i = 6
GeneColors = {}
for k,v in GeneGroups.items():
	for g in v:
		Colors[Genes.index(g)] = colors(i)[:3]
		_=plt.scatter(10,(i+1)*50,c=colors(i),marker=r"$ {} $".format(g),edgecolors='none',s=100)
		i += 1

plt.savefig('gene_colors.pdf')
plt.close()
Colors = np.array(Colors)

for t in range(1,9):
	tissue = 'tissue%d' % t
	im_shape = imageio.imread('%s/stitched/%s.tiff' % (tissue,Genes[0])).shape
	Merged = np.zeros([im_shape[0],im_shape[1],3])
	X = []
	for gene in Genes:
		im = imageio.imread('%s/stitched/%s.tiff' % (tissue,gene))
		X.append(im)
	max_gene = np.argmax(X,axis=0)
	X_max = np.array(X).reshape([len(Genes),-1])[max_gene.flatten(),np.arange(np.product(X[0].shape))]
	Merged = (Colors[max_gene.flatten()].T*X_max).T.reshape([im_shape[0],im_shape[1],3])
	max_val = np.iinfo('uint16').max
	threshold = np.percentile(Merged[Merged > 0],99)
	Merged_scaled = np.rint(Merged/threshold*max_val).astype('uint16')
	imageio.imsave('%s/stitched/all_genes.merged.tiff' % tissue, Merged_scaled)
	print(tissue)


