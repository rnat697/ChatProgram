import select
import socket
import sys
import signal


from utils import *

SERVER_HOST = 'localhost'
SERVER_PORT = 9988
# Modified from lab 5


class ChatServer(object):
    """ An example chat server using select """

    def __init__(self, backlog=5):
        self.clients = 0
        self.clientmap = {}
        self.listOfAllClients = {}
        self.clientGroupHost = {}
        self.clientSockets = {}
        self.numGroups = 0
        ## TO ADD SOMETING ABOUT GROUPS

        self.outputs = []  # list output sockets

        # ADD CERTIFICATE / ENCRYPTION
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, SERVER_PORT))
        self.server.listen(backlog)
        # Catch keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)

        print(f'Server listening to port: {SERVER_PORT} ...')

    def sighandler(self, signum, frame):
        """ Clean up client outputs"""
        print('Shutting down server...')

        # Close existing client sockets
        for output in self.outputs:
            output.close()

        self.server.close()

    def get_client_name(self, client):
        """ Return the name of the client """
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return name

    def getClients(self):
        return self.clientmap

    def run(self):
        # inputs = [self.server, sys.stdin]
        inputs = [self.server]
        self.outputs = []
        running = True
        while running:
            try:
                readable, writeable, exceptional = select.select(
                    inputs, self.outputs, [])
            except select.error as e:
                break

            for sock in readable:
                sys.stdout.flush()
                if sock == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    print(
                        f'Chat server: got connection {client.fileno()} from {address}')
                    # Read the login name
                    cname = receive(client).split('NAME: ')[1]

                    # Compute client name and send back
                    self.clients += 1
                    send(client, f'CLIENT: {str(address)}')
                    inputs.append(client)

                    self.clientmap[client] = (address, cname)
                    self.clientSockets[(address[0], address[1], cname)] = client
                    self.clientGroupHost[(address[0], address[1], cname)] =  []
                    self.listOfAllClients[(address[0], address[1], cname)] = []
                    # Send joining information to other clients
                    # msg = f'\n(Connected: New client ({self.clients}) from {self.get_client_name(client)})'
                    # for output in self.outputs:
                    #     send(output, msg)
                    self.outputs.append(client)

                else:
                    # handle all other sockets
                    try:
                        data = receive(sock)
                        if data:
                            # Send as new client's message...
                            # msg = f'\n#[{self.get_client_name(sock)}]>> {data}'

                            # # Send data to all except ourself
                            # for output in self.outputs:
                            #     if output != sock:
                            #         send(output, msg)
                            if (type(data) == int):
                                if(data == 2): # when client requests for list of all clients and groups
                                    send(sock, [self.listOfAllClients,self.clientGroupHost])
                                if(data == 3): # when client made a group chat
                                    # TO DO ADD PPL TO GROUP CHAT
                                    self.numGroups += 1
                                    groupName = "Group Chat " + str(self.numGroups) + " by " + cname
                                    self.clientGroupHost[(address[0], address[1], cname)] =  [self.numGroups, groupName]
                        else:
                            print(f'Chat server: {sock.fileno()} hung up')
                            # for client_socket in self.clientSockets.value():
                            #     if(client  == client_socket):

                            self.clients -= 1
                            sock.close()
                            inputs.remove(sock)
                            self.outputs.remove(sock)

                            # Sending client leaving information to others  BEED TO REMOVE FROM DICTIONARY
                            msg = f'\n(Now hung up: Client from {self.get_client_name(sock)})'

                            for output in self.outputs:
                                send(output, msg)
                    except socket.error as e:
                        # Remove
                        inputs.remove(sock)
                        self.outputs.remove(sock)
                        
        self.server.close()



if __name__ == "__main__":
    server = ChatServer()
    server.run()