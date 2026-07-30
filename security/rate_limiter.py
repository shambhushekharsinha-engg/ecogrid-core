"""
EcoGrid Core: Security Rate Limiting Engine
Implements a thread-safe Token Bucket Rate Limiter to protect authentication
and control endpoints against brute-force attacks and DDoS abuse.
"""

import time
from collections import defaultdict
import threading

class RateLimiter:
    """Thread-safe Token Bucket Rate Limiter."""

    def __init__(self, requests_per_minute: int = 60):
        self.rate = requests_per_minute
        self.capacity = requests_per_minute
        self.tokens = defaultdict(lambda: float(self.capacity))
        self.last_update = defaultdict(lambda: time.time())
        self.lock = threading.Lock()

    def is_allowed(self, client_identifier: str) -> bool:
        """Determines if a request from a client identifier is within rate limits."""
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update[client_identifier]
            self.last_update[client_identifier] = now

            # Replenish tokens based on elapsed time
            refill_amount = elapsed * (self.rate / 60.0)
            self.tokens[client_identifier] = min(self.capacity, self.tokens[client_identifier] + refill_amount)

            if self.tokens[client_identifier] >= 1.0:
                self.tokens[client_identifier] -= 1.0
                return True
            return False

rate_limiter = RateLimiter(requests_per_minute=60)
