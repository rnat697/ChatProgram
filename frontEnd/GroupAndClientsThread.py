import string
from PyQt5.QtCore import QThread, pyqtSignal, QObject, pyqtSlot
from time import sleep
import socket

class GroupAndClientsThread(QThread):
    clientNames = pyqtSignal(dict) 
    groupNames = pyqtSignal(dict)
    finished = pyqtSignal()

    def __init__(self,client):
        super().__init__()
        self.scanSocket = True
        self.client = client
        
    @pyqtSlot()
    def run(self):
        prevLengthClients = 0
        prevLengthGroups = 0
        while (self.scanSocket):
            sleep(0.5) # For some reason this allows the server to know that the client hung up when we press exit button on Chat connected window
            try:
                self.client.sendData(2) # Request server for client names and group names
                data = self.client.getData() # get the requested data
            except:
                break

            # check if list of clients has been changed
            if((prevLengthClients < len(data[0])) or (prevLengthClients > len(data[0])) ): 
                prevLengthClients = len(data[0]) # update length
                
                lengthClients = len(data[0]) # DELETE LATER
                print("\nclients: ", data[0], lengthClients) # DELETE LATER
                
                # Emit client names
                self.clientNames.emit(data[0])

            # check if list of groups has been changed
            if((prevLengthGroups < len(data[1])) or (prevLengthGroups > len(data[1]))):
                prevLengthGroups = len(data[1]) # update length
                print("\ngroup: ", data[1]) # DELETE LATER

                # Emit group names
                self.groupNames.emit(data[1])
        
        print("Finished thread")
        self.finished.emit()

    def stop(self):
        self.scanSocket = False


    def restart(self):
        self.scanSocket = True