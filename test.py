import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Параметры
L_x = 0.05  # длина по оси X (м)
L_y = 0.1   # длина по оси Y (м)
L_z = 0.1   # длина по оси Z (м)
T_initial = 500  # начальная температура объекта (°C)
T_ambient = 20  # температура окружающей среды (°C)
alpha = 1.5e-6  # коэффициент теплопроводности (м^2/с)
Nx = 20  # количество точек по оси X
Ny = 40  # количество точек по оси Y
Nz = 10  # количество точек по оси Z
Nt = 500  # количество временных шагов
dt = 0.1  # шаг по времени (с)

# Дискретизация
dx = L_x / (Nx - 1)
dy = L_y / (Ny - 1)
dz = L_z / (Nz - 1)

# Координаты сетки
x = np.linspace(0, L_x, Nx)
y = np.linspace(0, L_y, Ny)
z = np.linspace(0, L_z, Nz)

# Начальная температура (весь объект нагрет до T_initial)
T = np.ones((Nx, Ny, Nz)) * T_initial

# Моделирование теплопередачи
for n in range(1, Nt):
    T_new = T.copy()
    
    # Обновляем температуру в пространстве
    for i in range(1, Nx - 1):
        for j in range(1, Ny - 1):
            for k in range(1, Nz - 1):
                T_new[i, j, k] = T[i, j, k] + alpha * dt * (
                    (T[i + 1, j, k] - 2 * T[i, j, k] + T[i - 1, j, k]) / dx**2 +
                    (T[i, j + 1, k] - 2 * T[i, j, k] + T[i, j - 1, k]) / dy**2 +
                    (T[i, j, k + 1] - 2 * T[i, j, k] + T[i, j, k - 1]) / dz**2)
    
    # Применяем граничные условия
    T_new[0, :, :] = T_ambient
    T_new[-1, :, :] = T_ambient
    T_new[:, 0, :] = T_ambient
    T_new[:, -1, :] = T_ambient
    T_new[:, :, 0] = T_ambient
    T_new[:, :, -1] = T_ambient
    
    T = T_new

    # Визуализация после нескольких шагов
    if n % 50 == 0:
        # Генерируем сетку для осей X и Y
        Y, X = np.meshgrid(y, x)  # Поменяли местами x и y для согласования с температурным полем
        Z = T[:, :, Nz // 2]  # Срез по оси Z
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Создаем поверхность
        surf = ax.plot_surface(X, Y, Z, cmap='inferno', edgecolor='none')

        # Настройка графика
        ax.set_xlabel('X (м)')
        ax.set_ylabel('Y (м)')
        ax.set_zlabel('Температура (°C)')
        ax.set_title(f'Temperature distribution at time {n * dt:.2f} s')

        # Показать цветовую шкалу
        fig.colorbar(surf)

        # Отображаем график
        plt.show()
