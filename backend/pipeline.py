import os
import sys
import asyncio
from dotenv import load_dotenv

sys.path.append(os.path.dirname(__file__))

from parser.chat_parser import parse_file
from parser.anonymizer import Anonymizer
from parser.preprocessor import filter_noise
from analyzer.stats_analyzer import StatsAnalyzer
from analyzer.network_analyzer import NetworkAnalyzer
from analyzer.nlp_analyzer import NLPAnalyzer
from models.prompt_templates import build_character_prompt
from analyzer.llm_analyzer import LLMAnalyzer

async def main():
    # Load env variables (GEMINI_API_KEY)
    load_dotenv()
    
    # Ensure GEMINI_API_KEY is available early to prevent failing late
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY not found in .env file.")
        return
    
    file_path = "data/raw/example_group_chat_exports/WhatsApp Chat - Medikal/_chat.txt"
    if not os.path.exists(file_path):
        print(f"Error: Could not find file {file_path}")
        return
        
    print(f"Parsing {file_path}...")
    messages = parse_file(file_path)
    
    print("Anonymizing and Filtering...")
    anonymizer = Anonymizer()
    messages = anonymizer.anonymize_messages(messages)
    clean_messages = filter_noise(messages)
    
    # Run analyzers
    print("\n--- Phase 2: Running Analyzers ---")
    stats_analyzer = StatsAnalyzer(clean_messages)
    user_stats = stats_analyzer.compute_user_stats()
    reply_network = stats_analyzer.compute_reply_network()
    
    network_analyzer = NetworkAnalyzer(reply_network, list(user_stats.keys()))
    centrality_scores = network_analyzer.compute_centrality_scores()
    
    print("\n--- Phase 3: LLM Integration ---")
    llm_analyzer = LLMAnalyzer()
    
    if not user_stats:
        print("No users found to analyze.")
        return
        
    # Pick the most active user to test
    top_user = sorted(user_stats.keys(), key=lambda u: user_stats[u].get("total_messages", 0), reverse=True)[0]
    
    print(f"Testing LLM character analysis for {top_user}...")
    
    # Get a sample of their messages
    user_msgs = [m.content for m in clean_messages if m.sender_id == top_user and m.content]
    # Take the 15 longest messages as they usually show more personality
    user_msgs.sort(key=len, reverse=True)
    sample_msgs = user_msgs[:15]
    
    prompt = build_character_prompt(
        user_id=top_user,
        stats=user_stats.get(top_user, {}),
        centrality=centrality_scores.get(top_user, {}),
        sample_messages=sample_msgs
    )
    
    print("Sending prompt to Gemini... (Please wait)")
    result = await llm_analyzer.analyze_user_character(prompt)
    
    import json
    print("\nLLM Output JSON:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
