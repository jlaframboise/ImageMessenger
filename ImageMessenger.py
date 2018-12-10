'''

ImageMessenger.py
Jacob Laframboise
June 16th, 2017
Fully functional, looking nice.

This program ia a graphical program to take user input, encrypt the text into a picture, save it and send it over 
a socket connection where it will be decrypted by the other computer by comparing it to the same base image.
The plaintext will then be displayed on the other user's GUI. 

There is a window to select image and role, then two different windows depending on role selected to set up connection,
then there is a final window in which they can communicate. 

***REQUIRED:
    Python 3
    Pillow (fork of PIL library) *only one not included with python 
    TkInter
    Socket
    **Files:
        An image called TestImagePython.png in your current directory. 

'''

import socket  # need to communicate over network
# Import tkinter as short form
import tkinter as tk

# need to modify and open other img formats
from PIL import Image, ImageTk


# Function to encode text in picture
def encodePic(origImage, string):
    global imgNew
    imgNew = origImage.copy()  # copy to new image
    pixelMapNew = imgNew.load()  # load pixel data

    # string="hello World"
    # initialize variables
    toEncodeList = []  # list to hold binary data
    xPos = 0  # hold current pixel position
    yPos = 0
    varience = 1  # how much to modify value by
    for i in string:  # for every letter in string to encode
        binNum = (bin(ord(i)))  # convert ot binary
        binNum = binNum[:1] + binNum[2:]  # remove silly intital zero
        if len(binNum) < 8:  # in case it is less than than 8 bits
            binNum = '0' + str(binNum)  # add zero
        toEncodeList.append(binNum)  # add to list of bytes
    for x in toEncodeList:  # for every byte
        for y in x:  # for each bit in the byte
            if y == '1':  # if it is a 1, increase red val by 1
                if pixelMapNew[xPos, yPos][0] == 255:  # if it is max red already
                    varience = -2
                # actually change the rgb values
                # note a line is continued on next line so it isn't too long
                # redd value gets varience added, rest are same
                pixelMapNew[xPos, yPos] = (
                    pixelMapNew[xPos, yPos][0] + varience, pixelMapNew[xPos, yPos][1], pixelMapNew[xPos, yPos][2])
                varience = 1  # reset variance
            elif y == '0':
                if pixelMapNew[xPos, yPos][0] == 0:  # if it is min red already
                    varience = -2
                # actually write data
                # note a line is continued on next line so it isn't too long
                # redd value gets varience added, rest are same
                pixelMapNew[xPos, yPos] = (
                    pixelMapNew[xPos, yPos][0] - varience, pixelMapNew[xPos, yPos][1], pixelMapNew[xPos, yPos][2])
                varience = 1
            # move selected pixel along
            if xPos < imgNew.size[0] - 1:
                xPos += 1
            # if at end of line, move down a row
            elif xPos == imgNew.size[0] - 1:
                xPos = 0
                yPos += 1


# function to decode information from image
def decodePic(img, newImg):
    orgPixelMap = img.load()  # load image
    pixelMap = newImg.load()  # load new pixel data
    varience = 1
    # initialize
    currentByte = []  # to hold each group of 8 pixel changes
    decodedList = []

    for x in range(0, img.size[1]):  # for every row
        for i in range(0, img.size[0]):  # for every column
            # load original and new pixel data to variables moddedpixel and pixel
            moddedPixel = pixelMap[i, x]
            pixel = orgPixelMap[i, x]
            # if statement to check if pixel has been increased or decreased by variance
            if moddedPixel[0] == pixel[0] + varience or moddedPixel[0] == pixel[0] + (
                        -2 * varience):  # if r val increased
                currentByte.append(1)  # add a 1
            elif moddedPixel[0] == pixel[0] - varience or moddedPixel[0] == pixel[0] - (
                        -2 * varience):  # if r val decreased
                currentByte.append(0)  # add a 0
            if len(currentByte) == 8:  # if we have filled a byte
                valSum = 0
                # for each bit in the byte
                for a in range(0, 8):
                    if currentByte[a] == 1:  # convert binary to ascii values
                        valSum += 2 ** (7 - a)  # look through current byte and add respective power of two to ascii val
                decodedList.append(valSum)  # append ascii vals
                currentByte = []
    decodedString = ''.join(chr(i) for i in decodedList)  # convert from ascii to plaintext and join as string

    return decodedString  # return result


