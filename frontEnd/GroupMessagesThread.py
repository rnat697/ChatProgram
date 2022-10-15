from PyQt5.QtCore import QThread, pyqtSignal
from time import sleep

class GroupMessagesThread(QThread):
    message = pyqtSignal(str)
    members = pyqtSignal(list)
    imageFileName = pyqtSignal(list)

    def __init__(self,client):
        super().__init__()
        self.scanSocket = True
        self.pause = False
        self.client = client


    def run(self):
        while (self.scanSocket):
            sleep(0.3)
            try:
                data = self.client.getData()
            except:
                break
            
            # Check if its a message 
            if (type(data) == str):
                print(data)
                self.message.emit(data)
            
            # check if its the updated members list
            if(type(data) == list):
                if(data[0] == 2):
                    self.members.emit(data[1])
                    print("group members updated")
                
                if(data[0] == 3): # Check if image has been downloaded to server
                    self.imageFileName.emit(data)
                    print("Image received")

  
    
    def stopThread(self):
        self.terminate()

    def pauseThread(self):
        self.pause = True

    def unpauseThread(self):
        self.pause = False