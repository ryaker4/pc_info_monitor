import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.dates import DateFormatter

# Запрос имени файла у пользователя
while True:
    filename = input('Введите название файла с логами: ')
    
    if not filename.endswith('.csv'):
        print('Ошибка: файл должен иметь расширение .csv')
        continue
    
    if not os.path.exists(filename):
        print(f'Ошибка: файл "{filename}" не найден')
        continue
    
    break

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Мониторинг системы в реальном времени', fontsize=16, fontweight='bold')

timestamps = []
cpu_data = []
ram_data = []
net_sent_data = []
net_recv_data = []
disk_data = []

def read_csv_data():
    """Читает все данные из CSV файла."""
    timestamps.clear()
    cpu_data.clear()
    ram_data.clear()
    net_sent_data.clear()
    net_recv_data.clear()
    disk_data.clear()
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
                timestamps.append(timestamp)
                cpu_data.append(float(row['cpu_percent']))
                ram_data.append(float(row['ram_percent']))
                net_sent_data.append(float(row.get('net_sent_kbps', 0)))
                net_recv_data.append(float(row.get('net_recv_kbps', 0)))
                disk_data.append(float(row.get('disk_percent', 0)))
    except Exception as e:
        print(f'Ошибка чтения файла: {e}')

def update(frame):
    """Функция обновления графиков."""
    read_csv_data()
    
    if not timestamps:
        return
    
    for ax in axes.flat:
        ax.clear()
    
    # График CPU
    axes[0, 0].plot(timestamps, cpu_data, color='red', marker='o', linewidth=2, markersize=4)
    axes[0, 0].set_title('Использование CPU', fontsize=12, fontweight='bold')
    axes[0, 0].set_ylabel('Процент', fontsize=10)
    axes[0, 0].set_ylim(0, 100)
    axes[0, 0].grid(True, linestyle='--', alpha=0.7)
    axes[0, 0].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    
    # График RAM
    axes[0, 1].plot(timestamps, ram_data, color='blue', marker='s', linewidth=2, markersize=4)
    axes[0, 1].set_title('Использование RAM', fontsize=12, fontweight='bold')
    axes[0, 1].set_ylabel('Процент', fontsize=10)
    axes[0, 1].set_ylim(0, 100)
    axes[0, 1].grid(True, linestyle='--', alpha=0.7)
    axes[0, 1].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    
    # График сети
    axes[1, 0].plot(timestamps, net_sent_data, label='Отправка', color='green', linewidth=2)
    axes[1, 0].plot(timestamps, net_recv_data, label='Получение', color='orange', linewidth=2)
    axes[1, 0].set_title('Сетевой трафик', fontsize=12, fontweight='bold')
    axes[1, 0].set_ylabel('KB/s', fontsize=10)
    axes[1, 0].set_xlabel('Время', fontsize=10)
    axes[1, 0].grid(True, linestyle='--', alpha=0.7)
    axes[1, 0].legend(loc='best', fontsize=9)
    axes[1, 0].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    
    # График диска
    axes[1, 1].plot(timestamps, disk_data, color='purple', marker='^', linewidth=2, markersize=4)
    axes[1, 1].set_title('Использование диска', fontsize=12, fontweight='bold')
    axes[1, 1].set_ylabel('Процент', fontsize=10)
    axes[1, 1].set_ylim(0, 100)
    axes[1, 1].set_xlabel('Время', fontsize=10)
    axes[1, 1].grid(True, linestyle='--', alpha=0.7)
    axes[1, 1].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    
    for ax in axes.flat:
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')


ani = animation.FuncAnimation(fig, update, interval=2000, cache_frame_data=False)


plt.tight_layout()
plt.show()