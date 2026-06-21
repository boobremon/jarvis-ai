"""
JARVIS Settings Panel Widget
Created by Sohail Karim

Configuration panel for all JARVIS settings.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QSlider, QSpinBox, QCheckBox,
    QTabWidget, QTabBar, QScrollArea, QFrame, QDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from jarvis_app.ui.styles import JarvisTheme
from jarvis_app.core.config import JarvisConfig, VoiceConfig, UIConfig, AIConfig


class SettingsPanel(QDialog):
    """Settings configuration dialog"""

    # Signals
    settings_saved = pyqtSignal(dict)

    def __init__(self, config: JarvisConfig, parent=None):
        super().__init__(parent)
        self.config = config

        self.setWindowTitle("JARVIS Settings")
        self.setMinimumSize(600, 500)

        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Title
        title = QLabel("Settings")
        title.setStyleSheet(f"""
            color: {JarvisTheme.PRIMARY};
            font-size: 24px;
            font-weight: bold;
        """)
        main_layout.addWidget(title)

        # Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {JarvisTheme.PANEL_BORDER};
                border-radius: 8px;
                background-color: {JarvisTheme.BG_SECONDARY};
            }}
            QTabBar::tab {{
                background-color: {JarvisTheme.BG_TERTIARY};
                color: {JarvisTheme.TEXT_SECONDARY};
                border: 1px solid {JarvisTheme.PANEL_BORDER};
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 10px 20px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background-color: {JarvisTheme.BG_SECONDARY};
                color: {JarvisTheme.PRIMARY};
                border-color: {JarvisTheme.PRIMARY};
            }}
        """)

        # Voice tab
        voice_tab = self._create_voice_tab()
        tabs.addTab(voice_tab, "Voice")

        # UI tab
        ui_tab = self._create_ui_tab()
        tabs.addTab(ui_tab, "Interface")

        # AI tab
        ai_tab = self._create_ai_tab()
        tabs.addTab(ai_tab, "AI")

        # Automation tab
        auto_tab = self._create_automation_tab()
        tabs.addTab(auto_tab, "Automation")

        main_layout.addWidget(tabs)

        # Bottom buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Save")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self._save_settings)
        btn_layout.addWidget(save_btn)

        main_layout.addLayout(btn_layout)

    def _create_voice_tab(self) -> QWidget:
        """Create voice settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        # Enable voice
        self.voice_enabled = QCheckBox("Enable Voice System")
        layout.addWidget(self.voice_enabled)

        # Wake word
        wake_layout = QHBoxLayout()
        wake_layout.addWidget(QLabel("Wake Word:"))
        self.wake_word_input = QLineEdit()
        self.wake_word_input.setPlaceholderText("jarvis")
        wake_layout.addWidget(self.wake_word_input)
        layout.addLayout(wake_layout)

        # Voice selection
        voice_layout = QHBoxLayout()
        voice_layout.addWidget(QLabel("Voice:"))
        self.voice_combo = QComboBox()
        self.voice_combo.addItem("Male (JARVIS)", 0)
        self.voice_combo.addItem("Female (F.R.I.D.A.Y)", 1)
        voice_layout.addWidget(self.voice_combo)
        voice_layout.addStretch()
        layout.addLayout(voice_layout)

        # Speech rate
        rate_layout = QHBoxLayout()
        rate_layout.addWidget(QLabel("Speech Rate:"))
        self.rate_slider = QSlider(Qt.Orientation.Horizontal)
        self.rate_slider.setRange(100, 300)
        self.rate_slider.setValue(180)
        self.rate_label = QLabel("180")
        self.rate_slider.valueChanged.connect(lambda v: self.rate_label.setText(str(v)))
        rate_layout.addWidget(self.rate_slider)
        rate_layout.addWidget(self.rate_label)
        layout.addLayout(rate_layout)

        # Volume
        vol_layout = QHBoxLayout()
        vol_layout.addWidget(QLabel("Volume:"))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_label = QLabel("100%")
        self.volume_slider.valueChanged.connect(lambda v: self.volume_label.setText(f"{v}%"))
        vol_layout.addWidget(self.volume_slider)
        vol_layout.addWidget(self.volume_label)
        layout.addLayout(vol_layout)

        # Continuous listening
        self.continuous_listening = QCheckBox("Continuous Listening Mode")
        layout.addWidget(self.continuous_listening)

        layout.addStretch()
        return widget

    def _create_ui_tab(self) -> QWidget:
        """Create interface settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        # Theme
        layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark (JARVIS)", "Light", "Blue"])
        layout.addWidget(self.theme_combo)

        # Primary color
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Primary Color:"))
        self.primary_color = QLineEdit("#00D4FF")
        color_layout.addWidget(self.primary_color)
        layout.addLayout(color_layout)

        # Animation
        self.animation_enabled = QCheckBox("Enable Animations")
        self.animation_enabled.setChecked(True)
        layout.addWidget(self.animation_enabled)

        # Glass effect
        self.glass_effect = QCheckBox("Glass Effect Panels")
        self.glass_effect.setChecked(True)
        layout.addWidget(self.glass_effect)

        # Show stats
        self.show_stats = QCheckBox("Show System Stats")
        self.show_stats.setChecked(True)
        layout.addWidget(self.show_stats)

        # Show transcript
        self.show_transcript = QCheckBox("Show Transcript Panel")
        self.show_transcript.setChecked(True)
        layout.addWidget(self.show_transcript)

        layout.addStretch()
        return widget

    def _create_ai_tab(self) -> QWidget:
        """Create AI settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        # User name
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("User Name:"))
        self.user_name_input = QLineEdit()
        self.user_name_input.setPlaceholderText("Name")
        user_layout.addWidget(self.user_name_input)
        layout.addLayout(user_layout)

        # AI Provider
        provider_layout = QHBoxLayout()
        provider_layout.addWidget(QLabel("AI Provider:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["None (Local Only)", "Anthropic Claude", "OpenAI"])
        provider_layout.addWidget(self.provider_combo)
        provider_layout.addStretch()
        layout.addLayout(provider_layout)

        # Model
        layout.addWidget(QLabel("Model:"))
        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("claude-sonnet-4-20250514")
        layout.addWidget(self.model_input)

        # Context window
        context_layout = QHBoxLayout()
        context_layout.addWidget(QLabel("Context Window:"))
        self.context_spin = QSpinBox()
        self.context_spin.setRange(5, 50)
        self.context_spin.setValue(10)
        context_layout.addWidget(self.context_spin)
        context_layout.addWidget(QLabel("messages"))
        context_layout.addStretch()
        layout.addLayout(context_layout)

        # Memory enabled
        self.memory_enabled = QCheckBox("Enable Conversation Memory")
        self.memory_enabled.setChecked(True)
        layout.addWidget(self.memory_enabled)

        layout.addStretch()
        return widget

    def _create_automation_tab(self) -> QWidget:
        """Create automation settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        layout.addWidget(QLabel("Application Paths (leave empty for auto-detect):"))

        # Chrome path
        chrome_layout = QHBoxLayout()
        chrome_layout.addWidget(QLabel("Chrome:"))
        self.chrome_path = QLineEdit()
        self.chrome_path.setPlaceholderText("Auto-detect")
        chrome_layout.addWidget(self.chrome_path)
        layout.addLayout(chrome_layout)

        # VS Code path
        vscode_layout = QHBoxLayout()
        vscode_layout.addWidget(QLabel("VS Code:"))
        self.vscode_path = QLineEdit()
        self.vscode_path.setPlaceholderText("Auto-detect")
        vscode_layout.addWidget(self.vscode_path)
        layout.addLayout(vscode_layout)

        # Discord path
        discord_layout = QHBoxLayout()
        discord_layout.addWidget(QLabel("Discord:"))
        self.discord_path = QLineEdit()
        self.discord_path.setPlaceholderText("Auto-detect")
        discord_layout.addWidget(self.discord_path)
        layout.addLayout(discord_layout)

        # Spotify path
        spotify_layout = QHBoxLayout()
        spotify_layout.addWidget(QLabel("Spotify:"))
        self.spotify_path = QLineEdit()
        self.spotify_path.setPlaceholderText("Auto-detect")
        spotify_layout.addWidget(self.spotify_path)
        layout.addLayout(spotify_layout)

        layout.addStretch()
        return widget

    def _load_settings(self):
        """Load current settings into UI"""
        # Voice
        self.voice_enabled.setChecked(self.config.voice.enabled)
        self.wake_word_input.setText(self.config.voice.wake_word)
        self.voice_combo.setCurrentIndex(self.config.voice.voice_id or 0)
        self.rate_slider.setValue(self.config.voice.voice_rate)
        self.volume_slider.setValue(int(self.config.voice.voice_volume * 100))
        self.continuous_listening.setChecked(self.config.voice.continuous_listening)

        # UI
        self.primary_color.setText(self.config.ui.primary_color)
        self.animation_enabled.setChecked(self.config.ui.animation_enabled)
        self.glass_effect.setChecked(self.config.ui.glass_effect)
        self.show_stats.setChecked(self.config.ui.show_system_stats)
        self.show_transcript.setChecked(self.config.ui.show_transcript)

        # AI
        self.user_name_input.setText(self.config.user_name)
        self.model_input.setText(self.config.ai.model)
        self.context_spin.setValue(self.config.ai.context_window)
        self.memory_enabled.setChecked(self.config.ai.memory_enabled)

        # Automation
        self.chrome_path.setText(self.config.automation.chrome_path)
        self.vscode_path.setText(self.config.automation.vscode_path)
        self.discord_path.setText(self.config.automation.discord_path)
        self.spotify_path.setText(self.config.automation.spotify_path)

    def _save_settings(self):
        """Save settings and close"""
        settings = {
            "voice": {
                "enabled": self.voice_enabled.isChecked(),
                "wake_word": self.wake_word_input.text() or "jarvis",
                "voice_id": self.voice_combo.currentData(),
                "voice_rate": self.rate_slider.value(),
                "voice_volume": self.volume_slider.value() / 100,
                "continuous_listening": self.continuous_listening.isChecked(),
            },
            "ui": {
                "primary_color": self.primary_color.text(),
                "animation_enabled": self.animation_enabled.isChecked(),
                "glass_effect": self.glass_effect.isChecked(),
                "show_system_stats": self.show_stats.isChecked(),
                "show_transcript": self.show_transcript.isChecked(),
            },
            "ai": {
                "model": self.model_input.text(),
                "context_window": self.context_spin.value(),
                "memory_enabled": self.memory_enabled.isChecked(),
            },
            "user_name": self.user_name_input.text(),
            "automation": {
                "chrome_path": self.chrome_path.text(),
                "vscode_path": self.vscode_path.text(),
                "discord_path": self.discord_path.text(),
                "spotify_path": self.spotify_path.text(),
            },
        }

        self.settings_saved.emit(settings)
        self.accept()
