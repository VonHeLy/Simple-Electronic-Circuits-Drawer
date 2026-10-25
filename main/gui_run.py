import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from gui_sample import Ui_ElementEditor
from random import randint
from datetime import datetime


class MainWindow(QMainWindow, Ui_ElementEditor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = []

        self.__post_init__()

    def __post_init__(self):
        self.textEdit.textChanged.connect(self.text_processing)

    def text_processing(self):
        self.data.clear()
        self.elementList.clear()
        raw_text = str(self.textEdit.toPlainText())
        self.raw_data = raw_text.replace("\n", " ").replace("\t", " ")
        self.raw_data = self.raw_data.split(" ")
        for item in self.raw_data:
            if item != "":
                uid = str(randint(100000, 999999)) + datetime.now().strftime("%Y%m%d%H%M%S")
                self.data.append({"uid": uid, "type": item})
        for item in self.data:
            self.elementList.addItem(f"{item['uid']} - {item['type']}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())