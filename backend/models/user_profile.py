"""User profile and analysis metrics models."""
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ActivityStats:
    total_messages: int = 0
    total_words: int = 0
    total_chars: int = 0
    media_count: int = 0
    link_count: int = 0
    emoji_count: int = 0
    avg_message_length: float = 0.0
    messages_per_day: float = 0.0
    most_active_hour: Optional[int] = None
    most_active_day: Optional[str] = None
    first_message_date: Optional[str] = None
    last_message_date: Optional[str] = None
    silence_periods: list[dict] = field(default_factory=list)   # Periods of user inactivity

@dataclass
class OceanScores:
    """Big Five Personality Model scores (0.0 - 1.0)"""
    openness: float = 0.0
    conscientiousness: float = 0.0
    extraversion: float = 0.0
    agreeableness: float = 0.0
    neuroticism: float = 0.0
    confidence: float = 0.0     # Model confidence score for this profile

@dataclass
class SocialRole:
    """Social role detection within the group network"""
    primary_role: str = ""          # leader, mediator, entertainer, observer, provocateur...
    secondary_roles: list[str] = field(default_factory=list)
    influence_score: float = 0.0    # Behavioral influence power (0-1)
    centrality_score: float = 0.0   # Social network centrality metric

@dataclass
class IdeologicalProfile:
    """Value patterns and ideological alignments extracted from messages"""
    individualism_collectivism: float = 0.5     # 0=collectivist, 1=individualist
    authority_orientation: str = ""              # authoritarian / libertarian / neutral
    key_values: list[str] = field(default_factory=list)
    recurring_themes: list[str] = field(default_factory=list)
    political_signals: list[str] = field(default_factory=list)

@dataclass
class CommunicationStyle:
    humor_type: str = ""            # absurd, dark, pun, sarcastic, naive
    emoji_personality: str = ""     # ironic, warm, minimal, expressive
    aggression_level: float = 0.0   # 0=passive/gentle, 1=aggressive
    formality_level: float = 0.0    # 0=casual, 1=formal
    top_emojis: list[str] = field(default_factory=list)
    top_words: list[str] = field(default_factory=list)
    avg_response_time_min: Optional[float] = None

@dataclass
class UserProfile:
    user_id: str
    display_name: str               # Alias name
    activity: ActivityStats = field(default_factory=ActivityStats)
    ocean: OceanScores = field(default_factory=OceanScores)
    social_role: SocialRole = field(default_factory=SocialRole)
    ideology: IdeologicalProfile = field(default_factory=IdeologicalProfile)
    communication: CommunicationStyle = field(default_factory=CommunicationStyle)
    llm_narrative: str = ""         # Free-text qualitative character description by LLM
    silent_observer: bool = False   # Flag for group members who lurk without writing
