
import socket
from PIL import Image

def serverFunc(PORT=8888):

    HOST = ""
    # Arbitrary port not used by the system

    socketNum = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates the socket
    print('Socket created')

    socketNum.bind((HOST, PORT))  # Binds the socket to the host computer and portprint ('Socket bind complete')
    print("Server ip is "+str(socket.gethostbyname(socket.gethostname())) + " and port is "+ str(PORT))

    socketNum.listen(1)  # Waits or "listens" for a client computer to request a connection
    print('Server is now listening')

    conn, address = socketNum.accept()  # Accepts a connection from the client
    # This function stores the data in TWO different variables

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


def clientFunc(remote_ip=str(socket.gethostbyname(socket.gethostname())),port=int(8888)):
    socketNum = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Client socket created')
    #remote_ip = socket.gethostbyname(socket.gethostname())
    #remote_ip = '10.22.8.221'  # The ip address of the computer with server program
    #port = 8888  # Arbitrary port not used by the system

    print('Ip address of ' + str(remote_ip))

    socketNum.connect((remote_ip, port))  # Connect to remote server
    print('Socket Connected to  ip ' + remote_ip)

    while True:
        # gets message to send to server
        message = input("Client (You)>> ")

        # makes a new image containing the message
        makeNewEncodedImage("TestImagePython.png", message)

        # opens the image in binary mode
        imageToSend = open("NewImage.png", 'rb')

        # reads the image toi send as a 'bytes like object'
        imageToSend = imageToSend.read()

        if imageToSend == None:
            break

        socketNum.send(imageToSend)  # Sends data to the server
        # receives new image
        recvImage = socketNum.recv(2 * 4096)  # Receives data from client when it is sent

        # writes binary image to file
        recvFile = open("NewImage.png", 'wb')
        recvFile.write(recvImage)
        recvFile.close()

        # decodes from file and prints
        recvedMessage = returnNewDecodedString("TestImagePython.png", "NewImage.png")
        print("Server> " + recvedMessage)

    socketNum.close()  # Closes the connections


def decodePic(img, newImg):

    orgPixelMap=img.load()
    pixelMap=newImg.load()
    varience = 1

    currentByte=[]
    decodedList=[]

    for x in range(0,img.size[1]):
        for i in range(0,img.size[0]):
            moddedPixel=pixelMap[i,x]
            pixel=orgPixelMap[i,x]
            if moddedPixel[0]==pixel[0]+varience or moddedPixel[0]==pixel[0]+(-2*varience):
                currentByte.append(1)
            elif moddedPixel[0]==pixel[0]-varience or moddedPixel[0]==pixel[0]-(-2*varience):
                currentByte.append(0)
            if len(currentByte)==8:
                valSum=0
                for a in range(0,8):
                    if currentByte[a]==1:
                        valSum+=2**(7-a)
                decodedList.append(valSum)
                currentByte=[]
    decodedString=''.join(chr(i) for i in decodedList)

    return decodedString


def encodePic(origImage,string):

    global imgNew
    imgNew = origImage.copy()
    pixelMapNew = imgNew.load()

    #string="hello World"
    toEncodeList=[]
    xPos=0
    yPos=0
    varience = 1
    for i in string:
        binNum=(bin(ord(i)))
        binNum=binNum[:1]+binNum[2:]
        if len(binNum) < 8:
            binNum = '0' + str(binNum)
        toEncodeList.append(binNum)
    for x in toEncodeList:
        for y in x:
            if y=='1':
                if pixelMapNew[xPos,yPos][0]==255:
                    varience=-2
                pixelMapNew[xPos,yPos]=(pixelMapNew[xPos,yPos][0]+varience,pixelMapNew[xPos,yPos][1],pixelMapNew[xPos,yPos][2])
                varience=1
            elif y=='0':
                if pixelMapNew[xPos,yPos][0]==0:
                    varience=-2
                pixelMapNew[xPos,yPos]=(pixelMapNew[xPos,yPos][0]-varience,pixelMapNew[xPos,yPos][1],pixelMapNew[xPos,yPos][2])
                varience = 1
            if xPos<imgNew.size[0]-1:
                xPos+=1
            elif xPos==imgNew.size[0]-1:
                xPos=0
                yPos+=1


#this function takes the path of the original picture, the string to be encoded, and encodes it in a new png file called "NewImage.png". It then closes the images
def makeNewEncodedImage(origImagePath,string):
    origImage = Image.open(origImagePath)
    encodePic(origImage, string)
    origImage.close()
    imgNew.save('NewImage.png')
    imgNew.close()

#this function takes the location or name of the new file and the original file and opens them, decodes the new to a string, closes the images, and returns the string
def returnNewDecodedString(origImagePath,newImagePath="NewImage.png"):
    origImage=Image.open(origImagePath)
    newImage=Image.open(newImagePath)
    newString=decodePic(origImage, newImage)
    newImage.close()
    origImage.close()
    return newString
