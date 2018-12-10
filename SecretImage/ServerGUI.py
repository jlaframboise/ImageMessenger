import tkinter as tk
import socket
serverWin=tk.Tk()

serverWin.title("Secret Messenger Server")
serverWin.configure(background='black')
serverWin.geometry('{}x{}'.format(500,500))

ip=tk.StringVar(serverWin,socket.gethostbyname(socket.gethostname()))

ipToDisplay=tk.StringVar(serverWin,"Your ip is: "+ip.get())
ipLbl=tk.Label(serverWin,textvariable=ipToDisplay)
ipLbl.pack()

port=tk.StringVar(serverWin,"default")

portToDisplay=tk.StringVar(serverWin, "Port to use:"+port.get())

portLbl=tk.Label(serverWin,textvariable=portToDisplay)
portLbl.pack()

portBox=tk.Entry(serverWin,textvariable=port)
portBox.pack()














serverWin.mainloop()