"""
JARVIS Configuration Module
Created by Sohail Karim

Centralized configuration management for the JARVIS AI Assistant.
"""

import json
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class VoiceConfig:
    """Voice system configuration"""
    enabled: bool = True
    wake_word: str = "jarvis"
    alternative_wake_words: List[str] = field(default_factory=lambda: ["hey jarvis"])
    voice_rate: int = 180
    voice_volume: float = 1.0
    voice_id: Optional[int] = 0  # 0 for male, 1 for female
    listen_timeout: int = 5
    phrase_time_limit: int = 10
    continuous_listening: bool = False


@dataclass
class UIConfig:
    """UI configuration"""
    theme: str = "dark"
    primary_color: str = "#00D4FF"  # Cyan
    secondary_color: str = "#0078D4"  # Blue
    accent_color: str = "#FF6B35"  # Orange
    text_color: str = "#FFFFFF"
    background_color: str = "#0A0E1A"
    panel_color: str = "#0F1729"
    success_color: str = "#00FF88"
    error_color: str = "#FF4444"
    warning_color: str = "#FFB800"
    animation_enabled: bool = True
    animation_speed: float = 1.0
    glass_effect: bool = True
    show_system_stats: bool = True
    show_transcript: bool = True


@dataclass
class AIConfig:
    """AI configuration"""
    provider: str = "anthropic"
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 1024
    temperature: float = 0.7
    memory_enabled: bool = True
    context_window: int = 10  # Number of messages to keep
    system_prompt: str = """You are JARVIS, a sophisticated AI assistant created by Sohail Karim.
You are professional, intelligent, calm, and helpful.
You have a slight British-inspired tone and speak naturally, not robotically.
Your primary goal is to assist the user with their tasks efficiently and elegantly.
Keep responses concise but informative."""


@dataclass
class SystemConfig:
    """System configuration"""
    check_updates_on_startup: bool = True
    show_notifications: bool = True
    log_level: str = "INFO"
    auto_start: bool = False
    minimize_to_tray: bool = True
    run_on_startup: bool = False


@dataclass
class AutomationConfig:
    """Automation configuration"""
    chrome_path: str = ""
    steam_path: str = ""
    vscode_path: str = ""
    discord_path: str = ""
    spotify_path: str = ""
    custom_apps: dict = field(default_factory=dict)


