import re
import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow
from gui_sample import Ui_ElementEditor
from random import randint
from datetime import datetime

import elements


LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ELEMENTS_TYPES = [elements.Resistor, elements.Lamp, elements.Diode]


class MainWindow(QMainWindow, Ui_ElementEditor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = []
        self.__post_init__()
        self.typeInput.addItems([element_type.__name__ for element_type in ELEMENTS_TYPES])

    def __post_init__(self):
        self.parseButton.clicked.connect(self.text_processing)
        self.elementList.itemClicked.connect(self.show_element_properties)
        self.updatePromptBtn.clicked.connect(self.update_prompt)
        self.typeInput.currentTextChanged.connect(self.update_selected_element_type)
        self.idInput.textChanged.connect(self.update_selected_element_type)
        self.resistanceInput.valueChanged.connect(self.update_selected_element_type)

    def get_selected_element(self):
        current_item = self.elementList.currentItem()
        if current_item is None:
            return None

        selected_label = current_item.text()
        for item in self.data:
            if selected_label.split()[-1] == item['uid']:
                return item
        return None

    def update_prompt(self):
        if not self.data:
            self.text_processing()

        str_text = "\n".join(
            [f"{item['type']} [R={item.get('resistance', 0.0)}]" for item in self.data]
        )
        self.textEdit.setPlainText(str_text)

    def update_selected_element_type(self):
        selected = self.get_selected_element()
        if selected is None:
            return

        selected['type'] = self.typeInput.currentText()
        selected['resistance'] = self.resistanceInput.value()
        self.update_element_list()

    def save_data_to_file(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            self.status = f"Data saved to {filename}"
            self.statusbar.showMessage(self.status)
        except Exception as e:
            self.status = f"Error saving data to {filename}: {e}"
            self.statusbar.showMessage(self.status)
            print(f"Error saving data to {filename}: {e}")

    def show_element_properties(self):
        selected = self.get_selected_element()
        if selected is None:
            return

        self.status = str(selected)
        self.statusbar.showMessage(self.status)

        self.typeInput.blockSignals(True)
        self.resistanceInput.blockSignals(True)

        self.resistanceInput.setValue(selected.get('resistance', 0.0))
        self.typeInput.setCurrentText(selected.get('type', ''))
        self.idInput.setText(selected.get('uid', ''))
 
        self.typeInput.blockSignals(False)
        self.resistanceInput.blockSignals(False)
        
    def _extract_element_name_and_params(self, info):
        current_item = str(info).strip()
        if not current_item:
            raise elements.ParserError("Empty element data.")

        left_bracket = current_item.find("[")
        right_bracket = current_item.rfind("]")

        name_part = current_item
        parameters = ""

        if left_bracket != -1 and right_bracket != -1 and left_bracket < right_bracket:
            name_part = current_item[:left_bracket].strip()
            parameters = current_item[left_bracket + 1:right_bracket].strip()

        if not name_part:
            raise elements.ParserError(
                f"Missing element name in: {current_item}")

        parsed_params = {}
        if parameters:
            resistance_match = re.search(
                r"(?i)\bR\s*=?\s*([-+]?\d+(?:\.\d+)?)\b", parameters)
            if not resistance_match:
                resistance_match = re.fullmatch(
                    r"\s*([-+]?\d+(?:\.\d+)?)\s*", parameters)
            if not resistance_match:
                raise elements.ParserError(
                    f"Invalid parameters format: {current_item}")
            parsed_params["resistance"] = float(resistance_match.group(1))

        return name_part, parsed_params

    def init_element(self, info):
        current_item = str(info).strip()
        if not current_item:
            raise elements.ParserError("Empty element data.")

        name_part, params = self._extract_element_name_and_params(current_item)
        normalized_name = re.sub(
            r"[\[\]\s;,.\\/]+", "", name_part, flags=re.IGNORECASE).lower()

        detected_type = None
        for element_type in ELEMENTS_TYPES:
            if normalized_name in [name.lower() for name in element_type.names]:
                detected_type = element_type
                break

        if not detected_type:
            raise elements.ParserError(f"Unknown element type: {current_item}")

        uid = str(randint(100, 999)) + datetime.now().strftime("%d%H%M%S")
        element_data = {
            "uid": uid,
            "type": f"{detected_type.__name__}",
        }
        if "resistance" in params:
            element_data["resistance"] = params["resistance"]
        else:
            element_data["resistance"] = 0.0

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
            raise elements.ParserError("No data to process.")

        try:
            for item in raw_lines:
                try:
                    self.init_element(item)
                except elements.ParserError as exc:
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
