import socket 
import select 
import sys
  
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
 
IP_address = "127.0.0.1"
Port = 1278
server.connect((IP_address, Port)) 

print("Welcome to the Chatroom!")
name = input("Enter a username: ")
print("")
print("--------Instructions-------")
print("1. Type a message, then press enter to send")
print("2. Press enter without typing a message to load messages from other users")
print("3. Type 'quit' to close the connection")
print("")

while True: 

    try:
        while True:
            received = server.recv(2048)
            if len(received) < 1:
                break
            message = received.decode("utf-8")
            print(f"{message}")
            break
 
    except:
        continue
 
    msg = input(f"{name}: ")
 
    if msg:
        msg = name + ": " + msg
        msg = msg.encode("utf-8")
        if msg.decode('utf-8') == 'quit':
            print("Connection to the server has been closed")
            sys.exit()
        else:
            server.send(msg)
            continue

 
    

