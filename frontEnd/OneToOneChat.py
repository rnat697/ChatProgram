from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class OneToOneChatMenu(QWidget):
    def __init__(self,client,participantName, participantDetails):
        super().__init__()
        #self.client = client
        #self.participantName = participantName
        #self.participantDetails = participantDetails
        self.initUI()
        self.display()
        self.connectActions()


    
    def initUI(self):
        #main window size and title
        self.setWindowTitle('One To One Chat')
        self.setGeometry(300, 300, 500, 500)  # (x,x,horizontal,vertical)
        self.setMinimumHeight(300)
        self.setMinimumWidth(200)

        chatWithName = "Chat with " + self.participantName

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

    def connectActions(self):
        self.btnExit.clicked.connect(self.exitApplication)
    
    def exitApplication(self):
        #self.thread1To1.quit()
        self.close()

    def display(self):
        self.show()
        #self.runMessagesThread()
    
    def runMessagesThread():
        print("aa")


# delete later
if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = OneToOneChatMenu()
   ex.display();
   sys.exit(app.exec_())