import socket
import select
import errno
import sys

HEADER_LENGTH = 10

IP = "127.0.0.1"
Port = 1250

print("Welcome to the Chatroom!")
my_name = input("Username: ")
print("")
print("--------Instructions-------")
print("1. Type a message, then press enter to send")
print("2. Press enter without typing a message to load messages from other users")
print("3. Type 'quit' to close the connection")
print("")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, Port))
client_socket.setblocking(False)

name = my_name.encode("utf-8")
name_header = f"{len(name):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(name_header + name)


while True:
    msg = input(f"{my_name} > ")

    if msg:
        msg = msg.encode("utf-8")
        msg_header = f"{len(msg) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(msg_header + msg)

        if msg.decode('utf-8') == 'quit':
            print("Connection to the server has been closed")
            sys.exit()

    try:
        while True:
            name_header = client_socket.recv(HEADER_LENGTH)
            
            if not len(name_header):
                print("Connection closed by the server")
                sys.exit()

            username_length = int(name_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")

            if username != my_name:
                print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e))
        sys.exit()


