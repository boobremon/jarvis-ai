"""
JARVIS AI Engine Module
Created by Sohail Karim

Intelligent conversation engine with command understanding.
"""

import re
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum

from jarvis_app.core.logger import get_logger
from jarvis_app.memory.conversation import ConversationMemory, MessageRole


class CommandType(Enum):
    """Types of commands JARVIS can execute"""
    UNKNOWN = "unknown"
    GREETING = "greeting"
    WEATHER = "weather"
    TIME = "time"
    DATE = "date"
    OPEN_APP = "open_app"
    OPEN_WEBSITE = "open_website"
    SEARCH_GOOGLE = "search_google"
    SEARCH_YOUTUBE = "search_youtube"
    SYSTEM_COMMAND = "system_command"
    VOLUME = "volume"
    BRIGHTNESS = "brightness"
    INFORMATION = "information"
    CONVERSATION = "conversation"
    THANKS = "thanks"
    GOODBYE = "goodbye"
    JOKE = "joke"
    REMEMBER = "remember"
    RECALL = "recall"
    STATUS = "status"


@dataclass
class ParsedCommand:
    """Parsed command result"""
    command_type: CommandType
    content: str
    parameters: Dict
    confidence: float = 1.0


class CommandParser:
    """Parses user commands to understand intent"""

    def __init__(self):
        self.logger = get_logger()

        # Define command patterns
        self.patterns = {
            CommandType.GREETING: [
                r"^(hi|hello|hey|greetings|good morning|good afternoon|good evening).*",
                r"^(you (there|alive|awake)|are you (there|alive|awake)).*",
            ],
            CommandType.WEATHER: [
                r"^(weather|what'?s the weather|tell me the weather).*",
                r"^(temperature|what'?s the temperature).*",
            ],
            CommandType.TIME: [
                r"^(time|what time|what'?s the time|current time).*",
                r"^(tell me the time).*",
            ],
            CommandType.DATE: [
                r"^(date|what date|what'?s the date|current date|today).*
",
                r"^(what day is it).*",
            ],
            CommandType.OPEN_APP: [
                r"^open ([a-z\s]+)\s*(app|application)?$",
                r"^launch ([a-z\s]+)\s*(app|application)?$",
                r"^start ([a-z\s]+)\s*(app|application)?$",
                r"^run ([a-z\s]+)$",
            ],
            CommandType.OPEN_WEBSITE: [
                r"^open ([a-z\s]+) (website|site)$",
                r"^go to ([a-z\s]+)$",
                r"^browse ([a-z\s]+)$",
            ],
            CommandType.SEARCH_GOOGLE: [
                r"^search (google |)(for |)(.+)$",
                r"^google (.+)$",
                r"^look up (.+)$",
            ],
            CommandType.SEARCH_YOUTUBE: [
                r"^(search |find |)(.+)( on| in) youtube$",
                r"^youtube (.+)$",
                r"^play (.+)( on youtube)*$",
            ],
            CommandType.SYSTEM_COMMAND: [
                r"^(shutdown|shut down|turn off) (computer|pc|system)$",
                r"^(restart|reboot) (computer|pc|system)$",
                r"^(lock|lock (computer|pc|screen))$",
                r"^(sleep|hibernate) (computer|pc|system)$",
                r"^(sign out|log out|logout).*$",
            ],
            CommandType.VOLUME: [
                r"^(set |change |)(volume|vol)( to | )(\d+)( percent|\%|)$",
                r"^(mute|unmute)$",
                r"^(volume up|volume down)$",
            ],
            CommandType.INFORMATION: [
                r"^(what is|what are|who is|who are|what'?s) (.+)$",
                r"^(tell me about|explain|describe) (.+)$",
                r"^(how do (i|you)|how to) (.+)$",
            ],
            CommandType.THANKS: [
                r"^(thank(s| you)|thanks a lot|many thanks).*",
                r"^(i appreciate).*",
            ],
            CommandType.GOODBYE: [
                r"^(goodbye|bye|see you|good night|exit|quit|sleep jarvis).*",
            ],
            CommandType.JOKE: [
                r"^(tell me a joke|joke|say something funny).*",
            ],
            CommandType.REMEMBER: [
                r"^remember (that |)(.+)$",
                r"^(make a note|note|save) (.+)$",
            ],
            CommandType.RECALL: [
                r"^(what did you remember|what do you remember|recall).*",
                r"^(reminder|remind me).*",
            ],
            CommandType.STATUS: [
                r"^(system status|status report|diagnostics|how are you).*",
                r"^(cpu|memory|ram|gpu|disk|network) (usage|info|status).*$",
            ],
        }

    def parse(self, text: str) -> ParsedCommand:
        """Parse user text to extract command intent"""
        text_lower = text.lower().strip()

        # Check each command type
        for cmd_type, patterns in self.patterns.items():
            for pattern in patterns:
                try:
                    match = re.match(pattern, text_lower)
                    if match:
                        return self._build_command(cmd_type, text_lower, match)
                except Exception as e:
                    self.logger.error(f"Pattern error: {e}")
                    continue

        # Default to conversation
        return ParsedCommand(
            command_type=CommandType.CONVERSATION,
            content=text,
            parameters={}
        )

    def _build_command(self, cmd_type: CommandType, text: str, match) -> ParsedCommand:
        """Build parsed command from regex match"""
        params = {}

        # Extract groups based on command type
        if cmd_type == CommandType.OPEN_APP:
            params["app_name"] = match.group(1)
        elif cmd_type == CommandType.OPEN_WEBSITE:
            params["site_name"] = match.group(1)
        elif cmd_type in [CommandType.SEARCH_GOOGLE, CommandType.SEARCH_YOUTUBE]:
            # Find the search query in the groups
            for i, group in enumerate(match.groups()):
                if group and i > 0 and group not in ["google ", "for ", " on", " in", " on youtube", "search ", "find "]:
                    params["query"] = group.strip()
                    break
        elif cmd_type == CommandType.VOLUME:
            if "mute" in text:
                params["action"] = "mute"
            elif "unmute" in text:
                params["action"] = "unmute"
            elif "up" in text:
                params["action"] = "up"
            elif "down" in text:
                params["action"] = "down"
            else:
                # Extract percentage
                nums = re.findall(r'\d+', text)
                if nums:
                    params["level"] = int(nums[0])
                    params["action"] = "set"
        elif cmd_type == CommandType.REMEMBER:
            # Get the thing to remember
            content = match.group(2) if match.lastindex >= 2 else ""
            params["content"] = content

        return ParsedCommand(
            command_type=cmd_type,
            content=text,
            parameters=params
        )


