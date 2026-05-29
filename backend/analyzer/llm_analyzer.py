import os
import json
import asyncio
from typing import Dict, Any

class BaseLLMAnalyzer:
    def __init__(self):
        self._fallback_ocean = {
            "openness": 50, "conscientiousness": 50, "extraversion": 50,
            "agreeableness": 50, "neuroticism": 50
        }

    def _clean_json_response(self, raw_text: str) -> str:
        clean = raw_text.strip()
        if clean.startswith("```"):
            lines = clean.split("\n")
            lines = lines[1:] if lines[0].startswith("```") else lines
            lines = lines[:-1] if lines and lines[-1].strip() == "```" else lines
            clean = "\n".join(lines).strip()
        return clean

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

    async def _generate_content(self, prompt: str) -> str:
        raise NotImplementedError

    async def analyze_user_character(self, prompt: str) -> Dict[str, Any]:
        raw = await self._generate_content(prompt)
        if not raw:
            return self._error_response("LLM'den yanıt alınamadı.")

        cleaned = self._clean_json_response(raw)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            print(f"JSON parse hatası: {e}\nHam çıktı: {raw[:300]}")
            return self._error_response("JSON parse hatası.", raw_text=raw)

    async def analyze_silent_user(self, prompt: str) -> Dict[str, Any]:
        raw = await self._generate_content(prompt)
        if not raw:
            return self._error_response("Sessiz kullanıcı için yanıt alınamadı.")
        cleaned = self._clean_json_response(raw)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {"narrative": raw.strip(), "error": False}

    async def analyze_group_dynamics(self, prompt: str) -> str:
        raw = await self._generate_content(prompt)
        return raw.strip() if raw else "Grup dinamiği analizi yapılamadı."


class GeminiAnalyzer(BaseLLMAnalyzer):
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        super().__init__()
        import google.generativeai as genai
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is missing.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    async def _generate_content(self, prompt: str, retries: int = 5) -> str:
        for attempt in range(retries):
            try:
                response = await self.model.generate_content_async(prompt)
                return response.text
            except Exception as e:
                error_str = str(e).lower()
                if "quota" in error_str or "429" in error_str:
                    wait = 60
                else:
                    wait = 2 ** attempt
                print(f"[Gemini] Call failed (attempt {attempt+1}/{retries}). Retrying in {wait}s...")
                await asyncio.sleep(wait)
        return ""


class ClaudeAnalyzer(BaseLLMAnalyzer):
    def __init__(self, model_name: str = "claude-3-5-sonnet-20241022"):
        super().__init__()
        from anthropic import AsyncAnthropic
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is missing.")
        self.client = AsyncAnthropic(api_key=self.api_key)
        self.model_name = model_name

    async def _generate_content(self, prompt: str, retries: int = 5) -> str:
        for attempt in range(retries):
            try:
                response = await self.client.messages.create(
                    model=self.model_name,
                    max_tokens=2048,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            except Exception as e:
                error_str = str(e).lower()
                if "rate limit" in error_str or "429" in error_str:
                    wait = 60
                else:
                    wait = 2 ** attempt
                print(f"[Claude] Call failed (attempt {attempt+1}/{retries}). Retrying in {wait}s...")
                await asyncio.sleep(wait)
        return ""


class GroqAnalyzer(BaseLLMAnalyzer):
    def __init__(self, model_name: str = "llama3-70b-8192"):
        super().__init__()
        from groq import AsyncGroq
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is missing.")
        self.client = AsyncGroq(api_key=self.api_key)
        self.model_name = model_name

    async def _generate_content(self, prompt: str, retries: int = 5) -> str:
        for attempt in range(retries):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            except Exception as e:
                error_str = str(e).lower()
                if "rate limit" in error_str or "429" in error_str:
                    wait = 60
                else:
                    wait = 2 ** attempt
                print(f"[Groq] Call failed (attempt {attempt+1}/{retries}). Retrying in {wait}s...")
                await asyncio.sleep(wait)
        return ""


def get_llm_analyzer(provider: str) -> BaseLLMAnalyzer:
    if provider == "claude":
        return ClaudeAnalyzer()
    elif provider == "groq":
        return GroqAnalyzer()
    else:
        return GeminiAnalyzer()
