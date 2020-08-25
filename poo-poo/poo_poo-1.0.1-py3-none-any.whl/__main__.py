from random import*
from tkinter import*

window = Tk()
size = 500
c = Canvas(window, height=size, width=size, bg="brown")
c.pack()
window.title("poo poo poo poo evrywhere")
photo = PhotoImage(file = "poo.png")
window.iconphoto(False, photo)
while True:
    x0 = randint(0, size)
    y0 = randint(0, size)
    d = randint(0, size/5)
    c.create_oval(x0, y0, x0 + d, y0 + d, fill="yellow")
    window.update()
