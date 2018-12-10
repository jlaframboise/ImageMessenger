import socket
from EncodeToNewFile import *
 
HOST = ""  
PORT = 8888 # Arbitrary port not used by the system
 
socketNum = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Creates the socket
print ('Socket created')
 
socketNum.bind((HOST, PORT)) # Binds the socket to the host computer and portprint ('Socket bind complete')

socketNum.listen(1) # Waits or "listens" for a client computer to request a connection 
print ('Server is now listening')

 
conn, address = socketNum.accept()  #Accepts a connection from the client
                                    # This function stores the data in TWO different variables

print ('Connected with ' + address[0] + ':' + str(address[1])) # Displays client data

#testing change sync

while True:
    recvImage = conn.recv(2*4096) # Receives data from client when it is sent

    #writes incoming image to file
    recvFile=open("NewImage.png",'wb')
    recvFile.write(recvImage)
    recvFile.close()

    #decodes the incoming picture data
    recvedMessage=returnNewDecodedString("TestImagePython.png","NewImage.png")
    print("Client> "+recvedMessage)

    if recvImage == None:
        break

    #gets message to send
    message = input("Server (You)>> ")

    #makes encoded image with message
    makeNewEncodedImage("TestImagePython.png", message)

    #converts the image to the contents of a binary file, 'a bytes like object' to send
    imageToSend = open("NewImage.png", 'rb')
    imageToSend = imageToSend.read()

    conn.send(imageToSend)   # Sends data to the client. Note it must be coded to binary




conn.close() # Closes the connections
socketNum.close()
