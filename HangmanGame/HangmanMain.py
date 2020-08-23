import sys
from PySide2 import QtWidgets, QtGui, QtCore
import WelcomeTemplate, QuestionTemplate, ResultTemplate


class InviteDialog(QtWidgets.QDialog):
    """ Dialog for the game, enables the logical functioning """

    def __init__(self, parent=None):
        """ Initializes the dialog by creating the necessary UI framework.
        :param parent: provides ability to connect to external applications like Maya.
        :param type: parent class.
        :return None."""
        super(InviteDialog, self).__init__(parent)
        self.setWindowTitle("Hangman Beta © Meg Mugur 2020")
        self.setStyleSheet("background-color: #D1D1D1")
        self.init_create_stack_method()

        self.welcome_object = WelcomeTemplate.WelcomeClass()
        self.welcome_object.enter_button.pressed.connect(self.questions_page_method)
        self.welcome_page_method()
        self.init_question_page_method()
        self.result_object = ResultTemplate.ResultClass()
        self.init_stack_method()

    def init_create_stack_method(self):
        """Creates a stack of widgets for the different pages to be displayed.
        :return : None."""
        self.game_stack_widget = QtWidgets.QStackedWidget()
        self.game_stack_layout = QtWidgets.QVBoxLayout()
        self.question_widget = QtWidgets.QWidget()
        self.welcome_widget = QtWidgets.QWidget()
        self.result_widget = QtWidgets.QWidget()
        self.add_widgets_to_stack_method()

    def init_stack_method(self):
        """Basic setting up of the stack.
        :return : None."""
        self.setLayout(self.game_stack_layout)
        self.game_stack_layout.addWidget(self.game_stack_widget)
        self.setFixedWidth(800)
        self.setFixedHeight(400)

    def init_question_page_method(self):
        """Initializes the question page by creating an object of the QuestionClass type.
        Signal-slot connections for all buttons are made during initialization.
        Questions are loaded into a list.
        :return: None.
        TODO: accommodate spaces, i.e., multiple words
        """
        self.question_object = QuestionTemplate.QuestionClass()
        self.index_of_clicked_button = -1
        self.question = ""
        for index, button in enumerate(self.question_object.alphabet_button_list):
            self.question_object.alphabet_button_list[index].clicked.connect(self.check_guess_method)
        self.correct_guess_count = 0
        self.question_index = 0
        self.questions_list = ["Avatar", "Hulk"]

    def add_widgets_to_stack_method(self):
        """ Pages are added to the stack.
        :return: None.
        """
        self.game_stack_widget.addWidget(self.welcome_widget)
        self.game_stack_widget.addWidget(self.question_widget)
        self.game_stack_widget.addWidget(self.result_widget)

    def welcome_page_method(self):
        """Basic setting up of the Welcome page.
        :return : None."""
        self.welcome_widget.setLayout(self.welcome_object.welcome_layout)
        self.game_stack_widget.setCurrentWidget(self.welcome_widget)

    def questions_page_method(self):
        """Basic setting up of the Question page.
        :return : None.
        TODO : check if questions list is empty """
        self.question = self.questions_list[self.question_index]
        self.question_object.question_page_method(self.question)
        self.question_widget.setLayout(self.question_object.question_layout)
        self.game_stack_widget.setCurrentWidget(self.question_widget)

    def init_next_question_method(self):
        """Initialization and basic setting up of the next Question page.
        Deletes the old question widget, creates a new one, adds to stack, and sets as current page.
        :return : None."""
        self.question_widget.deleteLater()
        self.question_widget = QtWidgets.QWidget()
        self.game_stack_widget.addWidget(self.question_widget)
        self.question = self.questions_list[self.question_index]
        self.question_object.question_page_method(self.question)
        self.question_widget.setLayout(self.question_object.question_layout)
        self.game_stack_widget.setCurrentWidget(self.question_widget)

    def check_guess_method(self):
        """Checks if the alphabet clicked on, exists in movie name.
        If it exists, fills out the corresponding boxes with that letter.
        If it exists, and the entire movie name has been filled, goes to next question.
        If it does not exist, reduces health.
        If it does not exist, and health is already zero, ends the game.
        :return : None.
        TODO: Use partial instead of sender().
        TODO: When game ends, ask to start over."""
        self.index_of_clicked_button = self.question_object.alphabet_button_list.index(self.sender())
        self.question_object.alphabet_button_list[self.index_of_clicked_button].setStyleSheet("text-decoration: line-through")
        self.question_object.alphabet_button_list[self.index_of_clicked_button].setEnabled(False)
        if self.question_object.alphabet_list[self.index_of_clicked_button].upper() in self.question.upper():
            self.find_char_in_name_method()
        elif self.question_object.health_loss < 12:
            self.question_object.health_bars_list[self.question_object.health_loss].setStyleSheet("background-color : None")
            self.question_object.health_loss += 1
        else:
            self.result = "failure"
            self.result_page_method()

    def find_char_in_name_method(self):
        """Checks where the selected alphabet exists in the name of the movie.
        When the alphabet is found, increments correct_guess_count.
        Once current_guess_count matches the length of the movie name, goes to next question.
        If questions list is exhausted, proceeds to ending the game.
        :return : None."""
        for pos, char in enumerate(self.question):  # for every char in the question, check if
            # equal to the clicked char
            if self.question_object.alphabet_list[self.index_of_clicked_button].upper() != char.upper():
                continue
            self.question_object.answer_text_list[pos].setText(self.question_object.alphabet_list[self.index_of_clicked_button].upper())
            self.correct_guess_count += 1
            if self.correct_guess_count != len(self.question):
                continue
            if self.question_index + 1 == len(self.questions_list):
                self.result = "success"
                self.result_page_method()
                break
            self.next_question_method()

    def next_question_method(self):
        """Resets some parameters for new question. Sets up a new question page.
        :return : None."""
        self.question_index += 1
        del self.question_object
        self.index_of_clicked_button = -1
        self.correct_guess_count = 0
        self.question_object = QuestionTemplate.QuestionClass()
        self.init_next_question_method()
        for index, button in enumerate(self.question_object.alphabet_button_list):
            self.question_object.alphabet_button_list[index].clicked.connect(self.check_guess_method)

    def result_page_method(self):
        """Sets the result message label, and displays the result page.
        :return : None."""
        self.result_object.result = self.result
        self.result_object.result_method()
        self.result_widget.setLayout(self.result_object.result_layout)
        self.game_stack_widget.setCurrentWidget(self.result_widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    invite_dialog = InviteDialog()
    invite_dialog.exec_()

