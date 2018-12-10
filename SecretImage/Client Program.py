'''Client Program'''
import socket   #for sockets
from EncodeToNewFile import *
 
socketNum = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Client socket created')

remote_ip=socket.gethostbyname(socket.gethostname())
print(remote_ip)
#remote_ip = '10.22.8.221' # The ip address of the computer with server program
port = 8888     # Arbitrary port not used by the system
     
print ('Ip address of '  + remote_ip)  
 
socketNum.connect((remote_ip , port)) #Connect to remote server
print ('Socket Connected to  ip ' + remote_ip)

while True:
    #gets message to send to server
    message=input("Client (You)>> ")

    #makes a new image containing the message
    makeNewEncodedImage("TestImagePython.png",message)

    #opens the image in binary mode
    imageToSend = open("NewImage.png",'rb')

    #reads the image toi send as a 'bytes like object'
    imageToSend = imageToSend.read()

    if imageToSend == None:
        break
    
    socketNum.send(imageToSend)# Sends data to the server
    #receives new image
    recvImage = socketNum.recv(2 * 4096)  # Receives data from client when it is sent

    #writes binary image to file
    recvFile = open("NewImage.png", 'wb')
    recvFile.write(recvImage)
    recvFile.close()

    #decodes from file and prints
    recvedMessage = returnNewDecodedString("TestImagePython.png", "NewImage.png")
    print("Server> " + recvedMessage)


socketNum.close() # Closes the connections
