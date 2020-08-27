from tkinter import *
from time import *
import ctypes
from _thread import start_new_thread
global root
class Toast():
    def Short_Toast(self,message,color="black"):
        root=Tk()
        root.overrideredirect(True)
        root.attributes("-alpha", 0.6)
        root["background"]=color
        wd=root.winfo_screenwidth()
        hd=root.winfo_screenheight()
        if len(str(message)) > 10:
            raise ValueError("Error Short_Toast should in 10 space")
        font=("arial",30,"normal")
        a=50
        b=len(message)*50+10
        c=(wd-b)/2
        d=(hd-a)/2
        root.withdraw()
        root.geometry("%dx%d+%d+%d"%(b,a,c,d))
        Label(root,text=message,font=font,bg="black",fg="white").pack()
        root.deiconify()
        root.attributes("-topmost",1)
        root.after(800,root.destroy)
        root.mainloop()
    def Long_Toast(self,message="message here!",title="ToastNotifier",duration=5,*iconpath):
        try:
            import win10toast
        except ImportError:
            raise ImportError("Error Long_Toast function needs module 'win10toast',please download from pypi.org and try again.")
        if iconpath:
            hwnd=win10toast.ToastNotifier().show_toast(title=title,msg=message,duration=duration,iconpath=iconpath)
        if not iconpath:
            hwnd=win10toast.ToastNotifier().show_toast(title=title,msg=message,duration=duration)
        
        
