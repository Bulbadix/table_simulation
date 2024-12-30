import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import xml.etree.ElementTree as ET
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Table:
    def __init__(self, xml_file):
        self.table_width, self.table_length, self.board_height, self.min_height, self.max_height, self.current_height, self.step, self.leg_radius = self.load_table_data_from_xml(xml_file)

    def load_table_data_from_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        table_length = int(root.find('.//tabletop/length').text)
        table_width = int(root.find('.//tabletop/width').text)
        board_height = int(root.find('.//tabletop/height').text)
        min_height = int(root.find('.//leg/min_height').text)
        max_height = int(root.find('.//leg/max_height').text)
        current_height = min_height  # Начальная высота устанавливается равной минимальной
        step = int(root.find('.//leg/step').text)
        leg_radius = int(root.find('.//leg/radius').text)

        return table_width, table_length, board_height, min_height, max_height, current_height, step, leg_radius

    def draw(self, ax):
        # Вершины доски стола
        vertices = [
            [0, 0, self.current_height],
            [self.table_width, 0, self.current_height],
            [self.table_width, self.table_length, self.current_height],
            [0, self.table_length, self.current_height],
            [0, 0, self.current_height + self.board_height],
            [self.table_width, 0, self.current_height + self.board_height],
            [self.table_width, self.table_length, self.current_height + self.board_height],
            [0, self.table_length, self.current_height + self.board_height]
        ]
        
        # Грани доски стола
        faces = [
            [vertices[0], vertices[1], vertices[2], vertices[3]],
            [vertices[4], vertices[5], vertices[6], vertices[7]],
            [vertices[0], vertices[1], vertices[5], vertices[4]],
            [vertices[2], vertices[3], vertices[7], vertices[6]],
            [vertices[1], vertices[2], vertices[6], vertices[5]],
            [vertices[0], vertices[3], vertices[7], vertices[4]]
        ]
        
        # Рисуем стол
        ax.add_collection3d(Poly3DCollection(faces, facecolors='cyan', linewidths=1, edgecolors='r', alpha=0.25))
        
        # Рисуем ноги стола
        self.draw_legs(ax)
        
        # Устанавливаем границы
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim([0, self.table_width])
        ax.set_ylim([0, self.table_length])
        ax.set_zlim([0, self.max_height + self.board_height])

    def draw_legs(self, ax):
        # Функция для рисования цилиндров (ног стола)
        def draw_cylinder(x, y, z, radius, height):
            theta = np.linspace(0, 2 * np.pi, 30)
            x_circle = radius * np.cos(theta)
            y_circle = radius * np.sin(theta)
            z_circle = np.array([z, z + height])

            for i in range(2):
                ax.plot(x_circle + x, y_circle + y, z_circle[i], color='brown')
            for i in range(len(x_circle)):
                ax.plot([x + x_circle[i], x + x_circle[i]], [y + y_circle[i], y + y_circle[i]], [z, z + height], color='brown')

        # Рисуем 4 ноги стола
        draw_cylinder(100, 100, 0, self.leg_radius, self.current_height)
        draw_cylinder(100, self.table_length - 100, 0, self.leg_radius, self.current_height)
        draw_cylinder(self.table_width - 100, 100, 0, self.leg_radius, self.current_height)
        draw_cylinder(self.table_width - 100, self.table_length - 100, 0, self.leg_radius, self.current_height)

