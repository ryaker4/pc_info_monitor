import psutil
import platform
import argparse
import GPUtil
def cpu_info():
    print(platform.processor())
    print("======\nCPU:")
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Total cores:", psutil.cpu_count(logical=True))
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
def memory_info():
    # memory info
    svmem = psutil.virtual_memory()
    print("======\nMemory:")
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")
def disk_info():
    partitions = psutil.disk_partitions(all=False)
    print("======\nPartitions:")
    for part in partitions:
        usage = psutil.disk_usage(part.mountpoint)
        print("Device:", part.device)
        print("Mount:",part.mountpoint)
        print("Type:", part.fstype)
        print("Total:", get_size(usage.total))
        print("Used", get_size(usage.used))
        print("Available", get_size(usage.free))
        print("======")
def gpu_info():
    gpus = GPUtil.getGPUs()
    list_gpus = []
    for gpu in gpus:
        gpu_name = gpu.name
        gpu_total_memory = f"{gpu.memoryTotal}MB"
        gpu_temperature = f"{gpu.temperature} °C"
        gpu_uuid = gpu.uuid
        print("Name: ", gpu_name)
        print("Memory: ", gpu_total_memory)
        print("Temperature: ", gpu_temperature)
        print("uuid: ", gpu_uuid)

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
    args = parser.parse_args()
    
    if args.component == "cpu":
        cpu_info()
    elif args.component == "memory":
        memory_info()
    elif args.component == "disk":
        disk_info()
    elif args.component == "all":
        cpu_info()
        memory_info()
        disk_info()

if __name__ == "__main__":
    main()

