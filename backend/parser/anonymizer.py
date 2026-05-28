"""Anonymization and privacy layer.
Maps real names to consistent aliases. Real names never leave the local environment.
Example: "John Doe" → "User_07"
The mapping is saved securely per session and decoded only on the frontend."""
from typing import dict
import hashlib

class Anonymizer:
    def __init__(self, seed: str = ""):
        self._mapping: dict[str, str] = {}   # real name → alias
        self._reverse: dict[str, str] = {}   # alias → real name
        self._counter = 0
        self._seed = seed

    def anonymize_name(self, real_name: str) -> str:
        """Replaces real name with an alias. The same name always gets the same alias."""
        pass

    def restore_name(self, alias: str) -> str:
        """Restores alias back to real name (local usage only)."""
        pass

    def anonymize_messages(self, messages: list) -> list:
        """Anonymizes sender names in the entire message list."""
        pass

    def export_mapping(self) -> dict:
        """Returns the name mapping table for local storage."""
        pass
