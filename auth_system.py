#!/usr/bin/env python3
"""
API Key Authentication System for CodeInspiration
"""

import secrets
import hashlib
import time
from typing import Dict, Optional
from fastapi import HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

class APIKeyManager:
    """Manages API keys and user access"""
    
    def __init__(self):
        # In production, this would be a database
        self.api_keys = {
            # Demo keys for testing
            "demo_free_12345": {
                "user_id": "demo_user",
                "plan": "free",
                "requests_per_hour": 100,
                "requests_per_month": 1000,
                "current_hour_requests": 0,
                "current_month_requests": 0,
                "last_reset_hour": time.time(),
                "last_reset_month": time.time(),
                "active": True,
                "created_at": time.time()
            },
            "pro_key_67890": {
                "user_id": "pro_user",
                "plan": "pro",
                "requests_per_hour": 1000,
                "requests_per_month": 10000,
                "current_hour_requests": 0,
                "current_month_requests": 0,
                "last_reset_hour": time.time(),
                "last_reset_month": time.time(),
                "active": True,
                "created_at": time.time()
            }
        }
    
    def generate_api_key(self, user_id: str, plan: str = "free") -> str:
        """Generate a new API key"""
        key = f"{plan}_{secrets.token_urlsafe(16)}"
        
        limits = {
            "free": {"hour": 100, "month": 1000},
            "pro": {"hour": 1000, "month": 10000},
            "enterprise": {"hour": 10000, "month": 100000}
        }
        
        self.api_keys[key] = {
            "user_id": user_id,
            "plan": plan,
            "requests_per_hour": limits[plan]["hour"],
            "requests_per_month": limits[plan]["month"],
            "current_hour_requests": 0,
            "current_month_requests": 0,
            "last_reset_hour": time.time(),
            "last_reset_month": time.time(),
            "active": True,
            "created_at": time.time()
        }
        
        return key
    
    def validate_api_key(self, api_key: str) -> Dict:
        """Validate API key and check rate limits"""
        
        if not api_key or api_key not in self.api_keys:
            raise HTTPException(
                status_code=401,
                detail={
                    "error": {
                        "message": "Invalid API key",
                        "code": "INVALID_API_KEY",
                        "hint": "Get your API key at https://codeinspiration.dev/api-keys"
                    }
                }
            )
        
        key_data = self.api_keys[api_key]
        
        if not key_data["active"]:
            raise HTTPException(
                status_code=401,
                detail={
                    "error": {
                        "message": "API key is disabled",
                        "code": "DISABLED_API_KEY"
                    }
                }
            )
        
        # Check and reset hourly limits
        current_time = time.time()
        if current_time - key_data["last_reset_hour"] >= 3600:  # 1 hour
            key_data["current_hour_requests"] = 0
            key_data["last_reset_hour"] = current_time
        
        # Check and reset monthly limits
        if current_time - key_data["last_reset_month"] >= 2592000:  # 30 days
            key_data["current_month_requests"] = 0
            key_data["last_reset_month"] = current_time
        
        # Check hourly rate limit
        if key_data["current_hour_requests"] >= key_data["requests_per_hour"]:
            raise HTTPException(
                status_code=429,
                detail={
                    "error": {
                        "message": f"Hourly rate limit exceeded ({key_data['requests_per_hour']} requests/hour)",
                        "code": "RATE_LIMIT_HOURLY",
                        "reset_time": key_data["last_reset_hour"] + 3600,
                        "upgrade_hint": "Upgrade to Pro for higher limits"
                    }
                }
            )
        
        # Check monthly rate limit
        if key_data["current_month_requests"] >= key_data["requests_per_month"]:
            raise HTTPException(
                status_code=429,
                detail={
                    "error": {
                        "message": f"Monthly rate limit exceeded ({key_data['requests_per_month']} requests/month)",
                        "code": "RATE_LIMIT_MONTHLY",
                        "reset_time": key_data["last_reset_month"] + 2592000,
                        "upgrade_hint": "Upgrade to Pro for higher limits"
                    }
                }
            )
        
        # Increment counters
        key_data["current_hour_requests"] += 1
        key_data["current_month_requests"] += 1
        
        return key_data
    
    def get_usage_stats(self, api_key: str) -> Dict:
        """Get usage statistics for an API key"""
        if api_key not in self.api_keys:
            return None
        
        key_data = self.api_keys[api_key]
        
        return {
            "plan": key_data["plan"],
            "hourly_usage": {
                "used": key_data["current_hour_requests"],
                "limit": key_data["requests_per_hour"],
                "remaining": key_data["requests_per_hour"] - key_data["current_hour_requests"]
            },
            "monthly_usage": {
                "used": key_data["current_month_requests"],
                "limit": key_data["requests_per_month"],
                "remaining": key_data["requests_per_month"] - key_data["current_month_requests"]
            }
        }

# Global API key manager
api_key_manager = APIKeyManager()

# Dependency for API key authentication
def get_api_key(x_api_key: Optional[str] = Header(None)) -> Dict:
    """Extract and validate API key from header"""
    
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail={
                "error": {
                    "message": "API key required",
                    "code": "MISSING_API_KEY",
                    "hint": "Add 'X-API-Key: your_key_here' header to your request"
                }
            }
        )
    
    return api_key_manager.validate_api_key(x_api_key)

# Optional authentication (for free tier)
def get_optional_api_key(x_api_key: Optional[str] = Header(None)) -> Optional[Dict]:
    """Extract API key if provided, allow anonymous access otherwise"""
    
    if not x_api_key:
        return None  # Anonymous access
    
    try:
        return api_key_manager.validate_api_key(x_api_key)
    except HTTPException:
        return None  # Invalid key, but allow anonymous access

def create_demo_keys():
    """Create demo keys for testing"""
    print("🔑 Demo API Keys Created:")
    print()
    print("FREE TIER:")
    print("  Key: demo_free_12345")
    print("  Limits: 100 requests/hour, 1,000 requests/month")
    print()
    print("PRO TIER:")
    print("  Key: pro_key_67890")
    print("  Limits: 1,000 requests/hour, 10,000 requests/month")
    print()
    print("Usage: Add 'X-API-Key: demo_free_12345' to your request headers")

if __name__ == "__main__":
    create_demo_keys()