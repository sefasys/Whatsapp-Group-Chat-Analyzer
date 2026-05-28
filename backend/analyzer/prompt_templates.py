"""LLM prompt şablonları. Tüm sistem promptları ve build fonksiyonları burada."""

# ─────────────────────────────────────────────
# SİSTEM PROMPTLARI
# ─────────────────────────────────────────────

SYSTEM_PROMPT_CHARACTER = """Sen deneyimli bir sosyal psikolog ve davranış analistisin.
Sana anonim bir WhatsApp kullanıcısının mesaj geçmişi ve önceden hesaplanmış metin metrikleri verilecek.

Görevlerin:
- Big Five (OCEAN) kişilik skorlarını 0-100 arasında çıkar
- Gruptaki sosyal rol arketipini tespit et
- İletişim tarzını detaylandır
- Mesajlardan gizli değer, öncelik ve ideolojik eğilimleri çıkar

Kesin kurallar:
- Astroloji, burç veya sahte bilim referansı yapma
- Her kişilik çıkarımını somut mesaj kanıtlarıyla destekle
- Emin olmadığın konularda açıkça belirt
- Yanıtını YALNIZCA aşağıdaki JSON şemasıyla döndür, başka hiçbir şey yazma

Beklenen JSON şeması:
{
  "ocean_scores": {
    "openness": <0-100>,
    "conscientiousness": <0-100>,
    "extraversion": <0-100>,
    "agreeableness": <0-100>,
    "neuroticism": <0-100>,
    "confidence": <0.0-1.0>
  },
  "social_role": {
    "primary_role": "<lider|arabulucu|eğlendirici|bilgi_kaynağı|gözlemci|provokatör|takipçi>",
    "secondary_roles": ["..."],
    "influence_score": <0.0-1.0>,
    "evidence": "<bu rolü destekleyen mesaj örüntüsü>"
  },
  "communication_style": {
    "humor_type": "<absürd|kara|kelime_oyunu|sarkastik|naif|yok>",
    "emoji_personality": "<ironic|samimi|minimal|ekspresif>",
    "aggression_level": <0.0-1.0>,
    "formality_level": <0.0-1.0>,
    "dominant_tone": "<samimi|analitik|duygusal|nötr|mizahi>"
  },
  "ideology": {
    "individualism_collectivism": <0.0-1.0>,
    "authority_orientation": "<otoriter|özgürlükçü|nötr>",
    "key_values": ["<değer1>", "<değer2>"],
    "recurring_themes": ["<tema1>", "<tema2>"],
    "notes": "<ideolojik çıkarım için kanıt veya belirsizlik notu>"
  },
  "summary_tr": "<200-300 kelime Türkçe karakter yorumu, akıcı paragraf>"
}"""


SYSTEM_PROMPT_SILENT = """Sen grup dinamiği ve örgütsel sosyoloji uzmanısın.
Sana bir WhatsApp grubunun genel konuşma örüntüleri ve gruba katılıp hiç mesaj atmayan bir üyenin metadata'sı verilecek.
Bu üyenin sessizliğini sosyolojik ve psikolojik açıdan yorumla.

Yanıtını YALNIZCA şu JSON şemasıyla döndür:
{
  "silence_interpretation": "<neden sessiz kalıyor olabilir — sosyal anksiyete, gözlemci kişilik, gruba ilgisizlik, pasif tüketim vb.>",
  "estimated_engagement_level": "<yüksek_okuyucu|düşük_okuyucu|muhtemelen_çıkmış>",
  "social_archetype": "<hayalet_üye|pasif_gözlemci|sessiz_otorite|unutulmuş_üye>",
  "reintegration_likelihood": <0.0-1.0>,
  "summary_tr": "<100-150 kelime Türkçe yorum>"
}"""


SYSTEM_PROMPT_GROUP = """Sen endüstriyel-örgütsel bir sosyologsun.
Tüm kullanıcıların analiz profillerini ve grup istatistiklerini inceleyerek:
- Güç asimetrileri ve hiyerarşiyi
- Yapısal alt grupları / klanları
- Grup sağlık göstergelerini
- Genel dinamik özeti

açıkla. Yanıtın akıcı Türkçe paragraflar şeklinde olsun, JSON değil."""


# ─────────────────────────────────────────────
# BUILD FONKSİYONLARI
# ─────────────────────────────────────────────

