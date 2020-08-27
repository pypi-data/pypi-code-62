#!python
from tkinter import *
import os
import time

def future_editor():
	fg="white"
	bg="black"
	font="courier"

	def run_code():
		code_given = str(code.get("1.0",'end-1c'))
		create_file =  open("futureeditor.py","w+")
		create_file.write(code_given)
		create_file.close()
		os.system("python "+"futureeditor.py")

	window = Tk()
	window.resizable(False, False) # not resizable in both directions
	window.title("Future-editor")
	code = Text(window,bg=bg,fg=fg,insertbackground=fg)
	code.pack()
	run = Button(window,bg=fg,fg=bg,command=run_code,font=font,text="Run")
	run.pack(fill=BOTH)

	window.mainloop()

if __name__=='__main__':
	future_editor()