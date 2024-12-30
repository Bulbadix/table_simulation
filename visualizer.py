from cProfile import label
from cgitb import text
from tkinter import *
import tkinter as tk
from tkinter import ttk
from table import Table
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import cm
from cuboid import Cuboid
import xml.etree.ElementTree as ET

# Инициализация объекта стола
table = Table('table_data.xml')
# Читаем XML-файл
tree = ET.parse('table_data.xml')  # Замените на путь к вашему XML-файлу
root = tree.getroot()


selected_motherboard_type = "none"

def selected(event):
    # получаем выделенный элемент
    global selected_motherboard_type
    selected_motherboard_type = combobox.get()
    print(selected_motherboard_type)
    label["text"] = f"вы выбрали: {selected_motherboard_type}"
    update_cuboid(selected_motherboard_type)
    
# Список для материнских плат
motherboards = []

# Ищем все теги типов материнских плат внутри тега <type>
type_element = root.find('.//motherboard/type')  # Находим элемент <type> внутри <motherboard>

# Добавляем типы материнских плат в список
if type_element is not None:
    for motherboard_type in type_element:
        motherboard_name = motherboard_type.tag
        motherboards.append(motherboard_name)
        
# Инициализация объекта кубоида
cuboid = Cuboid('table_data.xml', selected_motherboard_type, center_x=table.table_width / 2, center_y=table.table_length / 2, center_z=table.current_height + (table.board_height / 2) - 50 / 2)

def update_cuboid(motherboard_type):
    global cuboid
    # Обновляем кубоид с новыми размерами на основе выбранного типа
    cuboid = Cuboid('table_data.xml', motherboard_type, center_x=table.table_width / 2, center_y=table.table_length / 2, center_z=table.current_height + (table.board_height / 2) - 50 / 2)
    update_visualization()  # Обновляем визуализацию с новыми размерами кубоида

# Обновление визуализации
def update_visualization():
    for widget in frame.winfo_children():
        widget.destroy()

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    table.draw(ax)
    # Визуализируем кубоид
    cuboid.draw(ax)

    # Настройка осей
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Ограничиваем оси
    ax.set_xlim([0, table.table_width])
    ax.set_ylim([0, table.table_length])
    ax.set_zlim([0, table.max_height + table.board_height])     # Устанавливаем ось Z от 0 до max_height + board_height

    # Вычисляем соотношение сторон для правильного отображения
    aspect_ratio_x = table.table_width
    aspect_ratio_y = table.table_length
    aspect_ratio_z = table.max_height

    ax.set_box_aspect([aspect_ratio_x, aspect_ratio_y, aspect_ratio_z])

    # Включаем сетку
    ax.grid(True)
    # Отображаем обновленный график
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Функции для изменения высоты стола
def move_up():
    if table.current_height < table.max_height:
        table.current_height += table.step
        cuboid.center_z += table.step
        height_label.config(text=f"Высота стола: {table.current_height} мм")
        update_visualization()

def move_down():
    if table.current_height > table.min_height:
        table.current_height -= table.step
        cuboid.center_z -= table.step
        height_label.config(text=f"Высота стола: {table.current_height} мм")
        update_visualization()

# Основное окно
root = tk.Tk()
root.title("Регулировка высоты стола")

# Заголовок
header_label = ttk.Label(root, text="Стол %dx%d мм"%(table.table_width, table.table_length), font=("Arial", 16))
header_label.grid(row=0, column=0, columnspan=2, pady=10)

# Метка высоты стола
height_label = ttk.Label(root, text=f"Высота стола: {table.current_height} мм", font=("Arial", 14))
height_label.grid(row=1, column=0, columnspan=2, pady=10)

# Рамка для визуализации
frame = tk.Frame(root)
frame.grid(row=2, column=0, rowspan=4, padx=10, pady=10)

# Начальная визуализация
update_visualization()

# Панель управления
right_panel = tk.Frame(root)
right_panel.grid(row=2, column=1, rowspan=4, padx=20, pady=10, sticky='n')

# Кнопки
up_button = ttk.Button(right_panel, text="Вверх", command=move_up)
up_button.pack(pady=10)
down_button = ttk.Button(right_panel, text="Вниз", command=move_down)
down_button.pack(pady=10)




# Кнопка выхода
exit_button = ttk.Button(right_panel, text="Выход", command=root.quit)
exit_button.pack(pady=10)

# Комбобокс с материнскими платами 
motherboards_var = StringVar(value=motherboards[0]) 
label = ttk.Label(textvariable=motherboards_var) 
combobox = ttk.Combobox(right_panel, textvariable=motherboards_var, values=motherboards, state="readonly") 
combobox.pack(padx=6, pady=6) 
combobox.bind("<<ComboboxSelected>>", selected)


# Запуск приложения
if __name__ == "__main__":
    root.mainloop()
