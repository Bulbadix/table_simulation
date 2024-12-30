import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import xml.etree.ElementTree as ET

# Функция для загрузки данных из XML
def load_table_data_from_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Загрузка данных из XML
    table_length = int(root.find('.//tabletop/length').text)
    table_width = int(root.find('.//tabletop/width').text)
    board_height = int(root.find('.//tabletop/height').text)

    min_height = int(root.find('.//leg/min_height').text)
    max_height = int(root.find('.//leg/max_height').text)
    current_height = min_height  # Начальная высота устанавливается равной минимальной
    step = int(root.find('.//leg/step').text)
    leg_radius = int(root.find('.//leg/radius').text)
    

    return table_width, table_length, board_height, min_height, max_height, current_height, step, leg_radius

# Загружаем данные из XML
table_width, table_length, board_height, min_height, max_height, current_height, step, leg_radius = load_table_data_from_xml('table_data.xml')

# Функция для рисования 3D прямоугольного параллелепипеда (стола)
def draw_table():
    fig = plt.figure(figsize=(10, 8))  # Увеличиваем размер графика
    ax = fig.add_subplot(111, projection='3d')

    # Вершины доски стола (с высотой 100 мм)
    vertices = [
    [0, 0, current_height],  # точка 1 (левая передняя)
    [table_width, 0, current_height],  # точка 2 (правая передняя)
    [table_width, table_length, current_height],  # точка 3 (правая задняя)
    [0, table_length, current_height],  # точка 4 (левая задняя)
    [0, 0, current_height + board_height],  # точка 5 (левая передняя верх)
    [table_width, 0, current_height + board_height],  # точка 6 (правая передняя верх)
    [table_width, table_length, current_height + board_height],  # точка 7 (правая задняя верх)
    [0, table_length, current_height + board_height]  # точка 8 (левая задняя верх)
]

    # Список граней доски стола
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # нижняя грань
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # верхняя грань
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # передняя грань
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # задняя грань
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # правая грань
        [vertices[0], vertices[3], vertices[7], vertices[4]]   # левая грань
    ]

    # Рисуем все грани доски стола
    ax.add_collection3d(Poly3DCollection(faces, facecolors='cyan', linewidths=1, edgecolors='r', alpha=0.25))

    # Рисуем цилиндры для ног стола
    #leg_radius = leg_radius  # Радиус цилиндра (для ног)
    leg_height = current_height   # Высота ноги

    # Функция для рисования цилиндра
    def draw_cylinder(x, y, z, radius, height, ax):
        # Углы для построения окружности
        theta = np.linspace(0, 2 * np.pi, 30)  # 30 точек для окружности
        x_circle = radius * np.cos(theta)
        y_circle = radius * np.sin(theta)
        z_circle = np.array([z, z + height])  # Два уровня для цилиндра (снизу и сверху)

        for i in range(2):
            ax.plot(x_circle + x, y_circle + y, z_circle[i], color='brown')  # Рисуем два круга (верх и низ цилиндра)
        for i in range(len(x_circle)):
            ax.plot([x + x_circle[i], x + x_circle[i]], [y + y_circle[i], y + y_circle[i]], [z, z + height], color='brown')  # Стенки цилиндра


    # Рисуем 4 цилиндра для ног
    draw_cylinder(100, 100, 0, leg_radius, leg_height, ax)  # Левая передняя нога
    draw_cylinder(100, table_length - 100, 0, leg_radius, leg_height, ax)  # Левая задняя нога
    draw_cylinder(table_width - 100, 100, 0, leg_radius, leg_height, ax)  # Правая передняя нога
    draw_cylinder(table_width - 100, table_length - 100, 0, leg_radius, leg_height, ax)  # Правая задняя нога

   

    # Устанавливаем границы для осей
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Ограничиваем оси
    ax.set_xlim([0, table_width])
    ax.set_ylim([0, table_length])
    
    # Устанавливаем ось Z от 0 до 900
    ax.set_zlim([0, max_height + board_height])

    # Вычисляем соотношение сторон для правильного отображения
    aspect_ratio_x = table_width
    aspect_ratio_y = table_length
    aspect_ratio_z = max_height

    ax.set_box_aspect([aspect_ratio_x, aspect_ratio_y, aspect_ratio_z])

    # Включаем сетку
    ax.grid(True)

    # Отображаем 3D-графику
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Функция для поднятия стола
def move_up():
    global current_height
    if current_height < max_height:
        current_height += step
        height_label.config(text=f"Высота стола: {current_height} мм")
        update_visualization()

# Функция для опускания стола
def move_down():
    global current_height
    if current_height > min_height:
        current_height -= step
        height_label.config(text=f"Высота стола: {current_height} мм")
        update_visualization()

# Функция для выхода из программы
def exit_program():
    root.quit()  # Завершаем работу tkinter
    root.destroy()  # Уничтожаем окно

# Обновление визуализации стола
def update_visualization():
    for widget in frame.winfo_children():
        widget.destroy()
    draw_table()

# Создаём главное окно
root = tk.Tk()
root.title("Регулировка высоты стола")

# Заголовок
header_label = ttk.Label(root, text="Стол %dx%d мм с ногами"%(table_width, table_length),   font=("Arial", 16))
header_label.grid(row=0, column=0, columnspan=2, pady=10)

# Метка для отображения текущей высоты стола
height_label = ttk.Label(root, text=f"Высота стола: {current_height} мм", font=("Arial", 14))
height_label.grid(row=1, column=0, columnspan=2, pady=10)

# Создаём рамку для визуализации
frame = tk.Frame(root)
frame.grid(row=2, column=0, rowspan=4, padx=10, pady=10)

# Начальная визуализация стола
draw_table()

# Создаём правую панель с кнопками
right_panel = tk.Frame(root)
right_panel.grid(row=2, column=1, rowspan=4, padx=20, pady=10, sticky='n')

# Кнопка "Вверх"
up_button = ttk.Button(right_panel, text="Вверх", command=move_up)
up_button.pack(pady=10)

# Кнопка "Вниз"
down_button = ttk.Button(right_panel, text="Вниз", command=move_down)
down_button.pack(pady=10)

# Кнопка "Выход"
exit_button = ttk.Button(right_panel, text="Выход", command=exit_program)
exit_button.pack(pady=10)

# Запускаем главный цикл
if __name__ == "__main__":
    root.mainloop()
