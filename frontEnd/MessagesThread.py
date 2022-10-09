from email import message
from PyQt5.QtCore import QtThread, pyqtSignal

class MessagesThread(QtThread):
    message = pyqtSignal(list)

    def __init__(self,client):
        super().__init__()
        self.scanSocket = True
        self.client = client

    def run(self):
        while (self.scanSocket):
            data = self.client.getData()
            if data[1]!=data[2]:
                self.message.emit(data)
    
    def stop(self):
        self.scanSocket = False

    def restart(self):
        self.scanSocket = True