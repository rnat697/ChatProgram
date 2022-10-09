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

        print("IN THE THREAD")
        while (self.scanSocket):
            self.client.sendData(2)
            data = self.client.getData()

            if(prevLengthClients < len(data[0])): # check if list of clients has been changed

                print("\ndata from thread: ",data) 
                prevLengthClients = len(data[0])
                lengthClients = len(data[0])
                print("\nclients: ", data[0], lengthClients)
                self.clientNames.emit(data[0])

            
            if(prevLengthGroups < len(data[1])):
                prevLengthGroups = len(data[1])
                print("\ngroup: ", data[1])
                self.groupNames.emit(data[1])
        self.finished.emit()

    def stop(self):
        self.scanSocket = False


    def restart(self):
        self.scanSocket = True