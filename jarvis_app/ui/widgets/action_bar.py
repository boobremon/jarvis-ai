"""
JARVIS Action Bar Widget
Created by Sohail Karim

Bottom action bar with quick actions and shortcuts.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from jarvis_app.ui.styles import JarvisTheme


class ActionButton(QPushButton):
    """Styled action button"""

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {JarvisTheme.BG_TERTIARY};
                color: {JarvisTheme.PRIMARY};
                border: 1px solid {JarvisTheme.PANEL_BORDER};
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {JarvisTheme.PRIMARY_DARK};
                border-color: {JarvisTheme.PRIMARY};
                color: {JarvisTheme.TEXT_PRIMARY};
            }}
            QPushButton:pressed {{
                background-color: {JarvisTheme.PRIMARY};
                color: {JarvisTheme.BG_PRIMARY};
            }}
        """)


class ActionBar(QWidget):
    """Bottom action bar with quick actions"""

    # Signals
    action_triggered = pyqtSignal(str)
    command_submitted = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 10, 15, 15)
        main_layout.setSpacing(10)

        # Command input
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Type a command or press Enter to speak...")
        self.command_input.returnPressed.connect(self._on_command_submit)
        self.command_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {JarvisTheme.BG_TERTIARY};
                color: {JarvisTheme.TEXT_PRIMARY};
                border: 2px solid {JarvisTheme.PANEL_BORDER};
                border-radius: 25px;
                padding: 12px 20px;
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border-color: {JarvisTheme.PRIMARY};
            }}
        """)
        input_layout.addWidget(self.command_input)

        main_layout.addLayout(input_layout)

        # Quick actions row
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        quick_actions = [
            ("Chrome", "open chrome"),
            ("YouTube", "open youtube"),
            ("Spotify", "open spotify"),
            ("Time", "what time is it"),
            ("Search", "search google for"),
            ("Status", "system status"),
        ]

        for label, action in quick_actions:
            btn = ActionButton(label)
            btn.clicked.connect(lambda checked, a=action: self._on_action_click(a))
            actions_layout.addWidget(btn)

        actions_layout.addStretch()

        main_layout.addLayout(actions_layout)

    def _on_action_click(self, action: str):
        """Handle action button click"""
        self.action_triggered.emit(action)

    def _on_command_submit(self):
        """Handle command input submit"""
        text = self.command_input.text().strip()
        if text:
            self.command_submitted.emit(text)
            self.command_input.clear()

    def set_listening_state(self, listening: bool):
        """Update UI for listening state"""
        if listening:
            self.command_input.setPlaceholderText("Listening...")
            self.command_input.setStyleSheet(f"""
                QLineEdit {{
                    background-color: {JarvisTheme.BG_TERTIARY};
                    color: {JarvisTheme.TEXT_PRIMARY};
                    border: 2px solid {JarvisTheme.SUCCESS};
                    border-radius: 25px;
                    padding: 12px 20px;
                    font-size: 13px;
                }}
            """)
        else:
            self.command_input.setPlaceholderText("Type a command or press Enter to speak...")
            self.command_input.setStyleSheet(f"""
                QLineEdit {{
                    background-color: {JarvisTheme.BG_TERTIARY};
                    color: {JarvisTheme.TEXT_PRIMARY};
                    border: 2px solid {JarvisTheme.PANEL_BORDER};
                    border-radius: 25px;
                    padding: 12px 20px;
                    font-size: 13px;
                }}
                QLineEdit:focus {{
                    border-color: {JarvisTheme.PRIMARY};
                }}
            """)
