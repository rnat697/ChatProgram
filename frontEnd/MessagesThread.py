from email import message
from PyQt5.QtCore import QThread, pyqtSignal
from time import sleep

class MessagesThread(QThread):
    message = pyqtSignal(str)

    def __init__(self,client):
        super().__init__()
        self.scanSocket = True
        self.client = client


    def run(self):
        while (self.scanSocket):
            sleep(0.5)
            try:
                data = self.client.getData()
            except:
                break
            
            print("MESSAGE from thread: ", data)
            print("message type: ", type(data))

            if (type(data) == str):
                #print("MESSAGE from thread: ", data)
                print("emitting data")
                self.message.emit(data)
        print("Finished msg thread")
    
    def stop(self):
        self.scanSocket = False

    def restart(self):
        self.scanSocket = True