import os
import json
import asyncio
import google.generativeai as genai
from typing import Dict, Any

class LLMAnalyzer:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is missing.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

        # Fallback OCEAN — parse başarısız olursa döner
        self._fallback_ocean = {
            "openness": 50, "conscientiousness": 50, "extraversion": 50,
            "agreeableness": 50, "neuroticism": 50
        }

    async def _call_gemini(self, prompt: str, retries: int = 3) -> str:
        """
        Gemini'yi async çağırır.
        Rate limit / ağ hatasında exponential backoff ile 3 kez dener.
        """
        for attempt in range(retries):
            try:
                response = await self.model.generate_content_async(prompt)
                return response.text
            except Exception as e:
                wait = 2 ** attempt
                print(f"Gemini call failed (attempt {attempt+1}/{retries}): {e}. Retrying in {wait}s...")
                await asyncio.sleep(wait)
        return ""

    def _clean_json_response(self, raw_text: str) -> str:
        """
        Markdown kod bloklarını temizler.
        ```json ... ``` veya ``` ... ``` formatlarını handle eder.
        """
        clean = raw_text.strip()
        if clean.startswith("```"):
            lines = clean.split("\n")
            lines = lines[1:] if lines[0].startswith("```") else lines
            lines = lines[:-1] if lines and lines[-1].strip() == "```" else lines
            clean = "\n".join(lines).strip()
        return clean

    async def analyze_user_character(self, prompt: str) -> Dict[str, Any]:
        """Karakter analizi prompt'unu çalıştırır, JSON parse eder."""
        raw = await self._call_gemini(prompt)
        if not raw:
            return self._error_response("LLM'den yanıt alınamadı.")

        cleaned = self._clean_json_response(raw)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            print(f"JSON parse hatası: {e}\nHam çıktı: {raw[:300]}")
            return self._error_response("JSON parse hatası.", raw_text=raw)

    async def analyze_silent_user(self, prompt: str) -> Dict[str, Any]:
        """Sessiz kullanıcı analizi prompt'unu çalıştırır."""
        raw = await self._call_gemini(prompt)
        if not raw:
            return self._error_response("Sessiz kullanıcı için yanıt alınamadı.")
        cleaned = self._clean_json_response(raw)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # Sessiz kullanıcı için serbest metin de kabul edilebilir
            return {"narrative": raw.strip(), "error": False}

    async def analyze_group_dynamics(self, prompt: str) -> str:
        """Grup dinamiği analizini serbest metin olarak döndürür."""
        raw = await self._call_gemini(prompt)
        return raw.strip() if raw else "Grup dinamiği analizi yapılamadı."

    def _error_response(self, reason: str, raw_text: str = "") -> Dict[str, Any]:
        return {
            "ocean_scores": self._fallback_ocean,
            "social_role": {"primary_role": "belirsiz", "secondary_roles": []},
            "communication_style": {},
            "ideology": {},
            "summary_tr": reason,
            "raw_text": raw_text[:500] if raw_text else "",
            "error": True
        }
