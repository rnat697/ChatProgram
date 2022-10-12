from PyQt5.QtCore import QThread, pyqtSignal
from time import sleep

class MessagesThread(QThread):
    message = pyqtSignal(str)

    def __init__(self,client):
        super().__init__()
        self.scanSocket = True
        self.client = client
        self.stop = False


    def run(self):
        while (self.scanSocket):
            if(not self.stop):
                sleep(0.3)
                try:
                    data = self.client.getData()
                except:
                    break

                if (type(data) == str):
                    print(data)
                    self.message.emit(data)
        print("Finished msg thread")
    
    def stopThread(self):
        self.terminate()


    def restart(self):
        self.scanSocket = True