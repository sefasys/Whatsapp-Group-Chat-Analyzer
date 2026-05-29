"""
Analiz pipeline orkestratörü.
Parse'dan rapora kadar tüm adımları sırayla çalıştırır.

Sıra:
  1. stats_analyzer   → Sayısal metrikler (LLM gerektirmez)
  2. nlp_analyzer     → Sentiment, konu tespiti (lokal transformer)
  3. network_analyzer → Sosyal ağ metrikleri (NetworkX)
  4. llm_analyzer     → Karakter yorumu, OCEAN, ideoloji (Gemini)
  5. report_builder   → Tüm çıktıları birleştirir
"""
import asyncio
from collections import Counter

from models.session import AnalysisSession, SessionStatus
from models.message import Message, MessageType
from analyzer.stats_analyzer import StatsAnalyzer
from analyzer.nlp_analyzer import NLPAnalyzer
from analyzer.network_analyzer import NetworkAnalyzer
from analyzer.llm_analyzer import get_llm_analyzer
from analyzer.prompt_templates import (
    build_character_prompt,
    build_silent_user_prompt,
    build_group_dynamics_prompt,
)
from parser.preprocessor import filter_noise, group_by_user, build_llm_chunks


async def run(session: AnalysisSession, messages: list[Message], provider: str = "gemini") -> dict:
    """
    Ana pipeline. Tüm analiz adımlarını sırayla çalıştırır.
    Session nesnesi ilerleme takibi için güncellenir.
    """
    session.status = SessionStatus.ANALYZING

    # Gürültüyü temizle
    clean_messages = filter_noise(messages)

    # ── 1. İstatistik ────────────────────────────────────
    session.progress_pct = 10
    stats_result = await _run_stats(clean_messages)

    # ── 2. NLP ───────────────────────────────────────────
    session.progress_pct = 30
    nlp_result = await _run_nlp(clean_messages)

    # ── 3. Sosyal ağ ─────────────────────────────────────
    session.progress_pct = 50
    network_result = await _run_network(clean_messages, list(stats_result["user_stats"].keys()))

    # ── 4. LLM ───────────────────────────────────────────
    session.progress_pct = 60
    llm_result = await _run_llm(clean_messages, stats_result, nlp_result, provider)

    # ── 5. Rapor ─────────────────────────────────────────
    session.progress_pct = 90
    report = await _build_report(session.session_id, stats_result, nlp_result, network_result, llm_result)

    session.status = SessionStatus.COMPLETED
    session.progress_pct = 100
    return report


# ─────────────────────────────────────────────────────────
# ADIM 1 — İstatistik
# ─────────────────────────────────────────────────────────

async def _run_stats(messages: list[Message]) -> dict:
    analyzer = StatsAnalyzer(messages)
    user_stats = analyzer.compute_user_stats()
    reply_network = analyzer.compute_reply_network()
    silence_periods = analyzer.compute_silence_periods()
    daily_activity = analyzer.compute_daily_activity()
    heatmap = analyzer.compute_activity_heatmap()

    return {
        "user_stats": user_stats,
        "reply_network": reply_network,
        "silence_periods": silence_periods,
        "daily_activity": daily_activity,
        "heatmap": heatmap,
        "total_messages": len(messages),
        "active_user_count": len(user_stats),
    }


# ─────────────────────────────────────────────────────────
# ADIM 2 — NLP
# ─────────────────────────────────────────────────────────

async def _run_nlp(messages: list[Message]) -> dict:
    analyzer = NLPAnalyzer()
    user_messages = group_by_user(messages)
    nlp_per_user = {}

    for user_id, user_msgs in user_messages.items():
        texts = [m.content for m in user_msgs if m.type == MessageType.TEXT and m.content.strip()]
        if not texts:
            nlp_per_user[user_id] = {"dominant_sentiment": "nötr", "sentiment_score": 0.0, "topics": [], "aggression_ratio": 0.0}
            continue

        # Batch sentiment
        sentiments = analyzer.batch_sentiment(texts[:200])   # max 200 mesaj
        pos = sum(1 for s in sentiments if s["label"] == "positive")
        neg = sum(1 for s in sentiments if s["label"] == "negative")
        total = len(sentiments)

        dominant = "pozitif" if pos > neg else ("negatif" if neg > pos else "nötr")
        score = (pos - neg) / total if total > 0 else 0.0

        # Konu tespiti
        topics = analyzer.detect_topics(texts[:100])

        # Agresiflik oranı
        aggression_results = [analyzer.detect_aggression(t) for t in texts[:50]]
        aggression_ratio = sum(1 for r in aggression_results if r.get("is_aggressive")) / max(len(aggression_results), 1)

        nlp_per_user[user_id] = {
            "dominant_sentiment": dominant,
            "sentiment_score": score,
            "topics": [t.get("topic", "") for t in topics[:5]],
            "aggression_ratio": aggression_ratio,
        }

    return {"per_user": nlp_per_user}


# ─────────────────────────────────────────────────────────
# ADIM 3 — Sosyal ağ
# ─────────────────────────────────────────────────────────

