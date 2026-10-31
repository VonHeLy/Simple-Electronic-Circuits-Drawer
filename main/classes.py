from dataclasses import dataclass


@dataclass
class Element:
    uid: str
    resistance: float
    size: tuple

    def draw(self, rotation=0):
        pass


@dataclass
class Resistor(Element):
    names = ["r", "resistor", "резистор"]


@dataclass
class Lamp(Element):
    names = ["l", "lamp", "лампа"]


@dataclass
class Diode(Element):
    names = ["d", "diode", "диод"]
