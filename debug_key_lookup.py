#!/usr/bin/env python3
"""
Debug script to test API key lookup process
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import db_manager
from auth_system import api_key_manager
import hashlib

def test_key_lookup():
    """Test the API key lookup process"""
    
    print("🔍 DEBUGGING API KEY LOOKUP")
    print("=" * 50)
    
    # Get all API keys from database
    all_keys = db_manager.get_all_api_keys()
    
    print(f"📊 Total keys in database: {len(all_keys)}")
    print()
    
    # Test each key
    for i, key_data in enumerate(all_keys, 1):
        print(f"🔑 Testing Key #{i}:")
        print(f"   User ID: {key_data['user_id']}")
        print(f"   Plan: {key_data['plan']}")
        print(f"   Active: {key_data['active']}")
        
        # Get the original API key (this should be the one user provides)
        original_key = key_data['api_key']
        print(f"   Original Key: {original_key[:20]}...")
        
        # Create hash of original key
        key_hash = hashlib.sha256(original_key.encode()).hexdigest()
        print(f"   Key Hash: {key_hash[:20]}...")
        
        # Test lookup by original key
        print("   🔍 Testing lookup by original key...")
        lookup_result = db_manager.get_api_key_data(original_key)
        
        if lookup_result:
            print("   ✅ Lookup SUCCESSFUL")
            print(f"   📋 Found User ID: {lookup_result['user_id']}")
            print(f"   📋 Found Plan: {lookup_result['plan']}")
        else:
            print("   ❌ Lookup FAILED")
        
        print()
    
    # Test with a specific key that should work
    print("🎯 TESTING WITH KNOWN WORKING KEY")
    print("=" * 50)
    
    # Use the first key from the database
    if all_keys:
        test_key = all_keys[0]['api_key']
        print(f"Testing with key: {test_key[:20]}...")
        
        # Test validation
        try:
            result = api_key_manager.validate_api_key(test_key)
            print("✅ Validation SUCCESSFUL")
            print(f"   User ID: {result['user_id']}")
            print(f"   Plan: {result['plan']}")
            print(f"   Hourly Usage: {result['current_hour_requests']}/{result['requests_per_hour']}")
        except Exception as e:
            print(f"❌ Validation FAILED: {e}")
    
    print()
    print("🔍 DATABASE SCHEMA CHECK")
    print("=" * 50)
    
    # Check database schema
    try:
        with db_manager._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(api_keys)")
            columns = cursor.fetchall()
            
            print("📋 API_KEYS table columns:")
            for col in columns:
                print(f"   {col[1]} ({col[2]}) - {'PRIMARY KEY' if col[5] else 'NOT NULL' if col[3] else 'NULL'}")
    
    except Exception as e:
        print(f"❌ Schema check failed: {e}")

if __name__ == "__main__":
    test_key_lookup()