async def _run_network(messages: list[Message], all_user_ids: list[str]) -> dict:
    # reply_network stats_analyzer'dan geliyor ama network_analyzer'a Counter gerekiyor
    stats_temp = StatsAnalyzer(messages)
    reply_network = stats_temp.compute_reply_network()

    # str → Counter dönüşümü (eğer dict geldiyse)
    counter_network = {
        sender: Counter(receivers) if not isinstance(receivers, Counter) else receivers
        for sender, receivers in reply_network.items()
    }

    analyzer = NetworkAnalyzer(counter_network)
    # İzole node'ları da ekle
    for uid in all_user_ids:
        if uid not in analyzer.graph:
            analyzer.graph.add_node(uid)

    centrality = analyzer.compute_centrality_scores()
    subgroups = analyzer.detect_subgroups()
    graph_json = analyzer.export_graph_json()

    return {
        "centrality": centrality,
        "subgroups": subgroups,
        "graph_json": graph_json,
    }


# ─────────────────────────────────────────────────────────
# ADIM 4 — LLM
# ─────────────────────────────────────────────────────────

async def _run_llm(messages: list[Message], stats: dict, nlp: dict, provider: str) -> dict:
    llm = get_llm_analyzer(provider)
    user_messages = group_by_user(messages)
    user_profiles = {}

    # Her kullanıcıyı sırayla analiz et (rate limit koruması için sıralı)
    for user_id, user_msgs in user_messages.items():
        user_stat = stats["user_stats"].get(user_id, {})
        user_nlp = nlp["per_user"].get(user_id, {})

        # Örnek mesajlar — sadece text, maksimum 80 adet
        sample_texts = [
            f"{m.sender_id} [{m.timestamp.strftime('%H:%M')}]: {m.content}"
            for m in user_msgs
            if m.type == MessageType.TEXT and m.content.strip()
        ][:80]

        # Sessizlik bilgisini stats'tan al
        user_stat["silence_periods"] = stats["silence_periods"].get(user_id, [])

        prompt = build_character_prompt(user_id, user_stat, sample_texts, user_nlp)
        result = await llm.analyze_user_character(prompt)
        result["user_id"] = user_id
        user_profiles[user_id] = result

        # Rate limit: 15 RPM (4 saniye bekleme)
        await asyncio.sleep(4)

    # Grup dinamiği analizi
    group_stats_summary = {
        "total_messages": stats["total_messages"],
        "active_user_count": stats["active_user_count"],
        "silent_user_count": 0,   # sessiz üyeler pipeline dışından beslenir
        "date_range": "tüm dönem",
        "most_active_day": _find_most_active_day(stats["daily_activity"]),
    }

    group_prompt = build_group_dynamics_prompt(
        list(user_profiles.values()), group_stats_summary
    )
    group_narrative = await llm.analyze_group_dynamics(group_prompt)

    return {
        "user_profiles": user_profiles,
        "group_narrative": group_narrative,
    }


# ─────────────────────────────────────────────────────────
# ADIM 5 — Rapor birleştirici
# ─────────────────────────────────────────────────────────

async def _build_report(
    session_id: str,
    stats: dict,
    nlp: dict,
    network: dict,
    llm: dict,
) -> dict:
    """
    Tüm modül çıktılarını frontend'in beklediği tek bir JSON'a dönüştürür.
    """
    active_users = []

    for user_id, profile in llm["user_profiles"].items():
        user_stat = stats["user_stats"].get(user_id, {})
        user_nlp = nlp["per_user"].get(user_id, {})
        centrality = network["centrality"].get(user_id, {})

        active_users.append({
            "userId": user_id,
            "displayName": user_id,
            "activity": {
                "totalMessages": user_stat.get("total_messages", 0),
                "totalWords": user_stat.get("total_words", 0),
                "mediaCount": user_stat.get("media_count", 0),
                "linkCount": user_stat.get("link_count", 0),
                "avgMessageLength": user_stat.get("avg_words_per_message", 0),
                "messagesPerDay": user_stat.get("messages_per_day", 0),
                "mostActiveHour": user_stat.get("most_active_hour"),
                "topEmojis": user_stat.get("top_emojis", []),
                "silencePeriods": stats["silence_periods"].get(user_id, []),
            },
            "ocean": profile.get("ocean_scores", {}),
            "socialRole": {
                **profile.get("social_role", {}),
                "influenceScore": centrality.get("pagerank", 0),
                "centralityScore": centrality.get("degree_centrality", 0),
            },
            "ideology": profile.get("ideology", {}),
            "communication": profile.get("communication_style", {}),
            "llmNarrative": profile.get("summary_tr", ""),
            "silentObserver": False,
            "error": profile.get("error", False),
        })

    return {
        "sessionId": session_id,
        "activeUsers": active_users,
        "silentUsers": [],   # sessiz üyeler routes.py'den beslenir
        "groupDynamicsSummary": llm["group_narrative"],
        "networkGraph": network["graph_json"],
        "groupStats": {
            "dailyActivity": stats["daily_activity"],
            "hourlyHeatmap": stats["heatmap"],
            "totalMessages": stats["total_messages"],
        },
    }


# ─────────────────────────────────────────────────────────
# YARDIMCI
# ─────────────────────────────────────────────────────────

def _find_most_active_day(daily_activity: list[dict]) -> str:
    if not daily_activity:
        return "belirsiz"
    return max(daily_activity, key=lambda x: x["count"])["date"]
