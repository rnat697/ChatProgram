from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os

import sys
from frontEnd.GroupMessagesThread import GroupMessagesThread
from frontEnd.Invite import InviteMenu
from frontEnd.SendImagesThread import SendImagesThread

class GroupChatMenu(QWidget):
    closed = pyqtSignal() # For Chat Connected Menu to know if window is closed, modified from https://stackoverflow.com/a/67519553
    def __init__(self,client,clientDetails,memberList,groupName, allClients):
        super().__init__()
        self.client = client
        self.clientDetails = clientDetails
        self.memberList = memberList
        self.groupName = groupName
        self.clientName = self.clientDetails[2]
        self.hostName = self.memberList[0][2]
        self.allClients = allClients

        self.initUI()
        self.initMemberBox()
        self.display()
        self.connectActions()

    def initUI(self):
        #main window size and title
        self.setWindowTitle('Group Chat')
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
        self.btnSendImg.clicked.connect(self.sendImageAction)

    def sendImageAction(self): 
        imageDir = self.openFileExplorer()

        if(imageDir): # check if response is not empty (if it isn't that means the user has picked an image)
            image = open(imageDir,"rb")
            print('img dir: ', imageDir)
            fileName = os.path.basename(imageDir)
            print("fileName: ", fileName)
            fileSize = os.path.getsize(imageDir)

            # using threads to send the image to the server. It will download the images to the ChatProgram parent folder
            self.sendImg = SendImagesThread(self.client,image,self.memberList,fileName,fileSize)
            self.sendImg.finished.connect(self.closeSendImageThread)
            self.sendImg.start()
    
    def closeSendImageThread(self):
        self.sendImg.stopThread()
        self.sendImg.quit()

    def openFileExplorer(self):
        # Opens a file explorer for user to find an image to send
        file_filter = 'JPEG(*.jpg *.jpeg);; PNG(*.png)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select an image file to send",
            directory=os.getcwd(),
            filter= file_filter,
            initialFilter= "PNG(*.png)"
        )
        return response[0]
     


    def showInviteMenu(self):
        self.inviteMenu = InviteMenu(self.client,self.memberList,self.groupName,self.allClients)
   
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
    
    def showImage(self,dataArray):
        # modified from https://stackoverflow.com/questions/73634833/text-aside-and-below-an-image-in-pyqt5
        imageMsg = dataArray[2]
        imgFileName = dataArray[1]
        html = f'''<img src="{imgFileName}" width= "200" height="200">'''
        self.teGroupMessages.append(imageMsg) # shows the message - [client name]: Sent an image - image file name
        self.teGroupMessages.append("")
        self.teGroupMessages.insertHtml(html)
        
        
    def closeEvent(self, event):
        self.closed.emit()
     
     # Thread to receive messages from members and receive updated member list
    def runGroupMessagesThread(self):
        self.groupMsgThread = GroupMessagesThread(self.client)
        self.groupMsgThread.message.connect(self.showMessages)
        self.groupMsgThread.members.connect(self.updateMemberList)
        self.groupMsgThread.imageFileName.connect(self.showImage)
        self.groupMsgThread.start()


# delete later
# if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    ex = GroupChatMenu()
#    ex.display()
#    sys.exit(app.exec_())