from dataclasses import dataclass


@dataclass
class Element:
    __name__ = "Базовый"
    uid: str
    resistance: float
    size: tuple

    def draw(self, rotation=0):
        pass


@dataclass
class Resistor(Element):
    __name__ = "Resistor"
    names = ["r", "resistor", "резистор"]


@dataclass
class Lamp(Element):
    __name__ = "Lamp"
    names = ["l", "lamp", "лампа"]


@dataclass
class Diode(Element):
    __name__ = "Diode"
    names = ["d", "diode", "диод"]


class ParserError(Exception):
    pass
