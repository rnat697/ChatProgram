from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import os

from frontEnd.MessagesThread import MessagesThread
from frontEnd.SendImagesThread import SendImagesThread

class OneToOneChatMenu(QWidget):
    closed = pyqtSignal() # For chat Connected to know if window is closed, modified from https://stackoverflow.com/a/67519553
    def __init__(self,client,clientDetails, targetDetails):
        super().__init__()
        self.client = client
        self.clientDetails = clientDetails
        self.targetDetails = targetDetails
        self.targetName = self.targetDetails[2]
        self.clientName = self.clientDetails[2]
        self.participants = [self.clientDetails, self.targetDetails]

        self.initUI()
        self.display()
        self.connectActions()

    def initUI(self):
        #main window size and title
        self.setWindowTitle('One To One Chat')
        self.setGeometry(800, 300, 500, 500) 
        self.setMinimumHeight(300)
        self.setMinimumWidth(200)

        chatWithName = "Chat with " + self.targetName

        # Labels for one to one chat
        self.chatWithLabel = QLabel(chatWithName,self)

        # TextEdit for showing messages
        self.teMessages = QTextEdit(self)
        self.teMessages.setReadOnly(True)

        # Line Edit for user writing messages
        self.leMessageBox =QLineEdit(self)
        
        # buttons for send message, send image and exit
        self.btnSendMsg = QPushButton("Send", self)
        self.btnSendImg = QPushButton("Send Image", self)
        self.btnExit = QPushButton("Exit", self)

         # Add labels, buttons and text edits to grid layout
        grid = QGridLayout(self)
        self.setLayout(grid)
        grid.addWidget(self.chatWithLabel, 0, 0,1,5)
        grid.addWidget(self.teMessages,1,0,1,5)
        grid.addWidget(self.leMessageBox,2,0,1,3)
        grid.addWidget(self.btnSendMsg,2,3)
        grid.addWidget(self.btnSendImg,2,4)
        grid.addWidget(self.btnExit,3,0,1,5)

    # connecting actions to widget events
    def connectActions(self):
        self.btnExit.clicked.connect(self.exitApplication)
        self.btnSendMsg.clicked.connect(self.sendMessageAction)
        self.btnSendImg.clicked.connect(self.sendImageAction)
        

    def sendImageAction(self): # Attempted to send images to server. Server should download the image into a folder serverImages
        # Currently, running this action causes GUI to crash.
        imageDir = self.openFileExplorer()

        if(imageDir): # check if response is not empty (if it isn't that means the user has picked an image)
            image = open(imageDir,"rb")
            print('img dir: ', imageDir)
            fileName = os.path.basename(imageDir)
            print("fileName: ", fileName)
            fileSize = os.path.getsize(imageDir)

            self.sendImg = SendImagesThread(self.client,image,self.participants,fileName,fileSize)
            self.sendImg.finished.connect(self.closeSendImageThread)
            self.sendImg.start()
        #     self.client.sendData([4,fileName,self.participants])
        #     print("waiting response")

        #     data = self.client.getData()
        #     print(data)
        #     if(data == 9):
        #         print("got response")
        #         imageBytes = image.read(40960000)
        #         while(imageBytes):
        #             print("sending image...")
        #             self.client.sendImageAll(imageBytes)
        #             imageBytes = image.read(40960000)
        #     image.close()
    def closeSendImageThread(self):
        self.sendImg.stopThread()
        self.sendImg.quit()

    def openFileExplorer(self):
        file_filter = 'JPEG(*.jpg *.jpeg);; PNG(*.png)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select an image file to send",
            directory=os.getcwd(),
            filter= file_filter,
            initialFilter= "PNG(*.png)"
        )
        return response[0]

    def sendMessageAction(self):
        msg = self.leMessageBox.text()
        self.leMessageBox.clear() # clear line edit
        self.client.sendData([1,self.participants,msg]) # Send participants and message to server to send to other clients
    
    def exitApplication(self):
        self.msgThread.stopThread()
        self.msgThread.quit()
        self.close()

    def display(self):
        self.show()
        self.runMessagesThread()
    
    def showMessages(self,msg):
        self.teMessages.append(msg) # show messages on textedit 
    
    def showImage(self,dataArray):
        # modified from https://stackoverflow.com/questions/73634833/text-aside-and-below-an-image-in-pyqt5
        imageMsg = dataArray[2]
        imgFileName = dataArray[1]
        html = f'''<img src="{imgFileName}" width= "200" height="200">'''
        self.teMessages.append(imageMsg)
        self.teMessages.append("")
        self.teMessages.insertHtml(html)
        


        
    def closeEvent(self, event):
        self.closed.emit()
    
    # Thread to receive messages from participants
    def runMessagesThread(self):
        self.msgThread = MessagesThread(self.client)
        self.msgThread.message.connect(self.showMessages)
        self.msgThread.imageFileName.connect(self.showImage)
        self.msgThread.start()


# delete later
# if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    ex = OneToOneChatMenu()
#    ex.display();
#    sys.exit(app.exec_())