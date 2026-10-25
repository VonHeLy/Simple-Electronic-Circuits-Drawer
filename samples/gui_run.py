import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from gui_sample import Ui_ElementEditor

class MyWidget(QMainWindow, Ui_ElementEditor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())