import sys
from PySide2 import QtWidgets, QtCore, QtGui


class WelcomeClass(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(WelcomeClass, self).__init__(parent)
        self.welcomeLayout = QtWidgets.QVBoxLayout()
        self.welcomeLabel = QtWidgets.QLabel("Welcome to Hangman! Are you ready?")
        self.enterButton = QtWidgets.QPushButton("Enter")
        self.welcomePage()

    def welcomePage(self):
        self.enterButton.setMaximumWidth(300)
        self.welcomeLayout.addWidget(self.welcomeLabel)
        self.welcomeLayout.addWidget(self.enterButton)
        self.welcomeLayout.setAlignment(QtCore.Qt.AlignCenter)