# Function to create a new image file(or modify existing) to contain the information
def makeNewEncodedImage(origImagePath, string):
    origImage = Image.open(origImagePath)  # load original image
    encodePic(origImage, string)  # make changes to encode data
    origImage.close()
    imgNew.save('NewImage.png')  # save image
    imgNew.close()


# this function takes the location or name of the new file and the original file and opens them,
# decodes the new to a string, closes the images, and returns the string
def returnNewDecodedString(origImagePath, newImagePath="NewImage.png"):
    origImage = Image.open(origImagePath)  # load original image
    newImage = Image.open(newImagePath)  # load new image
    newString = decodePic(origImage, newImage)  # decode to string
    newImage.close()
    origImage.close()
    return newString  # return decoded string


# open initial window
window = tk.Tk()
# configure initial window
window.title("Image Messenger")
window.configure(background="black")


# defining the function to run the window which will let user select to be server or client
def choiceGUI():
    global server
    # initialize var to store whether user is server
    server = False

    # initialize var to store image path to use for communication
    imagePathToModify1 = tk.StringVar(window, "TestImagePython.png")

    # function to erase canvas and run the server GUI
    def cleanChoiceServer():
        # make the path of image to use and server or not be available globally
        global imagePathToModify
        imagePathToModify = imageSelectBox.get()
        global server

        # remove widgets
        lbl1.grid_forget()
        s.grid_forget()
        c.grid_forget()
        imageSelectBox.grid_forget()
        imageSelectLabel.grid_forget()
        topFrame.grid_forget()
        bottomFrame.grid_forget()

        # remove reference to photoLabel image, so python garbages it
        del photoLabel.image

        # remove image widgets
        imageFrame.grid_forget()
        photoLabel.grid_forget()

        # launch server GUI
        server = True
        serverGUI()

    # function to erase widgets and run server GUI
    def cleanChoiceClient():
        # make image path available outside
        global imagePathToModify
        imagePathToModify = imageSelectBox.get()

        # remove widgets
        lbl1.grid_forget()
        s.grid_forget()
        c.grid_forget()
        imageSelectBox.grid_forget()
        imageSelectLabel.grid_forget()
        topFrame.grid_forget()
        bottomFrame.grid_forget()

        # remove reference to image
        del photoLabel.image

        # remove image widgets
        imageFrame.grid_forget()
        photoLabel.grid_forget()

        # decide to launch client GUI
        global server
        server = False
        clientGUI()

    def updateImage():
        global photoLabel
        # photoLabel.grid_forget()
        global imageWithPillow
        imageWithPillow = Image.open(imagePathToModify1.get())
        # imageWithPillow = Image.open('TestImagePython.png')
        size = 126, 126
        imageWithPillow.thumbnail(size)
        global imageWithTk
        imageWithTk = ImageTk.PhotoImage(imageWithPillow)

        photoLabel.configure(image=imageWithTk)
        photoLabel.image = imageWithTk  # keep a reference!

        # photoLabel.grid(column=1,row=1)

    # Create buttons to run the server and client choice commands

    # a frame to contain the choice to be server of client
    topFrame = tk.Frame(window, bg='red', padx=15, pady=10, bd=4, relief='sunken')
    topFrame.grid(column=2, row=2, sticky='we')

    # a frame to contain widgets to choose image
    bottomFrame = tk.Frame(window, bg='red', padx=15, pady=10, bd=4, relief='raised')
    bottomFrame.grid(column=2, row=3, sticky='we')

    # a frame to contain image
    imageFrame = tk.Frame(window, bg='green', padx=15, pady=10, bd=4, relief='sunken')
    imageFrame.grid(column=3, row=2, rowspan=2, sticky='ns')

    # label to select role
    lbl1 = tk.Label(topFrame, text="Select your role: ", padx=6, pady=3, relief='sunken')
    lbl1.grid(row=1, column=2)  # place into grid
    # button to choose server
    s = tk.Button(topFrame, text="Server", command=cleanChoiceServer, padx=6, pady=3)
    s.grid(row=2, column=1)
    # button to choose client
    c = tk.Button(topFrame, text="Client", command=cleanChoiceClient, padx=6, pady=3)
    c.grid(row=2, column=3)

    # label to say using this image
    imageSelectLabel = tk.Label(bottomFrame, text="Using this image: ", padx=6, pady=3, relief='sunken')
    imageSelectLabel.grid(row=3, column=1)

    # entry box to select image path
    imageSelectBox = tk.Entry(bottomFrame, textvariable=imagePathToModify1)
    imageSelectBox.grid(row=3, column=2)

    # button to update image thumbnail with path from entry box
    imageUpdateButton = tk.Button(bottomFrame, text="Update image", command=lambda: updateImage())
    imageUpdateButton.grid(row=4, column=2)

    # open an image with pillow/PIL
    imageWithPillow = Image.open(imagePathToModify1.get())
    # make the image a smaller thumbnail
    size = 150, 150
    imageWithPillow.thumbnail(size)
    # convert image to Tkinter photoimage object
    imageWithTk = ImageTk.PhotoImage(imageWithPillow)

    # create a label and put the image thumbnail inside it
    global photoLabel  # make it available outside function, to update it
    photoLabel = tk.Label(imageFrame, image=imageWithTk)
    photoLabel.image = imageWithTk  # keep a reference!
    photoLabel.grid(column=1, row=1)


