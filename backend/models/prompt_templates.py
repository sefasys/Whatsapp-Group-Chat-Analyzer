import json
from typing import List, Dict, Any

def build_character_prompt(
    user_id: str,
    stats: Dict[str, Any],
    centrality: Dict[str, float],
    sample_messages: List[str]
) -> str:
    """
    Builds the prompt instructing the LLM to analyze a user's personality based on their
    stats, network centrality, and a sample of their messages, returning a strict JSON.
    """
    
    stats_text = (
        f"Total Messages: {stats.get('total_messages', 0)}\n"
        f"Messages Per Day: {stats.get('messages_per_day', 0.0):.2f}\n"
        f"Avg Words Per Message: {stats.get('avg_words_per_message', 0.0):.2f}\n"
        f"Most Active Hour: {stats.get('most_active_hour', 'Unknown')}:00\n"
        f"Top Emojis: {', '.join(stats.get('top_emojis', []))}\n"
    )
    
    if centrality:
        stats_text += (
            f"Degree Centrality (Involvement): {centrality.get('degree_centrality', 0.0):.4f}\n"
            f"PageRank (Influence): {centrality.get('pagerank', 0.0):.4f}\n"
        )
        
    messages_text = "\n".join([f"- {msg}" for msg in sample_messages])
    
    prompt = f"""You are an expert behavioral psychologist and data analyst.
I am providing you with the communication data of a user named "{user_id}" from a WhatsApp group chat.

--- USER STATS ---
{stats_text}

--- RECENT MESSAGE SAMPLES ---
{messages_text}

Based on this data, analyze their personality using the OCEAN (Big Five) framework.
Rate each trait from 1 to 100.
Also, provide a short, fun, and insightful character summary (in Turkish) of this person's role in the group (e.g., 'Grup lideri', 'Sessiz gözlemci', 'Kaos kaynağı').

IMPORTANT: You MUST respond ONLY with a valid JSON object. Do not include markdown formatting like ```json or any other text before or after the JSON.
The JSON must strictly follow this structure:
{{
  "ocean_scores": {{
    "openness": <int>,
    "conscientiousness": <int>,
    "extraversion": <int>,
    "agreeableness": <int>,
    "neuroticism": <int>
  }},
  "summary_tr": "<String containing the Turkish character summary>"
}}
"""
    return prompt
