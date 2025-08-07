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

# Import database manager
from database import db_manager

class APIKeyManager:
    """Manages API keys and user access using database"""
    
    def __init__(self):
        # Initialize demo keys in database
        db_manager.create_demo_keys()
    
    def generate_api_key(self, user_id: str, email: str = None, plan: str = "free") -> str:
        """Generate a new API key for a user"""
        api_key = f"{plan}_{secrets.token_urlsafe(32)}"
        
        # Add to database
        if db_manager.add_api_key(api_key, user_id, email, plan):
            return api_key
        else:
            raise ValueError("Failed to generate API key - user may already exist")
    
    def validate_api_key(self, api_key: str) -> Dict:
        """Validate API key and check rate limits"""
        
        if not api_key:
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
        
        # Get key data from database
        key_data = db_manager.get_api_key_data(api_key)
        
        if not key_data:
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
        
        # Check rate limits
        current_time = time.time()
        
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
        
        # Update usage in database
        if not db_manager.update_usage(api_key, current_time):
            raise HTTPException(
                status_code=500,
                detail={
                    "error": {
                        "message": "Failed to update usage",
                        "code": "USAGE_UPDATE_ERROR"
                    }
                }
            )
        
        # Add the API key to the returned data
        key_data["api_key"] = api_key
        return key_data
    
    def get_usage_stats(self, api_key: str) -> Dict:
        """Get usage statistics for an API key"""
        return db_manager.get_usage_stats(api_key)

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
    # Demo keys are now created in the database directly
    pass

if __name__ == "__main__":
    create_demo_keys()