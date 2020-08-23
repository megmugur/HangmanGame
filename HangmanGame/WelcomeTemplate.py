import sys
from PySide2 import QtWidgets, QtCore, QtGui


class WelcomeClass(QtWidgets.QDialog):
    def __init__(self, parent=None):
        """Sets up the widgets in the Welcome template.
        :param: parent :  provides ability to connect to external applications like Maya.
        :param type: parent class.
        :return : None. """
        super(WelcomeClass, self).__init__(parent)
        self.welcome_layout = QtWidgets.QVBoxLayout()
        self.welcome_label = QtWidgets.QLabel("Welcome to Hangman! Are you ready?")
        self.enter_button = QtWidgets.QPushButton("Enter")
        self.welcome_page_method()

    def welcome_page_method(self):
        """Displays a welcome message, and an "Enter" button.
        :return: None.
        """
        self.enter_button.setMaximumWidth(300)
        self.welcome_layout.addWidget(self.welcome_label)
        self.welcome_layout.addWidget(self.enter_button)
        self.welcome_layout.setAlignment(QtCore.Qt.AlignCenter)
