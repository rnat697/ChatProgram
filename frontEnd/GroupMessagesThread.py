from PyQt5.QtCore import QThread, pyqtSignal
from time import sleep

 # Thread to receive messages from members, receive updated member list and receive any image file names that was sent
class GroupMessagesThread(QThread):
    message = pyqtSignal(str)
    members = pyqtSignal(list)
    imageFileName = pyqtSignal(list)

    def __init__(self,client):
        super().__init__()
        self.scanSocket = True
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
                self.message.emit(data) # emit the message
            
            # check if its the updated members list
            if(type(data) == list):
                if(data[0] == 2):
                    self.members.emit(data[1]) # emit the updated members list
                    print("group members updated")
                
                if(data[0] == 3): # Check if image has been downloaded to server
                    self.imageFileName.emit(data) # emit the image file name
                    print("Image received")

  
    
    def stopThread(self):
        self.terminate()