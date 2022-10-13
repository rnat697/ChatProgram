import select
import socket
import sys
import signal
import ssl

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
        self.groups = {}

        self.outputs = []  # list output sockets

        # Encryption using SSL/TLSv1.2 and cipher AES
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_cert_chain(certfile="cert.pem", keyfile="cert.pem")
        self.context.load_verify_locations('cert.pem')
        self.context.set_ciphers('AES128-SHA')

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, SERVER_PORT))
        self.server.listen(backlog)
        self.server = self.context.wrap_socket(self.server, server_side=True)
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
        host, name = info[0], info[1]
        return host,name
    
    def removeClientFromLists(self,addrLeft,nameLeft):
        groupToDelete = []
        # ----- Remove client lists and group lists -------- 
        # finding the groups that this user is hosting
        for group in self.groups:
            members = self.groups[group]
            if(group[1] == nameLeft):
                groupToDelete.append(group)
            
            indexMemberDelete = 0

            # finding the groups that the user is a member of 
            for member in members:
                # deleting the user from member list in the groups that user is a member of
                if(member[0] == addrLeft[0] and member[1] == addrLeft[0] and member[2] == nameLeft): 
                    members.pop(indexMemberDelete)
                indexMemberDelete +=1
        
        # deleting the groups that the user is the host of
        for groupsRemove in groupToDelete:
            self.numGroups -= 1
            del self.groups[groupsRemove]

        # Other deletes for client lists
        del self.listOfAllClients[(addrLeft[0],addrLeft[1],nameLeft)]
        del self.clientGroupHost[(addrLeft[0],addrLeft[1],nameLeft)]
        clientLeft = self.clientSockets[(addrLeft[0], addrLeft[1], nameLeft)]
        del self.clientmap[clientLeft]
        del self.clientSockets[addrLeft[0],addrLeft[1],nameLeft]

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

                            # To differentiate between client to client messages and thread requests
                            if (type(data) == int): # backend requests
                                if(data == 2): # when thread requests for list of all clients and groups
                                    send(sock, [self.listOfAllClients,self.groups])
                                
                                if(data == 3): # when client made a group chat
                                    self.numGroups += 1
                                    add, hostName = self.get_client_name(sock)
                                    groupName = "Group Chat " + str(self.numGroups) + " by " + hostName
                                    print(groupName, "is made")
                                    host  = (add[0],add[1], hostName)
                                    self.clientGroupHost[(add[0], add[1], hostName)] =  [groupName]
                                    self.groups[(groupName,hostName)] = [host]

                                
                                
                            else: 
                                if data[0] == 1: # Sending a message
                                    add, clientName = self.get_client_name(sock)
                                    participants = data[1]
                                    print("participants: ", participants)
                                    msg = "["+ clientName + "]: " + data[2]
                                    print(msg)
                                    
                                    # Send message data to specific clients
                                    for clientDetails in participants:
                                        clientSocket =self.clientSockets[clientDetails]
                                        send(clientSocket, msg)
                                
                                if (data[0] == 2): # joining or invite accepted to group
                                    print("Joining Group via server")
                                    groupName  = data[1]
                                    clientsJoining = data[2]
                                    groupHostName = data[3]
                                    members = self.groups[(groupName,groupHostName)]
                                    print(clientsJoining)
                                    
                                    # add joining and invited clients to the group
                                    members.append(clientsJoining)
                                    print(members)
                                    
                                    # send updated member to clients
                                    for member in members:
                                        print(member)
                                        clientSoc = self.clientSockets[member]
                                        send(clientSoc,[2,members]) 
                                
                                if(data[0] == 3): # sending invite to person
                                    inviteReceiver = data[1]
                                    groupName = data[2]
                                    inviteMsg = "You're invited to join //" + groupName + "// , would you like to join?"

                                    
                                    receivSocket = self.clientSockets[inviteReceiver]
                                    send(receivSocket,[1,inviteMsg])
                                    




                        else:  
                            addrLeft, nameLeft = self.get_client_name(sock)
                            print(f'Chat server: {sock.fileno()} - {nameLeft} hung up')
                            self.clients -= 1
                            sock.close()
                            inputs.remove(sock)
                            self.outputs.remove(sock)
                            self.removeClientFromLists(addrLeft,nameLeft)

                            
                            # msg = f'\n(Now hung up: Client from {addrLeft,name})'

                            # for output in self.outputs:
                            #     send(output, msg)
                    except socket.error as e:
                        # Remove
                        inputs.remove(sock)
                        self.outputs.remove(sock)
                        addrLeft, nameLeft = self.get_client_name(sock)
                        self.removeClientFromLists(addrLeft,nameLeft)
        
            
                        
        self.server.close()



if __name__ == "__main__":
    server = ChatServer()
    server.run()