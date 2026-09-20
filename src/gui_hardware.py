import tkinter as tk
from tkinter import ttk
import platform
import psutil

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Монитор системы (PC Info Monitor)")
        self.root.geometry("1000x800")
        self.root.resizable(False, False)

        # Верхняя панель
        top_frame = ttk.Frame(root, padding="10")
        top_frame.pack(fill=tk.X)

        ttk.Button(top_frame, text="Обновить", command=self.update_info).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Выход", command=root.quit).pack(side=tk.RIGHT, padx=5)

        # Область для вывода текста
        self.text_area = tk.Text(root, height=15, width=50, font=("Consolas", 11), bg="#1e1e1e", fg="#00ff00")
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Запуск и автообновление
        self.update_info()

    def get_cpu_info(self):
        cpu_text = (f"CPU:\n{platform.processor()}\n"
                    f"Физические ядра: { psutil.cpu_count(logical=False)}\n"
                    f"Всего ядер: {psutil.cpu_count(logical=True)}\n")
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            cpu_text += f"Ядро {i}: {percentage}%\n"
        cpu_text += f"Всего CPU использовано: {psutil.cpu_percent()}%\n"
        return cpu_text

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
    
        

    def update_info(self):
        # 1. Очищаем текстовое поле
        self.text_area.delete(1.0, tk.END)
        
        # 2. Собираем и вставляем новую информацию
        info = self.get_cpu_info() + self.get_memory_info() + self.get_disk_info()
        self.text_area.insert(tk.END, info)
        
        # 3. Планируем следующий вызов этой же функции через 2000 мс (2 секунды)
        self.root.after(2000, self.update_info)

if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.tk.call('tk', 'scaling', 1.5) # Увеличение масштаба для HiDPI экранов
    except:
        pass
    
    app = SystemMonitorApp(root)
    root.mainloop()



        
        
        