# the function which will contain the server functionality and allow them to set up connection.
def serverGUI():
    # a function to establish connection with client
    def startListen():
        # make socketNum available elsewhere
        global socketNum
        socketNum = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates the socket

        # global variable to hold ip taken from tkinter variable
        global globalIp
        globalIp = str(ip.get())

        # global variable to hold port taken from tkinter variable
        global globalPort
        globalPort = int(port.get())

        # Binds the socket to the host computer and portprint
        socketNum.bind((ip.get(), port.get()))
        socketNum.listen(1)  # listens

        # needs separate vars to send and recieve messages
        global conn
        global address
        conn, address = socketNum.accept()
        socketNum.settimeout(2)  # if there is no message to recv

        # open the main communication window
        convoWinOpen()

    # default ip is their own ip for testing
    ip = tk.StringVar(window, socket.gethostbyname(socket.gethostname()))
    # string var to use in labels/entries
    ipDisplay = tk.StringVar(window, "Your ip is: " + ip.get())

    # makes tk variable for port
    port = tk.IntVar(window, 8888)

    window.title("Image Messenger Server")

    # a frame for all the widgets
    frame1 = tk.Frame(window, padx=10, pady=10, width=270, bg='blue')
    frame1.grid(column=1, row=1)

    # label for ip
    ipLbl = tk.Label(frame1, textvariable=ipDisplay, padx=15, pady=2, relief='sunken')
    ipLbl.grid(row=1, column=1)

    # label for port
    portLbl = tk.Label(frame1, text="Port to use: ", padx=15, pady=2, relief='sunken')
    portLbl.grid(row=2, column=0)

    # lets user input port
    portEntry = tk.Entry(frame1, textvariable=port)
    portEntry.grid(row=2, column=1)

    # button to start listening
    listenButton = tk.Button(frame1, text="Start Listening", command=lambda: startListen(), padx=15, pady=2)
    listenButton.grid(row=3, column=1)


# A function to run the client setup GUI
def clientGUI():
    # change window title
    window.title("Image Messenger Client")

    # function to connect to a listening ip on a inputted port
    def connect():
        global socketNum
        socketNum = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates the socket
        socketNum.connect((ip.get(), port.get()))  # connects with port and ip
        convoWinOpen()  # starts main conversation window

    # tkinter variables to store and display the ip in labels
    ip = tk.StringVar(window, socket.gethostbyname(socket.gethostname()))
    ipDisplay = tk.StringVar(window, "Server ip: " + ip.get())

    # tkinter variables to store and display the ip in labels
    port = tk.IntVar(window, 8888)
    portDisplay = tk.StringVar(window, "Port to use: " + str(port.get()))

    # frame to hold all widgets
    frame1 = tk.Frame(window, padx=10, pady=10, width=270, bg='green')
    frame1.grid(column=1, row=1)

    # nice message saying title and stuff
    lbl0 = tk.Label(frame1, text="ImageMessenger.Client.3.0", padx=8, pady=2, relief='sunken')
    lbl0.grid(row=0, column=2)

    # entry for ip
    e1 = tk.Entry(frame1, textvariable=ip)
    e1.grid(row=1, column=2)

    # label to display ip
    lbl1 = tk.Label(frame1, textvariable=ipDisplay, padx=8, pady=2, relief='sunken')
    lbl1.grid(row=1, column=1)

    # entry widget to give port
    e2 = tk.Entry(frame1, textvariable=port)
    e2.grid(row=2, column=2)

    # label to display port
    lbl2 = tk.Label(frame1, textvariable=portDisplay, padx=8, pady=2, relief='sunken')
    lbl2.grid(row=2, column=1)

    # button to connect to socket
    bConnect = tk.Button(frame1, text="Connect", command=lambda: connect(), padx=15, pady=2)
    bConnect.grid(row=3, column=2)


