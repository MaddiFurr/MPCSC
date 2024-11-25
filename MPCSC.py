import datetime
import math
import platform
import re
import psutil
import speedtest

# For Windows-specific functions
try:
    import wmi
except ImportError:
    wmi = None


def get_system_info():
    """Gathers comprehensive system information with progress updates."""

    print("\n\033[1;33m[INFO]\033[0m Starting system diagnostics...")

    system_info = {}

    # --- CPU Information ---
    print("\033[1;34m[CPU]\033[0m Gathering CPU information...")
    system_info["CPU"] = {}
    if wmi:
        c = wmi.WMI()
        for cpu in c.Win32_Processor():
            system_info["CPU"]["Name"] = cpu.Name
            system_info["CPU"]["Cores"] = psutil.cpu_count(logical=False)
            system_info["CPU"]["Logical Cores"] = psutil.cpu_count(
                logical=True
            )
            system_info["CPU"]["Current Speed (GHz)"] = round(
                cpu.CurrentClockSpeed / 1000, 2
            )
            system_info["CPU"]["Base Speed (GHz)"] = round(
                cpu.MaxClockSpeed / 1000, 2
            )
            break
    print("\033[1;32m[CPU]\033[0m CPU information gathered successfully!")

    # --- GPU Information ---
    print("\033[1;34m[GPU]\033[0m Gathering GPU information...")
    system_info["GPU"] = []
    if wmi:
        c = wmi.WMI()
        for gpu in c.Win32_VideoController():
            gpu_info = {
                "Name": gpu.Name,
                "DriverVersion": gpu.DriverVersion,
            }
            if gpu.AdapterRAM is not None and gpu.AdapterRAM > 0:
                gpu_info["AdapterRAM (GB)"] = round(
                    gpu.AdapterRAM / (1024**3), 2
                )
            else:
                gpu_info["AdapterRAM (GB)"] = "Not available"
            system_info["GPU"].append(gpu_info)
    print("\033[1;32m[GPU]\033[0m GPU information gathered successfully!")

    # --- Storage Information ---
    print("\033[1;34m[STORAGE]\033[0m Gathering storage information...")
    system_info["Storage"] = []
    if wmi:
        c = wmi.WMI()
        physical_disks = c.Win32_DiskDrive()
        for partition in psutil.disk_partitions():
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                device_info = {
                    "Device": partition.device,
                    "Mount Point": partition.mountpoint,
                    "File System": partition.fstype,
                    "Total Size (GB)": round(
                        partition_usage.total / (1024**3), 2
                    ),
                    "Used Space (GB)": round(
                        partition_usage.used / (1024**3), 2
                    ),
                    "Free Space (GB)": round(
                        partition_usage.free / (1024**3), 2
                    ),
                }
                for (
                    physical_disk
                ) in physical_disks:
                    if re.search(
                        rf"{physical_disk.DeviceID.replace('\\', '\\\\')}",
                        partition.device,
                    ):
                        device_info["Type"] = physical_disk.MediaType
                        device_info["Model"] = physical_disk.Model
                        break
                system_info["Storage"].append(device_info)
            except PermissionError:
                pass
    else:  # For non-Windows systems
        for partition in psutil.disk_partitions():
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                device_info = {
                    "Device": partition.device,
                    "Mount Point": partition.mountpoint,
                    "File System": partition.fstype,
                    "Total Size (GB)": round(
                        partition_usage.total / (1024**3), 2
                    ),
                    "Used Space (GB)": round(
                        partition_usage.used / (1024**3), 2
                    ),
                    "Free Space (GB)": round(
                        partition_usage.free / (1024**3), 2
                    ),
                }
                system_info["Storage"].append(device_info)
            except PermissionError:
                pass
    print(
        "\033[1;32m[STORAGE]\033[0m Storage information gathered successfully!"
    )

    # --- Memory Information ---
    print("\033[1;34m[MEMORY]\033[0m Gathering memory information...")
    mem = psutil.virtual_memory()
    system_info["Memory"] = {
        "Total (GB)": round(mem.total / (1024**3), 2),
        "Available (GB)": round(mem.available / (1024**3), 2),
        "Used (GB)": round(mem.used / (1024**3), 2),
        "Percentage Used": mem.percent,
    }
    if wmi:
        c = wmi.WMI()
        for mem_module in c.Win32_PhysicalMemory():
            system_info["Memory"]["Speed (MHz)"] = mem_module.Speed
            break
    print("\033[1;32m[MEMORY]\033[0m Memory information gathered successfully!")

    # --- Network Speed Test ---
    print("\033[1;34m[NETWORK]\033[0m Performing network speed test...")
    try:
        st = speedtest.Speedtest()
        st.download()
        st.upload()
        system_info["Network"] = {
            "Download (Mbps)": round(st.results.download / 1000000, 2),
            "Upload (Mbps)": round(st.results.upload / 1000000, 2),
            "Ping (ms)": round(st.results.ping, 2),
        }
        print("\033[1;32m[NETWORK]\033[0m Network speed test completed!")
    except speedtest.ConfigRetrievalError:
        system_info["Network"] = {"Error": "Could not perform speed test."}
        print(
            "\033[1;31m[NETWORK]\033[0m Error: Could not perform speed test."
        )

    print("\033[1;33m[INFO]\033[0m System diagnostics complete!\n")

    return system_info


def format_markdown(system_info):
    """Formats system information into Markdown with program name, link, 
    system name, and date/time."""

    markdown_text = f"## [Maddi's Personal Computer Specification Checker](https://maddi.wtf)\n"

    hostname = platform.node()
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    markdown_text += f"**System:** {hostname}\n"
    markdown_text += f"**Date/Time:** {timestamp}\n\n"

    for section, info in system_info.items():
        if section == "Storage":
            for i, drive in enumerate(info):
                markdown_text += f"**Storage Device {i+1}**\n"
                for key, value in drive.items():
                    if key == "Used Space (GB)":
                        total = drive["Total Size (GB)"]
                        used_percent = round((value / total) * 100, 1)
                        markdown_text += f"> {key}: {value} GB ({used_percent}%)\n"
                    else:
                        markdown_text += f"> {key}: {value}\n"
                markdown_text += "\n"
        else:
            markdown_text += f"**{section}**\n"
            if isinstance(info, list):
                for item in info:
                    for key, value in item.items():
                        markdown_text += f"> {key}: {value}\n"
            else:
                for key, value in info.items():
                    if key == "Used (GB)":
                        total = info["Total (GB)"]
                        used_percent = round((value / total) * 100, 1)
                        markdown_text += f"> {key}: {value} GB ({used_percent}%)\n"
                    else:
                        markdown_text += f"> {key}: {value}\n"
            markdown_text += "\n"

    return markdown_text


def copy_to_clipboard(text):
    """Copies the given text to the clipboard."""
    try:
        import pyperclip

        pyperclip.copy(text)
        print("\033[1;32m[INFO]\033[0m System information copied to clipboard!")
    except ImportError:
        print(
            "\033[1;31m[ERROR]\033[0m 'pyperclip' not installed. Cannot copy to clipboard."
        )

if __name__ == "__main__":
    system_info = get_system_info()
    markdown_output = format_markdown(system_info)
    copy_to_clipboard(markdown_output)