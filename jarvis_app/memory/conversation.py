"""
JARVIS Conversation Memory Module
Created by Sohail Karim

Manages conversation history and context for intelligent responses.
"""

from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum
import json
from pathlib import Path


class MessageRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    """Conversation message"""
    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Message':
        return cls(
            role=MessageRole(data["role"]),
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {})
        )


@dataclass
class Conversation:
    """A single conversation session"""
    id: str
    started_at: datetime = field(default_factory=datetime.now)
    messages: List[Message] = field(default_factory=list)

    def add_message(self, role: MessageRole, content: str, metadata: dict = None) -> Message:
        """Add a message to the conversation"""
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        self.messages.append(message)
        return message

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "started_at": self.started_at.isoformat(),
            "messages": [m.to_dict() for m in self.messages]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Conversation':
        return cls(
            id=data["id"],
            started_at=datetime.fromisoformat(data["started_at"]),
            messages=[Message.from_dict(m) for m in data.get("messages", [])]
        )


class ConversationMemory:
    """Manages conversation history and context"""

    def __init__(self, context_window: int = 10, persist: bool = True):
        self.context_window = context_window
        self.persist = persist

        # Current session
        self.current_conversation: Optional[Conversation] = None

        # All conversations
        self.conversations: List[Conversation] = []

        # Storage path
        self.storage_path = Path.home() / ".jarvis" / "memory"
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # Load existing memory
        if self.persist:
            self._load()

    def start_conversation(self, system_prompt: str = None) -> Conversation:
        """Start a new conversation"""
        # Save previous conversation if exists
        if self.current_conversation and self.persist:
            self._save_conversation(self.current_conversation)

        # Create new
        conv_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_conversation = Conversation(id=conv_id)

        # Add system prompt
        if system_prompt:
            self.current_conversation.add_message(
                MessageRole.SYSTEM,
                system_prompt
            )

        self.conversations.append(self.current_conversation)
        return self.current_conversation

    def add_user_message(self, content: str, interrupt: bool = False) -> Message:
        """Add user message to current conversation"""
        if not self.current_conversation:
            self.start_conversation()

        metadata = {"interrupt": interrupt} if interrupt else {}
        return self.current_conversation.add_message(
            MessageRole.USER,
            content,
            metadata
        )

    def add_assistant_message(self, content: str, command_executed: str = None) -> Message:
        """Add assistant message to current conversation"""
        if not self.current_conversation:
            self.start_conversation()

        metadata = {"command_executed": command_executed} if command_executed else {}
        return self.current_conversation.add_message(
            MessageRole.ASSISTANT,
            content,
            metadata
        )

    def get_context(self) -> List[Dict[str, str]]:
        """Get recent messages for AI context"""
        if not self.current_conversation:
            return []

        # Get recent messages within context window
        messages = self.current_conversation.messages[-self.context_window:]

        return [
            {"role": m.role.value, "content": m.content}
            for m in messages
        ]

    def get_full_history(self) -> List[Message]:
        """Get all messages from current conversation"""
        if not self.current_conversation:
            return []
        return self.current_conversation.messages

    def clear_session(self) -> None:
        """Clear current session but keep in history"""
        if self.current_conversation and self.persist:
            self._save_conversation(self.current_conversation)
        self.current_conversation = None

    def clear_all(self) -> None:
        """Clear all conversation history"""
        if self.persist:
            for conv in self.conversations:
                self._save_conversation(conv)

        self.conversations = []
        self.current_conversation = None

    def _save_conversation(self, conversation: Conversation) -> None:
        """Save a conversation to disk"""
        try:
            if not conversation:
                return

            file_path = self.storage_path / f"{conversation.id}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(conversation.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save conversation: {e}")

    def _load(self) -> None:
        """Load conversations from disk"""
        try:
            for file_path in self.storage_path.glob("*.json"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    conv = Conversation.from_dict(data)
                    self.conversations.append(conv)

            # Sort by start time
            self.conversations.sort(key=lambda c: c.started_at)

        except Exception as e:
            print(f"Failed to load memory: {e}")

    def get_last_conversation(self) -> Optional[Conversation]:
        """Get the most recent conversation"""
        return self.conversations[-1] if self.conversations else None

    def search_conversations(self, query: str) -> List[Message]:
        """Search all conversations for a query"""
        results = []
        query_lower = query.lower()

        for conv in self.conversations:
            for msg in conv.messages:
                if query_lower in msg.content.lower():
                    results.append(msg)

        return results

    def get_conversation_summary(self) -> List[Dict]:
        """Get summary of all conversations"""
        return [
            {
                "id": conv.id,
                "started_at": conv.started_at,
                "message_count": len(conv.messages)
            }
            for conv in self.conversations
        ]
