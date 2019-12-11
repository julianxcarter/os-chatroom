import socket 
import select 
import sys 
from _thread import *
  
"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts. The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow."""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
  
  

IP_address = "0.0.0.0"
Port = 1278
  

#  Binds the server to the IP address and port number
server.bind((IP_address, Port)) 
  

# Listens for a maximum of 5 connections
server.listen(5) 
  
list_of_clients = [] 


class ThreadPool:

    threads = {}

    def __init__(self, thread_count):
        self.thread_count = thread_count

    def addClient(self, conn, addr):
        if len(self.threads) < self.thread_count:
            newthread = start_new_thread(ClientThread, (conn, addr))
            print("New thread started")
            self.threads[conn] = newthread

        else:
            return False

    def removeClient(self, connection):
        del self.threads[connection]
  
def ClientThread(conn, addr): 


    msg = "Thread had been initialized, connection to the server has been established!"
    conn.send(msg.encode('utf-8')) 
    
    while True: 
            try: 
                message = conn.recv(2048) 
                if message: 
    
                    # From the message, the username is extracted and the message is printed
                    message = message.decode("utf-8")
                    username = message.split(':')[0]
                    body = message.split(':')[1].strip()
                    print(f"Message from {username}({addr[0]}): {body}")
                    # Calls broadcast fucntion to send to other clients
                    send_to_all(message, conn)
    
                else: 
                    """message may have no content if the connection 
                    is broken, in this case we remove the connection"""
                    threadpool.removeClient(conn)
                    remove(conn)
    
            except: 
                continue
  
# Iterates through the client list, if a client isn't the sender the message is encoded and sent over
def send_to_all(message, connection): 
    for clients in list_of_clients: 
        if clients != connection: 
            try: 
                clients.send(message.encode("utf-8")) 
            except: 
                clients.close() 
                remove(clients) #Removes the client if the link is broken
  
# Removes the client from the threadpool
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 
                
                
threadpool = ThreadPool(5)


while True: 
  
    # Accepts a connection request, saving the client's socket under conn and the IP address under addr
    conn, addr = server.accept()
 

    # A list of clients to broadcast messages to
    list_of_clients.append(conn) 
  
    #Prints the address of the new client
    print (f"Socket from {addr[0]} is connected to the server")
  
    #Creates a new thread for each new client
    # start_new_thread(ClientThread,(conn,addr))
    threadpool.addClient(conn, addr)
      
  

