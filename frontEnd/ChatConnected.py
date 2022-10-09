from tkinter import E
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import threading
from backEnd.client import ChatClient
from PyQt5.QtCore import QThread, pyqtSignal, QObject

from frontEnd.GroupAndClientsThread import GroupAndClientsThread




class ChatConnectedMenu(QWidget):
    def __init__(self,client):
        super().__init__()
        self.client = client
        self.initUI()
        self.display()
        self.connectActions()


    
    def initUI(self):
        #main window size and title
        self.setWindowTitle('Chat Connected')
        self.setGeometry(300, 300, 400, 500)  # (x,x,horizontal,vertical)
        self.setMinimumHeight(300)
        self.setMinimumWidth(200)

        # Labels for connected clients and chat rooms
        self.clientsLabel = QLabel('Connected Clients', self)
        self.groupChatsLabel = QLabel('Group Chats', self)

        # TextBrowsers for showing clients and group chats
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

    def connectActions(self):
        self.btnExit.clicked.connect(self.exitApplication)
        # to add btnCreateGroupChat, btnJoinGroup, btnOneToOne
    
    def exitApplication(self):
        # self.worker.stop()
        # self.thread.quit()
        # self.thread.wait()
        
        self.threadClients.quit()
        self.client.cleanup()
        self.close()


    def display(self):
        self.show()
        self.runGroupNClientsThread()

    def showClientInfo(self, info):
        # Goes through the client dictionary and adds the name of the clients to the text browser
        self.tbClients.clear() # clears it first
        if(len(info) >0):
            for items in info:
                name = items[2]
                print("NAME: ", name)
                self.tbClients.append(name)
    
    def showGroupsInfo(self,info):
        # Goes through the group dictionary and adds the name of the groups to the text browser
        self.tbGroupChats.clear() # clears it first to avoid duplications
        for items in info.values():
            print("from group: ", items)
            if(not items): # if empty
                break
            else:
                groupName = items[1]
                print("GROUP NAME: ", groupName)
                self.tbGroupChats.append(groupName)

    def runGroupNClientsThread(self):
       
        # self.thread = QThread()
        # self.worker = GroupAndClientsThread(self.client)
        # self.worker.moveToThread(self.thread)
        # self.worker.clientNames.connect(self.showClientInfo)
        # self.worker.groupNames.connect(self.showGroupsInfo)
        # self.worker.finished.connect(self.thread.quit)
        # self.thread.started.connect(self.worker.run)
        # self.thread.finished.connect(self.exitApplication)
        # self.worker.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)
        # self.thread.start()


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