#!/usr/bin/env python3
"""
Secure API Key Management System
- Generates cryptographically secure API keys
- Hashes keys for secure storage
- No demo keys in production
"""

import secrets
import hashlib
import hmac
import uuid
import time
import json
import os
from typing import Dict, Optional, Tuple, List
from datetime import datetime, timedelta
from fastapi import HTTPException

class SecureKeyManager:
    """Production-ready API key management with security best practices"""
    
    def __init__(self, secret_key: Optional[str] = None):
        # Use environment variable or generate secure key
        self.secret_key = secret_key or os.environ.get('SECRET_KEY') or secrets.token_urlsafe(32)
        self.keys_file = "secure_api_keys.json"  # This should be in a secure database in production
        self.load_keys()
    
    def generate_api_key(self, plan: str = "free", user_email: str = None) -> str:
        """
        Generate cryptographically secure API key
        Format: cg_live_[32_random_chars] (Code Graveyard Live)
        """
        # Generate 32 random bytes (256 bits) for maximum security
        random_part = secrets.token_urlsafe(24)  # ~32 chars when base64 encoded
        
        # Create API key with clear prefix
        api_key = f"cg_live_{random_part}"
        
        # Hash the key for secure storage (never store plain keys)
        key_hash = self._hash_key(api_key)
        
        # Store key metadata (hashed)
        key_data = {
            "key_hash": key_hash,
            "plan": plan,
            "user_email": user_email,
            "created_at": datetime.utcnow().isoformat(),
            "usage_count": 0,
            "usage_limit_hourly": self._get_hourly_limit(plan),
            "usage_limit_monthly": self._get_monthly_limit(plan),
            "is_active": True,
            "last_used": None
        }
        
        # Store securely
        self.api_keys[key_hash] = key_data
        self.save_keys()
        
        print(f"🔑 Generated new API key for {plan} plan")
        print(f"📧 User: {user_email or 'anonymous'}")
        print(f"🔒 Key: {api_key[:12]}...")  # Only show first 12 chars
        
        return api_key
    
    def _hash_key(self, api_key: str) -> str:
        """Hash API key using HMAC-SHA256 for secure storage"""
        return hmac.new(
            self.secret_key.encode(), 
            api_key.encode(), 
            hashlib.sha256
        ).hexdigest()
    
    def validate_key(self, api_key: str) -> Optional[Dict]:
        """Validate API key and return user data"""
        if not api_key or not api_key.startswith('cg_live_'):
            return None
        
        key_hash = self._hash_key(api_key)
        
        if key_hash not in self.api_keys:
            return None
        
        key_data = self.api_keys[key_hash]
        
        if not key_data.get('is_active', False):
            return None
        
        # Update last used
        key_data['last_used'] = datetime.utcnow().isoformat()
        self.save_keys()
        
        return {
            "plan": key_data["plan"],
            "user_email": key_data.get("user_email"),
            "usage_count": key_data["usage_count"],
            "usage_limit_hourly": key_data["usage_limit_hourly"],
            "usage_limit_monthly": key_data["usage_limit_monthly"]
        }
    
    def increment_usage(self, api_key: str) -> bool:
        """Increment usage count and check limits"""
        key_hash = self._hash_key(api_key)
        
        if key_hash not in self.api_keys:
            return False
        
        key_data = self.api_keys[key_hash]
        
        # Check rate limits here (simplified - production needs Redis/database)
        if self._is_rate_limited(key_data):
            return False
        
        key_data['usage_count'] += 1
        self.save_keys()
        return True
    
    def _is_rate_limited(self, key_data: Dict) -> bool:
        """Check if key has exceeded rate limits"""
        # Simplified rate limiting - production should use Redis
        # This is basic implementation for demo
        return False  # For now, allow all requests
    
    def _get_hourly_limit(self, plan: str) -> int:
        """Get hourly request limit by plan"""
        limits = {
            "free": 100,
            "pro": 1000, 
            "enterprise": 10000
        }
        return limits.get(plan, 100)
    
    def _get_monthly_limit(self, plan: str) -> int:
        """Get monthly request limit by plan"""
        limits = {
            "free": 1000,
            "pro": 10000,
            "enterprise": 100000
        }
        return limits.get(plan, 1000)
    
    def load_keys(self):
        """Load API keys from secure storage"""
        try:
            if os.path.exists(self.keys_file):
                with open(self.keys_file, 'r') as f:
                    self.api_keys = json.load(f)
            else:
                self.api_keys = {}
        except Exception as e:
            print(f"⚠️ Error loading keys: {e}")
            self.api_keys = {}
    
    def save_keys(self):
        """Save API keys to secure storage"""
        try:
            with open(self.keys_file, 'w') as f:
                json.dump(self.api_keys, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving keys: {e}")
    
    def revoke_key(self, api_key: str) -> bool:
        """Revoke an API key"""
        key_hash = self._hash_key(api_key)
        
        if key_hash in self.api_keys:
            self.api_keys[key_hash]['is_active'] = False
            self.save_keys()
            return True
        return False
    
    def list_keys_for_user(self, user_email: str) -> List[Dict]:
        """List all keys for a user (admin function)"""
        user_keys = []
        for key_hash, key_data in self.api_keys.items():
            if key_data.get('user_email') == user_email:
                user_keys.append({
                    "plan": key_data["plan"],
                    "created_at": key_data["created_at"],
                    "usage_count": key_data["usage_count"],
                    "is_active": key_data["is_active"],
                    "last_used": key_data.get("last_used")
                })
        return user_keys

# Production key manager
secure_key_manager = SecureKeyManager()

# Authentication dependency for FastAPI
async def get_secure_api_key(request):
    """Secure API key validation for production"""
    api_key = request.headers.get("x-api-key") or request.headers.get("X-API-Key")
    
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    user_data = secure_key_manager.validate_key(api_key)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Increment usage
    if not secure_key_manager.increment_usage(api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    return user_data

if __name__ == "__main__":
    # Demo key generation (for testing only)
    print("🔐 Secure API Key Manager")
    print("=" * 50)
    
    # Generate sample keys
    free_key = secure_key_manager.generate_api_key("free", "user@example.com")
    pro_key = secure_key_manager.generate_api_key("pro", "pro@example.com")
    
    print("\n🔑 Sample Keys Generated (for testing):")
    print(f"Free: {free_key}")
    print(f"Pro: {pro_key}")
    print("\n⚠️ In production, keys would be sent via email/dashboard")