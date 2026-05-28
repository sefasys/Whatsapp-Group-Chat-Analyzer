"""Prepares raw message list for deep analysis.
Operations:
- Filter or label media / system messages
- Filter out extremely short messages (< 2 words)
- Group messages by sender
- Create time buckets (daily, weekly, monthly)
- Generate chunks for LLM context processing (sliding window)
"""
from models.message import Message, MessageType

def filter_noise(messages: list[Message]) -> list[Message]:
    """Cleans system messages, media placeholders, and single-character reactions."""
    clean_msgs = []
    for msg in messages:
        if msg.type in [MessageType.SYSTEM, MessageType.MEDIA, MessageType.DELETED]:
            continue
        # Also filter out extremely short text-only messages (noise)
        if msg.word_count < 2 and not msg.emojis and not msg.links and len(msg.content) < 3:
            continue
        clean_msgs.append(msg)
    return clean_msgs

def group_by_user(messages: list[Message]) -> dict[str, list[Message]]:
    """Groups messages by sender ID."""
    groups = {}
    for msg in messages:
        if msg.sender_id not in groups:
            groups[msg.sender_id] = []
        groups[msg.sender_id].append(msg)
    return groups

def group_by_timewindow(messages: list[Message], window_days: int = 7) -> list[list[Message]]:
    """Splits messages into N-day intervals."""
    if not messages:
        return []
    windows = []
    current_window = []
    start_time = messages[0].timestamp
    
    for msg in messages:
        if (msg.timestamp - start_time).days >= window_days or len(current_window) >= 500:
            windows.append(current_window)
            current_window = [msg]
            start_time = msg.timestamp
        else:
            current_window.append(msg)
            
    if current_window:
        windows.append(current_window)
    return windows

def build_llm_chunks(
    messages: list[Message],
    chunk_size: int = 400,
    overlap: int = 50) -> list[str]:
    """
    Creates text chunks for LLM using a sliding window.
    Each chunk contains the last `overlap` messages of the previous chunk for context continuity.
    Format: "User_01 [14:32]: message content"
    """
    if not messages:
        return []
        
    chunks = []
    i = 0
    while i < len(messages):
        chunk_msgs = messages[i:i + chunk_size]
        chunk_lines = []
        for msg in chunk_msgs:
            time_str = msg.timestamp.strftime("%H:%M")
            chunk_lines.append(f"{msg.sender_id} [{time_str}]: {msg.content}")
            
        chunks.append("\n".join(chunk_lines))
        
        if i + chunk_size >= len(messages):
            break
            
        i += (chunk_size - overlap)
        
    return chunks

def build_user_summary_prompt(user_id: str, messages: list[Message], stats: dict) -> str:
    """
    Constructs the character analysis prompt for a single user.
    Combines calculated statistical metrics with sample messages.
    """
    sample = messages[:80]  # ilk 80 mesaj örnek olarak
    sample_text = "\n".join(
        f"{msg.sender_id} [{msg.timestamp.strftime('%H:%M')}]: {msg.content}"
        for msg in sample
        if msg.type == MessageType.TEXT
    )
    return f"""
Kullanıcı ID: {user_id}
Toplam mesaj: {stats.get('total_messages', 0)}
Günlük ortalama: {stats.get('messages_per_day', 0):.1f}
En aktif saat: {stats.get('most_active_hour', '?')}:00
En çok kullanılan emojiler: {', '.join(stats.get('top_emojis', [])[:5])}

Örnek mesajlar (kronolojik):
{sample_text}
"""
