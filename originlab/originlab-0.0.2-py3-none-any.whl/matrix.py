import PyOrigin
import numpy as np

class MSheet:
	"""
	This class represent an Origin Matrix Sheet, it holds an instance of a PyOrigin MatrixSheet
	"""
	def __init__(self, ms):
		"""
		constructor from a MatrixSheet
		"""
		self.ms = ms

	def from_np(self, arr):
		"""
		Set a matrix sheet from a numpy array. Existing data and MatrixObjects will be deleted.
		
		Parameters:
			arr(numpy array): 2D to a single MatrixObject, and 3D for multiple MatrixObjects(rows,cols, N)
		"""
		if arr.ndim < 2:
			raise ValueError('1D array not supported')
		if arr.ndim == 2:
			row,col = arr.shape
			self.ms.SetShape(row,col)
			mat = self.ms.MatrixObjects(0)
			ret = mat.SetData(arr)
			if ret == 0:
				print('matrix set data error')
			return
		if arr.ndim != 3:
			raise ValueError('array greater then 3D not supported')
		rows, cols, depth = arr.shape
		self.ms.SetNumMats(depth)
		self.ms.SetShape(rows, cols)
		for i in range(depth):
			mo = self.ms[i]
			tmp = arr[:,:,i]
			mo.SetData(tmp)

	def to_np2d(self, index=0):
		"""
		Transfer data from a single MatrixObject to a numpy 2D array
		
		Parameters:
			index(int): MatrixObject index in the MatrixLayer
		"""
		return self.ms.MatrixObjects(index).GetData()

	def to_np3d(self):
		"""
		Transfer data in the MatrixSheet to a numpy 3D array
		
		Return:
			a 3D array with each MatrixObject stacked as the depth
		"""
		m2d = []
		for mo in self.ms.MatrixObjects:
			m2d.append(mo.GetData())

		return np.dstack(m2d)
		
	def show_image(self, show = True):
		"""
		Show as images or show as numbers
		"""
		mbook = self.ms.GetParent()
		print(mbook)
		mbook.SetNumProp("Image", show)

	def __show_contrll(self, show, slider):
		mbook = self.ms.GetParent()
		if not show:
			mbook.SetNumProp("Selector", 0)
		else:
			mbook.SetNumProp("Selector", 1)
			mbook.SetNumProp("Slider", slider)

	def show_thumbnails(self, show = True):
		"""
		Show thumbnail images for each MatrixObject
		"""
		self.__show_contrll(show, 0)
		
	
	def show_slider(self, show = True):
		"""
		Show a slider on top of the MatrixObjects
		"""
		self.__show_contrll(show, 1)
		
