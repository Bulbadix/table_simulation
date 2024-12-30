import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import xml.etree.ElementTree as ET

class Cuboid:
    def __init__(self,file_path, type, center_x, center_y, center_z):
        tree = ET.parse(file_path)
        root = tree.getroot()
        motherboard_element = root.find(f'.//motherboard/type/{type}')
        
        # Параметры кубоида
        self.length = float(motherboard_element.find('length').text)
        self.width = float(motherboard_element.find('width').text)
        self.height = float(motherboard_element.find('height').text)
        self.center_x = center_x
        self.center_y = center_y
        self.center_z = center_z

    def draw(self, ax):
        # Вершины кубоида
        vertices = [
            [self.center_x - self.length / 2, self.center_y - self.width / 2, self.center_z],
            [self.center_x + self.length / 2, self.center_y - self.width / 2, self.center_z],
            [self.center_x + self.length / 2, self.center_y + self.width / 2, self.center_z],
            [self.center_x - self.length / 2, self.center_y + self.width / 2, self.center_z],
            [self.center_x - self.length / 2, self.center_y - self.width / 2, self.center_z + self.height],
            [self.center_x + self.length / 2, self.center_y - self.width / 2, self.center_z + self.height],
            [self.center_x + self.length / 2, self.center_y + self.width / 2, self.center_z + self.height],
            [self.center_x - self.length / 2, self.center_y + self.width / 2, self.center_z + self.height]
        ]
        
        # Грани кубоида
        faces = [
            [vertices[0], vertices[1], vertices[2], vertices[3]],  # нижняя грань
            [vertices[4], vertices[5], vertices[6], vertices[7]],  # верхняя грань
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # передняя грань
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # задняя грань
            [vertices[1], vertices[2], vertices[6], vertices[5]],  # правая грань
            [vertices[0], vertices[3], vertices[7], vertices[4]]   # левая грань
        ]
        
        # Рисуем кубоид
        ax.add_collection3d(Poly3DCollection(faces, facecolors='green', linewidths=1, edgecolors='r', alpha=0.6))
