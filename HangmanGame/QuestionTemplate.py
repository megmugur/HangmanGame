import sys
from PySide2 import QtWidgets, QtCore
import string


class QuestionClass(QtWidgets.QWidget):
    def __init__(self, question, parent=None):
        """Sets up the widgets in the Question template.
        :param parent :  provides ability to connect to external applications like Maya.
        :type parent: QWidget."""
        super(QuestionClass, self).__init__(parent)
        self.question_layout = QtWidgets.QHBoxLayout()
        self.layout = QtWidgets.QVBoxLayout()
        self.widget = QtWidgets.QWidget()
        self.image_widget = QtWidgets.QWidget()
        self.image_layout = QtWidgets.QHBoxLayout()
        self.image_label = QtWidgets.QLabel()

        self.answer_boxes_widget = QtWidgets.QWidget()
        self.answer_boxes_layout = QtWidgets.QHBoxLayout()
        self.alphabet_widget = QtWidgets.QWidget()
        self.alphabet_layout = QtWidgets.QHBoxLayout()
        self.question = question
        self.health_loss = 0
        self.alphabet_list = []
        self.buttons_dict = {}
        self.labels_dict = {}

        self.initialize_answer_boxes()
        self.initialize_alphabet_buttons()

    def initialize_answer_boxes(self):
        """Creates the boxes for the answer display."""
        for index in range(len(self.question)):
            label = QtWidgets.QLabel()
            self.labels_dict[index] = label

    def initialize_alphabet_buttons(self):
        """Creates the alphabet buttons."""
        self.alphabet_list = [char for char in string.ascii_uppercase]

        for char in self.alphabet_list:
            self.buttons_dict[char] = QtWidgets.QPushButton(char)

    def setup_question_layout(self, current_question):
        """Sets up the layout for the Question page.
        :param current_question : current question, movie name.
        :type current_question : str """
        self.question = current_question
        self.setup_image_layout()
        self.setup_answer_boxes()
        self.setup_alphabet_buttons()
        self.question_layout.addWidget(self.widget)
        self.widget.setLayout(self.layout)
        self.layout.addWidget(self.image_widget)
        self.layout.addWidget(self.answer_boxes_widget)
        self.layout.addWidget(self.alphabet_widget)

    def setup_answer_boxes(self):
        """Sets up the answer_boxes_widget."""
        self.answer_boxes_widget.setLayout(self.answer_boxes_layout)
        self.answer_boxes_layout.setAlignment(QtCore.Qt.AlignCenter)
        for box in range(len(self.question)):
            self.answer_boxes_layout.addWidget(self.labels_dict[box])
            if self.question[box] != " ":
                self.labels_dict[box].setStyleSheet("background-color : #FFF3F3")
            self.labels_dict[box].setFixedSize(30, 30)
            self.labels_dict[box].setAlignment(QtCore.Qt.AlignCenter)

    def setup_alphabet_buttons(self):
        """Sets up the alphabet_widget."""
        self.alphabet_widget.setLayout(self.alphabet_layout)

        for btn in self.buttons_dict.keys():
            self.buttons_dict[btn].setMaximumWidth(20)
            self.alphabet_layout.addWidget(self.buttons_dict[btn])
            self.buttons_dict[btn].setFocusPolicy(QtCore.Qt.NoFocus)
            self.buttons_dict[btn].setStyleSheet("background-color : #FFF3F3")

    def setup_image_layout(self):
        """Sets up the image_widget."""
        self.image_widget.setLayout(self.image_layout)
        self.image_layout.addWidget(self.image_label)
        self.image_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setMaximumWidth(750)
        self.image_label.setStyleSheet("border: 2px solid grey;")
        self.image_label.setScaledContents(True)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
