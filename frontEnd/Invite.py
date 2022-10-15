from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class InviteMenu(QWidget):
    inviteThreadFinished = pyqtSignal()
    def __init__(self,client, memberList,groupName, allClients):
        super().__init__()
        self.client = client
        self.memberList = memberList
        self.groupName = groupName
        self.nonMembers  = []
        self.allClients = allClients
        self.updateClientAvailInfo = True
        self.initUI()
        self.initAvailClients()
        self.display()
        self.connectActions()

    def initUI(self):
        #main window size and title
        self.setWindowTitle('Invite to Group Chat')
        self.setGeometry(700, 200, 400, 600) 
        self.setMinimumHeight(300)
        self.setMinimumWidth(200)
        
        groupInviteTitle = "Invite Clients to " + self.groupName
        
        # Labels for group chat
        self.groupInviteLabel = QLabel(groupInviteTitle,self)

        # TextEdit for showing messages
        self.tbClientsAvail = QTextBrowser(self)

        # buttons for send message, send image and exit
        self.btnCancel = QPushButton("Cancel", self)
        self.btnInvite = QPushButton("Invite", self)

        # Add labels, buttons and text edits to grid layout
        grid = QGridLayout(self)
        self.setLayout(grid)
        grid.addWidget(self.groupInviteLabel, 0,0,1,2)
        grid.addWidget(self.tbClientsAvail,1,0,1,2)
        grid.addWidget(self.btnCancel,3,1)
        grid.addWidget(self.btnInvite,3,0)


    def initAvailClients(self):
        print("Finding available clients")
        for client in self.allClients:
            i = 0
            print("CLIENT: ", client)
            for member in self.memberList:
                # if client is already a member of the group chat, skip
                print("Member: ", member)
                if(client[0] == member[0] and client[1] == member[1] and client[2] == member[2]):
                    break
                
                elif(i == len(self.memberList)-1): # if the end of the member list has been reaached and client hasn't been found, client must be a non member
                    self.nonMembers.append(client)
                i+=1
            print(self.nonMembers)
        # Initialise text browser with non members (available clients) found
        self.initClientsBox()

    def initClientsBox(self):
        print("Initialising client box")
        if(len(self.nonMembers)>0):
            for availableClients in self.nonMembers:
                name = availableClients[2]
                self.tbClientsAvail.append(name)
            self.updateClientAvailInfo = False # update flag for text browser cursor position changed

    def display(self):
        self.show()

    def connectActions(self):
        self.btnCancel.clicked.connect(self.exitApplication)
        self.btnInvite.clicked.connect(self.inviteClients)
        self.tbClientsAvail.cursorPositionChanged.connect(self.onTextBrowserCursorPosChanged)

    def onTextBrowserCursorPosChanged(self):
        # from https://stackoverflow.com/questions/60139804/highlighting-lines-on-qtextedit-document
        # and https://stackoverflow.com/questions/22698105/qtextbrowser-how-to-highlight-a-clicked-line

        if(self.updateClientAvailInfo == False): # Only highlight when user is the one clicking on the lines, not when updating the client info by appending to text browser
            fmt =  QTextBlockFormat()
            fmt.setBackground(QColor('lightGray'))
            fmt_normal = QTextBlockFormat()
            fmt_normal.setBackground(QColor('white'))

            cursorAvail = self.tbClientsAvail.textCursor()
            self.blockNum = cursorAvail.blockNumber() # save line number
            print("block number Group: " + str(self.blockNum) ) 
            
            # Resets the highlight colour to white for all lines
            cursorAvail.select(QTextCursor.Document)
            cursorAvail.setBlockFormat(fmt_normal)

            # Create new cursor so that it only highlights the line that has been clicked
            cursor = QTextCursor(self.tbClientsAvail.document().findBlockByNumber(self.blockNum))
            cursor.setBlockFormat(fmt)
        else:
            self.blockNum = -1

    def inviteClients(self):
        if(self.blockNum != -1):
            receiver = self.nonMembers[self.blockNum]
            print("Sending invite to: ",receiver)
            
            # format is 3 flag, receiver, groupName
            self.client.sendData([3,receiver,self.groupName])

        
    def exitApplication(self):
        self.close()
    
   