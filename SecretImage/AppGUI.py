from ClientServerFunctions import *
import socket

import tkinter as tk
window=tk.Tk()
role=tk.StringVar()
role.set("0")

def doNone():
    print("hello world")


window.title("Secret Messenger")
window.configure(background='black')
window.geometry('{}x{}'.format(500,500))

menuBar=tk.Menu(window)

roleMenu= tk.Menu(menuBar, tearoff=0)

roleMenu.add_command(label="Client",command= lambda: role.set('1'))
roleMenu.add_command(label="Server", command=lambda: role.set('2'))
menuBar.add_cascade(label="Select Role", menu=roleMenu)


lbl1=tk.Label(window,text="Image Messenger 1.0", bg="black",fg="red")
lbl1.pack()

ip=tk.StringVar(window, socket.gethostbyname(socket.gethostname()))
print(ip.get())
ipLbl=tk.Label(window)
if role.get()=='2':
    ipLbl = tk.Label(window, textvariable=ip)
    ipLbl.pack()
else:
    ipLbl.pack_forget()




window.config(menu=menuBar)
window.update_idletasks()
window.mainloop()

