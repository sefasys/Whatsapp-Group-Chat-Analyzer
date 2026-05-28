from transformers import pipeline

class NLPAnalyzer:
    def __init__(self):
        self.sentiment_pipeline = None

    def _load_model(self):
        if self.sentiment_pipeline is None:
            print("Loading sentiment model (savasy/bert-base-turkish-sentiment-cased)...")
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis", 
                model="savasy/bert-base-turkish-sentiment-cased",
                truncation=True,
                max_length=512
            )

    def _detect_language(self, text: str) -> str:
        """Basit heuristik: Türkçe'ye özgü karakterler."""
        turkish_chars = set("çğışöüÇĞİŞÖÜ")
        ratio = sum(1 for c in text if c in turkish_chars) / max(len(text), 1)
        return "tr" if ratio > 0.02 else "en"

    def analyze_sentiment(self, text: str) -> dict:
        """Analyzes sentiment if text is Turkish."""
        if not text.strip():
            return {"label": "neutral", "score": 0.0}
            
        lang = self._detect_language(text)
        if lang == "en":
            # Skip or use neutral for English in this simple version
            return {"label": "neutral", "score": 0.0, "lang": "en"}
            
        self._load_model()
        
        try:
            result = self.sentiment_pipeline(text)[0]
            return {"label": result['label'], "score": result['score'], "lang": "tr"}
        except Exception as e:
            print(f"Sentiment analysis failed: {e}")
            return {"label": "error", "score": 0.0, "lang": "unknown"}

    def batch_sentiment(self, messages: list[str]) -> list[dict]:
        """Batch processing for faster inference."""
        self._load_model()
        valid_msgs = [t for t in messages if t.strip() and self._detect_language(t) == "tr"]
        if not valid_msgs:
            return [{"label": "neutral", "score": 0.0} for _ in messages]
            
        try:
            results = self.sentiment_pipeline(
                valid_msgs,
                truncation=True,
                batch_size=32
            )
            
            # Map back to original list keeping in mind English ones were skipped
            # For simplicity in this demo, returning list of same size is better
            final_results = []
            idx = 0
            for t in messages:
                if t.strip() and self._detect_language(t) == "tr":
                    r = results[idx]
                    final_results.append({"label": r["label"], "score": r["score"], "lang": "tr"})
                    idx += 1
                else:
                    final_results.append({"label": "neutral", "score": 0.0, "lang": "en"})
            return final_results
        except Exception as e:
            print(f"Batch sentiment failed: {e}")
            return [{"label": "error", "score": 0.0} for _ in messages]

    def detect_topics(self, messages: list[str]) -> list[str]:
        """Placeholder for topic modeling."""
        return []

    def detect_aggression(self, messages: list[str]) -> dict:
        """Placeholder for toxicity/aggression detection."""
        return {}

    def extract_keywords(self, text: str) -> list[str]:
        """Placeholder for keyword extraction."""
        return []

def run_dummy_test():
    analyzer = NLPAnalyzer()
    texts = [
        "Bugün harika bir gün, çok mutluyum!",
        "Bu proje beni çok yordu, her şey berbat gidiyor.",
        "Hello everyone, how are you today?"
    ]
    
    results = analyzer.batch_sentiment(texts)
    for text, res in zip(texts, results):
        print(f"Text: '{text}' -> Sentiment: {res['label']} ({res['score']:.4f}) [Lang: {res.get('lang')}]")

if __name__ == "__main__":
    run_dummy_test()
