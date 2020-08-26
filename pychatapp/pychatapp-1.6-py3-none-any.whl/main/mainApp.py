import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import os
#import mouse
import threading
import time
import requests
from plyer import notification
import sys

if not os.path.exists("database"):
    os.mkdir("database")

signed = True
signincond = False
condition = True
prevcon = ""
stringvar = ""
alldata=""
loginthread = ""
internet = "Hello there, there's no comment, if it was difficult to made, it should be difficult to understand"
lst = os.listdir("database")
##try:
##    lst.remove("data")
##except:
##    pass
##
##try:
##   uname = open("database/data").read()
##except:
##    signed = False
##    def create_account():
##        global signed, uname
##        newname = entryf.get().lower()
##        if signincond:
##            requests.get(f"http://rajma.pythonanywhere.com/register?username={newname}")
##            file = open("database/data","w")
##            file.write(entryf.get().lower())
##            loginthread.daemon
##            file.close()
##            signed = True
##            loginwin.destroy()
##            uname = open("database/data").read()
##    
##    def loginvar(text,color):
##        stringvar.set(text)
##        lab2 = tk.Label(loginwin,textvariable=stringvar,fg=color)
##        lab2.place(y=27)
##
##    def keepextracting():
##        global internet
##        while True:
##            try:
##                #print("Trying")
##                alldata = requests.get("http://rajma.pythonanywhere.com/retreve?uname=database&method=r",timeout=5).text
##                #print("Extracted")
##                alldata = alldata.split("\n")
##                if not internet:
##                    loginvar(f"Hello, select a unique username for yourself.","green")
##                internet = True
##            except:
##                loginvar("NO INTERNET!!!","red")
##                internet = False
##
##    def check_uname(event):
##        global signincond, loginthread
##        newusername = entryf.get()
##        if not internet:
##            loginvar("NO INTERNET!!!","red")
##            signincond = False
##
##        elif newusername == "":
##            loginvar(f"Hello, select a unique username for yourself.","green")
##            signincond = False
##
##        elif len(newusername) < 5:
##            loginvar("Username must have more than four characters.","orange")
##            signincond = False
##
##        elif len(newusername)> 20:
##            loginvar("Too long username","orange")
##            signincond = False
##
##        elif newusername in alldata:
##            loginvar("USERNAME TAKEN!!!","red")
##            signincond = False
##
##        else:
##            loginvar("Username available!!!","green")
##            signincond = True
##
##        
##    loginwin = tk.Tk()
##    loginwin.geometry("270x100")
##    stringvar = tk.StringVar(loginwin)
##
##    lab1 = tk.Label(loginwin,text="Username : ")
##    lab1.place(x=0,y=0)
##    loginvar(f"Hello, select a unique username for yourself.","green")
##    entryf = tk.Entry(loginwin,width=30)
##    entryf.place(x=67,y=1)
##    loginwin.bind("<Key>",check_uname)
##    button = tk.Button(loginwin,text="+ CREATE ACCOUNT +",command=create_account)
##    button.place(x=70,y=55)
##    loginthread = threading.Thread(target=keepextracting)
##    loginthread.start()
##    try:
##        alldata = requests.get("http://rajma.pythonanywhere.com/retreve?uname=database&method=r",timeout=5).text
##        alldata = alldata.split("\n")
##        internet = True
##    except:
##        loginvar("NO INTERNET!!!","red")
##        internet = False
##    loginwin.mainloop()
##    if not signed:
##        sys.exit(0)
##
##win = tk.Tk()
##win.geometry("550x500")
##
##img = tk.PhotoImage("send.GIF")
##
##variable = tk.StringVar(win)
##variable.set("SELECT CONTACT...")
##infovar = tk.StringVar(win)


def update_checkbox():
    cbox = ttk.Combobox(win, textvariable=variable, value = lst,state="readonly")
    cbox.place(x=70,y=10)
    chatselected = cbox.get()
    cbox.bind("<<ComboboxSelected>>", setchat)
    cbox.bind("<Enter>",lambda callback: call(text="Select user from available contact list...",event=callback))
    cbox.bind("<Leave>",clear)

