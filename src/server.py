import socket
import select
from threading import Thread
 
headerLength = 10
IP = "0.0.0.0"
PORT = 1250
 
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
 
serverSocket.bind((IP,PORT))
serverSocket.listen(5)
print("Server has been initiated, waiting for connections...")
 
sockets_list = [serverSocket]
 
clients = {}
threads = {}

class ClientThread(Thread): 

    def __init__(self, client_socket): 
        Thread.__init__(self)
        self.client_socket = client_socket
        self.user = self.recieveMsg() 
    
    def recieveMsg(self):
        try:
            message_header = self.client_socket.recv(headerLength)
 
            if not len(message_header):
                return False
 
            messegeLength = int(message_header.decode('utf-8').strip())
            return {'header': message_header, 'data': client_socket.recv(messegeLength)}
    
        except:
            return False

    def run(self):

            while True:
                message = self.recieveMsg()

                if message is False:
                    print(f"Closed connection from {self.client_socket['data'].decode('utf-8')}")
                    sockets_list.remove(self.client_socket)
                    del clients[self.client_socket]
                    del threads[self.client_socket]
                    continue

                if message['data'].decode('utf-8') == "quit":
                    print(f"Closed connection from {self.client_socket['data'].decode('utf-8')}")
                    sockets_list.remove(self.client_socket)
                    del clients[self.client_socket]
                    del threads[self.client_socket]
                    return False

                user = self.client_socket
                print(f"Recieved message from {self.user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
 
                for socket in clients:
                    if socket is not self.client_socket:
                        socket.send(self.user['header'] + self.user['data'] + message['header'] + message['data'])


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
 
    for notified_socket in read_sockets:
        if notified_socket == serverSocket:
            client_socket, client_address = serverSocket.accept()
            newthread = ClientThread(client_socket)
            
            newthread.start()
            user = newthread.user

            if user is False:
                continue
 
            sockets_list.append(client_socket)
            clients[client_socket] = user
            threads[client_socket] = newthread
 
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
