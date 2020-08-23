import sys
from PySide2 import QtWidgets, QtCore, QtGui
import string


class QuestionClass(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(QuestionClass, self).__init__(parent)
        self.quesLayout = QtWidgets.QHBoxLayout()
        self.leftLayout = QtWidgets.QVBoxLayout()
        self.rightLayout = QtWidgets.QVBoxLayout()
        self.leftWidget = QtWidgets.QWidget()
        self.rightWidget = QtWidgets.QWidget()
        self.quesLabel = QtWidgets.QLabel("Guess the movie:")
        self.imgWidget = QtWidgets.QWidget()
        self.imgLayout = QtWidgets.QHBoxLayout()
        self.imgLabel = QtWidgets.QLabel()
        self.quesBoxesWidget = QtWidgets.QWidget()
        self.quesBoxesLayout = QtWidgets.QHBoxLayout()
        self.alphWidget = QtWidgets.QWidget()
        self.alphLayout = QtWidgets.QHBoxLayout()
        self.question = ""

        self.answerTextInitMethod()
        self.alphabetButtonInitMethod()
        self.healthWidgetInitMethod()

    def answerTextInitMethod(self):
        self.ansTxtList = []
        for t in range(0, 25):  # TODO: Hardcoded a limit to number of characters. Try to avoid.
            ts = str(t)
            exec("self.ans%sTxt = QtWidgets.QLabel()" % ts)  # execute list of commands of type:
            # [ self.ans1Txt = QtWidgets.QLabel() ]
            exec("self.ansTxtList.append(self.ans%sTxt)" % ts)  # create "ansTxtList", a list of text boxes
            # for movie name letters.

    def alphabetButtonInitMethod(self):
        self.alphList = [char for char in string.ascii_uppercase]
        self.alphBtnList = []
        for indx, btn in enumerate(self.alphList):
            exec("self.alph%sBtn = QtWidgets.QPushButton('%s')" % (btn, btn))
            exec("self.alphBtnList.append(self.alph%sBtn)" % btn)

    def healthWidgetInitMethod(self):
        self.healthBarsList = []
        for num in range(12):
            exec("self.healthBar%s = QtWidgets.QLabel()" % str(num))
            exec("self.healthBarsList.append(self.healthBar%s)" % str(num))
        self.colorList = ["greenyellow", "greenyellow", "#adf802", "#fcc006", "#fec615", "#f5bf03", "#fe02a2",
                          "#fe019a", "#ff0784", "#fa4224", "#f4320c", "#fe0002"]
        self.healthLoss = 0

    def quesPage(self, currentQuestion):
        self.question = currentQuestion
        self.quesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.addImgMethod()
        self.addAnsTextBoxesMethod()
        self.addAlphabetWidgetMethod()
        self.addHealthBarsMethod()
        self.quesLayout.addWidget(self.leftWidget)
        self.quesLayout.addWidget(self.rightWidget)
        self.leftWidget.setLayout(self.leftLayout)
        self.rightWidget.setLayout(self.rightLayout)
        self.leftLayout.addWidget(self.quesLabel)                                                              # q1Label
        self.leftLayout.addWidget(self.imgWidget)                                                             # imgLabel
        self.leftLayout.addWidget(self.quesBoxesWidget)
        self.leftLayout.addWidget(self.alphWidget)

    def addAnsTextBoxesMethod(self):
        self.quesBoxesWidget.setLayout(self.quesBoxesLayout)                                             # q1BoxesWidget
        self.quesBoxesLayout.setAlignment(QtCore.Qt.AlignCenter)

        for box in range(len(self.question)):
            self.quesBoxesLayout.addWidget(self.ansTxtList[box])
            self.ansTxtList[box].setStyleSheet("background-color : #FFF3F3")
            self.ansTxtList[box].setFixedWidth(15)
            self.ansTxtList[box].setAlignment(QtCore.Qt.AlignCenter)

    def addAlphabetWidgetMethod(self):
        self.alphWidget.setLayout(self.alphLayout)                                                          # alphWidget
        for btn in range(len(self.alphBtnList)):
            self.alphBtnList[btn].setMaximumWidth(20)
            self.alphLayout.addWidget(self.alphBtnList[btn])
            self.alphBtnList[btn].setFocusPolicy(QtCore.Qt.NoFocus)
            self.alphBtnList[btn].setStyleSheet("background-color : #FFF3F3")

    def addImgMethod(self):                                                                       # TODO : Change images
        self.imgWidget.setLayout(self.imgLayout)
        self.imgLayout.addWidget(self.imgLabel)
        self.imgLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.imgLabel.setPixmap("avatar.jpg")
        self.imgLabel.setMaximumWidth(300)
        self.imgLabel.setMaximumHeight(300)
        self.imgLabel.setAlignment(QtCore.Qt.AlignCenter)

    def addHealthBarsMethod(self):
        for indx, lbl in enumerate(self.healthBarsList):
            self.rightLayout.addWidget(lbl)
            lbl.setFixedWidth(50)
            lbl.setStyleSheet("background-color: " + self.colorList[indx])