# A function to run the communication between server anc client once connection is established.
def convoWinOpen():
    # A function to send a message over the connection
    def sendMessage():
        message = messageOutEntry.get()  # get message from input box
        makeNewEncodedImage(imagePathToModify, message)  # Make a new encoded image
        imageToSend = open("NewImage.png", "rb")  # open to send
        imageToSend = imageToSend.read()  # get binary data

        # if statement to send differently based on being client or server
        if server:
            conn.send(imageToSend)  # Sending over socket
        else:
            socketNum.send(imageToSend)  # Sending over socket
        print("Just sent")  # so you know it did it

    # A function to receive a message.
    def recvMessage():

        # if statement to set timeout differently based on being client or server
        if server:
            conn.settimeout(2)
        else:
            pass
            socketNum.settimeout(2)

        # try to receive image,except if there is a timeout
        try:
            # if statement to receive differently based on being client or server
            if server:
                recvImage = conn.recv(2 * 4096)  # recieves image
            else:
                recvImage = socketNum.recv(2 * 4096)  # recieves image

            recvFile = open("NewImage.png", 'wb')  # opens a file to recieve data
            recvFile.write(recvImage)  # write data
            recvFile.close()

            # decodes with original image
            recvedMessage = returnNewDecodedString(imagePathToModify, "NewImage.png")

            global lastRecvedMessage
            lastRecvedMessage = recvedMessage
            inMessage.set(lastRecvedMessage)  # set a tkinter variable to display
            print("Just received")

        except socket.timeout:
            print("No New Message")

    newWin = tk.Toplevel()  # nice new top-level window addition to talk in

    # title based on role
    if server:
        newWin.title("Image Messenger Server")
    else:
        newWin.title("Image Messenger Client")

    # tk var to hold last in message, default is no messages
    inMessage = tk.StringVar(newWin, "No Messages")

    # frame on left side of screen to send
    sendFrame = tk.Frame(newWin, width=300, height=300, bg='red', padx=15, pady=10, bd=4, relief='groove')
    sendFrame.grid(row=1, column=1, sticky='ns')

    # frame on middle of screen to receive
    recvFrame = tk.Frame(newWin, width=300, height=300, bg='blue', padx=6, pady=6, bd=4, relief='groove')
    recvFrame.grid(row=1, column=2, sticky='ns')

    # frame on right of screen to show picture being used
    imageFrame2 = tk.Frame(newWin, bg='green', padx=8, pady=4, bd=4, relief='sunken')
    imageFrame2.grid(column=3, row=1, sticky='ns')

    # entry box to input message to send
    messageOutEntry = tk.Entry(sendFrame)
    messageOutEntry.grid(row=1, column=1)

    # button to send the message
    sendButton = tk.Button(sendFrame, text="Send", command=lambda: sendMessage(), padx=4, pady=2)
    sendButton.grid(row=2, column=1)

    # label to display last message
    recvMessageLabel = tk.Label(recvFrame, textvariable=inMessage, bd=2, relief='sunken', padx=4, pady=2,
                                wraplength=100)
    recvMessageLabel.grid(column=1, row=1)

    # button to check for a new message
    recvMessageButton = tk.Button(recvFrame, text="Load New Message", command=lambda: recvMessage(), padx=4, pady=2)
    recvMessageButton.grid(column=1, row=2)

    # open the image with pillow
    imageWithPillow2 = Image.open(imagePathToModify)

    # make image a thumbnail
    size = 150, 150
    imageWithPillow2.thumbnail(size)

    # make pillow image a Tkinter photo image object
    imageWithTk2 = ImageTk.PhotoImage(imageWithPillow2)

    # mkae a label to put picture in
    photoLabel2 = tk.Label(imageFrame2, image=imageWithTk2)
    photoLabel2.image = imageWithTk2  # keep a reference!
    photoLabel2.grid()

    newWin.mainloop()  # run this GUI


# run the first GUI
choiceGUI()

# run the first GUI
window.mainloop()
