#!/bin/bash

# 1. Create Complete Directory Structure
mkdir -p /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/api
mkdir -p /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/parser
mkdir -p /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/analyzer
mkdir -p /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/models
mkdir -p /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/utils
mkdir -p /home/sefasys/Desktop/whatsapp_group_chat_analyzer/data/raw
mkdir -p /home/sefasys/Desktop/whatsapp_group_chat_analyzer/data/processed
mkdir -p /home/sefasys/Desktop/whatsapp_group_chat_analyzer/docs

mkdir -p /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/components/dashboard
mkdir -p /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/components/profile
mkdir -p /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/components/charts
mkdir -p /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/components/upload
mkdir -p /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/pages
mkdir -p /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/hooks
mkdir -p /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/store
mkdir -p /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/utils
mkdir -p /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/types

echo "✅ Directories successfully created."

# ── BACKEND ──────────────────────────────────────────────

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/__init__.py << 'EOF'
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/main.py << 'EOF'
"""Main entry point. Starts the FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(title="WhatsApp Chat Analyzer", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/api/__init__.py << 'EOF'
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/api/routes.py << 'EOF'
"""API endpoint definitions.
POST /upload       → Upload and parse the chat file
POST /analyze      → Start the analysis process
GET  /report/{id}  → Fetch the analysis report
GET  /users/{id}   → Fetch group users list
"""
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/upload")
async def upload_chat(file: UploadFile = File(...)):
    # 1. Read file (.txt or .zip)
    # 2. Call parser.chat_parser.parse()
    # 3. Return normalized data
    pass

@router.post("/analyze/{session_id}")
async def analyze_chat(session_id: str):
    # 1. Load parsed data
    # 2. Call analyzer.pipeline.run()
    # 3. Trigger async analysis job
    pass

@router.get("/report/{session_id}")
async def get_report(session_id: str):
    # Return completed analysis report
    pass

@router.get("/users/{session_id}")
async def get_users(session_id: str):
    # Return list of all users in the group
    pass

@router.get("/user/{session_id}/{user_id}")
async def get_user_profile(session_id: str, user_id: str):
    # Return single user profile + psychological analysis
    pass
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/parser/__init__.py << 'EOF'
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/parser/chat_parser.py << 'EOF'
"""Parses WhatsApp .txt export files.
Examples of WhatsApp formats (varies by region):
  TR:  [27.05.2025, 14:32:11] Ahmet: merhaba
  EN:  [5/27/25, 2:32:11 PM] Ahmet: hello
  Alt: 27.05.2025, 14:32 - Ahmet: merhaba
