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
