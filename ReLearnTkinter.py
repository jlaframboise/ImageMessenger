import tkinter as tk
from ClientServerFunctions import *

window=tk.Tk()
window.title("Image Messenger")
window.geometry("400x400")
window.configure(background="black")

def choiceGUI():
    def cleanChoiceServer():
        lbl1.grid_forget()
        s.grid_forget()
        c.grid_forget()
        serverGUI()
        #window.mainloop()

    def cleanChoiceClient():
        lbl1.grid_forget()
        s.grid_forget()
        c.grid_forget()
        clientGUI()
        #window.mainloop()

    lbl1=tk.Label(window,text="Select your role: ")
    lbl1.grid(row=1,column=2)
    s=tk.Button(window,text="Server",command=cleanChoiceServer)
    s.grid(row=2,column=1)
    c=tk.Button(window,text="Client",command=cleanChoiceClient)
    c.grid(row=2,column=3)


def serverGUI():
    window.title("Image Messenger Server")
    var=tk.StringVar(window,"8888")

    lbl0=tk.Label(window,text="ImageMessenger.Server.1.0")
    lbl0.grid(row=0,column=1)
    lbl1=tk.Label(text="Port to use: ")
    lbl1.grid(row=2, column=0)

    e1=tk.Entry(window,textvariable=var)
    e1.grid(row=2,column=1)

    lbl2=tk.Label(window,text="Your ip is: xxxxxxxxxx")
    lbl2.grid(row=1,column=1)
    bListen=tk.Button(window,text="Start Listening",command= lambda: serverFunc(int(var.get())))
    bListen.grid(row=3,column=1)


def clientGUI():
    window.title("Image Messenger Client")
    ip=tk.StringVar(window,"ip")
    port=tk.IntVar(window,8888)

    lbl0 = tk.Label(window, text="ImageMessenger.Client.1.0")
    lbl0.grid(row=0, column=2)

    lbl1=tk.Label(window,text="Server ip: ")
    lbl1.grid(row=1,column=1)

    e1=tk.Entry(window,textvariable=ip)
    e1.grid(row=1,column=2)

    lbl2=tk.Label(window,text="Port to use: ")
    lbl2.grid(row=2,column=1)

    e2=tk.Entry(window,textvariable=port)
    e2.grid(row=2,column=2)

    bConnect = tk.Button(window, text="Connect", command=lambda : clientFunc(ip.get(), port.get()))
    bConnect.grid(row=3, column=2)


choiceGUI()











window.mainloop()