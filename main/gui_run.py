import re
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
        self.typeInput.addItems([element_type.name for element_type in ELEMENTS_TYPES])

    def __post_init__(self):
        self.parseButton.clicked.connect(self.text_processing)
        self.elementList.itemClicked.connect(self.show_element_properties)


    def show_element_properties(self):
        selected = self.elementList.currentItem().text()
        for item in self.data:
            if selected.split()[-1] == item['uid']:
                selected = item
                break
        self.resistanceInput.setValue(selected.get('resistance', 0.0))
        self.idInput.setText(selected.get('uid', ''))
        self.typeInput.setCurrentText(selected.get('type', ''))
        
    def _extract_element_name_and_params(self, info):
        current_item = str(info).strip()
        if not current_item:
            raise classes.ParserError("Empty element data.")

        left_bracket = current_item.find("[")
        right_bracket = current_item.rfind("]")

        name_part = current_item
        parameters = ""

        if left_bracket != -1 and right_bracket != -1 and left_bracket < right_bracket:
            name_part = current_item[:left_bracket].strip()
            parameters = current_item[left_bracket + 1:right_bracket].strip()

        if not name_part:
            raise classes.ParserError(
                f"Missing element name in: {current_item}")

        parsed_params = {}
        if parameters:
            resistance_match = re.search(
                r"(?i)\bR\s*=?\s*([-+]?\d+(?:\.\d+)?)\b", parameters)
            if not resistance_match:
                raise classes.ParserError(
                    f"Invalid parameters format: {current_item}")
            parsed_params["resistance"] = float(resistance_match.group(1))

        return name_part, parsed_params

    def init_element(self, info):
        current_item = str(info).strip()
        if not current_item:
            raise classes.ParserError("Empty element data.")

        name_part, params = self._extract_element_name_and_params(current_item)
        normalized_name = re.sub(
            r"[\[\]\s;,.\\/]+", "", name_part, flags=re.IGNORECASE).lower()

        detected_type = None
        for element_type in ELEMENTS_TYPES:
            if normalized_name in [name.lower() for name in element_type.names]:
                detected_type = element_type
                break

        if not detected_type:
            raise classes.ParserError(f"Unknown element type: {current_item}")

        uid = str(randint(100, 999)) + datetime.now().strftime("%d%H%M%S")
        element_data = {
            "uid": uid,
            "type": f"{detected_type.name}",
        }
        if "resistance" in params:
            element_data["resistance"] = params["resistance"]

        self.data.append(element_data)
        print(self.data)
        self.update_element_list()
        return element_data

    def update_element_list(self):
        self.elementList.clear()
        for item in self.data:
            label = f"{item['type']} {item['uid']}"
            """if 'resistance' in item:
                label = f"{label}"""""
            self.elementList.addItem(label)
            print(f"Added {item['type']} with UID {item['uid']} to the list.")
            if 'resistance' in item:
                print(f"Resistance: {item['resistance']}")

    def text_processing(self):
        self.data = []
        self.elementList.clear()
        raw_text = str(self.textEdit.toPlainText())
        raw_lines = [line.strip()
                     for line in raw_text.splitlines() if line.strip()]

        if not raw_lines:
            self.status = "ParserError: No data to process."
            self.statusbar.showMessage(self.status)
            raise classes.ParserError("No data to process.")

        try:
            for item in raw_lines:
                try:
                    self.init_element(item)
                except classes.ParserError as exc:
                    self.status = f"ParserError: {exc}"
                    self.statusbar.showMessage(self.status)
                    print(f"ParserError: {exc}")
                except (TypeError, ValueError, IndexError) as exc:
                    self.status = f"ParserGlobalError: Invalid element format: {exc}"
                    self.statusbar.showMessage(self.status)
                    print(f"ParserGlobalError: Invalid element format: {exc}")
                else:
                    self.status = "Parsing completed successfully."
                    self.statusbar.showMessage(self.status)
        except Exception as exc:
            self.status = f"ParserError: {exc}"
            self.statusbar.showMessage(self.status)
            print(f"ParserError: {exc}")
            raise


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