def build_character_prompt(
    user_id: str,
    stats: dict,
    sample_messages: list[str],
    nlp: dict
) -> str:
    """
    Aktif kullanıcı için tam LLM prompt'u oluşturur.
    İstatistiksel veri + mesaj örnekleri + NLP sonuçlarını birleştirir.
    """
    # İstatistik bloğu
    stats_block = f"""
=== KULLANICI METRİKLERİ ===
Kullanıcı ID     : {user_id}
Toplam mesaj     : {stats.get('total_messages', 0)}
Günlük ortalama  : {stats.get('messages_per_day', 0):.1f} mesaj/gün
Ortalama uzunluk : {stats.get('avg_words_per_message', 0):.1f} kelime/mesaj
En aktif saat    : {stats.get('most_active_hour', '?')}:00
Medya paylaşımı  : {stats.get('media_count', 0)}
Link paylaşımı   : {stats.get('link_count', 0)}
Silinen mesaj    : {stats.get('deleted_count', 0)}
En çok emoji     : {', '.join(stats.get('top_emojis', [])) or 'yok'}
Sessizlik dönemi : {len(stats.get('silence_periods', []))} uzun kesinti"""

    # NLP bloğu
    sentiment_label = nlp.get('dominant_sentiment', 'belirsiz')
    sentiment_score = nlp.get('sentiment_score', 0.0)
    nlp_block = f"""
=== NLP ANALİZİ ===
Baskın duygu tonu: {sentiment_label} (skor: {sentiment_score:.2f})
Tespit edilen konular: {', '.join(nlp.get('topics', [])) or 'yok'}
Agresif mesaj oranı: {nlp.get('aggression_ratio', 0.0):.1%}"""

    # Mesaj örnekleri bloğu — maksimum 60 örnek, boş olmayanlar
    clean_samples = [m.strip() for m in sample_messages if m.strip()][:60]
    samples_block = "\n".join(f"  • {m}" for m in clean_samples)

    return f"""{SYSTEM_PROMPT_CHARACTER}

{stats_block}
{nlp_block}

=== ÖRNEK MESAJLAR (kronolojik) ===
{samples_block}

Yukarıdaki verilere dayanarak bu kullanıcının psikolojik ve sosyolojik profilini çıkar.
Yanıtını YALNIZCA belirtilen JSON formatında döndür."""


def build_silent_user_prompt(user_id: str, group_context: str) -> str:
    """
    Hiç mesaj atmayan kullanıcı için analiz prompt'u oluşturur.
    group_context: grubun genel konu/ton özetini içeren metin.
    """
    return f"""{SYSTEM_PROMPT_SILENT}

=== KULLANICI BİLGİSİ ===
Kullanıcı ID : {user_id}
Durum        : Grupta kayıtlı, hiç mesaj atmamış

=== GRUBUN GENEL BAĞLAMI ===
{group_context}

Bu kullanıcının sessizliğini yorumla. Yanıtını YALNIZCA belirtilen JSON formatında döndür."""


def build_group_dynamics_prompt(profiles: list[dict], group_stats: dict) -> str:
    """
    Tüm kullanıcı profillerini ve grup istatistiklerini birleştirerek
    grup dinamiği analizi için prompt oluşturur.
    """
    # Her kullanıcı için özet satır
    user_lines = []
    for p in profiles:
        uid = p.get("user_id", "?")
        role = p.get("social_role", {}).get("primary_role", "belirsiz")
        ocean = p.get("ocean_scores", {})
        ext = ocean.get("extraversion", 50)
        agr = ocean.get("agreeableness", 50)
        neu = ocean.get("neuroticism", 50)
        inf = p.get("social_role", {}).get("influence_score", 0)
        user_lines.append(
            f"  {uid}: rol={role}, etki={inf:.2f}, "
            f"dışadönüklük={ext}, uyumluluk={agr}, nevrotizm={neu}"
        )

    users_block = "\n".join(user_lines)

    stats_block = f"""
Toplam mesaj       : {group_stats.get('total_messages', 0)}
Aktif kullanıcı    : {group_stats.get('active_user_count', 0)}
Sessiz kullanıcı   : {group_stats.get('silent_user_count', 0)}
Analiz dönemi      : {group_stats.get('date_range', 'belirsiz')}
En yoğun gün       : {group_stats.get('most_active_day', 'belirsiz')}"""

    return f"""{SYSTEM_PROMPT_GROUP}

=== KULLANICI PROFİLLERİ ===
{users_block}

=== GRUP İSTATİSTİKLERİ ===
{stats_block}

Bu grubun sosyal yapısını, güç dinamiklerini ve alt gruplarını analiz et.
Akıcı Türkçe paragraflarla yaz."""
