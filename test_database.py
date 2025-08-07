#!/usr/bin/env python3
"""
Test database integration
"""

import time
from database import db_manager
from auth_system import api_key_manager

def test_database():
    """Test database functionality"""
    print("🧪 Testing database integration...")
    
    # Test 1: Create a test key
    print("\n1. Testing key creation...")
    import secrets
    test_key = "test_" + secrets.token_urlsafe(16)
    success = db_manager.add_api_key(test_key, "test_user", "test@example.com", "free")
    if success:
        print("✅ Test key created successfully")
        key_data = db_manager.get_api_key_data(test_key)
        print(f"   User ID: {key_data['user_id']}")
        print(f"   Plan: {key_data['plan']}")
    else:
        print("❌ Failed to create test key")
    
    # Test 2: Generate new API key
    print("\n2. Testing API key generation...")
    new_key = api_key_manager.generate_api_key("test_user", "free")
    print(f"✅ Generated new key: {new_key[:20]}...")
    
    # Test 3: Validate API key
    print("\n3. Testing API key validation...")
    try:
        user_data = api_key_manager.validate_api_key(test_key)
        print(f"✅ API key validated: {user_data['user_id']} ({user_data['plan']})")
    except Exception as e:
        print(f"❌ API key validation failed: {e}")
    
    # Test 4: Check usage stats
    print("\n4. Testing usage stats...")
    stats = api_key_manager.get_usage_stats(test_key)
    if stats:
        print(f"✅ Usage stats: {stats['plan']} plan")
        print(f"   Hourly: {stats['hourly_usage']['used']}/{stats['hourly_usage']['limit']}")
        print(f"   Monthly: {stats['monthly_usage']['used']}/{stats['monthly_usage']['limit']}")
    else:
        print("❌ Usage stats not found")
    
    print("\n🎉 Database integration test complete!")

if __name__ == "__main__":
    test_database() 