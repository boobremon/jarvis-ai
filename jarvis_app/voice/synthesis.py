"""
JARVIS Text-to-Speech Module
Created by Sohail Karim

Natural voice synthesis with personality matching JARVIS character.
"""

import pyttsx3
import threading
import queue
from typing import Optional
import time

from jarvis_app.core.logger import get_logger


class VoiceSynthesizer:
    """Text-to-speech engine with JARVIS personality"""

    def __init__(
        self,
        rate: int = 180,
        volume: float = 1.0,
        voice_id: int = 0
    ):
        self.logger = get_logger()
        self.rate = rate
        self.volume = volume
        self.voice_id = voice_id

        # Engine
        self._engine: Optional[pyttsx3.Engine] = None
        self._speaking = False
        self._interrupt_flag = False
        self._speech_queue = queue.Queue()

        # Initialize
        self._init_engine()

    def _init_engine(self) -> bool:
        """Initialize the TTS engine"""
        try:
            self._engine = pyttsx3.init()

            # Configure voice
            voices = self._engine.getProperty('voices')
            if voices and len(voices) > self.voice_id:
                self._engine.setProperty('voice', voices[self.voice_id].id)

            self._engine.setProperty('rate', self.rate)
            self._engine.setProperty('volume', self.volume)

            self.logger.voice("TTS_INIT", f"Voice ID: {self.voice_id}, Rate: {self.rate}")
            return True

        except Exception as e:
            self.logger.error(f"TTS engine init failed: {e}")
            return False

    def set_voice(self, voice_index: int) -> bool:
        """Set voice by index"""
        try:
            if not self._engine:
                self._init_engine()

            voices = self._engine.getProperty('voices')
            if voices and 0 <= voice_index < len(voices):
                self._engine.setProperty('voice', voices[voice_index].id)
                self.voice_id = voice_index
                self.logger.voice("VOICE_CHANGED", f"Voice: {voices[voice_index].name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Set voice error: {e}")
            return False

    def set_rate(self, rate: int) -> None:
        """Set speech rate"""
        self.rate = rate
        if self._engine:
            self._engine.setProperty('rate', rate)

    def set_volume(self, volume: float) -> None:
        """Set volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        if self._engine:
            self._engine.setProperty('volume', self.volume)

    def speak(self, text: str, blocking: bool = True) -> bool:
        """Speak text"""
        if not text or not self._engine:
            return False

        try:
            self._speaking = True
            self._interrupt_flag = False

            self.logger.voice("SPEAKING", text[:100] + "..." if len(text) > 100 else text)

            if blocking:
                self._engine.say(text)
                self._engine.runAndWait()
            else:
                thread = threading.Thread(
                    target=self._speak_async,
                    args=(text,),
                    daemon=True
                )
                thread.start()

            self._speaking = False
            return True

        except Exception as e:
            self.logger.error(f"Speech error: {e}")
            self._speaking = False
            return False

    def _speak_async(self, text: str) -> None:
        """Speak asynchronously in a thread"""
        try:
            self._engine.say(text)
            self._engine.runAndWait()
        except Exception as e:
            self.logger.error(f"Async speech error: {e}")
        finally:
            self._speaking = False

    def interrupt(self) -> None:
        """Interrupt current speech"""
        if self._engine and self._speaking:
            self._interrupt_flag = True
            self._engine.stop()
            self._speaking = False
            self.logger.voice("INTERRUPTED", "Speech interrupted")

    def is_speaking(self) -> bool:
        """Check if currently speaking"""
        return self._speaking

    def get_available_voices(self) -> list:
        """Get list of available voices"""
        if not self._engine:
            self._init_engine()

        try:
            voices = self._engine.getProperty('voices')
            return [
                {
                    'id': i,
                    'name': voice.name,
                    'languages': voice.languages
                }
                for i, voice in enumerate(voices or [])
            ]
        except Exception as e:
            self.logger.error(f"Get voices error: {e}")
            return []

    def terminate(self) -> None:
        """Clean up resources"""
        if self._engine:
            self._engine.stop()
            self._speaking = False
            self.logger.voice("TTS_TERMINATED", "Engine stopped")
