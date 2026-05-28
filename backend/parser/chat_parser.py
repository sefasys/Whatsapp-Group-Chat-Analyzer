"""Parses WhatsApp .txt export files.
Examples of WhatsApp formats (varies by region):
  TR:  [27.05.2025, 14:32:11] Ahmet: merhaba
  EN:  [5/27/25, 2:32:11 PM] Ahmet: hello
  Alt: 27.05.2025, 14:32 - Ahmet: merhaba
Output: List[Message]
"""
import re
import uuid
from datetime import datetime
from typing import Optional
from models.message import Message, MessageType
import emoji
from dateutil import parser as date_parser

# Supported format regex patterns
MESSAGE_PATTERN = re.compile(r"^\[?(\d{1,2}[./]\d{1,2}[./]\d{2,4}),?\s(\d{1,2}:\d{2}(?::\d{2})?(?:\s?[aApP][mM])?)\]?\s(?:-\s)?(.+?):\s(.*)$", re.DOTALL)

MEDIA_TOKENS = ["<Media omitted>", "image omitted", "video omitted", "audio omitted", "document omitted", "GIF omitted", "<attached:"]
SYSTEM_TOKENS = ["joined using", "added", "removed", "left", "changed the subject", "changed this group", "created this group", "Messages and calls are end-to-end encrypted", "Waiting for this message", "added you", "missed voice call", "missed video call"]

def _clean_invisible_chars(text: str) -> str:
    """Removes invisible LRM, RLM and other bidirectional formatting characters WhatsApp uses."""
    return re.sub(r'[\u200e\u200f\u202a\u202b\u202c\u202d\u202e]', '', text)

def _normalize_sender(sender: str) -> str:
    """Telefon numarası formatındaki sender'ları normalize eder."""
    phone_pattern = re.compile(r'^\+?[\d\s\-\(\)]{7,}$')
    if phone_pattern.match(sender.strip()):
        return f"Unknown_{sender.strip().replace(' ', '').replace('+', '')[-4:]}"
    return sender.strip()

def parse_file(filepath: str) -> list[Message]:
    """Reads the file and returns a list of Message objects."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return parse_text(f.read())

def parse_text(raw_text: str) -> list[Message]:
    """Parses raw string data. Useful for testing."""
    messages = []
    lines = raw_text.split('\n')
    
    current_msg = None
    
    for line in lines:
        line = _clean_invisible_chars(line)
        if not line.strip():
            continue
            
        match = MESSAGE_PATTERN.match(line)
        if match:
            if current_msg:
                messages.append(current_msg)
                
            date_str, time_str, sender, content = match.groups()
            sender = _normalize_sender(sender)
            dt_str = f"{date_str} {time_str}"
            try:
                timestamp = date_parser.parse(dt_str, dayfirst=True)
            except ValueError:
                timestamp = datetime.now()
                
            msg_type = _classify_message(content, sender)
            msg_emojis = _extract_emojis(content)
            msg_links = _extract_links(content)
            
            word_count = len(content.split()) if msg_type == MessageType.TEXT else 0
            char_count = len(content) if msg_type == MessageType.TEXT else 0
            
            current_msg = Message(
                id=str(uuid.uuid4()),
                timestamp=timestamp,
                sender_id=sender.strip(),
                sender_raw=sender.strip(),
                content=content.strip(),
                type=msg_type,
                emojis=msg_emojis,
                links=msg_links,
                word_count=word_count,
                char_count=char_count
            )
        else:
            if current_msg:
                current_msg.content += "\n" + line.strip()
                if current_msg.type == MessageType.TEXT:
                    current_msg.word_count = len(current_msg.content.split())
                    current_msg.char_count = len(current_msg.content)
                    current_msg.emojis = _extract_emojis(current_msg.content)
                    current_msg.links = _extract_links(current_msg.content)

    if current_msg:
        messages.append(current_msg)
        
    return messages

def _detect_format(sample_lines: list[str]) -> Optional[re.Pattern]:
    """Detects which regex pattern matches the chat format."""
    return MESSAGE_PATTERN

def _classify_message(content: str, sender: str = "") -> MessageType:
    """Classifies message type: text, media, link, system, reaction."""
    if "This message was deleted" in content:
        return MessageType.DELETED
    if any(token in content for token in MEDIA_TOKENS):
        return MessageType.MEDIA
    if any(token in content for token in SYSTEM_TOKENS) or any(token in sender for token in SYSTEM_TOKENS):
        return MessageType.SYSTEM
    if "http://" in content or "https://" in content:
        return MessageType.LINK
    return MessageType.TEXT

def _extract_links(content: str) -> list[str]:
    """Extracts URLs from message content."""
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    return url_pattern.findall(content)

def _extract_emojis(content: str) -> list[str]:
    """Extracts emojis from message content."""
    return [token['emoji'] for token in emoji.emoji_list(content)]
