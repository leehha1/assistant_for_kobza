from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QLineEdit, QApplication, QWidget, \
    QCheckBox, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QTextEdit
import sys
import pandas as pd
import custom_parser
from word_dict import LETTER_DICT

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self._connect_all()


    def _connect_all(self):
        self.button_find.clicked.connect(self._button_find_clicked)
        self.button_reset.clicked.connect(self._button_reset_clicked)

    def _button_reset_clicked(self):
        for b in self.cb_not_in_word:
            b.setChecked(False)
        for b in self.cb_in_word:
            b.setChecked(False)
        for i, value in enumerate(self.input_fields):
            value.setText("")
        for i, value in enumerate(self.input_out_fields):
            value.setText("")

    def _button_find_clicked(self):

        self.df = pd.read_csv("D:/python/dictionaryParser/words.csv", index_col=False)

        self.exactly_in_word = []
        for b in self.cb_in_word:
            if b.isChecked():
                self.exactly_in_word.append(b.text())
            # print(b.text(), b.isChecked())

        self.exactly_not_in_word = []
        for b in self.cb_not_in_word:
            if b.isChecked():
                self.exactly_not_in_word.append(b.text())

        self.letters_pos = {}
        for i, value in enumerate(self.input_fields):
            if value.text() != '':
                self.letters_pos[i] = value.text()

        self.letters_out_pos = {}
        for i, value in enumerate(self.input_out_fields):
            if value.text() != '':
                print(value.text())
                self.letters_out_pos[i] = value.text()

        res = custom_parser.find_words_with_options(self.df,
                                                    exactly_in_word=self.exactly_in_word,
                                                    letters_pos=self.letters_pos,
                                                    exactly_not_in_word=self.exactly_not_in_word,
                                                    letters_out_pos=self.letters_out_pos,
                                                    )
        self.text_edit.setPlainText('\n'.join(res))

    def initUI(self):

        self.cb_in_word = []
        for w in LETTER_DICT.keys():
            self.cb_in_word.append(QCheckBox(w, self))
        self.vbox1 = QVBoxLayout()
        self.label_in_word = QLabel("exactly_in_word", self)
        self.vbox1.addWidget(self.label_in_word)
        for b in self.cb_in_word:
            self.vbox1.addWidget(b)

        self.cb_not_in_word = []
        for w in LETTER_DICT.keys():
            self.cb_not_in_word.append(QCheckBox(w, self))
        self.vbox2 = QVBoxLayout()
        self.label_not_in_word = QLabel("exactly_not_in_word", self)
        self.vbox2.addWidget(self.label_not_in_word)
        for b in self.cb_not_in_word:
            self.vbox2.addWidget(b)
        self.label_in_their_pos = QLabel("In their positions", self)

        self.letters_pos_input_widget = QWidget()
        self.letters_pos_input_layout = QHBoxLayout()
        self.input_fields = []
        for i in range(5):
            self.input_fields.append(QLineEdit())
        for i in self.input_fields:
            self.letters_pos_input_layout.addWidget(i)
        self.letters_pos_input_widget.setLayout(self.letters_pos_input_layout)

        self.label_out_their_pos = QLabel("Out of position", self)

        self.letters_out_pos_input_widget = QWidget()
        self.letters_out_pos_input_layout = QHBoxLayout()
        self.input_out_fields = []
        for i in range(5):
            self.input_out_fields.append(QLineEdit())
        for i in self.input_out_fields:
            self.letters_out_pos_input_layout.addWidget(i)
        self.letters_out_pos_input_widget.setLayout(self.letters_out_pos_input_layout)

        self.button_find = QPushButton('Find', self)
        self.button_reset = QPushButton('Reset', self)


        # Создание экземпляра QTextEdit
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)  # Только для чтения
        self.text_edit.setMinimumHeight(200)  # Минимальная высота

        self.vbox3 = QVBoxLayout()
        self.vbox3.addWidget(self.label_in_their_pos)
        self.vbox3.addWidget(self.letters_pos_input_widget)
        self.vbox3.addWidget(self.label_out_their_pos)
        self.vbox3.addWidget(self.letters_out_pos_input_widget)

        self.vbox3.addWidget(self.button_find)

        self.vbox3.addWidget(self.text_edit)
        self.vbox3.addWidget(self.button_reset)

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vbox1)
        self.hbox.addLayout(self.vbox2)
        self.hbox.addLayout(self.vbox3)
        self.hbox.addWidget(self.letters_pos_input_widget)

        self.setLayout(self.hbox)
        # self.setLayout(vbox2)
        self.setGeometry(0, 0, 1000, 1000)
        self.setWindowTitle('Word searcher')
        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

