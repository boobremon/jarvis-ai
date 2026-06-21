"""
JARVIS Transcript Panel Widget
Created by Sohail Karim

Live conversation feed with color-coded messages.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from datetime import datetime


class TranscriptMessage(QFrame):
    """Single transcript message"""

    def __init__(self, speaker: str, text: str, msg_type: str = "user", timestamp: str = None, parent=None):
        super().__init__(parent)

        self.msg_type = msg_type
        self.speaker = speaker
        self.text = text

        self._setup_ui(timestamp)

        # Apply type-based styling
        self._apply_style()

    def _setup_ui(self, timestamp: str = None):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)

        # Header with speaker and timestamp
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        # Speaker label
        self.speaker_label = QLabel(self.speaker)
        self.speaker_label.setObjectName("speakerLabel")
        header_layout.addWidget(self.speaker_label)

        header_layout.addStretch()

        # Timestamp
        ts = timestamp or datetime.now().strftime("%H:%M:%S")
        self.timestamp_label = QLabel(ts)
        self.timestamp_label.setObjectName("timestamp")
        header_layout.addWidget(self.timestamp_label)

        layout.addLayout(header_layout)

        # Message text
        self.text_label = QLabel(self.text)
        self.text_label.setWordWrap(True)
        self.text_label.setObjectName("messageText")
        layout.addWidget(self.text_label)

    def _apply_style(self):
        """Apply styling based on message type"""
        colors = {
            "user": "#4DA6FF",      # Blue
            "ai": "#00D4FF",         # Cyan
            "system": "#FF6B35",     # Orange
            "success": "#00FF88",    # Green
            "error": "#FF4444",      # Red
            "wake": "#FFB800",       # Yellow/Gold
        }

        color = colors.get(self.msg_type, "#FFFFFF")

        self.setStyleSheet(f"""
            TranscriptMessage {{
                background-color: rgba(255, 255, 255, 0.03);
                border-radius: 8px;
                margin: 2px 0;
            }}

            #speakerLabel {{
                color: {color};
                font-size: 12px;
                font-weight: bold;
            }}

            #messageText {{
                color: #FFFFFF;
                font-size: 13px;
            }}

            #timestamp {{
                color: #606060;
                font-size: 10px;
            }}
        """)


class TranscriptPanel(QWidget):
    """Scrollable transcript panel"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self._messages = []
        self._max_messages = 100

        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Title
        title = QLabel("TRANSCRIPT")
        title.setStyleSheet("""
            QLabel {
                color: #00D4FF;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 2px;
            }
        """)
        main_layout.addWidget(title)

        # Scroll area for messages
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #0F1729;
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background-color: #00A8CC;
                border-radius: 3px;
                min-height: 20px;
            }
        """)

        # Container for messages
        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setContentsMargins(5, 5, 5, 5)
        self.messages_layout.setSpacing(5)
        self.messages_layout.addStretch()

        self.scroll_area.setWidget(self.messages_container)
        main_layout.addWidget(self.scroll_area)

    def add_message(self, speaker: str, text: str, msg_type: str = "user") -> None:
        """Add a new message to the transcript"""
        message = TranscriptMessage(speaker, text, msg_type)
        self._messages.append(message)

        # Insert before the stretch
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, message)

        # Limit messages
        if len(self._messages) > self._max_messages:
            old_message = self._messages.pop(0)
            old_message.deleteLater()

        # Scroll to bottom
        QTimer.singleShot(100, self._scroll_to_bottom)

    def add_wake_detection(self, text: str) -> None:
        """Add wake word detection message"""
        self.add_message("WAKE WORD", f"Detected: '{text}'", "wake")

    def add_user_message(self, text: str) -> None:
        """Add user message"""
        self.add_message("USER", text, "user")

    def add_ai_message(self, text: str) -> None:
        """Add AI response"""
        self.add_message("JARVIS", text, "ai")

    def add_system_message(self, text: str) -> None:
        """Add system event message"""
        self.add_message("SYSTEM", text, "system")

    def add_success_message(self, text: str) -> None:
        """Add success message"""
        self.add_message("SUCCESS", text, "success")

    def add_error_message(self, text: str) -> None:
        """Add error message"""
        self.add_message("ERROR", text, "error")

    def _scroll_to_bottom(self) -> None:
        """Scroll to bottom of transcript"""
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear(self) -> None:
        """Clear all messages"""
        for message in self._messages:
            message.deleteLater()
        self._messages.clear()