Output: List[Message]
"""
import re
from datetime import datetime
from typing import Optional
from models.message import Message, MessageType

# Supported format regex patterns
PATTERNS = [
    r"\[(\d{1,2}[./]\d{1,2}[./]\d{2,4}),?\s(\d{1,2}:\d{2}(?::\d{2})?(?:\s?[AP]M)?)\]\s(.+?):\s(.*)",
    r"(\d{1,2}[./]\d{1,2}[./]\d{2,4}),?\s(\d{1,2}:\d{2}(?::\d{2})?(?:\s?[AP]M)?)\s-\s(.+?):\s(.*)",
]

MEDIA_TOKENS = ["<Media omitted>", "image omitted", "video omitted", "audio omitted", "document omitted", "GIF omitted"]
SYSTEM_TOKENS = ["joined using", "added", "removed", "left", "changed the subject", "changed this group"]

def parse_file(filepath: str) -> list[Message]:
    """Reads the file and returns a list of Message objects."""
    pass

def parse_text(raw_text: str) -> list[Message]:
    """Parses raw string data. Useful for testing."""
    pass

def _detect_format(sample_lines: list[str]) -> Optional[re.Pattern]:
    """Detects which regex pattern matches the chat format."""
    pass

def _classify_message(content: str) -> MessageType:
    """Classifies message type: text, media, link, system, reaction."""
    pass

def _extract_links(content: str) -> list[str]:
    """Extracts URLs from message content."""
    pass

def _extract_emojis(content: str) -> list[str]:
    """Extracts emojis from message content."""
    pass
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/parser/anonymizer.py << 'EOF'
"""Anonymization and privacy layer.
Maps real names to consistent aliases. Real names never leave the local environment.
Example: "John Doe" → "User_07"
The mapping is saved securely per session and decoded only on the frontend."""
from typing import dict
import hashlib

class Anonymizer:
    def __init__(self, seed: str = ""):
        self._mapping: dict[str, str] = {}   # real name → alias
        self._reverse: dict[str, str] = {}   # alias → real name
        self._counter = 0
        self._seed = seed

    def anonymize_name(self, real_name: str) -> str:
        """Replaces real name with an alias. The same name always gets the same alias."""
        pass

    def restore_name(self, alias: str) -> str:
        """Restores alias back to real name (local usage only)."""
        pass

    def anonymize_messages(self, messages: list) -> list:
        """Anonymizes sender names in the entire message list."""
        pass

    def export_mapping(self) -> dict:
        """Returns the name mapping table for local storage."""
        pass
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/parser/preprocessor.py << 'EOF'
"""Prepares raw message list for deep analysis.
Operations:
- Filter or label media / system messages
- Filter out extremely short messages (< 2 words)
- Group messages by sender
- Create time buckets (daily, weekly, monthly)
- Generate chunks for LLM context processing (sliding window)
"""
from models.message import Message
from models.session import AnalysisSession

def filter_noise(messages: list[Message]) -> list[Message]:
    """Cleans system messages, media placeholders, and single-character reactions."""
    pass

def group_by_user(messages: list[Message]) -> dict[str, list[Message]]:
    """Groups messages by sender ID."""
    pass

def group_by_timewindow(messages: list[Message], window_days: int = 7) -> list[list[Message]]:
    """Splits messages into N-day intervals."""
    pass

def build_llm_chunks(
    messages: list[Message],
    chunk_size: int = 400,
    overlap: int = 50) -> list[str]:
    """
    Creates text chunks for LLM using a sliding window.
    Each chunk contains the last `overlap` messages of the previous chunk for context continuity.
    Format: "User_01 [14:32]: message content"
    """
    pass

def build_user_summary_prompt(user_id: str, messages: list[Message], stats: dict) -> str:
    """
    Constructs the character analysis prompt for a single user.
    Combines calculated statistical metrics with sample messages.
    """
    pass
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/models/__init__.py << 'EOF'
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/models/message.py << 'EOF'
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
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/models/user_profile.py << 'EOF'
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
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/models/session.py << 'EOF'
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
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/analyzer/__init__.py << 'EOF'
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/analyzer/pipeline.py << 'EOF'
"""Analysis pipeline orchestrator.
Executes all profiling modules sequentially and synthesizes results.
Pipeline Steps:
  1. stats_analyzer   → Computational metrics (No LLM required)
  2. nlp_analyzer     → Sentiment, local intent classification
  3. network_analyzer → NetworkX social graph metrics
  4. llm_analyzer     → Deep psychological narrative, OCEAN, Ideology (Claude/Gemini APIs)
  5. report_builder   → Compile intermediate outputs into final JSON schema
