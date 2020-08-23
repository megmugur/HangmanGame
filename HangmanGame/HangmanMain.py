import sys
from PySide2 import QtWidgets, QtGui, QtCore
import WelcomeTemplate, QuestionTemplate, ResultTemplate


class InviteDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):                      # When you use Maya, this parent will be Maya! That's its use.
        super(InviteDialog, self).__init__(parent)
        self.setWindowTitle("Hangman Beta © Meg Mugur 2020")
        self.setStyleSheet("background-color: #D1D1D1")
        self.initCreateStack()

        self.wlcmObj = WelcomeTemplate.WelcomeClass()
        self.wlcmObj.enterButton.pressed.connect(self.questionsPage)
        self.welcomePage()
        self.initQuestionPage()
        self.resltObj = ResultTemplate.ResultClass()
        self.initStack()

    def initCreateStack(self):
        self.gameStackWidget = QtWidgets.QStackedWidget()
        self.gameStackLayout = QtWidgets.QVBoxLayout()
        self.quesWidget = QtWidgets.QWidget()
        self.welcomeWidget = QtWidgets.QWidget()
        self.resultWidget = QtWidgets.QWidget()
        self.addWidgetsToStack()

    def initStack(self):
        self.gameStackWidget.setLayout(self.gameStackLayout)
        self.setLayout(self.gameStackLayout)
        self.gameStackLayout.addWidget(self.gameStackWidget)
        self.setFixedWidth(800)
        self.setFixedHeight(400)

    def initQuestionPage(self):
        # Question page:
        self.quesObj = QuestionTemplate.QuestionClass()                   # Have to declare the object here, otherwise, the button signal won't work.
        self.indexOfClickedBtn = -1
        self.question = "a"
        for index, btn in enumerate(self.quesObj.alphBtnList):
            self.quesObj.alphBtnList[index].clicked.connect(self.checkGuess)
        self.correctGuessCount = 0
        self.quesIndx = 0
        self.questionsList = ["Avatar", "Hulk", "Inception"]                # TODO: accommodate spaces, i.e., multiple words

    def addWidgetsToStack(self):
        self.gameStackWidget.addWidget(self.welcomeWidget)
        self.gameStackWidget.addWidget(self.quesWidget)
        self.gameStackWidget.addWidget(self.resultWidget)

    def welcomePage(self):
        self.welcomeWidget.setLayout(self.wlcmObj.welcomeLayout)
        self.gameStackWidget.setCurrentWidget(self.welcomeWidget)

    def questionsPage(self):
        self.question = self.questionsList[self.quesIndx]
        self.quesObj.quesPage(self.question)
        self.quesWidget.setLayout(self.quesObj.quesLayout)
        self.gameStackWidget.setCurrentWidget(self.quesWidget)

    def updateQuesPage(self):
        self.quesWidget.deleteLater()
        self.quesWidget = QtWidgets.QWidget()
        self.gameStackWidget.addWidget(self.quesWidget)
        self.question = self.questionsList[self.quesIndx]
        self.quesObj.quesPage(self.question)
        self.quesWidget.setLayout(self.quesObj.quesLayout)
        self.gameStackWidget.setCurrentWidget(self.quesWidget)

    def checkGuess(self):
        self.indexOfClickedBtn = self.quesObj.alphBtnList.index(self.sender())          # TODO: Use partial instead.
        self.quesObj.alphBtnList[self.indexOfClickedBtn].setStyleSheet("text-decoration: line-through")
        self.quesObj.alphBtnList[self.indexOfClickedBtn].setEnabled(False)
        if self.quesObj.alphList[self.indexOfClickedBtn].upper() in self.question.upper():
            self.checkIfCharInName()
        elif self.quesObj.healthLoss < 12:  # else reduce health
            self.quesObj.healthBarsList[self.quesObj.healthLoss].setStyleSheet("background-color : None")
            self.quesObj.healthLoss += 1
        else:                                          # TODO: handle this differently
            self.result = "failure"
            self.resultPage()

    def checkIfCharInName(self):
        for pos, char in enumerate(self.question):  # for every char in the question, check if
            # equal to the clicked char
            if self.quesObj.alphList[self.indexOfClickedBtn].upper() != char.upper():
                continue
            self.quesObj.ansTxtList[pos].setText(self.quesObj.alphList[self.indexOfClickedBtn].upper())
            self.correctGuessCount += 1
            if self.correctGuessCount != len(self.question):
                continue
            if self.quesIndx + 1 == len(self.questionsList):
                self.result = "success"
                self.resultPage()
                break
            else:  # Go to next question!
                self.nextQuestion()

    def nextQuestion(self):
        self.quesIndx += 1
        del self.quesObj
        self.indexOfClickedBtn = -1
        self.correctGuessCount = 0
        self.quesObj = QuestionTemplate.QuestionClass()
        self.updateQuesPage()
        for index, btn in enumerate(self.quesObj.alphBtnList):
            self.quesObj.alphBtnList[index].clicked.connect(self.checkGuess)

    def resultPage(self):
        self.resltObj.result = self.result
        self.resltObj.resultMethod()
        self.resultWidget.setLayout(self.resltObj.resultLayout)
        self.gameStackWidget.setCurrentWidget(self.resultWidget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    inviteDialog = InviteDialog()
    inviteDialog.exec_()

