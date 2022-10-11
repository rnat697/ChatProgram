import select
import socket
import sys
import signal
import threading

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
        
        # Initial prompt
        self.prompt = f'[{name}@{socket.gethostname()}]> '
        
        # Connect to server at port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, self.port))
            print(f'Now connected to chat server@ port {self.port}')
            self.connected = True
            
            # Send my name...
            send(self.sock, 'NAME: ' + self.name)
            data = receive(self.sock)
            print(data)
            # Contains client address, set it
            addr = data.split('CLIENT: ')[1][1:-1].split(", ")
            print(addr)
            self.address = addr[0]
            self.portAddr = int(addr[1])
            #self.prompt = '[' + '@'.join((self.name, addr)) + ']> '

            #threading.Thread(target=get_and_send, args=(self,)).start()

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
                # if not data:
                #     print('Client shutting down.')
                #     self.connected = False
                #     break
                # else:
                return data
    
    def sendData(self,data):
        if data:
            send(self.sock, data)

# might not need this
    def run(self):
        """ Chat client main loop """
        while self.connected:
            try:
                #sys.stdout.write(self.prompt)
                #sys.stdout.flush()

                # Wait for input from stdin and socket
                # readable, writeable, exceptional = select.select([0, self.sock], [], [])
                readable, writeable, exceptional = select.select(
                    [self.sock], [], [])

                for sock in readable:
                    # if sock == 0:
                    #     data = sys.stdin.readline().strip()
                    #     if data:
                    #         send(self.sock, data)
                    if sock == self.sock:
                        data = receive(self.sock)
                        if not data:
                            print('Client shutting down.')
                            self.connected = False
                            break
                        else:
                            sys.stdout.write(data + '\n')
                            sys.stdout.flush()

            except KeyboardInterrupt:
                print(" Client interrupted. " "")
                stop_thread = True
                self.cleanup()
                break