"""
JARVIS AI Assistant
Created by Sohail Karim

Main application controller that orchestrates all components.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from typing import Optional

from jarvis_app.core.config import JarvisConfig
from jarvis_app.core.logger import get_logger
from jarvis_app.ui.main_window import JarvisMainWindow
from jarvis_app.ui.styles import JarvisStyles
from jarvis_app.voice.recognition import VoiceRecognizer
from jarvis_app.voice.synthesis import VoiceSynthesizer
from jarvis_app.memory.conversation import ConversationMemory
from jarvis_app.ai.engine import AIEngine, CommandType
from jarvis_app.automation.apps import AutomationEngine


class JarvisAssistant:
    """Main JARVIS application controller"""

    def __init__(self):
        # Initialize Qt application
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("J.A.R.V.I.S")
        self.app.setApplicationDisplayName("J.A.R.V.I.S by Sohail Karim")

        # Apply styling
        JarvisStyles.apply_theme(self.app)

        # Load configuration
        self.config = JarvisConfig.load()

        # Initialize logger
        self.logger = get_logger(self.config.system.log_level)

        # Initialize components
        self._init_components()

        # State
        self._is_listening = False
        self._current_mode = "idle"

        self.logger.system("JARVIS initialized")

    def _init_components(self):
        """Initialize all JARVIS components"""

        # Memory
        self.memory = ConversationMemory(
            context_window=self.config.ai.context_window,
            persist=self.config.ai.memory_enabled
        )

        # Conversation
        self.memory.start_conversation(self.config.ai.system_prompt)

        # Voice synthesis (TTS)
        self.synthesizer = VoiceSynthesizer(
            rate=self.config.voice.voice_rate,
            volume=self.config.voice.voice_volume,
            voice_id=self.config.voice.voice_id
        )

        # Voice recognition
        self.recognizer = VoiceRecognizer(
            wake_word=self.config.voice.wake_word,
            alternative_wake_words=self.config.voice.alternative_wake_words,
            timeout=self.config.voice.listen_timeout,
            phrase_time_limit=self.config.voice.phrase_time_limit
        )

        # Automation engine
        self.automation = AutomationEngine()

        # AI engine
        self.ai_engine = AIEngine(memory=self.memory)

        # Register command handlers
        self._register_handlers()

        # Create main window
        self.main_window = JarvisMainWindow(self.config)

        # Connect UI signals
        self._connect_signals()

        self.logger.system("Components initialized")

    def _register_handlers(self):
        """Register command handlers"""

        # Open application
        def handle_open_app(parsed):
            app_name = parsed.parameters.get("app_name", "")
            success, message = self.automation.open_application(app_name)
            return message, success, {"command_executed": "open_app", "app": app_name}
        self.ai_engine.register_handler(CommandType.OPEN_APP, handle_open_app)

        # Open website
        def handle_open_website(parsed):
            site_name = parsed.parameters.get("site_name", "")
            success, message = self.automation.open_website(site_name)
            return message, success, {"command_executed": "open_website", "site": site_name}
        self.ai_engine.register_handler(CommandType.OPEN_WEBSITE, handle_open_website)

        # Search Google
        def handle_search_google(parsed):
            query = parsed.parameters.get("query", "")
            success, message = self.automation.search_google(query)
            return message, success, {"command_executed": "search_google", "query": query}
        self.ai_engine.register_handler(CommandType.SEARCH_GOOGLE, handle_search_google)

        # Search YouTube
        def handle_search_youtube(parsed):
            query = parsed.parameters.get("query", "")
            success, message = self.automation.search_youtube(query)
            return message, success, {"command_executed": "search_youtube", "query": query}
        self.ai_engine.register_handler(CommandType.SEARCH_YOUTUBE, handle_search_youtube)

        # System commands
        def handle_system_command(parsed):
            success, message = self.automation.execute_system_command(parsed.content)
            return message, success, {"command_executed": "system_command"}
        self.ai_engine.register_handler(CommandType.SYSTEM_COMMAND, handle_system_command)

        # Volume
        def handle_volume(parsed):
            action = parsed.parameters.get("action", "set")
            if action == "set":
                level = parsed.parameters.get("level", 50)
                success, message = self.automation.set_volume(level)
            elif action == "mute":
                success, message = self.automation.execute_system_command("mute")
            else:
                success, message = False, "Volume command not understood"
            return message, success, {"command_executed": "volume"}
        self.ai_engine.register_handler(CommandType.VOLUME, handle_volume)

    def _connect_signals(self):
        """Connect UI signals to handlers"""

        # Action bar signals
        self.main_window.action_bar.action_triggered.connect(self._on_action_triggered)
        self.main_window.action_bar.command_submitted.connect(self._on_command_submitted)

    def _on_action_triggered(self, action: str):
        """Handle action button click"""
        self._process_command(action)

    def _on_command_submitted(self, command: str):
        """Handle text command submission"""
        self._process_command(command)

    def _process_command(self, text: str):
        """Process a user command"""
        if not text.strip():
            return

        # Update UI
        self._set_state("thinking")
        self.main_window.add_transcript_message("USER", text, "user")

        # Process through AI engine
        response_text, success, metadata = self.ai_engine.process(text)

        # Update transcript
        self.main_window.add_transcript_message("JARVIS", response_text, "ai" if success else "error")

        # Handle special commands
        if metadata.get("shutdown"):
            QTimer.singleShot(2000, self.quit)

        # Speak response
        if self.config.voice.enabled:
            self._set_state("speaking")
            self.synthesizer.speak(response_text, blocking=True)

        self._set_state("idle")
        self.logger.command(text, "SUCCESS" if success else "FAILED")

    def _process_voice_input(self, text: str, has_wake_word: bool):
        """Process voice input"""
        if has_wake_word:
            # Extract command after wake word
            command = self.recognizer.extract_command(text)

            self.main_window.add_wake_detection(text)

            if command:
                self._process_command(command)

        elif self._is_listening:
            # In continuous mode, process everything
            self._process_command(text)

    def _set_state(self, state: str):
        """Set AI state"""
        self._current_mode = state
        self.main_window.set_ai_state(state)

        if state == "listening":
            self.main_window.action_bar.set_listening_state(True)
        else:
            self.main_window.action_bar.set_listening_state(False)

    def start(self):
        """Start JARVIS"""
        self.logger.system("JARVIS starting")

        # Show main window (it handles startup screen internally)
        if not self.config.voice.enabled:
            self.main_window.show()

        return self.app.exec()

    def stop(self):
        """Stop JARVIS"""
        self.logger.system("JARVIS stopping")

        # Stop voice systems
        if self._is_listening:
            self.recognizer.stop_continuous_listening()

        self.synthesizer.terminate()

        # Save config
        self.config.save()

    def quit(self):
        """Quit application"""
        self.stop()
        self.app.quit()


def main():
    """Main entry point"""
    jarvis = JarvisAssistant()
    try:
        exit_code = jarvis.start()
        jarvis.stop()
        sys.exit(exit_code)
    except Exception as e:
        print(f"JARVIS error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
