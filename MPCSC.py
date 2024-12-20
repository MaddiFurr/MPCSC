import platform
import datetime
from sysinfo import get_system_info
from benchmarks import cpu_benchmark, gpu_benchmark, network_benchmark

def format_markdown(system_info, single_threaded_score, multi_threaded_score, gpu_score, network_info):
    """Formats system information and benchmark results into Markdown with program name, link, 
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
                if "Manufacturer" in drive:
                    markdown_text += f"> Manufacturer: {drive['Manufacturer']}\n"
                if "Model" in drive:
                    markdown_text += f"> Model: {drive['Model']}\n"
                if "Part Number" in drive:
                    markdown_text += f"> Part Number: {drive['Part Number']}\n"
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

    markdown_text += f"**CPU Benchmark Scores**\n"
    markdown_text += f"> Single-threaded: {single_threaded_score} primes\n"
    markdown_text += f"> Multi-threaded: {multi_threaded_score} primes\n\n"

    markdown_text += f"**GPU Benchmark Score**\n"
    markdown_text += f"> Frames Rendered: {gpu_score} frames\n\n"

    markdown_text += f"**Network Speed Test Results**\n"
    markdown_text += f"> Download Speed: {network_info['Network']['Download (Mbps)']} Mbps\n"
    markdown_text += f"> Upload Speed: {network_info['Network']['Upload (Mbps)']} Mbps\n"
    markdown_text += f"> Ping: {network_info['Network']['Ping (ms)']} ms\n"

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
    
    print("\nPerforming CPU benchmark...")
    single_threaded_score, multi_threaded_score = cpu_benchmark.run_benchmark_and_display()
    
    print("\nPerforming GPU benchmark...")
    frame_count = gpu_benchmark.gpu_stress_test()
    print(f"GPU Benchmark Score: {frame_count} frames rendered")
    
    print("\nPerforming network speed test...")
    network_info = network_benchmark.perform_network_speed_test()
    print(f"Network Speed Test Results: {network_info}")
    
    system_info = get_system_info()
    markdown_output = format_markdown(system_info, single_threaded_score, multi_threaded_score, frame_count, network_info)
    copy_to_clipboard(markdown_output)
    print(markdown_output)