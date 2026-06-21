"""
JARVIS Stats Panel Widget
Created by Sohail Karim

System statistics display panel.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from jarvis_app.system_monitor.monitor import SystemMonitor, SystemStats
from jarvis_app.ui.styles import JarvisTheme


class StatBar(QWidget):
    """Single stat bar with label"""

    def __init__(self, label: str, max_value: int = 100, color: str = None, parent=None):
        super().__init__(parent)
        self.max_value = max_value

        self._setup_ui(label, color or JarvisTheme.PRIMARY)

    def _setup_ui(self, label: str, color: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Label and value row
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        label_widget = QLabel(label.upper())
        label_widget.setStyleSheet(f"color: {JarvisTheme.TEXT_SECONDARY}; font-size: 11px; letter-spacing: 1px;")
        header_layout.addWidget(label_widget)

        header_layout.addStretch()

        self.value_label = QLabel("0%")
        self.value_label.setStyleSheet(f"color: {JarvisTheme.TEXT_PRIMARY}; font-size: 12px; font-weight: bold;")
        header_layout.addWidget(self.value_label)

        layout.addLayout(header_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {JarvisTheme.BG_TERTIARY};
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 4px;
            }}
        """)
        layout.addWidget(self.progress_bar)

    def set_value(self, value: float, suffix: str = "%"):
        """Set the current value"""
        int_value = int(value)
        self.progress_bar.setValue(int_value)
        self.value_label.setText(f"{int_value}{suffix}")

        # Color based on value
        if value >= 90:
            color = JarvisTheme.ERROR
        elif value >= 70:
            color = JarvisTheme.WARNING
        else:
            color = JarvisTheme.PRIMARY if self.progress_bar.styleSheet() != "" else JarvisTheme.PRIMARY

        # Update progress bar style
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {JarvisTheme.BG_TERTIARY};
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 4px;
            }}
        """)


class StatsPanel(QWidget):
    """System statistics panel"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self._monitor = SystemMonitor()

        self._setup_ui()
        self._start_updates()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # Title
        title = QLabel("SYSTEM STATUS")
        title.setStyleSheet(f"""
            QLabel {{
                color: {JarvisTheme.PRIMARY};
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 2px;
            }}
        """)
        main_layout.addWidget(title)

        # System info
        self.system_info = QLabel()
        self.system_info.setStyleSheet(f"color: {JarvisTheme.TEXT_TERTIARY}; font-size: 10px;")
        self._update_system_info()
        main_layout.addWidget(self.system_info)

        # Spacer
        spacer = QWidget()
        spacer.setFixedHeight(10)
        main_layout.addWidget(spacer)

        # CPU
        self.cpu_bar = StatBar("CPU", color=JarvisTheme.PRIMARY)
        main_layout.addWidget(self.cpu_bar)

        # RAM
        self.ram_bar = StatBar("RAM", color=JarvisTheme.SECONDARY)
        main_layout.addWidget(self.ram_bar)

        # GPU
        self.gpu_bar = StatBar("GPU", color=JarvisTheme.ACCENT)
        main_layout.addWidget(self.gpu_bar)

        # Disk
        self.disk_bar = StatBar("DISK", color=JarvisTheme.SUCCESS)
        main_layout.addWidget(self.disk_bar)

        # Network status
        self.network_label = QLabel()
        self.network_label.setStyleSheet(f"""
            color: {JarvisTheme.TEXT_SECONDARY};
            font-size: 11px;
            padding: 5px;
        """)
        main_layout.addWidget(self.network_label)

        # Uptime
        self.uptime_label = QLabel()
        self.uptime_label.setStyleSheet(f"""
            color: {JarvisTheme.TEXT_TERTIARY};
            font-size: 10px;
        """)
        main_layout.addWidget(self.uptime_label)

        main_layout.addStretch()

    def _start_updates(self):
        """Start update timer"""
        self._update_stats()
        self._update_timer = QTimer(self)
        self._update_timer.timeout.connect(self._update_stats)
        self._update_timer.start(1000)

    def _update_system_info(self):
        """Update system info label"""
        info = self._monitor.get_system_info()
        self.system_info.setText(f"{info['os']} | {info['cpu'][:30]}...")

    def _update_stats(self):
        """Update all stats"""
        try:
            stats = self._monitor.get_current_stats()

            self.cpu_bar.set_value(stats.cpu_percent)
            self.ram_bar.set_value(stats.ram_percent)

            # GPU (might be None)
            if stats.gpu_percent is not None:
                self.gpu_bar.set_value(stats.gpu_percent)
                self.gpu_bar.show()
            else:
                self.gpu_bar.hide()
                self.gpu_bar.set_value(0)

            self.disk_bar.set_value(stats.disk_percent)

            # Network
            upload = stats.network_upload_speed_kbps
            download = stats.network_download_speed_kbps

            upload_str = f"{upload:.0f}" if upload < 1000 else f"{upload/1000:.1f}M"
            download_str = f"{download:.0f}" if download < 1000 else f"{download/1000:.1f}M"

            self.network_label.setText(
                f"Network:  ↑ {upload_str} KB/s  ↓ {download_str} KB/s"
            )

            # Uptime
            uptime = self._monitor.format_uptime(stats.uptime_seconds)
            self.uptime_label.setText(f"Uptime: {uptime}")

            # Battery if available
            if stats.battery_percent is not None:
                plug_status = " (Charging)" if stats.battery_plugged else ""
                self.uptime_label.setText(
                    f"Uptime: {uptime} | Battery: {stats.battery_percent:.0f}%{plug_status}"
                )

        except Exception as e:
            print(f"Stats update error: {e}")