@dataclass
class JarvisConfig:
    """Main JARVIS configuration"""
    user_name: str = "Sohail"
    voice: VoiceConfig = field(default_factory=VoiceConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    ai: AIConfig = field(default_factory=AIConfig)
    system: SystemConfig = field(default_factory=SystemConfig)
    automation: AutomationConfig = field(default_factory=AutomationConfig)

    @classmethod
    def get_config_path(cls) -> Path:
        """Get configuration file path"""
        config_dir = Path.home() / ".jarvis"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "config.json"

    @classmethod
    def load(cls) -> 'JarvisConfig':
        """Load configuration from file"""
        config_path = cls.get_config_path()

        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    data = json.load(f)
                return cls.from_dict(data)
            except Exception:
                pass

        return cls()

    def save(self) -> None:
        """Save configuration to file"""
        config_path = self.get_config_path()
        with open(config_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "user_name": self.user_name,
            "voice": {
                "enabled": self.voice.enabled,
                "wake_word": self.voice.wake_word,
                "alternative_wake_words": self.voice.alternative_wake_words,
                "voice_rate": self.voice.voice_rate,
                "voice_volume": self.voice.voice_volume,
                "voice_id": self.voice.voice_id,
                "listen_timeout": self.voice.listen_timeout,
                "phrase_time_limit": self.voice.phrase_time_limit,
                "continuous_listening": self.voice.continuous_listening,
            },
            "ui": {
                "theme": self.ui.theme,
                "primary_color": self.ui.primary_color,
                "secondary_color": self.ui.secondary_color,
                "accent_color": self.ui.accent_color,
                "text_color": self.ui.text_color,
                "background_color": self.ui.background_color,
                "panel_color": self.ui.panel_color,
                "success_color": self.ui.success_color,
                "error_color": self.ui.error_color,
                "warning_color": self.ui.warning_color,
                "animation_enabled": self.ui.animation_enabled,
                "animation_speed": self.ui.animation_speed,
                "glass_effect": self.ui.glass_effect,
                "show_system_stats": self.ui.show_system_stats,
                "show_transcript": self.ui.show_transcript,
            },
            "ai": {
                "provider": self.ai.provider,
                "model": self.ai.model,
                "max_tokens": self.ai.max_tokens,
                "temperature": self.ai.temperature,
                "memory_enabled": self.ai.memory_enabled,
                "context_window": self.ai.context_window,
                "system_prompt": self.ai.system_prompt,
            },
            "system": {
                "check_updates_on_startup": self.system.check_updates_on_startup,
                "show_notifications": self.system.show_notifications,
                "log_level": self.system.log_level,
                "auto_start": self.system.auto_start,
                "minimize_to_tray": self.system.minimize_to_tray,
                "run_on_startup": self.system.run_on_startup,
            },
            "automation": {
                "chrome_path": self.automation.chrome_path,
                "steam_path": self.automation.steam_path,
                "vscode_path": self.automation.vscode_path,
                "discord_path": self.automation.discord_path,
                "spotify_path": self.automation.spotify_path,
                "custom_apps": self.automation.custom_apps,
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'JarvisConfig':
        """Create from dictionary"""
        voice_data = data.get("voice", {})
        ui_data = data.get("ui", {})
        ai_data = data.get("ai", {})
        system_data = data.get("system", {})
        automation_data = data.get("automation", {})

        return cls(
            user_name=data.get("user_name", "Sohail"),
            voice=VoiceConfig(
                enabled=voice_data.get("enabled", True),
                wake_word=voice_data.get("wake_word", "jarvis"),
                alternative_wake_words=voice_data.get("alternative_wake_words", ["hey jarvis"]),
                voice_rate=voice_data.get("voice_rate", 180),
                voice_volume=voice_data.get("voice_volume", 1.0),
                voice_id=voice_data.get("voice_id", 0),
                listen_timeout=voice_data.get("listen_timeout", 5),
                phrase_time_limit=voice_data.get("phrase_time_limit", 10),
                continuous_listening=voice_data.get("continuous_listening", False),
            ),
            ui=UIConfig(
                theme=ui_data.get("theme", "dark"),
                primary_color=ui_data.get("primary_color", "#00D4FF"),
                secondary_color=ui_data.get("secondary_color", "#0078D4"),
                accent_color=ui_data.get("accent_color", "#FF6B35"),
                text_color=ui_data.get("text_color", "#FFFFFF"),
                background_color=ui_data.get("background_color", "#0A0E1A"),
                panel_color=ui_data.get("panel_color", "#0F1729"),
                success_color=ui_data.get("success_color", "#00FF88"),
                error_color=ui_data.get("error_color", "#FF4444"),
                warning_color=ui_data.get("warning_color", "#FFB800"),
                animation_enabled=ui_data.get("animation_enabled", True),
                animation_speed=ui_data.get("animation_speed", 1.0),
                glass_effect=ui_data.get("glass_effect", True),
                show_system_stats=ui_data.get("show_system_stats", True),
                show_transcript=ui_data.get("show_transcript", True),
            ),
            ai=AIConfig(
                provider=ai_data.get("provider", "anthropic"),
                model=ai_data.get("model", "claude-sonnet-4-20250514"),
                max_tokens=ai_data.get("max_tokens", 1024),
                temperature=ai_data.get("temperature", 0.7),
                memory_enabled=ai_data.get("memory_enabled", True),
                context_window=ai_data.get("context_window", 10),
                system_prompt=ai_data.get("system_prompt", AIConfig().system_prompt),
            ),
            system=SystemConfig(
                check_updates_on_startup=system_data.get("check_updates_on_startup", True),
                show_notifications=system_data.get("show_notifications", True),
                log_level=system_data.get("log_level", "INFO"),
                auto_start=system_data.get("auto_start", False),
                minimize_to_tray=system_data.get("minimize_to_tray", True),
                run_on_startup=system_data.get("run_on_startup", False),
            ),
            automation=AutomationConfig(
                chrome_path=automation_data.get("chrome_path", ""),
                steam_path=automation_data.get("steam_path", ""),
                vscode_path=automation_data.get("vscode_path", ""),
                discord_path=automation_data.get("discord_path", ""),
                spotify_path=automation_data.get("spotify_path", ""),
                custom_apps=automation_data.get("custom_apps", {}),
            ),
        )
