"""
JARVIS System Monitor Module
Created by Sohail Karim

Real-time system monitoring for CPU, RAM, GPU, Network, and Disk.
"""

import psutil
import platform
import time
from typing import Dict, Optional
from dataclasses import dataclass
import subprocess
import threading


@dataclass
class SystemStats:
    """System statistics snapshot"""
    timestamp: float

    # CPU
    cpu_percent: float
    cpu_freq: float
    cpu_cores: int

    # Memory
    ram_percent: float
    ram_used_gb: float
    ram_total_gb: float
    ram_available_gb: float

    # Network
    network_sent_mb: float
    network_recv_mb: float

    # Disk
    disk_percent: float
    disk_used_gb: float
    disk_total_gb: float

    # Optional/Default fields below
    cpu_temp: Optional[float] = None
    gpu_percent: Optional[float] = None
    gpu_memory_percent: Optional[float] = None
    gpu_temp: Optional[float] = None
    network_upload_speed_kbps: float = 0
    network_download_speed_kbps: float = 0
    disk_read_speed_mbps: float = 0
    disk_write_speed_mbps: float = 0
    boot_time: float = 0
    uptime_seconds: float = 0
    battery_percent: Optional[float] = None
    battery_plugged: bool = False


class SystemMonitor:
    """Real-time system monitoring"""

    def __init__(self, update_interval: float = 1.0):
        self.update_interval = update_interval
        self._running = False
        self._last_stats: Optional[SystemStats] = None
        self._monitor_thread: Optional[threading.Thread] = None

        # Previous values for delta calculations
        self._last_net_io = None
        self._last_disk_io = None
        self._last_time = None

        # System info
        self.system = platform.system()
        self.hostname = platform.node()
        self.os_name = platform.system() + " " + platform.release()
        self.cpu_name = self._get_cpu_name()
        self.total_ram_gb = round(psutil.virtual_memory().total / (1024**3), 1)
        self.total_disk_gb = round(psutil.disk_usage('/').total / (1024**3), 1) if self.system != "Windows" else round(psutil.disk_usage('C:\\').total / (1024**3), 1)

    def _get_cpu_name(self) -> str:
        """Get CPU name"""
        try:
            if self.system == "Windows":
                import platform
                return platform.processor()
            else:
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if "model name" in line:
                            return line.split(":")[1].strip()
        except Exception:
            return "Unknown CPU"

    def _get_gpu_stats(self) -> Dict:
        """Get GPU stats (NVIDIA GPUs using nvidia-smi)"""
        gpu_stats = {
            "gpu_percent": None,
            "gpu_memory_percent": None,
            "gpu_temp": None
        }

        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu",
                 "--format=csv,noheader,nounits"],
                capture_output=True,
                text=True,
                timeout=2
            )

            if result.returncode == 0:
                parts = result.stdout.strip().split(", ")
                if len(parts) >= 4:
                    gpu_stats["gpu_percent"] = float(parts[0])
                    memory_used = float(parts[1])
                    memory_total = float(parts[2])
                    gpu_stats["gpu_memory_percent"] = (memory_used / memory_total) * 100 if memory_total > 0 else 0
                    gpu_stats["gpu_temp"] = float(parts[3])

        except Exception:
            pass

        return gpu_stats

    def _get_cpu_temp(self) -> Optional[float]:
        """Get CPU temperature"""
        try:
            if self.system == "Windows":
                # Try WMI
                import wmi
                w = wmi.WMI()
                temps = w.MSAcpi_ThermalZoneTemperature()
                if temps:
                    return temps[0].CurrentTemperature / 10 - 273.15
            else:
                # Try reading from system files
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        for entry in entries:
                            if "cpu" in name.lower() or "core" in entry.label.lower():
                                return entry.current
        except Exception:
            pass
        return None

    def get_current_stats(self) -> SystemStats:
        """Get current system statistics"""
        current_time = time.time()

        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0
        cpu_temp = self._get_cpu_temp()
        cpu_cores = psutil.cpu_count(logical=True)

        # Memory
        mem = psutil.virtual_memory()
        ram_percent = mem.percent
        ram_used_gb = round(mem.used / (1024**3), 1)
        ram_total_gb = round(mem.total / (1024**3), 1)
        ram_available_gb = round(mem.available / (1024**3), 1)

        # GPU
        gpu_stats = self._get_gpu_stats()

        # Network
        net_io = psutil.net_io_counters()
        network_sent_mb = round(net_io.bytes_sent / (1024**2), 1)
        network_recv_mb = round(net_io.bytes_recv / (1024**2), 1)

        # Calculate network speed
        network_upload_speed = 0
        network_download_speed = 0
        if self._last_net_io and self._last_time:
            time_delta = current_time - self._last_time
            if time_delta > 0:
                sent_delta = net_io.bytes_sent - self._last_net_io.bytes_sent
                recv_delta = net_io.bytes_recv - self._last_net_io.bytes_recv
                network_upload_speed = (sent_delta / time_delta) / 1024  # KB/s
                network_download_speed = (recv_delta / time_delta) / 1024

        self._last_net_io = net_io

        # Disk
        disk_path = 'C:\\' if self.system == "Windows" else '/'
        disk = psutil.disk_usage(disk_path)
        disk_percent = disk.percent
        disk_used_gb = round(disk.used / (1024**3), 1)
        disk_total_gb = round(disk.total / (1024**3), 1)

        # Calculate disk speed
        disk_io = psutil.disk_io_counters()
        disk_read_speed = 0
        disk_write_speed = 0
        if self._last_disk_io and self._last_time:
            time_delta = current_time - self._last_time
            if time_delta > 0:
                read_delta = disk_io.read_bytes - self._last_disk_io.read_bytes
                write_delta = disk_io.write_bytes - self._last_disk_io.write_bytes
                disk_read_speed = (read_delta / time_delta) / (1024**2)  # MB/s
                disk_write_speed = (write_delta / time_delta) / (1024**2)

        self._last_disk_io = disk_io

        # Battery
        battery = psutil.sensors_battery()
        battery_percent = battery.percent if battery else None
        battery_plugged = battery.power_plugged if battery else False

        # Boot time
        boot_time = psutil.boot_time()
        uptime = current_time - boot_time

        self._last_time = current_time

        stats = SystemStats(
            timestamp=current_time,
            cpu_percent=cpu_percent,
            cpu_freq=cpu_freq,
            cpu_temp=cpu_temp,
            cpu_cores=cpu_cores,
            ram_percent=ram_percent,
            ram_used_gb=ram_used_gb,
            ram_total_gb=ram_total_gb,
            ram_available_gb=ram_available_gb,
            gpu_percent=gpu_stats["gpu_percent"],
            gpu_memory_percent=gpu_stats["gpu_memory_percent"],
            gpu_temp=gpu_stats["gpu_temp"],
            network_sent_mb=network_sent_mb,
            network_recv_mb=network_recv_mb,
            network_upload_speed_kbps=network_upload_speed,
            network_download_speed_kbps=network_download_speed,
            disk_percent=disk_percent,
            disk_used_gb=disk_used_gb,
            disk_total_gb=disk_total_gb,
            disk_read_speed_mbps=disk_read_speed,
            disk_write_speed_mbps=disk_write_speed,
            boot_time=boot_time,
            uptime_seconds=uptime,
            battery_percent=battery_percent,
            battery_plugged=battery_plugged
        )

        self._last_stats = stats
        return stats

    def get_system_info(self) -> Dict:
        """Get static system information"""
        return {
            "hostname": self.hostname,
            "os": self.os_name,
            "cpu": self.cpu_name,
            "cpu_cores": psutil.cpu_count(logical=True),
            "ram_total_gb": self.total_ram_gb,
            "disk_total_gb": self.total_disk_gb,
            "system": self.system,
        }

    def format_uptime(self, seconds: float) -> str:
        """Format uptime to readable string"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

    def get_top_processes(self, by: str = "cpu", limit: int = 5) -> list:
        """Get top processes by CPU or memory usage"""
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu': proc.info['cpu_percent'] or 0,
                    'memory': proc.info['memory_percent'] or 0
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Sort by specified metric
        key = 'cpu' if by == 'cpu' else 'memory'
        processes.sort(key=lambda p: p[key], reverse=True)

        return processes[:limit]
