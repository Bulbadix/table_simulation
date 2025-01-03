import tkinter as tk
from tkinterweb import HtmlFrame  # Используем HtmlFrame вместо Web
import plotly.graph_objects as go
import numpy as np
import os

# Создание данных для 3D-графика
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
x, y = np.meshgrid(x, y)
z = np.sin(np.sqrt(x**2 + y**2))

# Создание 3D графика
fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])

# Настройка осей и отображение
fig.update_layout(
    title='3D Surface plot',
    scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z')
)

# Сохранение графика в HTML файл
html_file = "plot.html"
fig.write_html(html_file)

# Создание Tkinter окна
root = tk.Tk()
root.title("Plotly в Tkinter")

# Создание виджета для отображения HTML
browser = HtmlFrame(root, width=100, height=40)
browser.pack(padx=10, pady=10)

# Загружаем HTML-файл с помощью load_file
browser.load_file(os.path.abspath(html_file))

# Запуск Tkinter
root.mainloop()
