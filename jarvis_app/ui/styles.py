"""
JARVIS UI Styles Module
Created by Sohail Karim

Cinematic futuristic styling for the JARVIS HUD.
"""

from PyQt6.QtGui import QColor, QFont, QPalette
from PyQt6.QtWidgets import QApplication


class JarvisTheme:
    """JARVIS color theme"""

    # Primary Colors
    PRIMARY = "#00D4FF"  # Cyan
    PRIMARY_DARK = "#00A8CC"
    PRIMARY_LIGHT = "#33DDFF"

    # Secondary Colors
    SECONDARY = "#0078D4"  # Blue
    SECONDARY_DARK = "#005A9E"
    SECONDARY_LIGHT = "#4DA6FF"

    # Accent Colors
    ACCENT = "#FF6B35"  # Orange
    ACCENT_DARK = "#CC5629"
    ACCENT_LIGHT = "#FF8A5C"

    # Text Colors
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#B0B0B0"
    TEXT_TERTIARY = "#808080"

    # Background Colors
    BG_PRIMARY = "#0A0E1A"
    BG_SECONDARY = "#0F1729"
    BG_TERTIARY = "#151F35"

    # Status Colors
    SUCCESS = "#00FF88"
    ERROR = "#FF4444"
    WARNING = "#FFB800"
    INFO = "#00D4FF"

    # Panel Colors
    PANEL_BG = "#0F1729"
    PANEL_BORDER = "#1A2642"

    # Glow Colors
    GLOW_PRIMARY = "rgba(0, 212, 255, 0.3)"
    GLOW_SECONDARY = "rgba(0, 120, 212, 0.2)"


