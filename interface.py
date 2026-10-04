"""
interface.py - CLI interface with colors, ASCII art, and formatted output.
Includes screen clearing and dynamic refresh support.
"""
import sys
import os
import platform
from colorama import init, Fore, Style

# Initialize colorama for cross-platform color support
init(autoreset=True)


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def print_header():
    """Print an ASCII art banner and a short description."""
    banner = r"""

SYSTEMINFO TOOL BY KENCYPHER

    """
    print(Fore.CYAN + banner)
    print(Fore.YELLOW + "System Information Tool - Live Monitoring (refresh every 2s)")
    print(Fore.WHITE + "-" * 60 + "\n")


def colorize(text, color=Fore.WHITE, style=Style.NORMAL):
    """Return colored text."""
    return f"{style}{color}{text}{Style.RESET_ALL}"


def print_section(title):
    """Print a section header."""
    print(Fore.MAGENTA + Style.BRIGHT + f"\n[ {title} ]" + Style.RESET_ALL)
    print(Fore.WHITE + "-" * 40)


def print_key_value(key, value, indent=0):
    """Print a key-value pair with optional indentation."""
    indent_str = " " * indent
    if isinstance(value, dict):
        print(f"{indent_str}{Fore.GREEN}{key}:")
        for k, v in value.items():
            print_key_value(k, v, indent + 4)
    elif isinstance(value, list):
        print(f"{indent_str}{Fore.GREEN}{key}:")
        for idx, item in enumerate(value, start=1):
            if isinstance(item, dict):
                print(f"{indent_str}  {Fore.CYAN}Item {idx}:")
                for k, v in item.items():
                    print_key_value(k, v, indent + 6)
            else:
                print(f"{indent_str}  - {item}")
    else:
        print(f"{indent_str}{Fore.CYAN}{key}: {Fore.WHITE}{value}")


def display_info(info):
    """Display all gathered information in a structured, colorful way."""
    # OS Info
    print_section("Operating System")
    os_d = info['os']
    print_key_value("System", os_d.get('system'))
    print_key_value("Release", os_d.get('release'))
    print_key_value("Build Number", os_d.get('build'))
    print_key_value("Kernel", os_d.get('kernel'))
    print_key_value("Architecture", os_d.get('architecture'))

    # CPU Info
    print_section("CPU")
    cpu_d = info['cpu']
    print_key_value("Model", cpu_d.get('model'))
    print_key_value("Physical Cores", cpu_d.get('physical_cores'))
    print_key_value("Logical Cores", cpu_d.get('logical_cores'))
    print_key_value("Max Frequency (MHz)", cpu_d.get('max_freq_mhz'))

    # RAM Info
    print_section("RAM")
    ram_d = info['ram']
    print_key_value("Total (GB)", ram_d.get('total_gb'))
    print_key_value("Available (GB)", ram_d.get('available_gb'))
    print_key_value("Used (GB)", ram_d.get('used_gb'))
    print_key_value("Usage %", ram_d.get('percent'))

    # Disk Info
    print_section("Storage")
    disks = info['disks']
    for disk in disks:
        print(f"{Fore.YELLOW}Device: {disk.get('device')}")
        print_key_value("  Mount Point", disk.get('mountpoint'), indent=2)
        print_key_value("  File System", disk.get('fstype'), indent=2)
        print_key_value("  Total (GB)", disk.get('total_gb'), indent=2)
        print_key_value("  Used (GB)", disk.get('used_gb'), indent=2)
        print_key_value("  Free (GB)", disk.get('free_gb'), indent=2)
        print_key_value("  Usage %", disk.get('percent'), indent=2)
        print_key_value("  Type", disk.get('type'), indent=2)
        print()  # blank line between disks

    # GPU Info
    print_section("GPU(s)")
    gpus = info['gpus']
    if gpus:
        for gpu in gpus:
            print_key_value("Name", gpu.get('name'))
            print_key_value("Driver", gpu.get('driver'))
            print_key_value("Total Memory (MB)", gpu.get('memory_total_mb'))
            print_key_value("Used Memory (MB)", gpu.get('memory_used_mb'))
            print_key_value("Free Memory (MB)", gpu.get('memory_free_mb'))
            print_key_value("Utilization %", gpu.get('utilization_percent'))
            print_key_value("Temperature (°C)", gpu.get('temperature_celsius'))
            print()
    else:
        print(Fore.RED + "No GPU information available.")

    print(Fore.WHITE + "-" * 60)


def print_error(msg):
    """Print an error message in red."""
    print(Fore.RED + f"ERROR: {msg}" + Style.RESET_ALL)


def print_warning(msg):
    """Print a warning message in yellow."""
    print(Fore.YELLOW + f"WARNING: {msg}" + Style.RESET_ALL)
