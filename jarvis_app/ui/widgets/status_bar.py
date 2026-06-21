"""
JARVIS Status Bar Widget
Created by Sohail Karim

Top status bar with date, time, and system indicators.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from datetime import datetime
import requests


class StatusBar(QWidget):
    """Top status bar"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._start_updates()

    def _setup_ui(self):
        self.setFixedHeight(40)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 5, 20, 5)
        layout.setSpacing(20)

        # Date
        self.date_label = QLabel()
        self.date_label.setStyleSheet("""
            color: #00D4FF;
            font-size: 13px;
            font-weight: bold;
        """)
        layout.addWidget(self.date_label)

        # Time
        self.time_label = QLabel()
        self.time_label.setStyleSheet("""
            color: #FFFFFF;
            font-size: 16px;
            font-weight: bold;
        """)
        layout.addWidget(self.time_label)

        layout.addStretch()

        # AI Status
        self.ai_status = QLabel("STANDBY")
        self.ai_status.setStyleSheet("""
            color: #606060;
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 2px;
        """)
        layout.addWidget(self.ai_status)

        # Separator
        sep = QLabel("|")
        sep.setStyleSheet("color: #303030; margin: 0 10px;")
        layout.addWidget(sep)

        # Internet status
        self.internet_status = QLabel("ONLINE")
        self.internet_status.setStyleSheet("""
            color: #00FF88;
            font-size: 11px;
            font-weight: bold;
        """)
        layout.addWidget(self.internet_status)

        # Separator
        sep2 = QLabel("|")
        sep2.setStyleSheet("color: #303030; margin: 0 10px;")
        layout.addWidget(sep2)

        # User
        self.user_label = QLabel("SOHAIL")
        self.user_label.setStyleSheet("""
            color: #B0B0B0;
            font-size: 11px;
        """)
        layout.addWidget(self.user_label)

        # Update time
        self._update_time()

    def _start_updates(self):
        """Start update timers"""
        # Time update
        self._time_timer = QTimer(self)
        self._time_timer.timeout.connect(self._update_time)
        self._time_timer.start(1000)

        # Internet check
        self._internet_timer = QTimer(self)
        self._internet_timer.timeout.connect(self._check_internet)
        self._internet_timer.start(30000)  # Check every 30 seconds
        self._check_internet()

    def _update_time(self):
        """Update date and time labels"""
        now = datetime.now()
        self.date_label.setText(now.strftime("%A, %B %d"))
        self.time_label.setText(now.strftime("%I:%M %p"))

    def _check_internet(self):
        """Check internet connectivity"""
        try:
            # Quick ping to a reliable server
            requests.get("https://www.google.com", timeout=2)
            self.internet_status.setText("ONLINE")
            self.internet_status.setStyleSheet("""
                color: #00FF88;
                font-size: 11px;
                font-weight: bold;
            """)
        except Exception:
            self.internet_status.setText("OFFLINE")
            self.internet_status.setStyleSheet("""
                color: #FF4444;
                font-size: 11px;
                font-weight: bold;
            """)

    def set_ai_status(self, status: str):
        """Set AI status indicator"""
        status_upper = status.upper()
        self.ai_status.setText(status_upper)

        colors = {
            "STANDBY": "#606060",
            "IDLE": "#606060",
            "LISTENING": "#00FF88",
            "THINKING": "#FFB800",
            "SPEAKING": "#00D4FF",
            "ERROR": "#FF4444",
        }

        color = colors.get(status_upper, "#606060")
        self.ai_status.setStyleSheet(f"""
            color: {color};
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 2px;
        """)

    def set_user(self, name: str):
        """Set user name"""
        self.user_label.setText(name.upper())
