"""
JARVIS Voice Recognition Module
Created by Sohail Karim

Real-time speech recognition with wake word detection.
"""

import speech_recognition as sr
from typing import Optional, Callable
from queue import Queue
import threading
import time

from jarvis_app.core.logger import get_logger


class VoiceRecognizer:
    """Voice recognition with wake word detection"""

    def __init__(
        self,
        wake_word: str = "jarvis",
        alternative_wake_words: list = None,
        timeout: int = 5,
        phrase_time_limit: int = 10
    ):
        self.logger = get_logger()
        self.wake_word = wake_word.lower()
        self.alternative_wake_words = [
            w.lower() for w in (alternative_wake_words or ["hey jarvis"])
        ]
        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit

        # Initialize recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

        # State
        self._listening = False
        self._continuous = False
        self._audio_queue = Queue()
        self._callback: Optional[Callable] = None

        # Microphone
        self._microphone = None
        self._background_listener = None

    def _get_microphone(self) -> sr.Microphone:
        """Get or create microphone instance"""
        if self._microphone is None:
            self._microphone = sr.Microphone()
        return self._microphone

    def calibrate_microphone(self, duration: float = 1.0) -> bool:
        """Calibrate microphone for ambient noise"""
        try:
            with self._get_microphone() as source:
                self.logger.voice("CALIBRATING", f"Duration: {duration}s")
                self.recognizer.adjust_for_ambient_noise(source, duration=duration)
                self.logger.voice("CALIBRATED", f"Energy threshold: {self.recognizer.energy_threshold}")
                return True
        except Exception as e:
            self.logger.error(f"Microphone calibration failed: {e}")
            return False

    def listen_once(self) -> Optional[str]:
        """Listen for a single phrase"""
        try:
            with self._get_microphone() as source:
                self.logger.voice("LISTENING", "Waiting for speech...")
                audio = self.recognizer.listen(
                    source,
                    timeout=self.timeout,
                    phrase_time_limit=self.phrase_time_limit
                )

            return self._recognize_audio(audio)

        except sr.WaitTimeoutError:
            self.logger.voice("TIMEOUT", "No speech detected")
            return None
        except Exception as e:
            self.logger.error(f"Listen error: {e}")
            return None

    def _recognize_audio(self, audio: sr.AudioData) -> Optional[str]:
        """Recognize speech from audio"""
        try:
            self.logger.voice("RECOGNIZING", "Processing audio...")
            text = self.recognizer.recognize_google(audio, language='en-US')
            self.logger.voice("RECOGNIZED", text)
            return text

        except sr.UnknownValueError:
            self.logger.voice("UNRECOGNIZED", "Could not understand audio")
            return None
        except sr.RequestError as e:
            self.logger.error(f"Recognition service error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Recognition error: {e}")
            return None

    def detect_wake_word(self, text: str) -> bool:
        """Check if text contains wake word"""
        if not text:
            return False

        text_lower = text.lower().strip()

        # Check main wake word
        if self.wake_word in text_lower:
            return True

        # Check alternatives
        for alt_wake_word in self.alternative_wake_words:
            if alt_wake_word in text_lower:
                return True

        return False

    def extract_command(self, text: str) -> str:
        """Extract command after wake word"""
        if not text:
            return ""

        text_lower = text.lower()

        # Remove wake word and return command
        for wake in [self.wake_word] + self.alternative_wake_words:
            if wake in text_lower:
                command = text_lower.replace(wake, "", 1).strip()
                return command if command else text

        return text

    def start_continuous_listening(self, callback: Callable[[str, bool], None]) -> bool:
        """Start continuous background listening"""
        if self._listening:
            return True

        self._callback = callback
        self._continuous = True
        self._listening = True

        # Calibrate first
        if not self.calibrate_microphone():
            self._listening = False
            return False

        # Start background listener
        def listen_loop():
            while self._continuous:
                try:
                    with self._get_microphone() as source:
                        audio = self.recognizer.listen(
                            source,
                            timeout=1,
                            phrase_time_limit=self.phrase_time_limit
                        )
                        text = self._recognize_audio(audio)
                        if text and self._callback:
                            has_wake_word = self.detect_wake_word(text)
                            self._callback(text, has_wake_word)
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    self.logger.error(f"Continuous listen error: {e}")
                    time.sleep(0.5)

        self._background_listener = threading.Thread(
            target=listen_loop,
            daemon=True,
            name="VoiceListener"
        )
        self._background_listener.start()

        self.logger.voice("STARTED", "Continuous listening active")
        return True

    def stop_continuous_listening(self) -> None:
        """Stop continuous background listening"""
        self._continuous = False
        self._listening = False
        self._callback = None
        self.logger.voice("STOPPED", "Continuous listening stopped")

    def is_listening(self) -> bool:
        """Check if continuous listening is active"""
        return self._listening
