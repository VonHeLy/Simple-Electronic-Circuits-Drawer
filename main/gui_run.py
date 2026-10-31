import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from gui_sample import Ui_ElementEditor
from random import randint
from datetime import datetime


import classes


LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ELEMENTS_TYPES = [classes.Resistor, classes.Lamp, classes.Diode]

class MainWindow(QMainWindow, Ui_ElementEditor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = []

        self.__post_init__()

    def __post_init__(self):
        self.parseButton.clicked.connect(self.text_processing)

    def init_element(self, info):
        self.data.clear()
        current_item = info.strip()
        uid = str(randint(100, 999)) + \
            datetime.now().strftime("%Y%m%d%H%M%S")
        detected_type = None
        for element_type in ELEMENTS_TYPES:
            if current_item.strip().rstrip('[]0123456789R=- ;,./').lower() in element_type.names:
                detected_type = element_type
        self.data.append({"uid": uid, "type": detected_type})
        self.update_element_list()

    def update_element_list(self):
        self.elementList.clear()
        for item in self.data:
            self.elementList.addItem(str(item['type']))
            print(f"Added {item['type']} with UID {item['uid']} to the list.")

    def text_processing(self):
        self.elementList.clear()
        raw_text = str(self.textEdit.toPlainText())
        self.raw_data = raw_text.replace("\t", " ").replace("  ", " ")
        self.raw_data = self.raw_data.split("\n")

        for item in self.raw_data:
            if item.strip() != "":
                self.init_element(item)
            
        self.status = f"Processed {len(self.raw_data)} items."
        #self.statusLabel.setText(self.status)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
