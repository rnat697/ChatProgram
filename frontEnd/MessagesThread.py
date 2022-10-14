from PyQt5.QtCore import QThread, pyqtSignal
from time import sleep

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

            if (type(data) == str):
                print(data)
                self.message.emit(data)
            
            if(type(data)==list):
                if(data[0] == 3):
                    self.imageFileName.emit(data)

        #print("Finished msg thread")
    
    def stopThread(self):
        self.terminate()


    def restart(self):
        self.scanSocket = True