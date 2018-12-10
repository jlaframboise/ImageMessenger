from PIL import Image
import socket
import time

mainImg=Image.open("TestImagePython.png",'b')
 
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

while True:    
    data = conn.recv(4096) # Receives data from client when it is sent
    print ("Client >",data.decode()) # Displays the client data. Note it must be decoded from binary
    if data == "": 
        break

    reply = input ("Server >") # Gets data from the person using the server program     
    conn.send(reply.encode())   # Sends data to the client. Note it must be coded to binary
 
conn.close() # Closes the connections
socketNum.close()
