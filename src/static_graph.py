import csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Чтение данных из CSV файла
timestamps = []
cpu_percent = []
ram_percent = []

with open('system_log.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Преобразуем timestamp в datetime объект
        timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
        timestamps.append(timestamp)
        cpu_percent.append(float(row['cpu_percent']))
        ram_percent.append(float(row['ram_percent']))

# Создание графика
fig, ax = plt.subplots(figsize=(10, 6))

# Построение линий для CPU и RAM
ax.plot(timestamps, cpu_percent, label='CPU %', marker='o', linewidth=2, color='red')
ax.plot(timestamps, ram_percent, label='RAM %', marker='s', linewidth=2, color='blue')

# Настройка осей и форматирования
ax.set_xlabel('Время', fontsize=12)
ax.set_ylabel('Процент использования', fontsize=12)
ax.set_title('Использование CPU и RAM', fontsize=14, fontweight='bold')

# Форматирование оси X для отображения времени
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
fig.autofmt_xdate()  # Автоматический поворот меток времени

# Добавление сетки и легенды
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(loc='best', fontsize=10)

# Установка пределов оси Y
ax.set_ylim(0, 100)

# Оптимизация макета
plt.tight_layout()

# Отображение графика
plt.show()