"""
from models.session import AnalysisSession
from models.message import Message

async def run(session: AnalysisSession, messages: list[Message]) -> dict:
    """Core orchestrator pipeline. Runs all components sequentially."""
    pass

async def _run_stats(messages: list[Message], user_ids: list[str]) -> dict:
    pass

async def _run_nlp(messages: list[Message]) -> dict:
    pass

async def _run_network(messages: list[Message]) -> dict:
    pass

async def _run_llm(messages: list[Message], stats: dict, nlp: dict) -> dict:
    pass

async def _build_report(session_id: str, stats: dict, nlp: dict, network: dict, llm: dict) -> dict:
    pass
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/analyzer/stats_analyzer.py << 'EOF'
"""Statistical and mathematical text analysis. Runs entirely locally without LLM overhead.
Features:
- Per User: Message velocity, word counts, emoji distributions, active hours/days, media density
- Group-wide: Daily volume trends, reply matrix maps, response latency tracking
"""
from collections import Counter, defaultdict
from models.message import Message

def compute_user_stats(user_id: str, messages: list[Message]) -> dict:
    """Computes all quantitative metrics for a single user."""
    pass

def compute_group_stats(messages: list[Message]) -> dict:
    """Computes aggregate analytics for the entire chat room."""
    pass

def compute_activity_heatmap(messages: list[Message]) -> dict:
    """Generates Day x Hour activity distribution data."""
    pass

def compute_reply_network(messages: list[Message]) -> dict:
    """Calculates reply patterns (who responds to whom) — input for social network analytics."""
    pass

def compute_silence_periods(user_id: str, messages: list[Message], all_messages: list[Message]) -> list[dict]:
    """Identifies intervals where a user remains quiet during high group activity."""
    pass

def compute_emoji_profile(messages: list[Message]) -> dict:
    """Extracts emoji metadata signatures pointing to communication habits."""
    pass
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/analyzer/nlp_analyzer.py << 'EOF'
"""Local natural language processing layer. Requires no internet connectivity.
Uses HuggingFace Transformers or algorithmic rulesets.
Recommended Turkish target models:
- Sentiment: savasy/bert-base-turkish-sentiment-cased
- NER (Named Entity Recognition): savasy/bert-base-turkish-ner-cased
- Zero-shot classification: joeddav/xlm-roberta-large-xnli
"""

def analyze_sentiment(text: str) -> dict:
    """
    Evaluates emotional polarity: positive / negative / neutral.
    Returns: {"label": "positive", "score": 0.87}
    """
    pass

def batch_sentiment(messages: list[str]) -> list[dict]:
    """Processes sentiment mapping on broad message arrays."""
    pass

def detect_topics(messages: list[str], n_topics: int = 5) -> list[dict]:
    """
    Extracts core conversational tracks using LDA or zero-shot classifiers.
    """
    pass

def detect_aggression(text: str) -> dict:
    """
    Tracks hostile, abusive, or highly toxic language signals.
    Returns: {"is_aggressive": bool, "score": float, "signals": list[str]}
    """
    pass

def detect_humor_type(messages: list[str]) -> str:
    """Deduces active humor styles from syntactic structures."""
    pass

def extract_keywords(messages: list[str], top_n: int = 20) -> list[tuple]:
    """Identifies contextual keywords using TF-IDF ranking."""
    pass
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/analyzer/network_analyzer.py << 'EOF'
"""Social network visualization and analysis. Powered by NetworkX.
Graph Model:
- Nodes: Group Members
- Edges: Directed reply links (A → B implies User A replied to User B's message)
- Weight: Absolute volume of interactions
Metrics computed:
- Degree Centrality (Absolute interactivity footprint)
- Betweenness Centrality (Bridge role tracking — structural mediators)
- Clustering Coefficient (Sub-clique / inner group cluster detection)
- PageRank (Imputed social influence weight inside the system)
"""
import networkx as nx
from models.message import Message

def build_interaction_graph(messages: list[Message]) -> nx.DiGraph:
    """Generates a directed network graph from sequential reply chains."""
    pass

def compute_centrality_scores(graph: nx.DiGraph) -> dict[str, dict]:
    """Computes comprehensive network topology centralities."""
    pass

def detect_subgroups(graph: nx.DiGraph) -> list[list[str]]:
    """Applies community detection to find hidden sub-cliques within the group."""
    pass

def compute_influence_score(user_id: str, graph: nx.DiGraph) -> float:
    """Calculates normalized contextual hierarchy ranking (0-1)."""
    pass

def export_graph_json(graph: nx.DiGraph) -> dict:
    """Formats structural data into a JSON tree for frontend visualization graph engines."""
    pass
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/analyzer/llm_analyzer.py << 'EOF'
"""LLM-driven qualitative analysis.
Connects to Anthropic Claude or Google Gemini (configurable).
Executed Profiles:
- Big Five (OCEAN) score calculation
- Qualitative role archetype synthesis
- Ideological value mappings
- Structural style commentaries
- Explanatory deduction for silent members
"""
import os
from models.message import Message

# ─── Provider Configuration ────────────────────────────────────────
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")   # "claude" | "gemini" | "groq"
CLAUDE_MODEL = "claude-haiku-4-5-20251001"
GEMINI_MODEL = "gemini-1.5-flash"

async def analyze_user_character(
    user_id: str,
    messages: list[Message],
    stats: dict,
    nlp_results: dict) -> dict:
    """
    Profiles an active individual's traits. Feeds metrics + context samples to the LLM.
    Returns: {ocean, social_role, ideology, communication_style, narrative}
    """
    pass

async def analyze_silent_user(
    user_id: str,
    group_messages: list[Message],
    join_date: str) -> dict:
    """
    Evaluates completely silent group members.
    Deduces potential psychological or social reasons for their lurking patterns.
    """
    pass

async def analyze_group_dynamics(
    all_profiles: list[dict],
    group_stats: dict,
    network: dict) -> str:
    """Synthesizes global group traits into a unified descriptive report."""
    pass

async def _call_llm(prompt: str, system_prompt: str = "") -> str:
    """Dispatches calls to the selected infrastructure target."""
    if LLM_PROVIDER == "claude":
        return await _call_claude(prompt, system_prompt)
    elif LLM_PROVIDER == "gemini":
        return await _call_gemini(prompt, system_prompt)
    elif LLM_PROVIDER == "groq":
        return await _call_groq(prompt, system_prompt)
    raise ValueError(f"Unknown provider target: {LLM_PROVIDER}")

async def _call_claude(prompt: str, system_prompt: str) -> str:
    pass

async def _call_gemini(prompt: str, system_prompt: str) -> str:
    pass

async def _call_groq(prompt: str, system_prompt: str) -> str:
    pass
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/analyzer/prompt_templates.py << 'EOF'
"""LLM structural system prompt templates repository."""

SYSTEM_PROMPT_CHARACTER = """You are an expert Social Psychologist and Behavioral Analyst.
You will be provided with an anonymized user's WhatsApp messaging histories and pre-computed text metrics.
Your explicit objectives are:
- Map out the Big Five (OCEAN) personality scores accurately
- Detect structural social role archetypes inside the room context
- Detail underlying communication styles
- Impute latent values, priorities, or ideological traits from conversational context

Strict directives:
- Never use pseudo-scientific references (e.g., astrology, zodiac traits)
- Anchor every single personality conclusion with explicit semantic textual clues
- Produce output exclusively as a valid JSON payload matching the requested scheme"""

SYSTEM_PROMPT_SILENT = """You are an expert in group dynamics and organizational sociology.
You are given the general conversation topics of a chat room alongside metadata of a member who has never posted.
Provide a qualitative interpretation of their silence based on social patterns."""

SYSTEM_PROMPT_GROUP = """You are an industrial-organizational sociologist.
Analyze the composite profile mappings of all users to chart power asymmetries, structural subgroups, and group health indicators."""

def build_character_prompt(user_id: str, stats: dict, sample_messages: list[str], nlp: dict) -> str:
    """Compiles the analytical target prompt for an active user."""
    pass

def build_silent_user_prompt(user_id: str, group_context: str) -> str:
    """Compiles the profiling prompt for a lurking user."""
    pass

def build_group_dynamics_prompt(profiles: list[dict], group_stats: dict) -> str:
    """Compiles the aggregate global group analysis prompt."""
    pass
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/utils/__init__.py << 'EOF'
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/utils/file_handler.py << 'EOF'
"""Data storage and file parsing utilities.
Handles automated extraction of uploaded .zip containers and serialization of local sessions."""
import zipfile
import json
import uuid
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"

def extract_chat_file(uploaded_bytes: bytes, filename: str) -> str:
    """
    Processes incoming bytes, unzips archiving if needed, and streams raw text rows.
    """
    pass

def save_session(session_id: str, data: dict) -> None:
    """Serializes complete execution session state maps locally into JSON structures."""
    pass

def load_session(session_id: str) -> dict:
    """Deserializes local database states for ongoing operations."""
    pass

def generate_session_id() -> str:
    return str(uuid.uuid4())[:8]
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/utils/config.py << 'EOF'
"""Environment parsing configurations layer. Loads properties from .env records."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# LLM Keys
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Processing Parameters
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "400"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
MIN_MESSAGES_FOR_ANALYSIS = int(os.getenv("MIN_MESSAGES", "20"))
MAX_SAMPLE_MESSAGES = int(os.getenv("MAX_SAMPLE", "100"))

# Privacy Guards
ANONYMIZE_NAMES = os.getenv("ANONYMIZE_NAMES", "true").lower() == "true"
STORE_RAW_MESSAGES = os.getenv("STORE_RAW", "false").lower() == "true"
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/backend/requirements.txt << 'EOF'
fastapi==0.111.0
uvicorn[standard]==0.29.0
python-multipart==0.0.9
python-dotenv==1.0.1
pydantic==2.7.1
transformers==4.41.0
torch==2.3.0
sentence-transformers==2.7.0
scikit-learn==1.4.2
nltk==3.8.1
networkx==3.3
anthropic==0.26.0
google-generativeai==0.5.4
groq==0.8.0
emoji==2.11.1
python-dateutil==2.9.0
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/.env.example << 'EOF'
# LLM Provider Configuration: "claude" | "gemini" | "groq"
LLM_PROVIDER=gemini

# Core API Infrastructure credentials (Only fill your target provider)
ANTHROPIC_API_KEY=
GEMINI_API_KEY=
GROQ_API_KEY=

# Algorithmic Slicing Variables
CHUNK_SIZE=400
CHUNK_OVERLAP=50
MIN_MESSAGES=20
MAX_SAMPLE=100

# Local Guardrails
ANONYMIZE_NAMES=true
STORE_RAW_MESSAGES=false
EOF

echo "Backend components built cleanly."

# ── FRONTEND ─────────────────────────────────────────────────

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/package.json << 'EOF'
{
  "name": "whatsapp-analyzer-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^6.23.0",
    "recharts": "^2.12.0",
    "react-force-graph-2d": "^1.25.0",
    "axios": "^1.7.0",
    "zustand": "^4.5.2",
    "react-dropzone": "^14.2.3",
    "date-fns": "^3.6.0",
    "@radix-ui/react-progress": "^1.0.3",
    "@radix-ui/react-tabs": "^1.0.4"
  },
  "devDependencies": {
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.0",
    "typescript": "^5.4.0",
    "vite": "^5.2.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38"
  },
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  }
}
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/types/index.ts << 'EOF'
// ─── Base TypeScript Interfaces ───────────────────────────────────
export interface Message {
  id: string;
  timestamp: string;
  senderId: string;
  content: string;
  type: 'text' | 'media' | 'link' | 'system' | 'reaction' | 'deleted';
  emojis: string[];
  links: string[];
  isReply: boolean;
  replyToId?: string;
  wordCount: number;
}

