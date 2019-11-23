import socket
import select

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostbyname(''), 2007))


print("Welcome to The")


while True:
    msg = s.recv(8)
    print(msg.decode("utf-8"))