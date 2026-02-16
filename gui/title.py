from PyQt5 import QtWidgets

def Title(title, window):
    title_text = QtWidgets.QLabel(window)
    title_text.setText(title)
    title_text.move(20,20)
