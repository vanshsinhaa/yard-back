"""
Rate limiting middleware for CodeInspiration API
"""

import time
from typing import Dict, Tuple
from fastapi import Request, HTTPException, status
from app.core.exceptions import RateLimitError


class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed for the client"""
        now = time.time()
        
        # Initialize client if not exists
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Remove old requests (older than 1 minute)
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < 60
        ]
        
        # Check if under limit
        if len(self.requests[client_id]) >= self.requests_per_minute:
            return False
        
        # Add current request
        self.requests[client_id].append(now)
        return True
    
    def get_remaining_requests(self, client_id: str) -> int:
        """Get remaining requests for the client"""
        now = time.time()
        
        if client_id not in self.requests:
            return self.requests_per_minute
        
        # Remove old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < 60
        ]
        
        return max(0, self.requests_per_minute - len(self.requests[client_id]))


# Global rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=60)


def get_client_id(request: Request) -> str:
    """Extract client identifier from request"""
    # Try to get API key first
    api_key = request.headers.get("X-API-Key")
    if api_key:
        return f"api_key:{api_key}"
    
    # Fall back to IP address
    client_ip = request.client.host if request.client else "unknown"
    return f"ip:{client_ip}"


async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware"""
    
    # Skip rate limiting for health checks and docs
    if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
        return await call_next(request)
    
    client_id = get_client_id(request)
    
    if not rate_limiter.is_allowed(client_id):
        remaining_time = 60 - (time.time() % 60)
        raise RateLimitError(
            f"Rate limit exceeded. Try again in {int(remaining_time)} seconds. "
            f"Limit: {rate_limiter.requests_per_minute} requests per minute."
        )
    
    # Add rate limit headers to response
    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(rate_limiter.requests_per_minute)
    response.headers["X-RateLimit-Remaining"] = str(rate_limiter.get_remaining_requests(client_id))
    response.headers["X-RateLimit-Reset"] = str(int(time.time() + 60))
    
    return response 