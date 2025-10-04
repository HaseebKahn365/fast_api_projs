from fastapi import Request, HTTPException
import time
from collections import defaultdict

class SimpleRateLimiter:
    def __init__(self, times: int = 5, seconds: int = 60):
        self.times = times
        self.seconds = seconds
        self.requests = defaultdict(list)  # client_ip -> list of timestamps

    def __call__(self, request: Request):
        client_ip = request.client.host if request.client else "unknown"

        # Clean old requests
        current_time = time.time()
        self.requests[client_ip] = [
            ts for ts in self.requests[client_ip]
            if current_time - ts < self.seconds
        ]  # sliding window

        # Check if limit exceeded
        if len(self.requests[client_ip]) >= self.times:
            raise HTTPException(status_code=429, detail="Too many requests")

        # Add current request
        self.requests[client_ip].append(current_time)

# Global rate limiter instance
rate_limiter = SimpleRateLimiter(times=5, seconds=60)