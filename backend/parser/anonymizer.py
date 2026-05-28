"""Anonymization and privacy layer.
Maps real names to consistent aliases. Real names never leave the local environment.
Example: "John Doe" → "User_07"
The mapping is saved securely per session and decoded only on the frontend."""
import hashlib

class Anonymizer:
    def __init__(self, seed: str = ""):
        self._mapping: dict[str, str] = {}   # real name → alias
        self._reverse: dict[str, str] = {}   # alias → real name
        self._counter = 0
        self._seed = seed

    def anonymize_name(self, real_name: str) -> str:
        """Replaces real name with an alias. The same name always gets the same alias."""
        if real_name not in self._mapping:
            self._counter += 1
            alias = f"User_{self._counter:02d}"
            self._mapping[real_name] = alias
            self._reverse[alias] = real_name
        return self._mapping[real_name]

    def restore_name(self, alias: str) -> str:
        """Restores alias back to real name (local usage only)."""
        return self._reverse.get(alias, alias)

    def anonymize_messages(self, messages: list) -> list:
        """Anonymizes sender names in the entire message list."""
        for msg in messages:
            msg.sender_id = self.anonymize_name(msg.sender_raw)
        return messages

    def export_mapping(self) -> dict:
        """Returns the name mapping table for local storage."""
        return self._mapping