export interface ActivityStats {
  totalMessages: number;
  totalWords: number;
  mediaCount: number;
  linkCount: number;
  emojiCount: number;
  avgMessageLength: number;
  messagesPerDay: number;
  mostActiveHour: number;
  mostActiveDay: string;
  firstMessageDate: string;
  lastMessageDate: string;
  silencePeriods: SilencePeriod[];
}

export interface SilencePeriod {
  start: string;
  end: string;
  durationDays: number;
  groupActivityLevel: 'low' | 'medium' | 'high';
}

export interface OceanScores {
  openness: number;
  conscientiousness: number;
  extraversion: number;
  agreeableness: number;
  neuroticism: number;
  confidence: number;
}

export interface SocialRole {
  primaryRole: string;
  secondaryRoles: string[];
  influenceScore: number;
  centralityScore: number;
}

export interface IdeologicalProfile {
  individualismCollectivism: number;
  authorityOrientation: string;
  keyValues: string[];
  recurringThemes: string[];
  politicalSignals: string[];
}

export interface CommunicationStyle {
  humorType: string;
  emojiPersonality: string;
  aggressionLevel: number;
  formalityLevel: number;
  topEmojis: string[];
  topWords: string[];
  avgResponseTimeMin?: number;
}

export interface UserProfile {
  userId: string;
  displayName: string;
  activity: ActivityStats;
  ocean: OceanScores;
  socialRole: SocialRole;
  ideology: IdeologicalProfile;
  communication: CommunicationStyle;
  llmNarrative: string;
  silentObserver: boolean;
}

