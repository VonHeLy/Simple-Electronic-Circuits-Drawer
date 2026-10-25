import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from gui_sample import Ui_ElementEditor
from random import randint
from datetime import datetime


LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"


class MainWindow(QMainWindow, Ui_ElementEditor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = []

        self.__post_init__()

    def __post_init__(self):
        self.parseButton.clicked.connect(self.text_processing)

    def text_processing(self):
        # uid = str(randint(100000, 999999)) + datetime.now().strftime("%Y%m%d%H%M%S")

        self.data.clear()
        self.elementList.clear()
        raw_text = str(self.textEdit.toPlainText())
        self.raw_data = raw_text.replace("\n", " ").replace("\t", " ")
        sbracket_open = False
        fbracket_open = False
        can_be_closed = False
        elements = 0
        current_item = ""
        for i, char in enumerate(self.raw_data):
            if char == "[":
                sbracket_open = True
                continue
            elif char == "]":
                sbracket_open = False
                can_be_closed = True

            if ((char == " " and self.raw_data[i + 1] in LETTERS)\
                or (char in [']', '}', ')']))\
                and not sbracket_open and not fbracket_open\
                and current_item != ""\
                or i == len(self.raw_data) - 1:
                can_be_closed = True

            if can_be_closed:
                current_item = current_item.strip()
                uid = str(randint(100, 999)) + \
                    datetime.now().strftime("%Y%m%d%H%M%S")
                self.data.append({"uid": uid, "type": current_item})
                elements += 1
                current_item = ""
                continue
            else:
                if char.replace(" ", "") != "":
                    current_item += char

        for item in self.data:
            self.elementList.addItem(f"{item['uid']} - {item['type']}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
