# Maddi's Personal Computer Specification Checker (MPCSC)

This Python script gathers comprehensive information about your computer system, including CPU, GPU, storage, memory, and network details, and presents it in a user-friendly format. It also generates a visually appealing image with graphs and charts summarizing the system diagnostics.

## Features

- **Comprehensive System Information:** Gathers details about:
    - CPU (name, cores, speed, etc.)
    - GPU (name, memory, driver version)
    - Storage devices (type, model, capacity, usage)
    - Memory (total, used, speed)
    - Network (download/upload speed, ping)
- **Markdown Formatting:** Formats the system information into Markdown text for easy sharing on platforms like Discord.
- **Clipboard Copying:** Copies the Markdown-formatted text to the clipboard for quick pasting.
- **Image Generation:** Creates an image with graphs and charts visualizing the system data.
- **Watermark:** Adds a watermark to the image with the program name, your website link, system name, and timestamp.

## Requirements

- Python 3.6 or higher
- `psutil` library (`pip install psutil`)
- `speedtest-cli` library (`pip install speedtest-cli`)
- `wmi` library (for Windows) (`pip install wmi`)
- `pyperclip` library (`pip install pyperclip`)
- `matplotlib` library (`pip install matplotlib`)

## Usage

**Install the required libraries:**
```bash
pip install psutil speedtest-cli wmi pyperclip matplotlib
```
python mpcsc.py  # Replace mpcsc.py with the actual filename