export interface GroupReport {
  sessionId: string;
  dateRange: { start: string; end: string };
  totalMessages: number;
  activeUsers: UserProfile[];
  silentUsers: UserProfile[];
  groupDynamicsSummary: string;
  networkGraph: NetworkGraph;
  groupStats: GroupStats;
}

export interface NetworkGraph {
  nodes: NetworkNode[];
  edges: NetworkEdge[];
}

export interface NetworkNode {
  id: string;
  label: string;
  influenceScore: number;
  primaryRole: string;
}

export interface NetworkEdge {
  source: string;
  target: string;
  weight: number;
}

export interface GroupStats {
  dailyActivity: { date: string; count: number }[];
  hourlyHeatmap: number[][];
  topicDistribution: { topic: string; percentage: number }[];
  sentimentOverTime: { date: string; score: number }[];
}

export type AnalysisStatus = 'idle' | 'uploading' | 'parsing' | 'analyzing' | 'completed' | 'error';
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/store/analysisStore.ts << 'EOF'
/**
 * Global State Management (Zustand).
 * Tracks UI tracking matrices, asynchronous jobs progress states, and final diagnostic reports data stores.
 */
import { create } from 'zustand';
import { GroupReport, AnalysisStatus } from '../types';

interface AnalysisStore {
  sessionId: string | null;
  status: AnalysisStatus;
  progress: number;
  error: string | null;
  report: GroupReport | null;
  selectedUserId: string | null;
  setSessionId: (id: string) => void;
  setStatus: (status: AnalysisStatus) => void;
  setProgress: (pct: number) => void;
  setError: (msg: string) => void;
  setReport: (report: GroupReport) => void;
  selectUser: (userId: string | null) => void;
  reset: () => void;
}

