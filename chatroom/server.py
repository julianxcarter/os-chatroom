import socket
import select

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostbyname(''), 2007))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"The connect from { address } has been established!")
    clientsocket.send(bytes("Welcome to the server!", "utf-8")) 
    clientsocket.close()