import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from gui.window import MainWindow
from gui.title import Title

def application():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    
    title = Title("USB Scanner", window)  
    
    window.show()
    
    sys.exit(app.exec_())
if __name__ == "__main__":
    application()
