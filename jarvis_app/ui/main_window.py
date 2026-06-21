"""
JARVIS Main Window
Created by Sohail Karim

Main HUD interface with futuristic design.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QSizePolicy, QApplication, QStackedWidget
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from jarvis_app.ui.styles import JarvisStyles, JarvisTheme
from jarvis_app.ui.widgets import (
    AICoreWidget, TranscriptPanel, StatsPanel,
    ActionBar, StatusBar, SettingsPanel
)
from jarvis_app.ui.startup_screen import StartupScreen


class JarvisMainWindow(QMainWindow):
    """Main JARVIS HUD window"""

    def __init__(self, config):
        super().__init__()
        self.config = config
        self._startup_complete = False

        self._setup_window()
        self._setup_ui()
        self._apply_styles()

        # Start with startup screen
        self._show_startup()

    def _setup_window(self):
        """Configure main window"""
        self.setWindowTitle("J.A.R.V.I.S")
        self.setMinimumSize(1280, 800)

        # Get screen size
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(
            (screen.width() - 1280) // 2,
            (screen.height() - 800) // 2,
            1280, 800
        )

    def _setup_ui(self):
        """Build main UI layout"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Status bar
        self.status_bar = StatusBar()
        main_layout.addWidget(self.status_bar)

        # Content area (3 columns)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(10)

        # Left panel
        self.left_panel = QFrame()
        self.left_panel.setObjectName("leftPanel")
        self.left_panel.setFixedWidth(250)
        self._setup_left_panel(content_layout)

        # Center panel
        self.center_panel = QFrame()
        self.center_panel.setObjectName("centerPanel")
        self._setup_center_panel(content_layout)

        # Right panel
        self.right_panel = QFrame()
        self.right_panel.setObjectName("rightPanel")
        self.right_panel.setFixedWidth(300)
        self._setup_right_panel(content_layout)

        main_layout.addLayout(content_layout)

        # Action bar
        self.action_bar = ActionBar()
        self.action_bar.setFixedHeight(100)
        main_layout.addWidget(self.action_bar)

    def _setup_left_panel(self, layout: QHBoxLayout):
        """Setup left stats panel"""
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        # Stats panel
        self.stats_panel = StatsPanel()
        left_layout.addWidget(self.stats_panel)

        layout.addWidget(self.left_panel)

    def _setup_center_panel(self, layout: QHBoxLayout):
        """Setup center AI core panel"""
        center_layout = QVBoxLayout(self.center_panel)
        center_layout.setContentsMargins(20, 20, 20, 20)
        center_layout.setSpacing(20)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # AI core visualization
        self.ai_core = AICoreWidget()
        center_layout.addWidget(self.ai_core, alignment=Qt.AlignmentFlag.AlignCenter)

        # Status text
        self.status_text = QLabel("Ready to assist")
        self.status_text.setStyleSheet(f"""
            color: {JarvisTheme.TEXT_SECONDARY};
            font-size: 14px;
            letter-spacing: 2px;
        """)
        self.status_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_layout.addWidget(self.status_text)

        layout.addWidget(self.center_panel, stretch=1)

    def _setup_right_panel(self, layout: QHBoxLayout):
        """Setup right transcript panel"""
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Transcript panel
        self.transcript_panel = TranscriptPanel()
        right_layout.addWidget(self.transcript_panel)

        layout.addWidget(self.right_panel)

    def _apply_styles(self):
        """Apply stylesheets"""
        pass

    def _show_startup(self):
        """Show startup sequence"""
        self.startup_screen = StartupScreen(self.config.user_name)
        self.startup_screen.startup_complete.connect(self._on_startup_complete)
        self.startup_screen.show()

    def _on_startup_complete(self):
        """Handle startup completion"""
        self._startup_complete = True
        self.show()

        # Update status bar
        self.status_bar.set_ai_status("IDLE")
        self.status_bar.set_user(self.config.user_name)

        # Add welcome to transcript
        import random
        from datetime import datetime

        hour = datetime.now().hour
        if 5 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        self.transcript_panel.add_system_message("System initialized")
        self.transcript_panel.add_ai_message(
            f"{greeting}, {self.config.user_name}. All systems operational. How may I assist you today?"
        )

    # Public methods for external control
    def set_ai_state(self, state: str):
        """Set AI state (idle, listening, thinking, speaking)"""
        self.ai_core.set_state(state)
        self.status_bar.set_ai_status(state)

        status_texts = {
            "idle": "Ready to assist",
            "listening": "Listening...",
            "thinking": "Processing...",
            "speaking": "Speaking...",
        }
        self.status_text.setText(status_texts.get(state, "Ready"))

    def add_transcript_message(self, speaker: str, text: str, msg_type: str = "user"):
        """Add message to transcript"""
        if speaker.lower() in ["jarvis", "ai", "assistant"]:
            self.transcript_panel.add_ai_message(text)
        elif speaker.lower() in ["user", "you"]:
            self.transcript_panel.add_user_message(text)
        elif msg_type == "success":
            self.transcript_panel.add_success_message(text)
        elif msg_type == "error":
            self.transcript_panel.add_error_message(text)
        else:
            self.transcript_panel.add_system_message(text)

    def add_wake_detection(self, text: str):
        """Add wake word detection to transcript"""
        self.transcript_panel.add_wake_detection(text)

    def show_settings(self):
        """Show settings dialog"""
        settings = SettingsPanel(self.config, self)
        if settings.exec():
            # Handle saved settings
            pass

    def get_current_command(self) -> str:
        """Get current text from command input"""
        return self.action_bar.command_input.text()

    def clear_command_input(self):
        """Clear the command input"""
        self.action_bar.command_input.clear()

    def closeEvent(self, event):
        """Handle window close"""
        # Instead of closing, minimize to tray if configured
        if self.config.system.minimize_to_tray:
            event.ignore()
            self.hide()
        else:
            event.accept()