def extractdatabase():
   global internet
   try:
      global alldata
      alldata = requests.get("http://rajma.pythonanywhere.com/retreve?uname=database&method=r",timeout=5).text
      alldata = alldata.split("\n")
      #print(alldata)
      internet = True

   except:
      infovar.set("NO INTERNET!!!")
      internet = False

def receive():
   global internet
   newmsgcount = 0
   while True:
       
      #print("here")
      try:
         chats = requests.get("http://rajma.pythonanywhere.com/retreve?uname=%s&method=r"%uname,timeout=5).text
         #print("after here")
         if chats is not "":
            msgslst = chats.split("::")
            for cont in msgslst:
               try:
                  cont = cont.split(" : ")
                  msgfrom = cont[1]
                  msg = cont[0]
                  file = open("database/"+msgfrom,"a")
                  file.write(msgfrom+" : "+msg+"\n")
                  file.close()
                  if cbox.get() == msgfrom:
                      text.config(state="normal")
                      text.insert(tk.END,msg,"rec")
                      text.insert(tk.END,"\n\n")
                      text.config(state="disabled")
                      text.see(tk.END)
                      
                  else:
                     print("New messages")
                     newmsgcount += 1
                     if msgfrom not in lst:
                         lst.append(msgfrom)
                         update_checkbox()
                  requests.get("http://rajma.pythonanywhere.com/retreve?uname=%s&method=w&data="%uname)

               except:
                  pass
         if newmsgcount > 0:
            notification.notify("PyChat","You have %s new messages"%newmsgcount)
            newmsgcount = 0
      except Exception as e:
         print("No net",e)
         internet = False
         infovar.set("NO INTERNET!!!")
         pass

def setchat(eventObject = None,chat = None):
    text.config(state="normal")
    if not chat:
      chat = cbox.get()
    #print(chat)
    if chat != "SELECT CONTACT...":
        file = open("database/"+chat)
        data = file.read()
        data = data.split("\n")
        text.delete(0.0,tk.END)
        try:
            for line in data:
                newdata = line.split(" : ")
                #print(newdata)
                if newdata[0] == chat:
                    text.insert(tk.END,newdata[1],"rec")

                elif newdata[0] == uname:
                    text.insert(tk.END,newdata[1],"sen")

                elif newdata == [""]:
                    text.insert(tk.END,"-"*65,"newmsg")
                text.insert(tk.END,"\n\n")
            text.config(state="disabled")
            text.see(tk.END)
        except:
            pass

def send(event=None):
   global condition, prevcon, con, internet
   con = entry.get()
   person = cbox.get()
   #print(person)
   #print(con)
   if con != "" and person != "SELECT CONTACT..." and internet:
      file = open("database/"+person,"a")
      file.write(uname+" : "+con+"\n")
      file.close()
      url = ("http://rajma.pythonanywhere.com/retreve?uname=%s&method=a&data=%s : %s::"%(person,con,uname))
      #print(url)
      requests.get(url)
      entry.delete(0,tk.END)
    #  if prevcon != con:
      text.config(state="normal")
      text.insert(tk.END,con,"sen")
      text.insert(tk.END,"\n\n")
      text.config(state="disabled")
      text.see(tk.END)
      prevcon = con

   elif person == "SELECT CONTACT...":
      messagebox.showinfo("Info","You can't talk to nobody, select any user first or search user globally.")

   elif not internet:
      messagebox.showwarning("INTERNET ERROR","COMPUTE NOT CONNECTED TO INTERNET")



