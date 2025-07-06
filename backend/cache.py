"""Caching utilities for frequent and response queries with TTL."""
import time
from typing import Any, Dict, Optional

class SimpleCache:
    def __init__(self):
        self.cache: Dict[str, Any] = {}
        self.expiry: Dict[str, float] = {}

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        self.cache[key] = value
        if ttl:
            self.expiry[key] = time.time() + ttl
        elif key in self.expiry:
            del self.expiry[key]

    def get(self, key: str) -> Optional[Any]:
        if key in self.expiry and time.time() > self.expiry[key]:
            self.cache.pop(key, None)
            self.expiry.pop(key, None)
            return None
        return self.cache.get(key)

    def clear(self):
        self.cache.clear()
        self.expiry.clear()

# Singleton cache instances
frequent_query_cache = SimpleCache()
response_cache = SimpleCache()
