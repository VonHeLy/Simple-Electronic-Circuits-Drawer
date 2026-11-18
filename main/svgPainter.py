import xml.etree.ElementTree as ET
import elements
import math


class SVGGenerator:
    def __init__(self, width=400, height=400):
        self.width = width
        self.height = height

        self.svg = ET.Element(
            "svg",
            {
                "xmlns": "http://www.w3.org/2000/svg",
                "width": str(width),
                "height": str(height),
                "viewBox": f"0 0 {width} {height}"
            }
        )

    def add_component(self, element, x, y, rotation=0):
        group = ET.SubElement(
            self.svg,
            "g",
            {
                "transform": f"translate({x} {y}) rotate({rotation})"
            }
        )

        name = element.__name__

        match name:
            case "Resistor":
                ET.SubElement(
                    group, "path",
                    {
                        "d": "M -20 0 H -10 V 5 H 10 V -5 H -10 V 0 H 20",
                        "stroke": "white",
                        "stroke-width": "2",
                        "fill": "none"
                    }
                )

            case "Lamp":
                ET.SubElement(
                    group, "circle",
                    {
                        "cx": "0",
                        "cy": "0",
                        "r": "10",
                        "stroke": "white",
                        "stroke-width": "2",
                        "fill": "none"
                    }
                )

                ET.SubElement(
                    group, "path",
                    {
                        "d": "M -7 -7 L 7 7 M 7 -7 L -7 7 M -20 0 H -10 M 10 0 H 20",
                        "stroke": "white",
                        "stroke-width": "2",
                        "fill": "none"
                    }
                )

            case "Diode":
                ET.SubElement(
                    group, "path",
                    {
                        "d": "M -20 0 H -10 M -10 -7 L 5 0 L -10 7 Z M 5 -7 V 7 M 5 0 H 20",
                        "stroke": "white",
                        "stroke-width": "2",
                        "fill": "none"
                    }
                )

    def add_battery(self, x, y):
        ET.SubElement(
            self.svg, "path",
            {
                "d": f"M {x-12} {y-8} H {x+12} M {x-7} {y+5} H {x+7}",
                "stroke": "white",
                "stroke-width": "2",
                "fill": "none"
            }
        )

        ET.SubElement(
            self.svg, "text",
            {
                "x": str(x+17),
                "y": str(y-5),
                "fill": "white",
                "font-size": "10"
            }
        ).text = "+"

        ET.SubElement(
            self.svg, "text",
            {
                "x": str(x+17),
                "y": str(y+8),
                "fill": "white",
                "font-size": "10",
            }
        ).text = "−"

    def add_line(self, x1, y1, x2, y2):
        ET.SubElement(
            self.svg,
            "line",
            {
                "x1": str(x1),
                "y1": str(y1),
                "x2": str(x2),
                "y2": str(y2),
                "stroke": "white",
                "stroke-width": "2"
            }
        )

    def add_wire(self, points):

        ET.SubElement(
            self.svg, "path",
            {
                "d": f"{"M " + " L ".join(f"{x} {y}" for x, y in points)}",
                "stroke": "white",
                "stroke-width": "2",
                "fill": "none"
            }
        )

    def arrange_components(
        self,
        components,
        columns=5,
        pin_offset=20,
        gap=30,
        row_spacing=100,
        margin=50
    ):
        if not components:
            return

        if columns < 1:
            raise ValueError("columns must be greater than 0")

        rows = math.ceil(len(components) / columns)

        spacing = pin_offset * 2 + gap

        self.width = (
            margin * 2
            + (columns - 1) * spacing
            + pin_offset * 2
        )

        self.height = (
            margin * 2
            + (rows - 1) * row_spacing
        )

        self.svg.set("width", str(self.width))
        self.svg.set("height", str(self.height))
        self.svg.set(
            "viewBox",
            f"0 0 {self.width} {self.height}"
        )

        positions = []

        for i, element in enumerate(components):

            row = i // columns
            col = i % columns

            rotation = 180 if row % 2 else 0

            if row % 2:
                col = columns - 1 - col

            x = margin + pin_offset + col * spacing
            y = margin + row * row_spacing

            if rotation == 0:
                input_pin = (x - pin_offset, y)
                output_pin = (x + pin_offset, y)
            else:
                input_pin = (x + pin_offset, y)
                output_pin = (x - pin_offset, y)

            positions.append({
                "element": element,
                "x": x,
                "y": y,
                "rotation": rotation,
                "input": input_pin,
                "output": output_pin
            })

        for current, next_element in zip(
            positions,
            positions[1:]
        ):
            x1, y1 = current["output"]
            x2, y2 = next_element["input"]

            self.add_line(x1, y1, x2, y2)

        for item in positions:
            self.add_component(
                item["element"],
                item["x"],
                item["y"],
                item["rotation"]
            )

    def get_svg(self):
        return ET.tostring(
            self.svg,
            encoding="utf-8",
            xml_declaration=True
        )

    def save(self, filename):
        ET.ElementTree(self.svg).write(
            filename,
            encoding="unicode",
            xml_declaration=True
        )


components = [
    elements.Resistor,
    elements.Lamp,
    elements.Diode,
    elements.Resistor,
    elements.Lamp,
    elements.Diode,
    elements.Resistor,
    elements.Lamp,
    elements.Diode
]

generator = SVGGenerator()
generator.arrange_components(
    components,
    columns=4
)

svg_data = generator.get_svg()
generator.add_battery(200, 200)
generator.save("output.svg")
