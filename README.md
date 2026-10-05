# 🖥️ SystemInfo Tool

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Interface](https://img.shields.io/badge/Interface-CLI-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

A lightweight, cross-platform **command-line system monitoring tool** written in Python. It gathers operating system, CPU, RAM, storage, and GPU details and displays them in a colorful, well-structured terminal dashboard that **refreshes automatically every 2 seconds**.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Installation](#-installation)
- [Usage](#-usage)
- [Information Displayed](#-information-displayed)
- [Sample Output](#-sample-output)
- [Platform Support](#-platform-support)
- [Customization](#-customization)
- [Troubleshooting](#-troubleshooting)
- [Known Limitations](#-known-limitations)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 📖 Overview

**SystemInfo Tool** is a simple but useful utility for quickly checking what is running inside your machine. Instead of opening multiple system panels, you can run a single command and see everything in one place, updated live.

The project is split into small, easy-to-understand modules:

- one module **collects** the data,
- one module **displays** the data,
- one module **runs** the loop.

This makes the code easy to read, maintain, and extend.

---

## ✨ Features

- 🔄 **Live monitoring** – the screen is cleared and refreshed every 2 seconds
- 🧩 **Operating System details** – system name, release, build number, kernel, architecture
- ⚙️ **CPU details** – model name, physical cores, logical cores, maximum frequency
- 🧠 **RAM details** – total, available, used memory and usage percentage
- 💾 **Storage details** – every partition with total, used, and free space, file system, usage percentage, and SSD/HDD type
- 🎮 **GPU details** – name, driver, total/used/free memory, utilization, and temperature
- 🎨 **Colorful interface** – color-coded sections and values using `colorama`
- 🛡️ **Error handling** – unexpected errors are caught and shown clearly
- ⌨️ **Clean exit** – press `Ctrl+C` to stop the program safely

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core programming language |
| [psutil](https://pypi.org/project/psutil/) | CPU, RAM, and disk information |
| [GPUtil](https://pypi.org/project/GPUtil/) | GPU information (NVIDIA GPUs) |
| [colorama](https://pypi.org/project/colorama/) | Cross-platform colored terminal output |
| `platform`, `subprocess`, `re`, `os`, `sys` | Python standard library modules |

---

## 📂 Project Structure

```
systeminfo/
├── main.py              # Entry point – runs the live refresh loop
├── interface.py         # CLI interface – colors, headers, formatted output
├── systemdetection.py   # Data collection – OS, CPU, RAM, disk, GPU
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

| File | Responsibility |
|------|----------------|
| `main.py` | Clears the screen, prints the header, fetches data, displays it, waits 2 seconds, and repeats |
| `interface.py` | Screen clearing, ASCII banner, section headers, key-value printing, error/warning messages |
| `systemdetection.py` | Functions that gather all system information and return it as a dictionary |
| `requirements.txt` | List of packages required to run the project |

---

## ⚙️ How It Works

```
┌──────────────┐     get_all_info()      ┌─────────────────────┐
│   main.py    │ ──────────────────────► │  systemdetection.py │
│ (loop: 2s)   │ ◄────────────────────── │  (collect data)     │
└──────┬───────┘     info dictionary     └─────────────────────┘
       │
       │ display_info(info)
       ▼
┌──────────────┐
│ interface.py │  → colored, formatted output in the terminal
└──────────────┘
```

**Step by step:**

1. `main.py` starts an infinite loop.
2. In every cycle it clears the screen and prints the header.
3. It calls `get_all_info()` from `systemdetection.py`, which returns a dictionary containing `os`, `cpu`, `ram`, `disks`, and `gpus`.
4. The dictionary is passed to `display_info()` in `interface.py`, which prints each section in color.
5. The program sleeps for 2 seconds and the loop repeats.
6. On `Ctrl+C`, the loop stops and the program exits cleanly.

### Functions in `systemdetection.py`

| Function | Description |
|----------|-------------|
| `get_os_info()` | Returns OS name, release, version, architecture, build, and kernel |
| `get_cpu_info()` | Returns CPU model, physical/logical cores, and max frequency |
| `get_ram_info()` | Returns total, available, used RAM (in GB) and usage percent |
| `get_disk_info()` | Returns a list of partitions with size, usage, and file system |
| `detect_disk_type(device)` | Tries to detect whether a disk is `SSD`, `HDD`, or `Unknown` |
| `get_gpu_info()` | Returns a list of GPUs with name, driver, memory, load, and temperature |
| `get_all_info()` | Combines everything into a single dictionary |

### Functions in `interface.py`

| Function | Description |
|----------|-------------|
| `clear_screen()` | Clears the terminal (`cls` on Windows, `clear` on others) |
| `print_header()` | Prints the banner and short description |
| `print_section(title)` | Prints a styled section title |
| `print_key_value(key, value, indent)` | Prints a key-value pair (supports nested dicts and lists) |
| `display_info(info)` | Displays all collected information |
| `colorize(text, color, style)` | Returns colored text |
| `print_error(msg)` / `print_warning(msg)` | Prints red errors and yellow warnings |

---

## 🚀 Installation

### Prerequisites

- **Python 3.8 or higher** – check with `python --version`
- **pip** – Python package manager
- **Git** (optional, only for cloning)

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/systeminfo.git
cd systeminfo
```

**2. (Recommended) Create a virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

**3. Install the dependencies**

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the program from the project folder:

```bash
# Windows
python main.py

# Linux / macOS
python3 main.py
```

The dashboard will start and refresh every **2 seconds**.

To stop it, press:

```
Ctrl + C
```

---

## 📊 Information Displayed

| Section | Details |
|---------|---------|
| **Operating System** | System, Release, Build Number, Kernel, Architecture |
| **CPU** | Model, Physical Cores, Logical Cores, Max Frequency (MHz) |
| **RAM** | Total (GB), Available (GB), Used (GB), Usage % |
| **Storage** | Device, Mount Point, File System, Total / Used / Free (GB), Usage %, Type (SSD/HDD) |
| **GPU(s)** | Name, Driver, Total / Used / Free Memory (MB), Utilization %, Temperature (°C) |

---

## 📸 Sample Output

```
SYSTEMINFO TOOL BY KENCYPHER

System Information Tool - Live Monitoring (refresh every 2s)
------------------------------------------------------------

Press Ctrl+C to exit

[ Operating System ]
----------------------------------------
System: Linux
Release: 6.x.x
Build Number: N/A
Kernel: 6.x.x
Architecture: x86_64

[ CPU ]
----------------------------------------
Model: Intel(R) Core(TM) i5
Physical Cores: 4
Logical Cores: 8
Max Frequency (MHz): 3600.0

[ RAM ]
----------------------------------------
Total (GB): 16.0
Available (GB): 9.8
Used (GB): 5.4
Usage %: 38.5

[ Storage ]
----------------------------------------
Device: /dev/sda1
  Mount Point: /
  File System: ext4
  Total (GB): 233.0
  Used (GB): 120.5
  Free (GB): 100.3
  Usage %: 54.5
  Type: SSD

[ GPU(s) ]
----------------------------------------
No GPU information available.
```

> ⚠️ These values are only an example. Your output depends on your own system.

---

## 🌐 Platform Support

| Feature | Windows | Linux | macOS |
|---------|:-------:|:-----:|:-----:|
| OS Information | ✅ | ✅ | ✅ |
| CPU Information | ✅ | ✅ | ✅ |
| RAM Information | ✅ | ✅ | ✅ |
| Disk Information | ✅ | ✅ | ✅ |
| SSD/HDD Detection | ⚠️ Limited | ✅ | ❌ |
| GPU Information (full) | ✅ NVIDIA | ✅ NVIDIA | ❌ |
| GPU Name (fallback) | ⚠️ Placeholder | ✅ via `lspci` | ✅ via `system_profiler` |

---

## 🎛️ Customization

| What you want to change | Where |
|-------------------------|-------|
| Refresh speed | `refresh_interval = 2` in `main.py` |
| Banner / title text | `print_header()` in `interface.py` |
| Colors | `Fore` and `Style` values in `interface.py` |
| Information collected | The `get_*_info()` functions in `systemdetection.py` |

---

## 🧯 Troubleshooting

| Problem | Possible Cause | Solution |
|---------|----------------|----------|
| `ModuleNotFoundError: No module named 'psutil'` | Dependencies not installed | Run `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'colorama'` | Dependencies not installed | Run `pip install -r requirements.txt` |
| "No GPU information available." | No NVIDIA GPU or driver missing | Install NVIDIA drivers, or ignore if you have no dedicated GPU |
| Disk type shows `Unknown` | Detection not supported on your OS or `wmic` is unavailable | This is expected on some systems |
| Some disks are missing | No permission to read the partition | Try running the terminal as Administrator / with `sudo` |
| Colors not showing | Terminal does not support ANSI colors | Use a modern terminal (Windows Terminal, VS Code, etc.) |

---

## ⚠️ Known Limitations

- GPU details (memory, load, temperature) depend on **GPUtil**, which works with **NVIDIA** GPUs only.
- SSD/HDD detection on Windows relies on `wmic`, which is deprecated in newer Windows versions, so the result may be `Unknown`.
- SSD/HDD detection is not implemented for macOS.
- On Windows, the **Build Number** field may not show the exact build.
- The screen is cleared on every refresh, so the output may flicker slightly in some terminals.

---

## 🔮 Future Improvements

- [ ] Add network usage information (upload/download speed)
- [ ] Add battery information for laptops
- [ ] Add CPU usage percentage per core
- [ ] Add a running processes section
- [ ] Add command-line options (e.g. custom refresh interval)
- [ ] Export system information to a JSON or text file
- [ ] Improve GPU support for AMD and Intel graphics

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. **Fork** the repository
2. **Create** a new branch: `git checkout -b feature/your-feature-name`
3. **Commit** your changes: `git commit -m "Add your feature"`
4. **Push** to the branch: `git push origin feature/your-feature-name`
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute it.

> If you choose a different license, update this section and the badge at the top.

---

## 👤 Author

**KenCypher**

- GitHub: [@your-username](https://github.com/your-username)

---

⭐ If you found this project useful, please consider giving it a star!
