from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
from frontEnd.GroupMessagesThread import GroupMessagesThread

class GroupChatMenu(QWidget):
    closed = pyqtSignal() # For chat Connected to know if window is closed, modified from https://stackoverflow.com/a/67519553
    def __init__(self,client,clientDetails,memberList,groupName):
        super().__init__()
        self.client = client
        self.clientDetails = clientDetails
        self.memberList = memberList
        self.groupName = groupName
        self.clientName = self.clientDetails[2]
        self.hostName = self.memberList[0][2]

        self.initUI()
        self.initMemberBox()
        self.display()
        self.connectActions()

    def initUI(self):
        #main window size and title
        self.setWindowTitle('One To One Chat')
        self.setGeometry(600, 200, 800, 700) 
        self.setMinimumHeight(300)
        self.setMinimumWidth(200)

        # Labels for group chat
        self.groupNameLabel = QLabel(self.groupName,self)
        self.memberLabel = QLabel("Members", self)

        # TextEdit for showing messages
        self.teGroupMessages = QTextEdit(self)
        self.teGroupMessages.setReadOnly(True)
        self.tbMembers = QTextBrowser(self)

        # Line Edit for user writing messages
        self.leMessageBoxGroup =QLineEdit(self)

        # buttons for send message, send image and exit
        self.btnSendMsg = QPushButton("Send", self)
        self.btnSendImg = QPushButton("Send Image", self)
        self.btnExit = QPushButton("Exit", self)
        self.btnInvite = QPushButton("Invite", self)

        # Add labels, buttons and text edits to grid layout
        grid = QGridLayout(self)
        self.setLayout(grid)
        grid.setColumnStretch(0,7)
        grid.setSpacing(3)
        grid.addWidget(self.groupNameLabel, 0, 0,1,7)
        grid.addWidget(self.memberLabel,0,7)
        grid.addWidget(self.teGroupMessages,1,0,1,7)
        grid.addWidget(self.tbMembers,1,7)
        grid.addWidget(self.leMessageBoxGroup,2,0,1,4)
        grid.addWidget(self.btnSendMsg,2,4)
        grid.addWidget(self.btnSendImg,2,5)
        grid.addWidget(self.btnInvite,3,7)
        grid.addWidget(self.btnExit,3,0,1,6)


    def display(self):
        self.show()
        self.runGroupMessagesThread()

    def connectActions(self):
        self.btnExit.clicked.connect(self.exitApplication)
        self.btnSendMsg.clicked.connect(self.sendMessageAction)
        self.btnInvite.clicked.connect(self.showInviteMenu)

    def showInviteMenu(self):
        print("invite")
    
    def sendMessageAction(self):
        msg = self.leMessageBoxGroup.text()
        self.leMessageBoxGroup.clear() # clear line edit
        self.client.sendData([1,self.memberList,msg]) # send to server
        
    def exitApplication(self):
        self.groupMsgThread.stopThread()
        self.groupMsgThread.quit()
        self.close()
    
    def initMemberBox(self):
        for member in self.memberList:
            name = member[2]

            # Edit name for formatting
            if(name == self.clientName and name == self.hostName):
                name+= " (Host)(Me)"
            elif(name == self.hostName):
                name += " (Host)"
            elif(name == self.clientName):
                name += " (Me)"
            
            self.tbMembers.append(name)
    
    def updateMemberList(self,memList):
        self.tbMembers.clear()
        self.memberList.clear()
        for member in memList:
            self.memberList.append(member)
            name = member[2]

            # Edit name for formatting
            if(name == self.clientName and name == self.hostName):
                name+= " (Host)(Me)"
            elif(name == self.hostName):
                name += " (Host)"
            elif(name == self.clientName):
                name += " (Me)"
                
            self.tbMembers.append(name)


    def showMessages(self,msg):
        self.teGroupMessages.append(msg) # show messages on textedit 
        
    def closeEvent(self, event):
        self.closed.emit()
     
     # Thread to receive messages from members and receive updated member list
    def runGroupMessagesThread(self):
        self.groupMsgThread = GroupMessagesThread(self.client)
        self.groupMsgThread.message.connect(self.showMessages)
        self.groupMsgThread.members.connect(self.updateMemberList)
        self.groupMsgThread.start()


# delete later
# if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    ex = GroupChatMenu()
#    ex.display()
#    sys.exit(app.exec_())