class JarvisStyles:
    """JARVIS stylesheet definitions"""

    @staticmethod
    def get_main_stylesheet() -> str:
        """Get main application stylesheet"""
        return f"""
            QMainWindow {{
                background-color: {JarvisTheme.BG_PRIMARY};
            }}

            QWidget {{
                color: {JarvisTheme.TEXT_PRIMARY};
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }}

            /* Panels */
            QFrame#leftPanel, QFrame#rightPanel, QFrame#centerPanel {{
                background-color: {JarvisTheme.PANEL_BG};
                border: 1px solid {JarvisTheme.PANEL_BORDER};
                border-radius: 10px;
            }}

            /* Labels */
            QLabel {{
                color: {JarvisTheme.TEXT_PRIMARY};
                background: transparent;
            }}

            QLabel#titleLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {JarvisTheme.PRIMARY};
                padding: 5px;
            }}

            QLabel#subtitleLabel {{
                font-size: 14px;
                color: {JarvisTheme.TEXT_SECONDARY};
            }}

            QLabel#statusLabel {{
                font-size: 12px;
                color: {JarvisTheme.TEXT_TERTIARY};
            }}

            /* Buttons */
            QPushButton {{
                background-color: {JarvisTheme.BG_TERTIARY};
                color: {JarvisTheme.TEXT_PRIMARY};
                border: 1px solid {JarvisTheme.PANEL_BORDER};
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
            }}

            QPushButton:hover {{
                background-color: {JarvisTheme.PRIMARY_DARK};
                border-color: {JarvisTheme.PRIMARY};
            }}

            QPushButton:pressed {{
                background-color: {JarvisTheme.PRIMARY};
            }}

            QPushButton#primaryButton {{
                background-color: {JarvisTheme.PRIMARY};
                color: {JarvisTheme.BG_PRIMARY};
                font-weight: bold;
            }}

            QPushButton#primaryButton:hover {{
                background-color: {JarvisTheme.PRIMARY_LIGHT};
            }}

            /* Scroll Areas */
            QScrollArea {{
                background: transparent;
                border: none;
            }}

            QScrollArea > QWidget > QWidget {{
                background: transparent;
            }}

            QScrollBar:vertical {{
                background-color: {JarvisTheme.BG_SECONDARY};
                width: 8px;
                border-radius: 4px;
                margin: 0;
            }}

            QScrollBar::handle:vertical {{
                background-color: {JarvisTheme.PRIMARY_DARK};
                border-radius: 4px;
                min-height: 20px;
            }}

            QScrollBar::handle:vertical:hover {{
                background-color: {JarvisTheme.PRIMARY};
            }}

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
                background: none;
            }}

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}

            /* Progress Bars */
            QProgressBar {{
                background-color: {JarvisTheme.BG_TERTIARY};
                border: none;
                border-radius: 5px;
                text-align: center;
                color: {JarvisTheme.TEXT_PRIMARY};
                font-size: 11px;
            }}

            QProgressBar::chunk {{
                background-color: {JarvisTheme.PRIMARY};
                border-radius: 5px;
            }}

            /* Line Edits */
            QLineEdit {{
                background-color: {JarvisTheme.BG_TERTIARY};
                border: 1px solid {JarvisTheme.PANEL_BORDER};
                border-radius: 8px;
                padding: 10px;
                color: {JarvisTheme.TEXT_PRIMARY};
                font-size: 13px;
            }}

            QLineEdit:focus {{
                border-color: {JarvisTheme.PRIMARY};
            }}

            /* Text Edits */
            QTextEdit {{
                background-color: {JarvisTheme.BG_TERTIARY};
                border: 1px solid {JarvisTheme.PANEL_BORDER};
                border-radius: 8px;
                padding: 10px;
                color: {JarvisTheme.TEXT_PRIMARY};
            }}

            /* Combo Box */
            QComboBox {{
                background-color: {JarvisTheme.BG_TERTIARY};
                border: 1px solid {JarvisTheme.PANEL_BORDER};
                border-radius: 8px;
                padding: 8px 15px;
                color: {JarvisTheme.TEXT_PRIMARY};
            }}

            QComboBox:hover {{
                border-color: {JarvisTheme.PRIMARY};
            }}

            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}

            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {JarvisTheme.PRIMARY};
            }}

            QComboBox QAbstractItemView {{
                background-color: {JarvisTheme.BG_SECONDARY};
                border: 1px solid {JarvisTheme.PANEL_BORDER};
                selection-background-color: {JarvisTheme.PRIMARY_DARK};
            }}

            /* Sliders */
            QSlider::groove:horizontal {{
                background: {JarvisTheme.BG_TERTIARY};
                height: 6px;
                border-radius: 3px;
            }}

            QSlider::handle:horizontal {{
                background: {JarvisTheme.PRIMARY};
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }}

            QSlider::handle:horizontal:hover {{
                background: {JarvisTheme.PRIMARY_LIGHT};
            }}

            /* Spinners */
            QSpinBox {{
                background-color: {JarvisTheme.BG_TERTIARY};
                border: 1px solid {JarvisTheme.PANEL_BORDER};
                border-radius: 8px;
                padding: 8px;
                color: {JarvisTheme.TEXT_PRIMARY};
            }}

            /* Checkboxes */
            QCheckBox {{
                color: {JarvisTheme.TEXT_PRIMARY};
                spacing: 8px;
            }}

            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid {JarvisTheme.PANEL_BORDER};
                background-color: {JarvisTheme.BG_TERTIARY};
            }}

            QCheckBox::indicator:checked {{
                background-color: {JarvisTheme.PRIMARY};
                border-color: {JarvisTheme.PRIMARY};
            }}

            QCheckBox::indicator:hover {{
                border-color: {JarvisTheme.PRIMARY};
            }}

            /* Tabs */
            QTabWidget::pane {{
                border: 1px solid {JarvisTheme.PANEL_BORDER};
                border-radius: 8px;
                background-color: {JarvisTheme.BG_SECONDARY};
            }}

            QTabBar::tab {{
                background-color: {JarvisTheme.BG_TERTIARY};
                border: 1px solid {JarvisTheme.PANEL_BORDER};
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 10px 20px;
                color: {JarvisTheme.TEXT_SECONDARY};
            }}

            QTabBar::tab:selected {{
                background-color: {JarvisTheme.BG_SECONDARY};
                border-color: {JarvisTheme.PRIMARY};
                color: {JarvisTheme.PRIMARY};
            }}

            QTabBar::tab:hover:!selected {{
                color: {JarvisTheme.PRIMARY_LIGHT};
            }}

            /* Tooltip */
            QToolTip {{
                background-color: {JarvisTheme.BG_TERTIARY};
                color: {JarvisTheme.TEXT_PRIMARY};
                border: 1px solid {JarvisTheme.PRIMARY};
                border-radius: 4px;
                padding: 5px;
            }}
        """

    @staticmethod
    def get_transcript_styles() -> str:
        """Get transcript-specific styles"""
        return f"""
            #transcriptWidget {{
                background-color: {JarvisTheme.BG_TERTIARY};
                border: none;
            }}

            #userMessage {{
                color: {JarvisTheme.SECONDARY_LIGHT};
                font-size: 13px;
            }}

            #aiMessage {{
                color: {JarvisTheme.PRIMARY};
                font-size: 13px;
            }}

            #systemMessage {{
                color: {JarvisTheme.ACCENT};
                font-size: 12px;
            }}

            #successMessage {{
                color: {JarvisTheme.SUCCESS};
                font-size: 12px;
            }}

            #errorMessage {{
                color: {JarvisTheme.ERROR};
                font-size: 12px;
            }}

            #timestamp {{
                color: {JarvisTheme.TEXT_TERTIARY};
                font-size: 10px;
            }}
        """

    @staticmethod
    def apply_theme(app: QApplication) -> None:
        """Apply JARVIS theme to application"""
        stylesheet = JarvisStyles.get_main_stylesheet()
        app.setStyleSheet(stylesheet)

        # Set palette for additional control
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(JarvisTheme.BG_PRIMARY))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(JarvisTheme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Base, QColor(JarvisTheme.BG_SECONDARY))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(JarvisTheme.BG_TERTIARY))
        palette.setColor(QPalette.ColorRole.Text, QColor(JarvisTheme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Button, QColor(JarvisTheme.BG_TERTIARY))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(JarvisTheme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(JarvisTheme.PRIMARY))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(JarvisTheme.BG_PRIMARY))

        app.setPalette(palette)
