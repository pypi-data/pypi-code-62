import PyOrigin
#import numpy as np
from datetime import timedelta as tdlt
import pandas as pd


class WSheet:
	"""
	This class reprsent an Origin Worksheet, it holds an instance of a PyOrigin Worksheet
	"""
	def __init__(self, wks):
		"""
		constructor from a Worksheet
		"""
		self.wks = wks
		
	# Adds a maximum of needecols columns beginning with c1 to
	# Origin worksheet wks:
	def __check_add_cols(self, needecols, c1 = 0):
		if self.wks.Cols < needecols + c1:
			self.wks.Cols = c1 + needecols

	def	from_df(self, df, c1=0):
		"""
		sets a pandas DataFrame to an Origin worksheet
		
		Parameters:
			df(DataFrame): Input pandas DataFrame object
			c1(int): Starting Column Index
		"""
		if c1 < 0:	# caller's mistake
			return
		
		if df.empty:
			return

		ndfcols = len(df.columns)
		self.__check_add_cols(ndfcols, c1)
		col = c1
		for key, value in df.iteritems():
			colobj = self.wks[col]
			#print(value.dtype)
			if str(value.dtype) == 'category':
				dfseriestypechar = 'cat'		# our own "name" for convenience
			else:
				dfseriestypechar = df.dtypes[col - c1].char
			#print(dfseriestypechar)
			if dfseriestypechar == 'd':	# if floating:
				colobj.SetDataFormat(PyOrigin.DF_DOUBLE)
				listtoset = list(value)
			elif dfseriestypechar == 'q':	# if integer
				colobj.SetDataFormat(PyOrigin.DF_LONG)
				listtoset = list(value)
			elif dfseriestypechar == 'D':	# if complex:
				colobj.SetDataFormat(PyOrigin.DF_COMPLEX)
				listtoset = list(value)
			elif dfseriestypechar == 'M':	# if datetime64[ns]:
				colobj.SetDataFormat(PyOrigin.DF_DATE)
				listtoset = [vv.to_julian_date() for vv in value]
			elif dfseriestypechar == 'm':	# if 'timedelta':
				colobj.SetDataFormat(PyOrigin.DF_TIME)
				# See https://pandas.pydata.org/pandas-docs/stable/user_guide/timedeltas.html
				# under "Frequency conversion"
				# Here need to convert it to number of days as float64:
				#listtoset = [vv/np.timedelta64(1, 'D') for vv in value]
				# See https://docs.python.org/2/library/datetime.html
				# under 8.1.2. timedelta Objects
				# In Origin Time column contains numeric floating values which represent fractions of one day.
				listtoset = [vv/tdlt(days=1) for vv in value]
			elif dfseriestypechar == 'cat':	# if categorical
				colobj.SetDataFormat(PyOrigin.DF_TEXT)
				colobj.CategMapType = PyOrigin.CMTYPE_ORDINAL
				listtoset = list(value)
			else:
				colobj.SetDataFormat(PyOrigin.DF_TEXT_NUMERIC)
				listtoset = list(value)

			colobj.SetData(listtoset)
			colobj.LongName = key
			col += 1
			
	def	to_df(self, c1=0, numcols = -1):
		"""
		creates a pandas DataFrame from an Origin worksheet
		
		Parameters:
			c1(int): starting column
			numcols(int):	Total number of columns, -1 to the end
		Return:
			a pandas DataFrame object
		"""
		df = pd.DataFrame()
		if c1 < 0:	# caller's mistake
			return df
			
		if numcols < 0:
			totalcols = self.wks.Cols - c1
		else:
			totalcols = min(self.wks.Cols - c1, numcols)
			
		for col in range(c1, c1 + totalcols):
			colobj = self.wks[col]
			coldata = colobj.GetData()
			coldatatype = colobj.GetDataFormat()
			if coldatatype == PyOrigin.DF_DATE:
				# See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html
				listtimestamps = pd.to_datetime(coldata, unit='D', origin='julian')
				dfseries = pd.Series(listtimestamps, list(range(len(listtimestamps))))
			elif coldatatype == PyOrigin.DF_TIME:
				# See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_timedelta.html
				listtimedeltas = pd.to_timedelta(coldata, unit='d')
				dfseries = pd.Series(listtimedeltas, list(range(len(listtimedeltas))))
			elif colobj.CategMapType != PyOrigin.CMTYPE_NONE:
				dfseries = pd.Series(coldata, list(range(len(coldata))), dtype="category")
			else:
				dfseries = pd.Series(coldata, list(range(len(coldata))))
			loc = col - c1
			df.insert(loc, colobj.LongName, dfseries)
		
		return df
	