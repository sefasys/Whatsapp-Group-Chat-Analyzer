from collections import Counter, defaultdict
from datetime import datetime, timedelta
import re
from typing import Dict, Any, List

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.message import Message, MessageType

class StatsAnalyzer:
    def __init__(self, messages: List[Message]):
        self.messages = messages
        self.text_messages = [m for m in messages if m.type == MessageType.TEXT]

    def compute_user_stats(self) -> Dict[str, Dict[str, Any]]:
        """Computes basic stats for each user."""
        user_stats = defaultdict(lambda: {
            "total_messages": 0,
            "total_words": 0,
            "hourly_counts": Counter(),
            "emojis": Counter(),
            "media_count": 0,
            "link_count": 0,
            "deleted_count": 0,
            "first_message_date": None,
            "last_message_date": None
        })

        for msg in self.messages:
            sender = msg.sender_id
            stats = user_stats[sender]
            
            stats["total_messages"] += 1
            
            if msg.type == MessageType.TEXT:
                stats["total_words"] += msg.word_count
                for emoji in msg.emojis:
                    stats["emojis"][emoji] += 1
                    
            elif msg.type == MessageType.MEDIA:
                stats["media_count"] += 1
            elif msg.type == MessageType.LINK:
                stats["link_count"] += 1
            elif msg.type == MessageType.DELETED:
                stats["deleted_count"] += 1
                
            stats["hourly_counts"][msg.timestamp.hour] += 1

            if not stats["first_message_date"] or msg.timestamp < stats["first_message_date"]:
                stats["first_message_date"] = msg.timestamp
            if not stats["last_message_date"] or msg.timestamp > stats["last_message_date"]:
                stats["last_message_date"] = msg.timestamp

        # Finalize stats
        final_stats = {}
        for user, stats in user_stats.items():
            days_active = max(1, (stats["last_message_date"] - stats["first_message_date"]).days)
            avg_words = stats["total_words"] / stats["total_messages"] if stats["total_messages"] > 0 else 0
            most_active_hour = stats["hourly_counts"].most_common(1)[0][0] if stats["hourly_counts"] else None
            top_emojis = [emoji for emoji, count in stats["emojis"].most_common(5)]
            
            final_stats[user] = {
                "total_messages": stats["total_messages"],
                "total_words": stats["total_words"],
                "messages_per_day": stats["total_messages"] / days_active,
                "most_active_hour": most_active_hour,
                "top_emojis": top_emojis,
                "avg_words_per_message": avg_words,
                "media_count": stats["media_count"],
                "link_count": stats["link_count"],
                "deleted_count": stats["deleted_count"]
            }
            
        return final_stats

    def compute_reply_network(self) -> Dict[str, Counter]:
        """
        Uses heuristic to guess replies:
        1. Explicit mention (@User)
        2. Temporal proximity (replying within 5 minutes of another user's message)
        Returns dict of sender -> Counter(receiver -> count)
        """
        reply_network = defaultdict(Counter)
        
        users = set(msg.sender_id for msg in self.messages if msg.sender_id)
        
        for i, msg in enumerate(self.messages):
            if msg.type in [MessageType.SYSTEM, MessageType.DELETED]:
                continue
                
            sender = msg.sender_id
            
            # 1. Mention check
            mentioned = False
            for user in users:
                if user != sender and user != msg.sender_raw:
                    if f"@{user}" in msg.content:
                        reply_network[sender][user] += 1
                        mentioned = True
            
            if mentioned:
                continue
                
            # 2. Temporal proximity check
            for j in range(i-1, max(-1, i-6), -1):
                prev_msg = self.messages[j]
                if prev_msg.type in [MessageType.SYSTEM, MessageType.DELETED]:
                    continue
                    
                time_diff = (msg.timestamp - prev_msg.timestamp).total_seconds()
                if time_diff <= 300: # 5 minutes
                    if prev_msg.sender_id != sender:
                        reply_network[sender][prev_msg.sender_id] += 1
                        break
                else:
                    break
                    
        return reply_network

    def compute_silence_periods(self, window_days: int = 1) -> Dict[str, List[Dict]]:
        """
        Identifies periods where the group was active but a specific user was silent.
        """
        if not self.messages:
            return {}
            
        silence_records = defaultdict(list)
        all_users = set(msg.sender_id for msg in self.messages if msg.sender_id)
        
        # Simple windowing by day
        windows = defaultdict(list)
        for msg in self.messages:
            day = msg.timestamp.date()
            windows[day].append(msg)
            
        for day, w in sorted(windows.items()):
            if len(w) > 5:
                window_users = set(msg.sender_id for msg in w if msg.sender_id)
                silent_users = all_users - window_users
                for su in silent_users:
                    silence_records[su].append({
                        "date": str(day),
                        "start": w[0].timestamp,
                        "end": w[-1].timestamp,
                        "window_msg_count": len(w)
                    })
                    
        return silence_records

    def compute_daily_activity(self) -> list[dict]:
        daily = Counter()
        for msg in self.messages:
            day = msg.timestamp.strftime("%Y-%m-%d")
            daily[day] += 1
        return [{"date": d, "count": c} for d, c in sorted(daily.items())]

    def compute_activity_heatmap(self) -> list[list[int]]:
        matrix = [[0]*24 for _ in range(7)]  # [gün][saat]
        for msg in self.messages:
            day = msg.timestamp.weekday()   # 0=Pazartesi
            hour = msg.timestamp.hour
            matrix[day][hour] += 1
        return matrix
