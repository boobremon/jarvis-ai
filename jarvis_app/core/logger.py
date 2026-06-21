"""
JARVIS Logging Module
Created by Sohail Karim

Centralized logging system for the JARVIS AI Assistant.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from logging.handlers import RotatingFileHandler


class JarvisLogger:
    """Centralized logging for JARVIS"""

    _instance: Optional['JarvisLogger'] = None
    _initialized: bool = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        log_level: str = "INFO",
        log_to_file: bool = True,
        log_to_console: bool = True
    ):
        if self._initialized:
            return

        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.logger = logging.getLogger("JARVIS")
        self.logger.setLevel(self.log_level)

        # Clear any existing handlers
        self.logger.handlers.clear()

        # Create formatter
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Console handler
        if log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.log_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        # File handler with rotation
        if log_to_file:
            log_dir = Path.home() / ".jarvis" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)

            log_file = log_dir / f"jarvis_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=5 * 1024 * 1024,
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        self._initialized = True

    def info(self, message: str) -> None:
        self.logger.info(message)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def critical(self, message: str) -> None:
        self.logger.critical(message)

    def command(self, command: str, result: str = "SUCCESS") -> None:
        self.logger.info(f"COMMAND: {command} | RESULT: {result}")

    def voice(self, event: str, transcript: str = "") -> None:
        self.logger.info(f"VOICE: {event} | {transcript}")

    def ai(self, prompt: str, response: str) -> None:
        self.logger.debug(f"AI PROMPT: {prompt[:100]}...")
        self.logger.debug(f"AI RESPONSE: {response[:100]}...")

    def system(self, event: str, details: str = "") -> None:
        self.logger.info(f"SYSTEM: {event} | {details}")


# Global logger instance
def get_logger(log_level: str = "INFO") -> JarvisLogger:
    return JarvisLogger(log_level=log_level)
