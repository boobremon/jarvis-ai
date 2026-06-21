"""
JARVIS AI Core Animation Widget
Created by Sohail Karim

Circular reactor-style animation for the AI assistant.
"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QRadialGradient, QPainterPath
import math
import time

from jarvis_app.ui.styles import JarvisTheme


class AICoreWidget(QWidget):
    """Animated AI core visualization"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # State
        self._state = "idle"  # idle, listening, thinking, speaking
        self._animation_phase = 0.0
        self._pulse_phase = 0.0
        self._rotation_angle = 0.0

        # Animation timers
        self._animation_timer = QTimer(self)
        self._animation_timer.timeout.connect(self._update_animation)
        self._animation_timer.start(16)  # ~60 FPS

        # Pulse effect
        self._pulse_timer = QTimer(self)
        self._pulse_timer.timeout.connect(self._update_pulse)
        self._pulse_timer.start(50)

        self.setMinimumSize(300, 300)

    def set_state(self, state: str):
        """Set AI state (idle, listening, thinking, speaking)"""
        self._state = state
        self.update()

    def _update_animation(self):
        """Update animation state"""
        self._animation_phase += 0.05 * (1.5 if self._state == "thinking" else 1.0)
        self._rotation_angle += 0.02 * (2.0 if self._state == "speaking" else 1.0)

        if self._animation_phase > 2 * math.pi:
            self._animation_phase -= 2 * math.pi

        if self._rotation_angle > 360:
            self._rotation_angle -= 360

        self.update()

    def _update_pulse(self):
        """Update pulse effect"""
        self._pulse_phase += 0.1
        if self._pulse_phase > 2 * math.pi:
            self._pulse_phase -= 2 * math.pi
        self.update()

    def paintEvent(self, event):
        """Draw the AI core visualization"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Center point
        center_x = self.width() // 2
        center_y = self.height() // 2
        base_radius = min(center_x, center_y) - 20

        # Draw outer glow
        self._draw_glow(painter, center_x, center_y, base_radius)

        # Draw rotating arcs
        self._draw_rotating_arcs(painter, center_x, center_y, base_radius)

        # Draw core circles
        self._draw_core_circles(painter, center_x, center_y, base_radius)

        # Draw center reactor
        self._draw_reactor(painter, center_x, center_y, base_radius)

        # Draw state indicator
        self._draw_state_indicator(painter, center_x, center_y, base_radius)

        painter.end()

    def _draw_glow(self, painter: QPainter, cx: int, cy: int, radius: int):
        """Draw outer glow effect"""
        # Primary glow
        glow_color = QColor(JarvisTheme.PRIMARY)
        glow_color.setAlphaF(0.1 + 0.1 * math.sin(self._pulse_phase))
        glow_gradient = QRadialGradient(cx, cy, radius + 30)
        glow_gradient.setColorAt(0, QColor(0, 212, 255, 100))
        glow_gradient.setColorAt(0.5, QColor(0, 212, 255, 30))
        glow_gradient.setColorAt(1, QColor(0, 212, 255, 0))

        painter.setBrush(QBrush(glow_gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(cx - radius - 30, cy - radius - 30, 2 * (radius + 30), 2 * (radius + 30))

    def _draw_rotating_arcs(self, painter: QPainter, cx: int, cy: int, radius: int):
        """Draw rotating arc patterns"""
        # Primary rotating arc
        primary_color = QColor(JarvisTheme.PRIMARY)

        for i in range(3):
            angle_offset = (i * 120) + self._rotation_angle
            arc_radius = radius - (i * 10)

            pen = QPen(primary_color)
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)

            # Draw arc
            rect = int(cx - arc_radius), int(cy - arc_radius), int(2 * arc_radius), int(2 * arc_radius)
            start_angle = int(angle_offset * 16)
            span_angle = int(90 * 16)

            painter.drawArc(*rect, start_angle, span_angle)
            painter.drawArc(*rect, start_angle + 180 * 16, span_angle)

    def _draw_core_circles(self, painter: QPainter, cx: int, cy: int, radius: int):
        """Draw core concentric circles"""
        secondary_color = QColor(JarvisTheme.SECONDARY)
        primary_color = QColor(JarvisTheme.PRIMARY)

        # Outer circle
        pen = QPen(primary_color)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(cx - radius, cy - radius, 2 * radius, 2 * radius)

        # Middle circle
        mid_radius = radius * 0.7
        pen.setWidth(2)
        pen.setColor(secondary_color)
        painter.setPen(pen)
        painter.drawEllipse(int(cx - mid_radius), int(cy - mid_radius), int(2 * mid_radius), int(2 * mid_radius))

        # Inner circle with pulse
        inner_radius = radius * 0.4 + 5 * math.sin(self._pulse_phase)
        pen.setWidth(2)
        pen.setColor(primary_color)
        painter.setPen(pen)
        painter.drawEllipse(
            int(cx - inner_radius), int(cy - inner_radius),
            int(2 * inner_radius), int(2 * inner_radius)
        )

    def _draw_reactor(self, painter: QPainter, cx: int, cy: int, radius: int):
        """Draw center reactor core"""
        # State-based colors
        if self._state == "listening":
            core_color = QColor(JarvisTheme.SUCCESS)
        elif self._state == "thinking":
            core_color = QColor(JarvisTheme.WARNING)
        elif self._state == "speaking":
            core_color = QColor(JarvisTheme.PRIMARY)
        else:
            core_color = QColor(JarvisTheme.PRIMARY)

        # Gradient fill
        reactor_radius = radius * 0.2
        gradient = QRadialGradient(cx, cy, reactor_radius)
        gradient.setColorAt(0, core_color.lighter(150))
        gradient.setColorAt(0.5, core_color)
        gradient.setColorAt(1, core_color.darker(150))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(
            int(cx - reactor_radius), int(cy - reactor_radius),
            int(2 * reactor_radius), int(2 * reactor_radius)
        )

        # Inner bright core
        inner_gradient = QRadialGradient(cx, cy, reactor_radius * 0.5)
        inner_gradient.setColorAt(0, QColor(255, 255, 255, 200))
        inner_gradient.setColorAt(1, QColor(255, 255, 255, 0))

        painter.setBrush(QBrush(inner_gradient))
        painter.drawEllipse(
            int(cx - reactor_radius * 0.5), int(cy - reactor_radius * 0.5),
            int(reactor_radius), int(reactor_radius)
        )

    def _draw_state_indicator(self, painter: QPainter, cx: int, cy: int, radius: int):
        """Draw state text around core"""
        font = QFont("Segoe UI", 10, QFont.Weight.Light)
        painter.setFont(font)

        # Draw state text
        state_texts = {
            "idle": "STANDBY",
            "listening": "LISTENING",
            "thinking": "PROCESSING",
            "speaking": "SPEAKING"
        }

        text = state_texts.get(self._state, "STANDBY")

        color = QColor(JarvisTheme.TEXT_SECONDARY)
        if self._state == "listening":
            color = QColor(JarvisTheme.SUCCESS)
        elif self._state == "thinking":
            color = QColor(JarvisTheme.WARNING)
        elif self._state == "speaking":
            color = QColor(JarvisTheme.PRIMARY)

        painter.setPen(color)
        text_rect = painter.fontMetrics().boundingRect(text)
        painter.drawText(cx - text_rect.width() // 2, int(cy + radius * 0.6), text)
