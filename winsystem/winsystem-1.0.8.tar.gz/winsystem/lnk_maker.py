import os,sys,pythoncom
from win32com.shell import shell,shellcon
def make_lnk(filename,lnkname):
    sc=pythoncom.CoCreateInstance(
        shell.CLSID_ShellLink,
        None,
        pythoncom.CLSCTX_INPROC_SERVER,
        shell.IID_IShellLink
        )
    sc.SetPath(filename)
    sc.SetDescription(os.path.basename(lnkname))
    sc.SetIconLocation(filename,0)
    na=sc.QueryInterface(pythoncom.IID_IPersistFile)
    na.Save(lnkname,0)
