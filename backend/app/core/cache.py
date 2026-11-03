import time
from threading import Lock
from typing import Any


class TTLCache:
    """Thread-safe in-memory cache with Time-To-Live (TTL) expiration.

    Lightweight, zero-dependency process cache suited for read-heavy aggregations
    (e.g., dashboard analytics) and frequently accessed entity lookups.
    """

    def __init__(self, default_ttl: float = 60.0):
        self._default_ttl = default_ttl
        self._cache: dict[str, tuple[float, Any]] = {}
        self._lock = Lock()

    def get(self, key: str) -> Any | None:
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return None

            expiry, value = entry
            if time.time() > expiry:
                self._cache.pop(key, None)
                return None

            return value

    def set(self, key: str, value: Any, ttl: float | None = None) -> None:
        with self._lock:
            effective_ttl = self._default_ttl if ttl is None else ttl
            expiry = time.time() + effective_ttl
            self._cache[key] = (expiry, value)

    def invalidate(self, key: str) -> None:
        with self._lock:
            self._cache.pop(key, None)

    def invalidate_prefix(self, prefix: str) -> None:
        with self._lock:
            keys_to_remove = [k for k in self._cache if k.startswith(prefix)]
            for k in keys_to_remove:
                self._cache.pop(k, None)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()


# Default process-level cache instance with 60-second default TTL
cache = TTLCache(default_ttl=60.0)
