from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

from frontEnd.MessagesThread import MessagesThread
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
        #SEND IMAGE BUTTON

    
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
        
    def closeEvent(self, event):
        self.closed.emit()
    
    # Thread to receive messages from participants
    def runMessagesThread(self):
        self.msgThread = MessagesThread(self.client)
        self.msgThread.message.connect(self.showMessages)
        self.msgThread.start()


# delete later
# if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    ex = OneToOneChatMenu()
#    ex.display();
#    sys.exit(app.exec_())