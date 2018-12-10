import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
openPorts=[]
usePorts=[]
for i in range(446,2000):
    result = sock.connect_ex(('127.0.0.1',i))
    if result == 0:
        if i == 135:
            print("port "+str(i)+" is in use")
            usePorts.append(i)
        else:
            openPorts.append(i)
            print("Port "+str(i)+" is open")

            #import FlashFlash.py

    else:
       print("Port "+str(i)+" is not open")


print("Open ports: ")
print(openPorts)
print()
print("UsedPorts: ")
print(usePorts)
