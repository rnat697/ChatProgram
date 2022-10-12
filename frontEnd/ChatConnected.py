from http import client
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
import sys
import threading
from backEnd.client import ChatClient
from PyQt5.QtCore import QThread, pyqtSignal, QObject

from frontEnd.GroupAndClientsThread import GroupAndClientsThread
from frontEnd.OneToOneChat import OneToOneChatMenu
from time import sleep



class ChatConnectedMenu(QWidget):
    def __init__(self,client,clientName):
        super().__init__()
        self.client = client
        self.clientName = clientName
        self.clientInfoList = []
        self.groupNameList = []
        self.groupsMemberList = []
        self.blockNumClient = -1
        self.clientIndex = -1
        self.blockNumGroup = -1

        # self.setFocus()
        # qApp.focusChanged.connect(self.onFocusChanged)

        self.initUI()
        self.display()
        self.connectActions()
 
    def initUI(self):
        #main window size and title
        self.setWindowTitle('Chat Connected')
        self.setGeometry(800, 300, 400, 500)  # (x,x,horizontal,vertical)
        self.setMinimumHeight(300)
        self.setMinimumWidth(200)
        self.highlightLine= False
        self.updateClientInfo = True
        # Labels for connected clients and chat rooms
        self.clientsLabel = QLabel('Connected Clients', self)
        self.groupChatsLabel = QLabel('Group Chats', self)

        # text browser for showing clients and group chats
        self.tbClients = QTextBrowser(self)
        self.tbGroupChats = QTextBrowser(self)
        
        # Buttons for exitting, 1:1 chat, create group chat, join group chat
        self.btnExit = QPushButton("Exit",self)
        self.btnOneToOne = QPushButton("1 : 1 Chat",self)
        self.btnCreateGroup = QPushButton("Create Group",self)
        self.btnJoinGroup = QPushButton("Join Group",self)

        # Add labels, buttons and text browsers to grid layout
        grid = QGridLayout(self)
        self.setLayout(grid)
        grid.addWidget(self.clientsLabel, 0, 0)
        grid.addWidget(self.tbClients, 1, 0)
        grid.addWidget(self.btnOneToOne, 1, 1)
        grid.addWidget(self.groupChatsLabel, 2,0)
        grid.addWidget(self.tbGroupChats,3,0,2,1)
        grid.addWidget(self.btnCreateGroup,2,1)
        grid.addWidget(self.btnJoinGroup,3,1)
        grid.addWidget(self.btnExit,5,1)
    


    def onTextBrowserClientCursorPosChanged(self):
        # from https://stackoverflow.com/questions/60139804/highlighting-lines-on-qtextedit-document
        # and https://stackoverflow.com/questions/22698105/qtextbrowser-how-to-highlight-a-clicked-line

        if(self.updateClientInfo == False): # Only highlight when user is the one clicking on the lines, not when updating the client info by appending to text browser

            self.fmt =  QTextBlockFormat()
            self.fmt.setBackground(QtGui.QColor('lightGray'))
            self.fmt_normal = QTextBlockFormat()
            self.fmt_normal.setBackground(QtGui.QColor('white'))

            cursorClient = self.tbClients.textCursor()
            self.blockNumClient = cursorClient.blockNumber() # save line number
            print("block numberClient: " + str(self.blockNumClient) ) 
            
            # Resets the highlight colour to white for all lines
            cursorClient.select(QTextCursor.Document)
            cursorClient.setBlockFormat(self.fmt_normal)

            # Create new cursor so that it only highlights the line that has been clicked
            cursor = QTextCursor(self.tbClients.document().findBlockByNumber(self.blockNumClient))
            cursor.setBlockFormat(self.fmt)
        else:
            self.blockNumClient = -1
        
    def onTextBrowserGroupCursorPosChanged(self):
        # from https://stackoverflow.com/questions/60139804/highlighting-lines-on-qtextedit-document
        # and https://stackoverflow.com/questions/22698105/qtextbrowser-how-to-highlight-a-clicked-line

        if(self.updateGroupInfo == False): # Only highlight when user is the one clicking on the lines, not when updating the client info by appending to text browser

            self.fmt =  QTextBlockFormat()
            self.fmt.setBackground(QtGui.QColor('lightGray'))
            self.fmt_normal = QTextBlockFormat()
            self.fmt_normal.setBackground(QtGui.QColor('white'))

            cursorGroup = self.tbGroupChats.textCursor()
            self.blockNumGroup = cursorGroup.blockNumber() # save line number
            print("block number Group: " + str(self.blockNumGroup) ) 
            
            # Resets the highlight colour to white for all lines
            cursorGroup.select(QTextCursor.Document)
            cursorGroup.setBlockFormat(self.fmt_normal)

            # Create new cursor so that it only highlights the line that has been clicked
            cursor = QTextCursor(self.tbGroupChats.document().findBlockByNumber(self.blockNumGroup))
            cursor.setBlockFormat(self.fmt)
        else:
            self.blockNumGroup = -1
    

    def connectActions(self):
        self.btnExit.clicked.connect(self.exitApplication)
        self.tbClients.cursorPositionChanged.connect(self.onTextBrowserClientCursorPosChanged)
        self.btnOneToOne.clicked.connect(self.connectToOneToOneChat)
        self.tbGroupChats.cursorPositionChanged.connect(self.onTextBrowserGroupCursorPosChanged)
        self.btnCreateGroup.clicked.connect(self.createGroup)
        self.btnJoinGroup.clicked.connect(self.joinGroup)
        # to add btnCreateGroupChat, btnJoinGroup, btnOneToOne
    
    def createGroup(self):
        self.client.sendData(3) # tells server that we want to create a group
    
    def joinGroup(self):
        groupName = self.groupNameList[self.blockNumGroup]
        groupMembers = self.groupsMemberList[self.blockNumGroup]
        clientInfo = self.clientInfoList[self.clientIndex]
        clientExists = False
        groupHost = groupMembers[0][2]
        print("HOST: ",groupHost)
        # Check if client is a member of the group chat
        for member in groupMembers:
            if(member[0] ==  clientInfo[0] and member[1] == clientInfo[1] and member[2] == clientInfo[2]):
                clientExists = True
                break
        
        # if client is not a member of the chat, send membership request to server
        if(not clientExists):
            self.client.sendData([2,groupName,clientInfo,groupHost])
            print("membership requested")
            sleep(0.8)
        # connect to group chat
        print("connecting to chat")


    def exitApplication(self):
        self.threadClients.quit()
        self.client.cleanup() # close client socket
        self.close()
    
    def connectToOneToOneChat(self):
        if((self.blockNumClient != -1) and (self.blockNumClient != self.clientIndex)):
            self.threadClients.pauseThread()
            # find corresponding participant name and details
            targetDetails = self.clientInfoList[self.blockNumClient]
            clientDetails = self.clientInfoList[self.clientIndex]
            self.oneToOneChat = OneToOneChatMenu(self.client, clientDetails, targetDetails)
            self.oneToOneChat.closed.connect(self.unpauseThread) # Using signal in OneToChatMenu, check if closed signal has been emitted
           
    
    def unpauseThread(self): # Unpause thread when oneToOne chat is closed
        # Modified from https://stackoverflow.com/a/67519553
        self.threadClients.restart()

    def display(self):
        self.show()
        self.runGroupNClientsThread()

    def showClientInfo(self, info):
        # Goes through the client dictionary and adds the name of the clients to the text browser
        self.updateClientInfo = True
        self.tbClients.clear() # clears it first
        self.clientInfoList.clear()
        i = 0
        if(len(info) >0):
            for items in info:
                print("info: ", items)
                self.clientInfoList.append(items) # add to list for 1:1 chat reference
                name = items[2]
                if(name == self.clientName):
                    self.clientIndex = i # stores index number of current client
                    # Add a "me" indicator if name in client info list is the same as the current client
                    meIndicatorName = name + " (me)"
                    self.tbClients.append(meIndicatorName)
                else:
                    self.tbClients.append(name)
                i = i +1
        self.updateClientInfo = False

    
    def showGroupsInfo(self,info):
        # Goes through the group dictionary and adds the name of the groups to the text browser
        self.updateGroupInfo = True
        self.tbGroupChats.clear() # clears it first to avoid duplications
        self.groupNameList.clear()
        self.groupsMemberList.clear()
        for items in info.keys():
            print("from group: ", items)
            if(not items): # if empty
                break
            else:
                groupName = items[0]
                self.groupNameList.append(groupName)
                print("GROUP NAME: ", groupName)
                self.tbGroupChats.append(groupName)
        
        for members in info.values():
            print("MEMBERS: ", members)  
            self.groupsMemberList.append(members)   
        self.updateGroupInfo = False


    def runGroupNClientsThread(self):
        self.threadClients = GroupAndClientsThread(self.client)
        self.threadClients.clientNames.connect(self.showClientInfo)
        self.threadClients.groupNames.connect(self.showGroupsInfo)
        self.threadClients.start()

# delete later
# if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    ex = ChatConnectionMenu()
#    ex.display();
#    sys.exit(app.exec_())