def searchUser():
   global stringvar, found, alldata
   found = False

   def addcontact():
      global found
      user = entryf.get()
      if found and user not in lst: 
         file = open("database/"+user,"w")
         file.close()
         setchat(chat=user)
         cbox.set(user)
         lst.append(user)
         update_checkbox()
         win2.destroy()

      elif user in lst:
         setchat(chat=user)
         cbox.set(user)
         win2.destroy()

      else:
         messagebox.showwarning("Error","Username not found in our database")
         
   
   def setvar(text,color):
      stringvar.set(text)
      lab2 = tk.Label(win2,textvariable=stringvar,fg=color)
      lab2.place(y=22)

      
##      lab2 = tk.Label(win2,textvariable=stringvar)
##      lab2.place(y=20)
   def extractdatabase():
      global alldata
      alldata = requests.get("http://rajma.pythonanywhere.com/retreve?uname=database&method=r").text
      alldata = alldata.split("\n")
      #print(alldata)

   def user_exists(eventObject = None):
      global alldata, found
      thread = threading.Thread(target=extractdatabase)
      thread.start()
      #print("here")
      username = entryf.get()
      if username != "":
         setvar(f"Searching {username} in database...","blue")
         #print(username)
         if username in alldata:
            setvar(f"{username} found in database","green")
            found = True

         else:
            setvar(f"{username} not found in database","red")
            found = False
      else:
         setvar(f"Hi {uname.title()}, search users globally","green")

   try:
      extractdatabase()

      win2 = tk.Tk()
      win2.geometry("195x75")
      stringvar = tk.StringVar(win2)

      lab1 = tk.Label(win2,text="Username : ")
      lab1.place(x=0,y=0)
      setvar(f"Hi {uname.title()}, search users globally","green")
      entryf = tk.Entry(win2)
      entryf.place(x=67,y=1)
      win2.bind("<Key>",user_exists)
      button = tk.Button(win2,text="STRAT CHATTING",command=addcontact)
      button.place(x=45,y=45)

   except:
      messagebox.showwarning("Error","NO INTERNET")

def call(text,event = None):
   infovar.set(text)
   threading.Thread(target=extractdatabase).start()
   

def clear(event):
   threading.Thread(target=extractdatabase).start()
   infovar.set(f"Hello {uname.title()}!")

def help_user():
    messagebox.showinfo("PyChat",f"""Hello {uname.title()}, Thank you for installing PyChatApp.
To use this app, simply select contact you want
to chat with from the dropdown menu in the top right corner
and select the contact you want to chat with.
A blue line will appear in the chatbox, this is a "Here you left" sign.

If there's no user in the dropdown list, click on "Search user" and
search new users by their username, similar to Telegram.
Just like we need phone number to call someone, here we need their username.

Purpose of PyChatApp is to bring python community together
and connect with various Pythonistas around the world.

To Do:
1. In next update, we will try to add feature to send images.""")
   
try:
    lst.remove("data")
except:
    pass

try:
   uname = open("database/data").read()
