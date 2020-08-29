import sys
from PySide2 import QtWidgets, QtGui, QtCore
import WelcomeTemplate, QuestionTemplate, ResultTemplate
import json

class InviteDialog(QtWidgets.QDialog):
    """ Sets up the dialog widget for the game, includes all the game logic """

    def __init__(self, parent=None):
        """ Initializes the dialog by creating the necessary UI framework.
        :param parent: provides ability to connect to external applications like Maya.
        :type: QWidget.
        """
        super(InviteDialog, self).__init__(parent)
        self.setWindowTitle("Hangman Beta © Meg Mugur 2020")
        self.setStyleSheet("background-color: #D1D1D1")

        self.create_game_stack_widget()
        self.setLayout(self.game_stack_layout)

        self.initialize_welcome_page()
        self.initialize_question_page()

        self.setup_welcome_page()

    def create_game_stack_widget(self):
        """Creates a stack of widgets for the different pages to be displayed."""
        self.game_stack_layout = QtWidgets.QVBoxLayout()
        self.game_stack_widget = QtWidgets.QStackedWidget()
        self.game_stack_layout.addWidget(self.game_stack_widget)

        self.question_page_widget = QtWidgets.QWidget()
        self.welcome_page_widget = QtWidgets.QWidget()
        self.result_page_widget = QtWidgets.QWidget()

        self.game_stack_widget.addWidget(self.welcome_page_widget)
        self.game_stack_widget.addWidget(self.question_page_widget)
        self.game_stack_widget.addWidget(self.result_page_widget)

        self.stack_design()

    def stack_design(self):
        """Basic design settings of the stack."""
        self.setFixedWidth(800)
        self.setFixedHeight(600)

    def initialize_welcome_page(self):
        """Basic setting up of the Welcome page:
        Creates the welcome layout using the WelcomeTemplate, makes signal-slot connections"""
        self.welcome_object = WelcomeTemplate.WelcomeClass()
        self.welcome_object.enter_button.pressed.connect(self.setup_question_page)

    def setup_welcome_page(self):
        """sets the layout to welcome_page_widget,
        and adds the welcome_page_widget to the game_stack_widget"""
        self.welcome_page_widget.setLayout(self.welcome_object.welcome_layout)
        self.game_stack_widget.setCurrentWidget(self.welcome_page_widget)

    def initialize_question_page(self):
        """Initializes the question page by creating an object of the QuestionClass type.
        Signal-slot connections for all buttons are made during initialization.
        Questions are loaded from the database into a list.
        """
        self.question_object = QuestionTemplate.QuestionClass()
        self.index_of_clicked_button = -1
        for index, button in enumerate(self.question_object.alphabet_button_list):
            self.question_object.alphabet_button_list[index].clicked.connect(self.examine_guessed_alphabet)
        self.allowed_attempts = 9
        self.correct_guess_count = 0
        self.question_index = 0
        self.image_path = ""
        self.questions_list = []
        database_file = open("Database/MoviesDatabase.json")
        try:
            self.questions_dict = json.load(database_file)
            for movie_names in self.questions_dict:
                self.questions_list.append(movie_names)
            print(self.questions_list)
        except ValueError as json_error:
            print("Error: ", json_error)
            exit()

        if self.questions_list is None:
            self.result = "empty"
            self.setup_result_page()
        self.question = self.questions_list[0]

    def setup_question_page(self):
        """Basic setting up of the Question page.
        TODO : check if questions list is empty """
        self.question = self.questions_list[self.question_index]
        self.question_object.setup_question_layout(self.question)
        self.question_page_widget.setLayout(self.question_object.question_layout)
        self.game_stack_widget.setCurrentWidget(self.question_page_widget)
        self.setup_clue_image()

    def setup_clue_image(self):
        self.image_path = "Images/" + self.question.replace(" ", "") + "/"\
                          + self.questions_dict[self.question][:-4].replace(" ", "") + "_"\
                          + str(self.allowed_attempts - self.question_object.health_loss)\
                          + self.questions_dict[self.question][-4:]
        self.question_object.image_label.setPixmap(self.image_path)

    def examine_guessed_alphabet(self):
        """Checks if the alphabet clicked on, exists in movie   name.
        If it exists, fills out the corresponding boxes with that letter.
        If it exists, and the entire movie name has been filled, goes to next question.
        If it does not exist, reduces health.
        If it does not exist, and health is already zero, ends the game.
        TODO: Use partial instead of sender().
        TODO: When game ends, ask to start over.
        TODO: When movie has been guessed, display "correct", and display a "next" button."""
        self.index_of_clicked_button = self.question_object.alphabet_button_list.index(self.sender())
        self.clicked_button = self.question_object.alphabet_button_list[self.index_of_clicked_button]
        self.clicked_button.setEnabled(False)
        self.clicked_button.setStyleSheet("border : 0")
        if self.question_object.alphabet_list[self.index_of_clicked_button].upper() in self.question.upper():
            self.find_alphabet_position()
        elif self.question_object.health_loss < self.allowed_attempts:
            self.question_object.health_loss += 1
            self.setup_clue_image()
        else:
            self.result = "failure"
            self.setup_result_page()

    def find_alphabet_position(self):
        """Looks for the position of the selected alphabet in the movie name.
        Each time the alphabet is found, increments correct_guess_count.
        Once the entire movie name has been guessed correctly, goes to next question.
        If questions list is exhausted, proceeds to ending the game."""
        for pos, char in enumerate(self.question):
            if self.question_object.alphabet_list[self.index_of_clicked_button].upper() != char.upper():
                continue
            self.question_object.answer_letters_list[pos].setText(self.question_object.alphabet_list[self.index_of_clicked_button].upper())
            self.correct_guess_count += 1
            if self.correct_guess_count != len(self.question) - self.question.count(" "):
                continue
            if self.question_index + 1 == len(self.questions_list) - self.question.count(" "):
                self.result = "success"
                self.setup_result_page()
                break
            self.setup_next_question_page()

    def initialize_next_question_page(self):
        """Initialization and basic setting up of the next Question page.
        Deletes the old question widget, creates a new one, adds to stack, and sets as current page."""
        self.question_page_widget.deleteLater()
        self.question_page_widget = QtWidgets.QWidget()
        self.game_stack_widget.addWidget(self.question_page_widget)
        self.question = self.questions_list[self.question_index]
        self.question_object = QuestionTemplate.QuestionClass()
        # self.question_object.initialize_answer_boxes()
        self.question_object.setup_question_layout(self.question)
        self.question_page_widget.setLayout(self.question_object.question_layout)
        self.game_stack_widget.setCurrentWidget(self.question_page_widget)

    def setup_next_question_page(self):
        """Resets some parameters for new question. Sets up a new question page."""
        self.question_index += 1
        del self.question_object
        self.index_of_clicked_button = -1
        self.correct_guess_count = 0
        self.initialize_next_question_page()
        for index, button in enumerate(self.question_object.alphabet_button_list):
            self.question_object.alphabet_button_list[index].clicked.connect(self.examine_guessed_alphabet)
        self.setup_clue_image()

    def setup_result_page(self):
        """Sets the result message label, and displays the result page."""
        self.result_object = ResultTemplate.ResultClass()
        self.result_object.result = self.result
        self.result_object.setup_result_layout()
        self.result_page_widget.setLayout(self.result_object.result_layout)
        self.game_stack_widget.setCurrentWidget(self.result_page_widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    invite_dialog = InviteDialog()
    invite_dialog.exec_()

