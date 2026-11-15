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
    name = "Resistor"
    names = ["r", "resistor", "резистор"]


@dataclass
class Lamp(Element):
    name = "Lamp"
    names = ["l", "lamp", "лампа"]


@dataclass
class Diode(Element):
    name = "Diode"
    names = ["d", "diode", "диод"]


class ParserError(Exception):
    pass
