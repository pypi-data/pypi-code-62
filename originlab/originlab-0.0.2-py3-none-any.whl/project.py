import PyOrigin
from .worksheet import WSheet
from .matrix import MSheet

def __new_book(type, lname, template, keep_sn, hidden):
	if len(template) == 0:
	  template = 'Origin'
	visible = PyOrigin.CREATE_HIDDEN if hidden else PyOrigin.CREATE_VISIBLE
	sname = '' if keep_sn else lname
	book = PyOrigin.CreatePage(type, sname, template, visible)
	if len(lname) > 0:
		sname = book.GetName()
		if len(lname) > len(sname):
			book.SetLongName(lname)
	return book

def new_wbook(lname='', template='', keep_sn = False, hidden=False):
	"""
		Create a new workbook
	Parameters:
		lname(str): Long Name of the book
		template(str): Template name, if path not specified, assumed to be in UFF or EXE
		keep_sn(bool): Rename the book using lname. False will keep default book short name
		hidden(bool): True will make created book as hidden
	Return:
		a new WorksheetPage object
	"""
	return __new_book(PyOrigin.PGTYPE_WKS, lname, template, keep_sn, hidden)

def new_mbook(lname='', template='', keep_sn = False, hidden=False):
	"""
		Create a new matrix book
	Parameters:
		lname(str): Long Name of the book
		template(str): Template name, if path not specified, assumed to be in UFF or EXE
		keep_sn(bool): Rename the book using lname. False will keep default book short name
		hidden(bool): True will make created book as hidden
	Return:
		a new MatrixPage object
	"""
	return __new_book(PyOrigin.PGTYPE_MATRIX, lname, template, keep_sn, hidden)
	
def __new_sheet(type, lname, template, hidden):
	book = __new_book(type, lname, template, True, hidden)
	return book.Layers(0)
	
def new_msheet(lname='', template='', hidden=False):
	"""
	Create a new MBook and return the first MSheet
	
	Parameters:
		lname(str): Long Name of the book
		template(str): Template name, if path not specified, assumed to be in UFF or EXE
		hidden(bool): True will make created book as hidden
	Return:
		a new MSheet object
	"""
	return MSheet(__new_sheet(PyOrigin.PGTYPE_MATRIX, lname, template, hidden))
	

def new_wsheet(lname='', template='', hidden=False):
	"""
		same as new_wbook but return the first worksheet
	
	Parameters:
		lname(str): Long Name of the book
		template(str): Template name, if path not specified, assumed to be in UFF or EXE
		hidden(bool): True will make created book as hidden
	Return:
		a new Worksheet object
	"""
	return WSheet(__new_sheet(PyOrigin.PGTYPE_WKS, lname, template, hidden))
