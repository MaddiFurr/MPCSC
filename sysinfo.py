import platform
import datetime
import psutil
import wmi

def get_system_info():
    """Gathers system information."""
    system_info = {}

    # --- Storage Information ---
    print("\033[1;34m[STORAGE]\033[0m Gathering storage information...")
    system_info["Storage"] = []
    c = wmi.WMI()
    for partition in psutil.disk_partitions():
        if partition.fstype:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                device_info = {
                    "Device": partition.device,
                    "Mountpoint": partition.mountpoint,
                    "File System Type": partition.fstype,
                    "Total Size (GB)": round(usage.total / (1024**3), 2),
                    "Used Space (GB)": round(usage.used / (1024**3), 2),
                    "Free Space (GB)": round(usage.free / (1024**3), 2),
                    "Percentage Used": usage.percent,
                }

                # Get additional information using WMI
                for disk in c.Win32_DiskDrive():
                    if partition.device in disk.DeviceID:
                        device_info["Manufacturer"] = disk.Manufacturer
                        device_info["Model"] = disk.Model
                        device_info["Part Number"] = disk.PartNumber
                        break

                system_info["Storage"].append(device_info)
            except PermissionError:
                pass
    print("\033[1;32m[STORAGE]\033[0m Storage information gathered successfully!")

    # --- Memory Information ---
    print("\033[1;34m[MEMORY]\033[0m Gathering memory information...")
    mem = psutil.virtual_memory()
    system_info["Memory"] = {
        "Total (GB)": round(mem.total / (1024**3), 2),
        "Available (GB)": round(mem.available / (1024**3), 2),
        "Used (GB)": round(mem.used / (1024**3), 2),
        "Percentage Used": mem.percent,
    }
    for mem_module in c.Win32_PhysicalMemory():
        system_info["Memory"]["Speed (MHz)"] = mem_module.Speed
        break
    print("\033[1;32m[MEMORY]\033[0m Memory information gathered successfully!")

    return system_info

# Example usage
if __name__ == "__main__":
    system_info = get_system_info()
    print(system_info)