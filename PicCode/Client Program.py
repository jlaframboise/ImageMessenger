'''Client Program'''
from PIL import Image
import socket
import time

mainImg=Image.open("TestImagePython.png",'b')
 
socketNum = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Client socket created')

remote_ip = '192.168.1.143' # The ip address of the computer with server program
port = 8888     # Arbitrary port not used by the system
     
print ('Ip address of '  + remote_ip)  
 
socketNum.connect((remote_ip , port)) #Connect to remote server
print ('Socket Connected to  ip ' + remote_ip)

while True:
    data=mainImg
    #data = input ("Client> ") # Gets data from person using client program
    if data == "":
        break
    
    socketNum.send(data)# Sends data to the server. Note it must be coded to binary
    
    reply = socketNum.recv(4096) # Gets data from the person using the server program  
    print ("Server>> ", reply.decode()) # Displays the client data. Note it must be decoded from binary


socketNum.close() # Closes the connections
