"""Analysis session model tracker. Manages state from parsing to final reports."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

class SessionStatus(Enum):
    UPLOADED = "uploaded"
    PARSING = "parsing"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class AnalysisSession:
    session_id: str
    created_at: datetime
    status: SessionStatus = SessionStatus.UPLOADED
    filename: str = ""
    total_messages: int = 0
    date_range_start: Optional[datetime] = None
    date_range_end: Optional[datetime] = None
    user_ids: list[str] = field(default_factory=list)
    silent_user_ids: list[str] = field(default_factory=list)   # Users who read but never posted
    error: Optional[str] = None
    progress_pct: int = 0
