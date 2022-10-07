from PyQt5.QtWidgets import *
import sys
from frontEnd.ChatConnection import ChatConnectionMenu


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = ChatConnectionMenu()
   ex.display()
   sys.exit(app.exec_())