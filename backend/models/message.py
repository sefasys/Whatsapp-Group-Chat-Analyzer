"""Core data models."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

class MessageType(Enum):
    TEXT = "text"
    MEDIA = "media"
    LINK = "link"
    SYSTEM = "system"
    REACTION = "reaction"
    DELETED = "deleted"

@dataclass
class Message:
    id: str
    timestamp: datetime
    sender_id: str          # Anonymized user ID
    sender_raw: str         # Real name (local environment only, never sent to API)
    content: str
    type: MessageType
    emojis: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    is_reply: bool = False
    reply_to_id: Optional[str] = None
    word_count: int = 0
    char_count: int = 0
