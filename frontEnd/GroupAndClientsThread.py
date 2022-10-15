from PyQt5.QtCore import QThread, pyqtSignal, QObject, pyqtSlot
from time import sleep

# Checks for any invites, updates to the list of groups, clients and group members sent by the server
class GroupAndClientsThread(QThread):
    clientNames = pyqtSignal(dict) 
    groupNames = pyqtSignal(dict)
    inviteMsg = pyqtSignal(str) 

    def __init__(self,client):
        super().__init__()
        self.scanSocket = True
        self.client = client
        self.pause = False
        
    @pyqtSlot()
    def run(self):
        prevLengthClients = 0
        prevLengthGroups = 0
        prevlengthofMembers = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
        while (self.scanSocket):
            if(not self.pause): # Checks if thread is paused
                sleep(0.5) # For some reason this allows the server to know that the client hang up when we press exit button on Chat connected window
                try:
                    self.client.sendData(2) # Request server for client names and group names
                    data = self.client.getData() # get the requested data
                except:
                    break

                if(type(data) == list): # check if the data sent is a list
                    
                    # Check if an invite has been received
                    if(data[0] == 1):
                        msg = data[1]
                        print(msg)
                        self.inviteMsg.emit(msg) #emit invite message

                    # check if data at position 0 is a dictionary which means server sent the list of clients and groups
                    if(type(data[0]) == dict):
                        # check if list of clients has been changed
                        if((prevLengthClients < len(data[0])) or (prevLengthClients > len(data[0])) ): 
                            prevLengthClients = len(data[0]) # update length
                            # Emit client names
                            self.clientNames.emit(data[0])

                        # check if list of groups has been changed
                        if((prevLengthGroups < len(data[1])) or (prevLengthGroups > len(data[1]))):
                            prevLengthGroups = len(data[1]) # update length
                            # Emit group information
                            self.groupNames.emit(data[1])

                        # Check if list of members has changed
                        index = 0
                        for members in data[1].values():
                            if (prevlengthofMembers[index] < len(members) or prevlengthofMembers[index] > len(members)):
                                prevlengthofMembers[index] = len(members)
                                self.groupNames.emit(data[1])
                                break
                            index+=1
            else:
                sleep(1)
            

    def stop(self):
        self.scanSocket = False

    def pauseThread(self):
        self.pause = True

    def restart(self):
        self.pause = False