export const useAnalysisStore = create<AnalysisStore>((set) => ({
  sessionId: null,
  status: 'idle',
  progress: 0,
  error: null,
  report: null,
  selectedUserId: null,
  setSessionId: (id) => set({ sessionId: id }),
  setStatus: (status) => set({ status }),
  setProgress: (progress) => set({ progress }),
  setError: (error) => set({ error, status: 'error' }),
  setReport: (report) => set({ report, status: 'completed' }),
  selectUser: (selectedUserId) => set({ selectedUserId }),
  reset: () => set({ sessionId: null, status: 'idle', progress: 0, error: null, report: null }),
}));
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/hooks/useAnalysis.ts << 'EOF'
/**
 * Execution pipeline hook manager.
 * Orchestrates sequencing flows: Upload → Engine Parsing → Async Processing Engine Poll
 */
import { useCallback } from 'react';
import { useAnalysisStore } from '../store/analysisStore';
import { uploadChat, startAnalysis, pollReport } from '../utils/api';

export function useAnalysis() {
  const { setSessionId, setStatus, setProgress, setError, setReport } = useAnalysisStore();

  const runAnalysis = useCallback(async (file: File) => {
    try {
      setStatus('uploading');
      const { sessionId } = await uploadChat(file);
      setSessionId(sessionId);
      setStatus('parsing');
      
      await startAnalysis(sessionId);
      setStatus('analyzing');
      
      const report = await pollReport(sessionId, (pct) => setProgress(pct));
      setReport(report);
    } catch (err: any) {
      setError(err.message ?? 'An unknown system exception occurred.');
    }
  }, [setSessionId, setStatus, setProgress, setError, setReport]);

  return { runAnalysis };
}
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/utils/api.ts << 'EOF'
/**
 * Core HTTP Client API interactions layer.
 */
