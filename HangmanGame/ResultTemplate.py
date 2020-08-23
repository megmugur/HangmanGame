import sys
from PySide2 import QtWidgets, QtCore, QtGui


class ResultClass(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ResultClass, self).__init__(parent)
        self.result = "a"
        self.resultLayout = QtWidgets.QVBoxLayout()
        self.resultLabel = QtWidgets.QLabel()

    def resultMethod(self):
        if self.result == "success":
            self.resultLabel.setText("Well played. But damn, stop watching so many movies. Do some work.")
        elif self.result == "failure":
            self.resultLabel.setText("All those wrong guesses! SMH. Start over.")
        self.resultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.resultLayout.addWidget(self.resultLabel)
