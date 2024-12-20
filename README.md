# Maddi's Personal Computer Specification Checker (MPCSC)

This Python script gathers comprehensive information about your computer system, including CPU, GPU, storage, memory, and network details, and presents it in a user-friendly format. It also formats the information into Markdown text for easy sharing.

## Features

- **Comprehensive System Information:** Gathers details about:
    - CPU (name, cores, speed, etc.)
    - GPU (name, memory, driver version)
    - Storage devices (type, model, capacity, usage, manufacturer, part number)
    - Memory (total, used, speed)
    - Network (download/upload speed, ping)
- **Markdown Formatting:** Formats the system information into Markdown text for easy sharing on platforms like Discord.
- **Clipboard Copying:** Copies the Markdown-formatted text to the clipboard for quick pasting.
- **Benchmarks:** Includes CPU, GPU, and network benchmarks to give a rough indication of system performance.

## Disclaimer

The benchmark numbers provided by this script are not indicative of true performance and are meant to give a rough placement of your system. They should not be used as a definitive measure of performance.

## Requirements

- Python 3.6 or higher
- `psutil` library (`pip install psutil`)
- `speedtest-cli` library (`pip install speedtest-cli`)
- `wmi` library (for Windows) (`pip install wmi`)
- `pyperclip` library (`pip install pyperclip`)
- `tqdm` library (`pip install tqdm`)

## Usage

**Install the required libraries:**
```bash
pip install psutil speedtest-cli wmi pyperclip tqdm