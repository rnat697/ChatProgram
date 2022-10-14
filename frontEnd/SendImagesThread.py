from PyQt5.QtCore import QThread, pyqtSignal
from time import sleep
import os

class SendImagesThread(QThread):
    finished = pyqtSignal()

    def __init__(self,client, image, participants, fileName, fileSize):
        super().__init__()
        self.scanSocket = True
        self.client = client
        self.image = image
        self.participants = participants
        self.fileName =fileName
        self.fileSize = fileSize


    def run(self):
        self.client.sendData([4,self.fileName,self.participants,self.fileSize])
        # print("waiting response")

        # while(self.scanSocket):
        #     sleep(0.5)
        #     data = self.client.getData()
            
        #     print(data)
        #     if(data == 9):
        #         print("got response")
        #         break
        print("wooooooo")
        imageBytes = self.image.read(40960000)
        while(imageBytes):
            print("sending image...")
            self.client.sendImageAll(imageBytes)
            imageBytes = self.image.read(40960000)
            print("still sending")
        self.image.close()
        print("Image sent")

        self.finished.emit()
        #print("Finished msg thread")
    
    def stopThread(self):
        self.terminate()


    def restart(self):
        self.scanSocket = True