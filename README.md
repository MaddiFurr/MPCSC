# Maddi's Personal Computer Specification Checker (MPCSC)

This Python script gathers comprehensive information about your computer system, including CPU, GPU, storage, memory, and network details, and presents it in a user-friendly format. It also generates a visually appealing image with graphs and charts summarizing the system diagnostics.

I honestly wrote this so that I can ask friends for their system specs without having to walk them through gathering it. The nice discord formatting makes things easier. Also it means I don't have to give them User Benchmark!

## Features

- **Comprehensive System Information:** Gathers details about:
    - CPU (name, cores, speed, etc.)
    - GPU (name, memory, driver version)
    - Storage devices (type, model, capacity, usage, manufacturer, part number)
    - Memory (total, used, speed)
    - Network (download/upload speed, ping)
- **Markdown Formatting:** Formats the system information into Markdown text for easy sharing on platforms like Discord.
- **Clipboard Copying:** Copies the Markdown-formatted text to the clipboard for quick pasting.

## Requirements

- Python 3.6 or higher
- `psutil` library (`pip install psutil`)
- `speedtest-cli` library (`pip install speedtest-cli`)
- `wmi` library (for Windows) (`pip install wmi`)
- `pyperclip` library (`pip install pyperclip`)

## Usage

**Install the required libraries:**
```bash
pip install psutil speedtest-cli wmi pyperclip
```
python mpcsc.py  # Replace mpcsc.py with the actual filename
