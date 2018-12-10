from PIL import Image
import socket
import time

#Curreently error when sending image bc its not binary. should do modification and then save. then send and recieve and savee and open to translaste.

mainImg=Image.open("TestImagePython.png")



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

def encodePic(img,string):
    #global imgNew
    imgNew = img.copy()
    pixelMapNew = imgNew.load()

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
    return pixelMapNew


def serverFunc(img):
    port=8888
    host=""

    socket1=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")
    socket1.bind((host, port))
    socket1.listen(1)
    print('server is listening')
    conn, address=socket1.accept()
    print("connected with "+str(address[0])+':'+str(address[1]))

    runConnect=True
    while runConnect:
        imgData= conn.recv(4096)
        #imgData=imgData.decode()
        imgData=decodePic(img, imgData)
        print("Client: "+imgData)
        if imgData=="":
            break
        elif imgData=='exit':
            runConnect==False
        reply = input("Server: ")
        reply = encodePic(img, reply)
        conn.send(reply)
    conn.close()
    socket1.close()

def clientFunc(host, img):
    port=8888

    socket1=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")
    socket1.connect((host,port))
    print("connected to ip "+host)

    runConnect=True
    while runConnect:
        data = input("Client: ")

        imgData=encodePic(img, data)


        if imgData=="":
            break
        elif imgData=='exit':
            runConnect==False
        socket1.send(imgData)
        reply = socket1.recv(4096)
        #reply=reply.decode()
        reply=decodePic(img,reply)
        print("Server: "+reply)
    socket1.close()

choice=input("server1 or client2: ")
if choice=='1':
    serverFunc(mainImg)
elif choice=='2':
    clientFunc('192.168.1.143',mainImg)


