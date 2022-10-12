from PyQt5.QtCore import QThread, pyqtSignal, QObject, pyqtSlot
from time import sleep

class GroupAndClientsThread(QThread):
    clientNames = pyqtSignal(dict) 
    groupNames = pyqtSignal(dict)
    finished = pyqtSignal()


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
            
        
        print("Finished client thread")
        self.finished.emit()

    def stop(self):
        print("stopping thread")
        self.scanSocket = False

    def pauseThread(self):
        print("pausing thread")
        self.pause = True

    def restart(self):
        print("restarting thread")
        self.pause = False