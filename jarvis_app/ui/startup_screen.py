"""
JARVIS Startup Screen
Created by Sohail Karim

Cinematic boot animation for JARVIS initialization.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QApplication
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QMovie
import time


class StartupScreen(QWidget):
    """Cinematic JARVIS boot screen"""

    # Signals
    startup_complete = pyqtSignal()

    def __init__(self, user_name: str = "Sohail"):
        super().__init__()
        self.user_name = user_name
        self._step = 0

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: #0A0E1A;")

        self._setup_ui()
        self._start_sequence()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # JARVIS logo/title
        self.title_label = QLabel("J.A.R.V.I.S")
        self.title_label.setStyleSheet("""
            QLabel {
                color: #00D4FF;
                font-size: 72px;
                font-weight: bold;
                letter-spacing: 10px;
            }
        """)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        # Subtitle
        self.subtitle_label = QLabel("Just A Rather Very Intelligent System")
        self.subtitle_label.setStyleSheet("""
            QLabel {
                color: #606060;
                font-size: 14px;
                letter-spacing: 3px;
            }
        """)
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.subtitle_label)

        # Status
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #00D4FF;
                font-size: 12px;
                letter-spacing: 2px;
            }
        """)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMaximumHeight(4)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        self.progress.setStyleSheet("""
            QProgressBar {
                background-color: #1A2642;
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background-color: #00D4FF;
                border-radius: 2px;
            }
        """)
        layout.addWidget(self.progress)

        # Version info
        self.version_label = QLabel("v2.0 | Created by Sohail Karim")
        self.version_label.setStyleSheet("""
            QLabel {
                color: #404040;
                font-size: 10px;
            }
        """)
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.version_label)

    def _start_sequence(self):
        """Start boot sequence"""
        self._boot_steps = [
            ("Initializing core systems...", 10),
            ("Loading AI modules...", 25),
            ("Calibrating voice recognition...", 40),
            ("Establishing system monitoring...", 55),
            ("Connecting automation protocols...", 70),
            ("Running diagnostics...", 85),
            ("All systems operational", 100),
        ]
        self._step = 0
        self._run_next_step()

    def _run_next_step(self):
        """Run next startup step"""
        if self._step >= len(self._boot_steps):
            # Startup complete
            self.subtitle_label.setText("ONLINE")
            self.subtitle_label.setStyleSheet("""
                QLabel {
                    color: #00FF88;
                    font-size: 18px;
                    font-weight: bold;
                    letter-spacing: 5px;
                }
            """)

            # Welcome message after delay
            QTimer.singleShot(1000, self._show_welcome)
            return

        text, progress = self._boot_steps[self._step]
        self.status_label.setText(text)
        self._animate_progress(progress)

        self._step += 1
        QTimer.singleShot(500, self._run_next_step)

    def _animate_progress(self, target: int):
        """Animate progress bar to target"""
        current = self.progress.value()
        if current < target:
            self.progress.setValue(current + 1)
            QTimer.singleShot(20, lambda: self._animate_progress(target))

    def _show_welcome(self):
        """Show welcome message"""
        import random
        from datetime import datetime

        hour = datetime.now().hour
        if 5 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 17:
            greeting = "Good afternoon"
        elif 17 <= hour < 21:
            greeting = "Good evening"
        else:
            greeting = "Good evening"

        self.status_label.setText(f"{greeting}, {self.user_name}.")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 18px;
                letter-spacing: 1px;
            }
        """)

        # Emit complete signal after delay
        QTimer.singleShot(2500, self._finish)

    def _finish(self):
        """Complete startup"""
        self.startup_complete.emit()
        self.close()
