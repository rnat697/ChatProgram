from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from frontEnd.ChatConnected import ChatConnectedMenu
from backEnd.client import ChatClient

class ChatConnectionMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.display()
        self.connectActions()
    
    def initUI(self):
        #main window size and title
        self.setWindowTitle('Connect To Chat')
        self.setGeometry(800, 300, 450, 330) 
        self.setMinimumHeight(200)
        self.setMinimumWidth(300)

       # Labels for IP address, Port and nickname 
        self.IPLabel = QLabel('IP Address', self)
        self.portLabel = QLabel('Port', self)
        self.nicknameLabel = QLabel('Nickname', self)

        # Line edits for IP address, Port and nickname
        self.IPLineEdit =QLineEdit(self)
        self.portLineEdit =QLineEdit(self)
        self.nicknameLineEdit =QLineEdit(self)
        
        # Buttons for connecting and exiting
        self.connectBtn = QPushButton("Connect",self)
        self.exitBtn = QPushButton("Exit", self)

        # Add labels, buttons and line edits to grid layout
        grid = QGridLayout(self)
        self.setLayout(grid)
        grid.addWidget(self.IPLabel, 0, 0)
        grid.addWidget(self.IPLineEdit, 0, 1)
        grid.addWidget(self.portLabel, 1, 0)
        grid.addWidget(self.portLineEdit, 1, 1)
        grid.addWidget(self.nicknameLabel, 2, 0)
        grid.addWidget(self.nicknameLineEdit, 2, 1)
        grid.addWidget(self.connectBtn,4,2)
        grid.addWidget(self.exitBtn,4,3)
        
        # error dialogue for incorrect port number or address
        self.error_dialog = QErrorMessage()

    

    def connectToServer(self):
        address = self.IPLineEdit.text()
        name = self.nicknameLineEdit.text()
        port = self.portLineEdit.text()

        # check if line edits are not empty
        if(address != "localhost" or port != "9988" or name ==""):
            self.error_dialog.showMessage('Incorrect address or port. Correct address and port format - Address: localhost  Port: 9988. Name can not be empty')
        else:
            print(address,name,port)
            self.client = ChatClient(name,port,address) # connects client socket to server
            self.connectionMenu = ChatConnectedMenu(self.client,name)

    def connectActions(self):
        self.exitBtn.clicked.connect(QCoreApplication.instance().quit)
        self.connectBtn.clicked.connect(self.connectToServer)
   

    def display(self):
        self.show()

