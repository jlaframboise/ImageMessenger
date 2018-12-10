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

    def cleanChoiceClient():
        lbl1.grid_forget()
        s.grid_forget()
        c.grid_forget()
        clientGUI()

    lbl1=tk.Label(window,text="Select your role: ")
    lbl1.grid(row=1,column=2)
    s=tk.Button(window,text="Server",command=cleanChoiceServer)
    s.grid(row=2,column=1)
    c=tk.Button(window,text="Client",command=cleanChoiceClient)
    c.grid(row=2,column=3)


def serverGUI():
    window.title("Image Messenger Server")
    var=tk.StringVar(window,"8888")
    status=tk.StringVar("status")

    lbl0=tk.Label(window,text="ImageMessenger.Server.1.0")
    lbl0.grid(row=0,column=1)
    lbl1=tk.Label(text="Port to use: ")
    lbl1.grid(row=2, column=0)

    e1=tk.Entry(window,textvariable=var)
    e1.grid(row=2,column=1)

    lbl2=tk.Label(window,text="Your ip is: xxxxxxxxxx")
    lbl2.grid(row=1,column=1)
    bListen=tk.Button(window,text="Start Listening")
    bListen.grid(row=3,column=1)

    lbl4=tk.Label(window,textvariable=status)
    lbl4.grid(row=4,column=6)


    HOST = ""
    # Arbitrary port not used by the system
    PORT=var.get()

    socketNum = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates the socket
    print('Socket created')

    socketNum.bind((HOST, PORT))  # Binds the socket to the host computer and portprint ('Socket bind complete')
    print("Server ip is " + str(socket.gethostbyname(socket.gethostname())) + " and port is " + str(PORT))

    socketNum.listen(1)  # Waits or "listens" for a client computer to request a connection
    #Change a status bar instead
    status.set("Server is listening")
    print('Server is now listening')

    conn, address = socketNum.accept()  # Accepts a connection from the client
    # This function stores the data in TWO different variables
    status.set('Connected with ' + address[0] + ':' + str(address[1]))
    print('Connected with ' + address[0] + ':' + str(address[1]))  # Displays client data

    # testing change sync

    while True:
        recvImage = conn.recv(2 * 4096)  # Receives data from client when it is sent

        # writes incoming image to file
        recvFile = open("NewImage.png", 'wb')
        recvFile.write(recvImage)
        recvFile.close()

        # decodes the incoming picture data
        recvedMessage = returnNewDecodedString("TestImagePython.png", "NewImage.png")
        print("Client> " + recvedMessage)

        if recvImage == None:
            break

        # gets message to send
        message = input("Server (You)>> ")

        # makes encoded image with message
        makeNewEncodedImage("TestImagePython.png", message)

        # converts the image to the contents of a binary file, 'a bytes like object' to send
        imageToSend = open("NewImage.png", 'rb')
        imageToSend = imageToSend.read()

        conn.send(imageToSend)  # Sends data to the client. Note it must be coded to binary

    conn.close()  # Closes the connections
    socketNum.close()

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

    bConnect = tk.Button(window, text="Connect")
    bConnect.grid(row=3, column=2)
    clientFunc(ip.get(), port.get())

choiceGUI()











window.mainloop()