except:
    signed = False
    def create_account():
        global signed, uname
        newname = entryf.get().lower()
        if signincond:
            requests.get(f"http://rajma.pythonanywhere.com/register?username={newname}")
            file = open("database/data","w")
            file.write(entryf.get().lower())
            loginthread.daemon
            file.close()
            signed = True
            loginwin.destroy()
            uname = open("database/data").read()
    
    def loginvar(text,color):
        stringvar.set(text)
        lab2 = tk.Label(loginwin,textvariable=stringvar,fg=color)
        lab2.place(y=27)

    def keepextracting():
        global internet
        while True:
            try:
                #print("Trying")
                alldata = requests.get("http://rajma.pythonanywhere.com/retreve?uname=database&method=r",timeout=5).text
                #print("Extracted")
                alldata = alldata.split("\n")
                if not internet:
                    loginvar(f"Hello, select a unique username for yourself.","green")
                internet = True
            except:
                loginvar("NO INTERNET!!!","red")
                internet = False

    def check_uname(event):
        global signincond, loginthread
        newusername = entryf.get()
        if not internet:
            loginvar("NO INTERNET!!!","red")
            signincond = False

        elif newusername == "":
            loginvar(f"Hello, select a unique username for yourself.","green")
            signincond = False

        elif len(newusername) < 5:
            loginvar("Username must have more than four characters.","orange")
            signincond = False

        elif len(newusername)> 20:
            loginvar("Too long username","orange")
            signincond = False

        elif newusername in alldata:
            loginvar("USERNAME TAKEN!!!","red")
            signincond = False

        else:
            loginvar("Username available!!!","green")
            signincond = True

        
    loginwin = tk.Tk()
    loginwin.geometry("270x100")
    stringvar = tk.StringVar(loginwin)

    lab1 = tk.Label(loginwin,text="Username : ")
    lab1.place(x=0,y=0)
    loginvar(f"Hello, select a unique username for yourself.","green")
    entryf = tk.Entry(loginwin,width=30)
    entryf.place(x=67,y=1)
    loginwin.bind("<Key>",check_uname)
    button = tk.Button(loginwin,text="+ CREATE ACCOUNT +",command=create_account)
    button.place(x=70,y=55)
    loginthread = threading.Thread(target=keepextracting)
    loginthread.start()
    try:
        alldata = requests.get("http://rajma.pythonanywhere.com/retreve?uname=database&method=r",timeout=5).text
        alldata = alldata.split("\n")
        internet = True
    except:
        loginvar("NO INTERNET!!!","red")
        internet = False
    loginwin.mainloop()
    if not signed:
        sys.exit(0)

win = tk.Tk()
win.geometry("550x500")

img = tk.PhotoImage("send.GIF")

variable = tk.StringVar(win)
variable.set("SELECT CONTACT...")
infovar = tk.StringVar(win)

sb = tk.Scrollbar(win)
sb.pack(side = tk.RIGHT, fill = tk.Y)

  
#mylist = tk.Listbox(win, yscrollcommand = sb.set )  
  
##for line in range(30):  
##    mylist.insert(END, "Number sdkcg j" + str(line))

tk.Label(win,text="Talking to :").place(x=3,y=10)
  
text = tk.Text(win, wrap=tk.WORD, yscrollcommand=sb.set,height = 25, width = 65)
text.tag_config('rec', background="yellow", foreground="black")
text.tag_config('sen', background="light green", foreground="black")
text.tag_config('newmsg', background="cyan", foreground="black")
text.place(x=5,y=35)
text.config(state="disabled")
sb.config(command=text.yview)

entry = tk.Entry(win,width=30,font=('Verdana',17))
entry.place(x=5,y=450)
entry.bind("<Enter>",lambda callback: call(text="Type message...",event=callback))
entry.bind("<Leave>",clear)

button1 = tk.Button(win,text="SEND",command=send,width=6,font=('Verdana',11))
button1.place(x=465,y=449)
win.bind("<Return>",send)
button1.bind("<Enter>",lambda callback: call(text="Send message...",event=callback))
button1.bind("<Leave>",clear)

cbox = ttk.Combobox(win, textvariable=variable, value = lst,state="readonly")
cbox.place(x=70,y=10)
chatselected = cbox.get()
cbox.bind("<<ComboboxSelected>>", setchat)
cbox.bind("<Enter>",lambda callback: call(text="Select user from available contact list...",event=callback))
cbox.bind("<Leave>",clear)

button2 = tk.Button(win,text="Search User",command=searchUser)
button2.place(x=457,y=5)
button2.bind("<Enter>",lambda callback: call(text="Search user from our database and initiate new conversation...",event=callback))
button2.bind("<Leave>",clear)

button3 = tk.Button(win,text="HELP",font=('Verdana',5),command=help_user)
button3.place(x=505,y=483)
button3.bind("<Enter>",lambda callback: call(text="Need help? Click to read user manual and about this application.",event=callback))
button3.bind("<Leave>",clear)


infovar.set(f"Hello {uname.title()}!")

infolabel = tk.Label(win,textvariable=infovar)
infolabel.place(x=1,y=482)
threading.Thread(target=receive).start()

tk.mainloop()
