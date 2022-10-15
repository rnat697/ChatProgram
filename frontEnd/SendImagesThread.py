from PyQt5.QtCore import QThread, pyqtSignal
from time import sleep
import os

class SendImagesThread(QThread):
    finished = pyqtSignal()

    def __init__(self,client, image, participants, fileName, fileSize):
        super().__init__()
        self.client = client
        self.image = image
        self.participants = participants
        self.fileName =fileName
        self.fileSize = fileSize


    def run(self):
        self.client.sendData([4,self.fileName,self.participants,self.fileSize])
        imageBytes = self.image.read(40960000)

        while(imageBytes):
            print("sending image...")
            self.client.sendImageAll(imageBytes)
            imageBytes = self.image.read(40960000)
        self.image.close()
        print("Image sent")

        self.finished.emit()
    
    def stopThread(self):
        self.terminate()
