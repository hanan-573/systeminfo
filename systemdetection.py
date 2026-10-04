"""
info.py - Fetches all system and OS information.
"""
import os
import sys
import platform
import psutil
import subprocess
import re

# Optional GPU library
try:
    import GPUtil
    HAS_GPU = True
except ImportError:
    HAS_GPU = False


def get_os_info():
    """Return a dict with OS name, version, build number, and architecture."""
    os_info = {}

    # OS name (e.g., Windows, Linux, Darwin)
    os_info['system'] = platform.system()
    os_info['release'] = platform.release()
    os_info['version'] = platform.version()          # includes build number on Windows
    os_info['architecture'] = platform.machine()     # e.g., AMD64

    # Build number on Windows is inside version string; extract if possible
    build = None
    if os_info['system'] == 'Windows':
        # platform.version() returns something like "10.0.19045"
        match = re.search(r'(\d+)\.(\d+)', os_info['version'])
        if match:
            build = match.group(2)
    elif os_info['system'] == 'Linux':
        # Try to get build from /etc/os-release
        try:
            with open('/etc/os-release') as f:
                content = f.read()
                # Look for VERSION_ID or BUILD_ID
                for line in content.splitlines():
                    if line.startswith('VERSION_ID='):
                        build = line.split('=')[1].strip('"')
                        break
                    elif line.startswith('BUILD_ID='):
                        build = line.split('=')[1].strip('"')
                        break
        except FileNotFoundError:
            pass
    elif os_info['system'] == 'Darwin':  # macOS
        try:
            # sw_vers -buildVersion
            build = subprocess.check_output(['sw_vers', '-buildVersion'], text=True).strip()
        except:
            pass

    os_info['build'] = build if build else 'N/A'

    # Additional detail: kernel version
    os_info['kernel'] = platform.release()

    return os_info


def get_cpu_info():
    """Return CPU details: model, cores (physical/logical), frequency."""
    cpu_info = {}
    cpu_info['model'] = platform.processor()
    if not cpu_info['model']:
        # Fallback: try to get from /proc/cpuinfo on Linux
        if sys.platform.startswith('linux'):
            try:
                with open('/proc/cpuinfo') as f:
                    for line in f:
                        if line.startswith('model name'):
                            cpu_info['model'] = line.split(':')[1].strip()
                            break
            except:
                pass
        elif sys.platform == 'win32':
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                     r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
                cpu_info['model'] = winreg.QueryValueEx(key, "ProcessorNameString")[0]
                winreg.CloseKey(key)
            except:
                pass

    cpu_info['physical_cores'] = psutil.cpu_count(logical=False)
    cpu_info['logical_cores'] = psutil.cpu_count(logical=True)
    cpu_info['max_freq_mhz'] = psutil.cpu_freq().max if psutil.cpu_freq() else None

    return cpu_info


def get_ram_info():
    """Return RAM details: total, available, used, percentage."""
    mem = psutil.virtual_memory()
    ram_info = {
        'total_gb': round(mem.total / (1024**3), 2),
        'available_gb': round(mem.available / (1024**3), 2),
        'used_gb': round(mem.used / (1024**3), 2),
        'percent': mem.percent
    }
    return ram_info


def get_disk_info():
    """Return disk details for each partition: device, mount point, total, used, free, type (SSD/HDD if detectable)."""
    disk_list = []
    for partition in psutil.disk_partitions():
        if partition.fstype:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk = {
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total_gb': round(usage.total / (1024**3), 2),
                    'used_gb': round(usage.used / (1024**3), 2),
                    'free_gb': round(usage.free / (1024**3), 2),
                    'percent': usage.percent,
                    'type': 'Unknown'   # will attempt to detect
                }
                # Try to detect SSD/HDD
                disk['type'] = detect_disk_type(partition.device)
                disk_list.append(disk)
            except PermissionError:
                continue
    return disk_list


def detect_disk_type(device):
    """
    Attempt to detect if the disk is SSD (solid state) or HDD (rotational).
    Returns 'SSD', 'HDD', or 'Unknown'.
    """
    # Windows: use wmic (if available)
    if sys.platform == 'win32':
        # Try to get the physical disk index from the device path
        # e.g., \\.\PHYSICALDRIVE0
        try:
            # Extract drive letter from device string, e.g., "C:" -> "C"
            import win32file
            drive_letter = device[0]  # crude
            # Use wmic to get media type
            output = subprocess.check_output(
                f'wmic diskdrive where "DeviceID=\'{device}\'" get MediaType',
                shell=True, text=True
            )
            if 'SSD' in output or 'Solid State' in output:
                return 'SSD'
            elif 'HDD' in output or 'Rotational' in output:
                return 'HDD'
        except:
            pass
        # Alternative: check if it's an SSD via Win32 API (not implemented here)

    # Linux: check /sys/block/*/queue/rotational
    elif sys.platform.startswith('linux'):
        # device like /dev/sda1 -> base name sda
        base = re.sub(r'^/dev/', '', device)
        # Remove partition number
        base = re.sub(r'\d+$', '', base)
        rotational_path = f'/sys/block/{base}/queue/rotational'
        try:
            with open(rotational_path) as f:
                val = f.read().strip()
                if val == '0':
                    return 'SSD'
                elif val == '1':
                    return 'HDD'
        except:
            pass

    # macOS: use system_profiler or diskutil? Not trivial.
    # We'll return Unknown if detection fails.
    return 'Unknown'


def get_gpu_info():
    """Return GPU details: name, driver, memory, etc."""
    gpu_list = []
    if HAS_GPU:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            gpu_info = {
                'name': gpu.name,
                'driver': gpu.driver,
                'memory_total_mb': gpu.memoryTotal,
                'memory_used_mb': gpu.memoryUsed,
                'memory_free_mb': gpu.memoryFree,
                'utilization_percent': gpu.load * 100 if gpu.load else None,
                'temperature_celsius': gpu.temperature if hasattr(gpu, 'temperature') else None
            }
            gpu_list.append(gpu_info)
    else:
        # Fallback: try to get basic info via platform or subprocess
        if sys.platform == 'win32':
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                     r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}")
                # We need to enumerate subkeys to get GPU adapters
                # This is complex; we'll just put a placeholder
                gpu_list.append({'name': 'Unknown (fallback)', 'driver': 'N/A', 'memory_total_mb': 'N/A'})
            except:
                pass
        elif sys.platform.startswith('linux'):
            # Try lspci
            try:
                output = subprocess.check_output(['lspci', '-v'], text=True)
                for line in output.splitlines():
                    if 'VGA' in line or '3D' in line:
                        # extract name
                        name = line.split(':')[1].strip()
                        gpu_list.append({'name': name, 'driver': 'N/A', 'memory_total_mb': 'N/A'})
                        break
            except:
                pass
        elif sys.platform == 'darwin':
            # system_profiler SPDisplaysDataType
            try:
                output = subprocess.check_output(['system_profiler', 'SPDisplaysDataType'], text=True)
                # parse for Chipset Model
                match = re.search(r'Chipset Model: (.+)', output)
                if match:
                    gpu_list.append({'name': match.group(1), 'driver': 'N/A', 'memory_total_mb': 'N/A'})
            except:
                pass

    return gpu_list


def get_all_info():
    """Return a dictionary containing all system information."""
    info = {
        'os': get_os_info(),
        'cpu': get_cpu_info(),
        'ram': get_ram_info(),
        'disks': get_disk_info(),
        'gpus': get_gpu_info()
    }
    return info