import xml.etree.ElementTree as ET

class Table:
    def __init__(self, length, width, height):
        self.length = length  # длина стола
        self.width = width    # ширина стола
        self.height = height  # высота стола

    @staticmethod
    def load_from_xml(filename):
        """Загружает данные о столе из XML-файла"""
        tree = ET.parse(filename)
        root = tree.getroot()
        
        length = float(root.find("length").text)
        width = float(root.find("width").text)
        height = float(root.find("height").text)

        return Table(length, width, height)
