import psutil
import platform
import argparse
import contextlib

import csv
import time
import os
from datetime import datetime


def cpu_info():
    cpu_text = (f"CPU:\n{platform.processor()}\n"
                f"Физические ядра: { psutil.cpu_count(logical=False)}\n"
                f"Всего ядер: {psutil.cpu_count(logical=True)}\n")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        cpu_text += f"Ядро {i}: {percentage}%\n"
    cpu_text += f"Всего CPU использовано: {psutil.cpu_percent()}%\n"
    return cpu_text
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
def get_memory_info(self): 
    mem = psutil.virtual_memory()
    return ("Оперативная память:\n"
            f"Всего: {get_size(mem.total)}\n"
            f"Доступно: {get_size(mem.available)}\n"
            f"Использовано: {get_size(mem.used)}\n"
            f"Процент использования: {mem.percent}%\n")
    
def get_disk_info(self):
    partitions = psutil.disk_partitions(all=False)
    disk_text = "Диски\n"
    for part in partitions:
        usage = psutil.disk_usage(part.mountpoint)
        disk_text += (f"Устройство:{part.device}\n"
                    f"Путь: {part.mountpoint}\n"
                    f"Тип: {part.fstype}\n"
                    f"Всего:{get_size(usage.total)}\n"
                    f"Использовано { get_size(usage.used)}\n"
                    f"Доступно { get_size(usage.free)}\n")
    return disk_text

# --- Логирование в CSV ---
def log_to_csv(filepath, components):
    """Записывает одну строку лога в CSV-файл."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Собираем данные
    row = {"timestamp": timestamp}
    row["cpu_percent"] = psutil.cpu_percent()
    row["ram_percent"] = psutil.virtual_memory().percent


    # Проверяем, существует ли файл, чтобы записать заголовок только один раз
    file_exists = os.path.exists(filepath)

    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def start_logging(components, interval, filepath):
    """Цикл логирования с заданным интервалом."""
    print(f"Логирование запущено!")
    print(f"   Компоненты: {', '.join(components)}")
    print(f"   Интервал: {interval} сек")
    print(f"   Файл: {filepath}")
    print(f"   Нажмите Ctrl+C для остановки\n")

    try:
        while True:
            log_to_csv(filepath, components)
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Запись добавлена в {filepath}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\nЛогирование остановлено. Данные сохранены в {filepath}")

def main():
    parser = argparse.ArgumentParser(description="System monitor")
    parser.add_argument(
        "component",
        choices=["cpu", "memory", "disk", "all"],
        help="Что показать: cpu, memory, disk или all"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Подробный вывод"
    )
    #аргумент путь к файлу
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Сохранить вывод в текстовый файл (например: report.txt)"
    )

    parser.add_argument(
        "-t", "--time",
        type=int,
        default=5,
        help="Задать интервал логирования(указывать в секундах)"
    )

    parser.add_argument(
        "--log",
        action="store_true",
        help="Включить режим непрерывного логирования в CSV(По умолчанию:system_log.csv)"
    )
    
    args = parser.parse_args()
    
    if args.log:
        log_file = args.output if args.output else "system_log.csv"
        log_components = ["cpu", "memory"]
        start_logging(log_components, args.time, log_file)
        return
    
    # Функция-обертка для запуска нужных модулей
    def run_info():
        if args.component in ["cpu", "all"]:
            print(cpu_info())
        if args.component in ["memory", "all"]:
            print(memory_info())
        if args.component in ["disk", "all"]:
            print(disk_info())
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            with contextlib.redirect_stdout(f):
                run_info()
        print(f"Информация успешно сохранена в файл: {args.output}")
    else:
        # Если файл не указан, просто выводим в терминал
        run_info()

if __name__ == "__main__":
    main()