import axios from 'axios';
import { GroupReport } from '../types';

const BASE = 'http://localhost:8000/api';

export async function uploadChat(file: File): Promise<{ sessionId: string }> {
  const form = new FormData();
  form.append('file', file);
  const res = await axios.post(`${BASE}/upload`, form);
  return res.data;
}

export async function startAnalysis(sessionId: string): Promise<void> {
  await axios.post(`${BASE}/analyze/${sessionId}`);
}

export async function pollReport(
  sessionId: string,
  onProgress: (pct: number) => void): Promise<GroupReport> {
  return new Promise((resolve, reject) => {
    const interval = setInterval(async () => {
      try {
        const res = await axios.get(`${BASE}/report/${sessionId}`);
        const { status, progress, report } = res.data;
        onProgress(progress);
        if (status === 'completed') {
          clearInterval(interval);
          resolve(report);
        } else if (status === 'failed') {
          clearInterval(interval);
          reject(new Error(res.data.error));
        }
      } catch (e) {
        clearInterval(interval);
        reject(e);
      }
    }, 2000);
  });
}

export async function getUserProfile(sessionId: string, userId: string) {
  const res = await axios.get(`${BASE}/user/${sessionId}/${userId}`);
  return res.data;
}
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/pages/UploadPage.tsx << 'EOF'
/**
 * Main dashboard landing root. File ingest dropping field.
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import FileDropzone from '../components/upload/FileDropzone';
import { useAnalysis } from '../hooks/useAnalysis';
import { useAnalysisStore } from '../store/analysisStore';

export default function UploadPage() {
  const { runAnalysis } = useAnalysis();
  const navigate = useNavigate();

  const handleFile = async (file: File) => {
    await runAnalysis(file);
    navigate('/dashboard');
  };

  return (
    <div>
      {/* FileDropzone component mounts here */}
    </div>
  );
}
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/pages/DashboardPage.tsx << 'EOF'
/**
 * High-level core workspace report metrics display container dashboard views.
 */
import React from 'react';
import { useAnalysisStore } from '../store/analysisStore';

export default function DashboardPage() {
  const { report } = useAnalysisStore();
  if (!report) return <div>Loading diagnostic analytics report systems...</div>;

  return (
    <div>
      {/* Structural workspace dashboard metrics presentation UI sub-components mount here */}
    </div>
  );
}
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/pages/UserProfilePage.tsx << 'EOF'
/**
 * Detailed Individual Deep-dive behavioral display components.
 */
import React from 'react';
import { useParams } from 'react-router-dom';
import { useAnalysisStore } from '../store/analysisStore';

export default function UserProfilePage() {
  const { userId } = useParams<{ userId: string }>();
  const { report } = useAnalysisStore();
  
  const user = report?.activeUsers.find(u => u.userId === userId)
            ?? report?.silentUsers.find(u => u.userId === userId);

  if (!user) return <div>Target user profile record cannot be verified.</div>;

  return (
    <div>
      {/* Individual profiling metric presentation view components layout fields */}
    </div>
  );
}
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/components/upload/FileDropzone.tsx << 'EOF'
import React from 'react';
import { useDropzone } from 'react-dropzone';

interface Props {
  onFile: (file: File) => void;
}

export default function FileDropzone({ onFile }: Props) {
  const { getRootProps, getInputProps } = useDropzone({
    accept: { 'text/plain': ['.txt'], 'application/zip': ['.zip'] },
    maxFiles: 1,
    onDrop: (accepted) => { if (accepted[0]) onFile(accepted[0]); },
  });

  return (
    <div { ...getRootProps() }>
      <input { ...getInputProps() } />
    </div>
  );
}
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/components/dashboard/GroupSummaryCard.tsx << 'EOF'
import React from 'react';
import { GroupReport } from '../../types';