class AIEngine:
    """Main AI engine for JARVIS"""

    def __init__(
        self,
        memory: ConversationMemory,
        command_parser: CommandParser = None,
    ):
        self.logger = get_logger()
        self.memory = memory
        self.command_parser = command_parser or CommandParser()

        # Memory storage for remember/recall
        self._remembered_items: Dict[str, str] = {}

        # Command handlers
        self._handlers: Dict[CommandType, Callable] = {}

        # Registered AI provider (external, not included for API key safety)
        self._ai_provider: Optional[Callable] = None

    def register_handler(self, cmd_type: CommandType, handler: Callable) -> None:
        """Register a custom command handler"""
        self._handlers[cmd_type] = handler

    def register_ai_provider(self, provider: Callable) -> None:
        """Register an AI provider function (e.g., Anthropic API)"""
        self._ai_provider = provider

    def process(self, text: str, interrupt: bool = False) -> Tuple[str, bool, Dict]:
        """Process user input and generate response"""
        # Parse command
        parsed = self.command_parser.parse(text)

        # Store in memory
        self.memory.add_user_message(text, interrupt=interrupt)

        # Check for registered handler
        if parsed.command_type in self._handlers:
            try:
                response, success, metadata = self._handlers[parsed.command_type](parsed)
            except Exception as e:
                self.logger.error(f"Handler error: {e}")
                response = "I encountered an error processing that request, Sir."
                success = False
                metadata = {"error": str(e)}
        else:
            # Use default processing
            response, success, metadata = self._process_default(parsed)

        # Store response
        self.memory.add_assistant_message(response, metadata.get("command_executed"))

        return response, success, metadata

    def _process_default(self, parsed: ParsedCommand) -> Tuple[str, bool, Dict]:
        """Default command processing"""
        cmd_type = parsed.command_type
        params = parsed.parameters

        if cmd_type == CommandType.GREETING:
            return self._handle_greeting(), True, {}

        elif cmd_type == CommandType.TIME:
            from datetime import datetime
            time_str = datetime.now().strftime("%I:%M %p")
            return f"The current time is {time_str}, Sir.", True, {}

        elif cmd_type == CommandType.DATE:
            from datetime import datetime
            date_str = datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {date_str}, Sir.", True, {}

        elif cmd_type == CommandType.THANKS:
            return "You're most welcome, Sir. It's my pleasure to assist you.", True, {}

        elif cmd_type == CommandType.GOODBYE:
            return "Goodbye, Sir. Standing by for your next session.", True, {"shutdown": True}

        elif cmd_type == CommandType.JOKE:
            import pyjokes
            joke = pyjokes.get_joke()
            return joke, True, {}

        elif cmd_type == CommandType.REMEMBER:
            content = params.get("content", "")
            if content:
                key = f"note_{len(self._remembered_items)}"
                self._remembered_items[key] = content
                return f"I've noted that, Sir: {content}", True, {"content": content}
            return "What would you like me to remember, Sir?", False, {}

        elif cmd_type == CommandType.RECALL:
            if self._remembered_items:
                items = list(self._remembered_items.values())
                if len(items) == 1:
                    return f"You asked me to remember: {items[0]}", True, {}
                return f"I have {len(items)} items noted. The most recent is: {items[-1]}", True, {}
            return "I don't have anything noted at the moment, Sir.", True, {}

        elif cmd_type == CommandType.STATUS:
            return "All systems are operational, Sir. Ready to assist.", True, {}

        elif cmd_type == CommandType.CONVERSATION:
            return self._handle_conversation(parsed.content)

        else:
            # Default response with command recognition
            return f"I understand you want to {parsed.content}, but I need that capability to be configured. Would you like me to help with something else?", False, {}

    def _handle_greeting(self) -> str:
        """Handle greeting commands"""
        import random
        from datetime import datetime

        hour = datetime.now().hour
        if 5 <= hour < 12:
            time_greeting = "Good morning"
        elif 12 <= hour < 17:
            time_greeting = "Good afternoon"
        elif 17 <= hour < 21:
            time_greeting = "Good evening"
        else:
            time_greeting = "Good evening"

        responses = [
            f"{time_greeting}, Sir. At your service.",
            f"{time_greeting}. JARVIS is online and ready.",
            f"{time_greeting}, Sir. All systems operational.",
            f"{time_greeting}. How may I assist you today?",
        ]
        return random.choice(responses)

    def _handle_conversation(self, content: str) -> Tuple[str, bool, Dict]:
        """Handle general conversation"""
        if self._ai_provider:
            try:
                context = self.memory.get_context()
                response = self._ai_provider(content, context)
                return response, True, {}
            except Exception as e:
                self.logger.error(f"AI provider error: {e}")
                return "I apologize, Sir, but I'm having trouble accessing my intelligence systems.", False, {"error": str(e)}

        # Fallback responses when no AI provider configured
        fallback_responses = [
            "I'm here to assist you, Sir. My full conversation capabilities require an AI provider to be configured.",
            "Understood, Sir. For complete conversation support, please configure an AI provider.",
            "I'm operational but my advanced thinking capabilities need to be configured.",
        ]
        import random
        return random.choice(fallback_responses), True, {"needs_ai_provider": True}
