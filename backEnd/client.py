import select
import socket
import sys
import ssl
from socket import*

from backEnd.utils import *

# Modified from lab 5

SERVER_HOST = 'localhost'

stop_thread = False

# def get_and_send(client, data):
#     while not stop_thread:
#         if data:
#             send(client.sock, data)


class ChatClient():
    """ A command line chat client using select """
    def __init__(self, name, port, host=SERVER_HOST):
        self.name = name
        self.connected = False
        self.host = host
        self.port = int(port)
        
        # Encryption using TLSv1.2 
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        
        # Connect to server at port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = self.context.wrap_socket(self.sock, server_hostname=host)
            self.sock.connect((host, self.port))
            print(f'Now connected to chat server@ port {self.port}')
            self.connected = True
            
            # Send my name...
            send(self.sock, 'NAME: ' + self.name)
            data = receive(self.sock)
            # Contains client address, set it
            addr = data.split('CLIENT: ')[1][1:-1].split(", ")
            print(addr)
            self.address = addr[0]
            self.portAddr = int(addr[1])

        except socket.error as e:
            print(f'Failed to connect to chat server @ port {self.port}')
            sys.exit(1)

    def cleanup(self):
        """Close the connection and wait for the thread to terminate."""
        print("Closing client socket")
        self.sock.close()
 
    def getData(self):
        readable, writeable, exceptional = select.select([self.sock], [], [])
        for sock in readable:
            if sock == self.sock:
                data = receive(self.sock)
                return data
    
    def sendData(self,data):
        if data:
            send(self.sock, data)
    def sendImageAll(self,data):
        if(data):
           self.sock.sendall(data)
