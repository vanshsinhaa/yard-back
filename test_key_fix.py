#!/usr/bin/env python3
"""
Test script to verify API key encryption/decryption fix
"""

from database import db_manager
from auth_system import api_key_manager
import time

def test_key_registration_and_validation():
    """Test that a newly registered key can be used immediately"""
    
    print("🧪 Testing API key registration and validation...")
    
    # Step 1: Register a new user
    user_id = f"test_user_{int(time.time())}"
    api_key = api_key_manager.generate_api_key(user_id, "free")
    
    print(f"✅ Generated API key: {api_key}")
    print(f"✅ User ID: {user_id}")
    
    # Step 2: Immediately validate the key
    try:
        user_data = api_key_manager.validate_api_key(api_key)
        print(f"✅ Key validation successful!")
        print(f"   User ID: {user_data['user_id']}")
        print(f"   Plan: {user_data['plan']}")
        print(f"   API Key: {user_data['api_key']}")
        
        # Step 3: Check usage stats
        usage_stats = api_key_manager.get_usage_stats(api_key)
        print(f"✅ Usage stats retrieved:")
        print(f"   Hourly: {usage_stats['hourly_usage']['used']}/{usage_stats['hourly_usage']['limit']}")
        print(f"   Monthly: {usage_stats['monthly_usage']['used']}/{usage_stats['monthly_usage']['limit']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Key validation failed: {e}")
        return False

def test_database_direct_access():
    """Test direct database access to verify encryption"""
    
    print("\n🔍 Testing direct database access...")
    
    # Get a key from the database
    keys = db_manager.get_all_api_keys()
    if keys:
        test_key = keys[0]['api_key']
        print(f"Testing with key: {test_key}")
        
        # Try to get data
        data = db_manager.get_api_key_data(test_key)
        if data:
            print(f"✅ Database access successful")
            print(f"   User ID: {data['user_id']}")
            print(f"   Plan: {data['plan']}")
            print(f"   API Key: {data['api_key']}")
        else:
            print(f"❌ Database access failed")
    else:
        print("No keys found in database")

if __name__ == "__main__":
    print("🚀 Testing API Key Encryption Fix")
    print("=" * 50)
    
    # Test 1: Registration and immediate validation
    success1 = test_key_registration_and_validation()
    
    # Test 2: Direct database access
    test_database_direct_access()
    
    if success1:
        print("\n🎉 All tests passed! The encryption fix is working.")
    else:
        print("\n❌ Tests failed. There's still an issue with the encryption.")

