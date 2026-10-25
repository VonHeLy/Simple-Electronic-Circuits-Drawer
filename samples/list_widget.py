
import sys

from PyQt6.QtWidgets import (
    QApplication, QWidget, QListWidget, QPushButton,
    QLineEdit, QLabel, QVBoxLayout, QHBoxLayout
)


class ElementEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Редактор элементов")

        self.elements = []

        self.element_list = QListWidget()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название элемента")

        self.add_button = QPushButton("Добавить")
        self.remove_button = QPushButton("Удалить")

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Элементы"))
        left_layout.addWidget(self.element_list)
        left_layout.addWidget(self.add_button)
        left_layout.addWidget(self.remove_button)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Название"))
        right_layout.addWidget(self.name_input)
        right_layout.addStretch()

        main_layout = QHBoxLayout(self)
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)

        self.add_button.clicked.connect(self.add_element)
        self.remove_button.clicked.connect(self.remove_element)
        self.element_list.currentRowChanged.connect(
            self.select_element
        )
        self.name_input.textEdited.connect(self.rename_element)

    def add_element(self):
        name = f"Элемент {len(self.elements) + 1}"
        self.elements.append({"name": name})

        self.element_list.addItem(name)
        self.element_list.setCurrentRow(len(self.elements) - 1)

    def remove_element(self):
        row = self.element_list.currentRow()

        if row < 0:
            return

        self.elements.pop(row)
        self.element_list.takeItem(row)

        if self.elements:
            self.element_list.setCurrentRow(
                min(row, len(self.elements) - 1)
            )
        else:
            self.name_input.clear()

    def select_element(self, row):
        if row < 0:
            self.name_input.clear()
            return

        self.name_input.setText(self.elements[row]["name"])

    def rename_element(self, name):
        row = self.element_list.currentRow()

        if row < 0:
            return

        self.elements[row]["name"] = name
        self.element_list.item(row).setText(name)


app = QApplication(sys.argv)
window = ElementEditor()
window.resize(650, 400)
window.show()
sys.exit(app.exec())