interface Props { report: GroupReport; }
export default function GroupSummaryCard({ report }: Props) {
  return <div></div>;
}
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/components/dashboard/UserList.tsx << 'EOF'
import React from 'react';
import { UserProfile } from '../../types';

interface Props { users: UserProfile[]; silentUsers: UserProfile[]; }
export default function UserList({ users, silentUsers }: Props) {
  return <div></div>;
}
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/components/profile/PersonalityCard.tsx << 'EOF'
import React from 'react';
import { OceanScores, CommunicationStyle } from '../../types';

interface Props { ocean: OceanScores; communication: CommunicationStyle; }
export default function PersonalityCard({ ocean, communication }: Props) {
  return <div></div>;
}
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/components/profile/IdeologyCard.tsx << 'EOF'
import React from 'react';
import { IdeologicalProfile } from '../../types';

interface Props { ideology: IdeologicalProfile; }
export default function IdeologyCard({ ideology }: Props) {
  return <div></div>;
}
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/components/charts/OceanRadar.tsx << 'EOF'
import React from 'react';
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer } from 'recharts';
import { OceanScores } from '../../types';

interface Props { scores: OceanScores; }
export default function OceanRadar({ scores }: Props) {
  const data = [
    { label: 'Openness', value: scores.openness * 100 },
    { label: 'Conscientiousness', value: scores.conscientiousness * 100 },
    { label: 'Extraversion', value: scores.extraversion * 100 },
    { label: 'Agreeableness', value: scores.agreeableness * 100 },
    { label: 'Neuroticism', value: scores.neuroticism * 100 },
  ];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <RadarChart data={data}>
        <PolarGrid />
        <PolarAngleAxis dataKey="label" />
        <Radar dataKey="value" fill="#8884d8" fillOpacity={0.5} />
      </RadarChart>
    </ResponsiveContainer>
  );
}
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/components/charts/ActivityChart.tsx << 'EOF'
import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

interface Props { data: { date: string; count: number }[]; }
export default function ActivityChart({ data }: Props) {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <LineChart data={data}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="count" stroke="#8884d8" dot={false} />
      </LineChart>
    </ResponsiveContainer>
  );
}
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/components/charts/ActivityHeatmap.tsx << 'EOF'
import React from 'react';

interface Props { heatmap: number[][] }
export default function ActivityHeatmap({ heatmap }: Props) {
  return <div></div>;
}
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/components/charts/NetworkGraph.tsx << 'EOF'
import React from 'react';
import { NetworkGraph as NetworkGraphType } from '../../types';

interface Props { graph: NetworkGraphType; }
export default function NetworkGraph({ graph }: Props) {
  return <div></div>;
}
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/App.tsx << 'EOF'
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import UploadPage from './pages/UploadPage';
import DashboardPage from './pages/DashboardPage';
import UserProfilePage from './pages/UserProfilePage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={ <UploadPage /> } />
        <Route path="/dashboard" element={ <DashboardPage /> } />
        <Route path="/user/:userId" element={ <UserProfilePage /> } />
      </Routes>
    </BrowserRouter>
  );
}
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/main.tsx << 'EOF'
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOF

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/frontend/src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --color-primary: #6c63ff;
  --color-bg: #0f0f13;
  --color-surface: #1a1a24;
  --color-text: #e2e2f0;
  --color-muted: #8888aa;
}
EOF

echo "✅ Frontend modules built cleanly."

# ── DOCS & ROOT ───────────────────────────────────────────

cat > /home/sefasys/Desktop/whatsapp_group_chat_analyzer/README.md << 'EOF'
# WhatsApp Chat Analyzer
An analytical research platform designed to capture quantitative and deep socio-psychological traits inside group messaging dumps.
EOF

echo "✅ Success! All workspace trees mapped into /home/sefasys/Desktop/whatsapp_group_chat_analyzer/"
find /home/sefasys/Desktop/whatsapp_group_chat_analyzer -type f | sort