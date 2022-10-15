from PyQt5.QtCore import QThread, pyqtSignal
from time import sleep

# Checks if there are any client messages or any images sent
class MessagesThread(QThread):
    message = pyqtSignal(str)
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
            
            # Messages sent by other client
            if (type(data) == str):
                print(data)
                self.message.emit(data) # emit the message
            
            # Image received
            if(type(data)==list):
                if(data[0] == 3):
                    self.imageFileName.emit(data) # emit image file name

        #print("Finished msg thread")
    
    def stopThread(self):
        self.terminate()

