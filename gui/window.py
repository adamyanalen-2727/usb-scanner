from PyQt5.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("USB Scanner")
        self.setGeometry(500, 500, 500, 500)


#    main_text = QtWidgets.QLabel(window)

#    main_text.setText("USB Scanner")
#    main_text.move(250,250)
#    main_text.adjustSize()
#
#    button = QtWidgets.QPushButton(window)
#    button.move(250, 300)
#    button.setText("Click on me")
#    button.setFixedWidth(200)
#    button.clicked.connect(add_label)

