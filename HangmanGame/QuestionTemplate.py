import sys
from PySide2 import QtWidgets, QtCore, QtGui
import string


class QuestionClass(QtWidgets.QDialog):
    def __init__(self, parent=None):
        """Sets up the widgets in the Question template.
        :param: parent :  provides ability to connect to external applications like Maya.
        :param type: parent class.
        :return : None. """
        super(QuestionClass, self).__init__(parent)
        self.question_layout = QtWidgets.QHBoxLayout()
        self.left_layout = QtWidgets.QVBoxLayout()
        self.right_layout = QtWidgets.QVBoxLayout()
        self.left_widget = QtWidgets.QWidget()
        self.right_widget = QtWidgets.QWidget()
        self.question_label = QtWidgets.QLabel("Guess the movie:")
        self.image_widget = QtWidgets.QWidget()
        self.image_layout = QtWidgets.QHBoxLayout()
        self.image_label = QtWidgets.QLabel()
        self.answer_boxes_widget = QtWidgets.QWidget()
        self.answer_boxes_layout = QtWidgets.QHBoxLayout()
        self.alphabet_widget = QtWidgets.QWidget()
        self.alphabet_layout = QtWidgets.QHBoxLayout()
        self.question = ""

        self.init_answer_text_method()
        self.init_alphabet_button_method()
        self.init_health_widget_method()

    def init_answer_text_method(self):
        """Creates the boxes for the answer display.
        :return : None.
        TODO: Avoid hardcoding a limit to the number of boxes."""
        self.answer_letters_list = []
        for index in range(0, 25):
            index_string = str(index)
            exec("self.ans%sTxt = QtWidgets.QLabel()" % index_string)  # execute list of commands of type:
            # [ self.ans1Txt = QtWidgets.QLabel() ]
            exec("self.answer_letters_list.append(self.ans%sTxt)" % index_string)  # create "answer_letters_list", a list of text boxes
            # for movie name letters.

    def init_alphabet_button_method(self):
        """Creates the alphabet buttons.
        :return : None."""
        self.alphabet_list = [char for char in string.ascii_uppercase]
        self.alphabet_button_list = []
        for button in self.alphabet_list:
            exec("self.alph%sBtn = QtWidgets.QPushButton('%s')" % (button, button))
            exec("self.alphabet_button_list.append(self.alph%sBtn)" % button)

    def init_health_widget_method(self):
        """Creates health bars.
        :return : None."""
        self.health_bars_list = []
        for number in range(12):
            exec("self.health_bar%s = QtWidgets.QLabel()" % str(number))
            exec("self.health_bars_list.append(self.health_bar%s)" % str(number))
        self.color_list = ["greenyellow", "greenyellow", "#adf802", "#fcc006", "#fec615", "#f5bf03", "#fe02a2",
                          "#fe019a", "#ff0784", "#fa4224", "#f4320c", "#fe0002"]
        self.health_loss = 0

    def question_page_method(self, current_question):
        """Sets up the UI for the Question page.
        :return : None."""
        self.question = current_question
        self.question_label.setAlignment(QtCore.Qt.AlignCenter)
        self.add_image_method()
        self.add_answer_boxes_method()
        self.add_alphabet_widget_method()
        self.add_health_bars_method()
        self.question_layout.addWidget(self.left_widget)
        self.question_layout.addWidget(self.right_widget)
        self.left_widget.setLayout(self.left_layout)
        self.right_widget.setLayout(self.right_layout)
        self.left_layout.addWidget(self.question_label)
        self.left_layout.addWidget(self.image_widget)
        self.left_layout.addWidget(self.answer_boxes_widget)
        self.left_layout.addWidget(self.alphabet_widget)

    def add_answer_boxes_method(self):
        """Sets up the answer_boxes_widget.
        :return : None."""
        self.answer_boxes_widget.setLayout(self.answer_boxes_layout)
        self.answer_boxes_layout.setAlignment(QtCore.Qt.AlignCenter)

        for box in range(len(self.question)):
            self.answer_boxes_layout.addWidget(self.answer_letters_list[box])
            self.answer_letters_list[box].setStyleSheet("background-color : #FFF3F3")
            self.answer_letters_list[box].setFixedWidth(15)
            self.answer_letters_list[box].setAlignment(QtCore.Qt.AlignCenter)

    def add_alphabet_widget_method(self):
        """Sets up  the alphabet_widget.
        :return : None. """
        self.alphabet_widget.setLayout(self.alphabet_layout)
        for btn in range(len(self.alphabet_button_list)):
            self.alphabet_button_list[btn].setMaximumWidth(20)
            self.alphabet_layout.addWidget(self.alphabet_button_list[btn])
            self.alphabet_button_list[btn].setFocusPolicy(QtCore.Qt.NoFocus)
            self.alphabet_button_list[btn].setStyleSheet("background-color : #FFF3F3")

    def add_image_method(self):
        """Sets up the image_widget.
        :return None.
        TODO: Change images """
        self.image_widget.setLayout(self.image_layout)
        self.image_layout.addWidget(self.image_label)
        self.image_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setPixmap("Avatar.jpg")
        self.image_label.setMaximumWidth(300)
        self.image_label.setMaximumHeight(300)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)

    def add_health_bars_method(self):
        """Sets up the health_bars_widget.
        :return : None.
        TODO: replace with hangman visual."""
        for index, label in enumerate(self.health_bars_list):
            self.right_layout.addWidget(label)
            label.setFixedWidth(50)
            label.setStyleSheet("background-color: " + self.color_list[index])

