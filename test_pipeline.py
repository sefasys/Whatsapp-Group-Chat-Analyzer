import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from parser.chat_parser import parse_file
from parser.anonymizer import Anonymizer
from parser.preprocessor import filter_noise, group_by_user, build_llm_chunks
from analyzer.stats_analyzer import StatsAnalyzer
from analyzer.network_analyzer import NetworkAnalyzer
from analyzer.nlp_analyzer import NLPAnalyzer

def run_test():
    file_path = "data/raw/example_group_chat_exports/WhatsApp Chat - Medikal/_chat.txt"
    print(f"Parsing {file_path}...")
    messages = parse_file(file_path)
    
    anonymizer = Anonymizer()
    messages = anonymizer.anonymize_messages(messages)
    clean_messages = filter_noise(messages)
    
    print("\n--- PHASE 2: ANALYZERS ---")
    
    # 1. Stats Analyzer
    print("\n1. Stats Analyzer Results:")
    stats_analyzer = StatsAnalyzer(clean_messages)
    user_stats = stats_analyzer.compute_user_stats()
    
    # Print stats for User_03 (or any first available user)
    if user_stats:
        sample_user = list(user_stats.keys())[0]
        print(f"Stats for {sample_user}:")
        for k, v in user_stats[sample_user].items():
            print(f"  {k}: {v}")
            
    reply_network = stats_analyzer.compute_reply_network()
    silence_periods = stats_analyzer.compute_silence_periods()
    print(f"Computed reply network edges for {len(reply_network)} users.")
    
    # 2. Network Analyzer
    print("\n2. Network Analyzer Results:")
    network_analyzer = NetworkAnalyzer(reply_network)
    centrality_scores = network_analyzer.compute_centrality_scores()
    if centrality_scores:
        sample_user_net = list(centrality_scores.keys())[0]
        print(f"Centrality for {sample_user_net}:")
        for k, v in centrality_scores[sample_user_net].items():
            print(f"  {k}: {v:.4f}")

if __name__ == "__main__":
    run_test()
