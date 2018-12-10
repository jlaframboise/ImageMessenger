from ClientServerFunctions import *
import socket

import tkinter as tk

window=tk.Tk()

choice=input("Will you be  (1)client or (2)server?")

if choice == '1':

    ip=input("What is the server ip? ")
    port=input("What port will you use? ")
    args=(ip,port)
    if port=='':
        clientFunc(ip)
    else:
        clientFunc(ip,port)

elif choice =='2':
    port=input("What port will you use? ")
    if port=='':
        serverFunc()
    else:
        serverFunc(port)