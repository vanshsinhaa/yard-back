#!/usr/bin/env python3
"""
Debug encryption/decryption step by step
"""

from encryption import key_encryption
from database import db_manager
import time

def test_encryption_consistency():
    """Test that encryption is consistent"""
    print("🔐 Testing encryption consistency...")
    
    test_key = "free_test123"
    encrypted1 = key_encryption.encrypt_api_key(test_key)
    encrypted2 = key_encryption.encrypt_api_key(test_key)
    
    print(f"Original key: {test_key}")
    print(f"Encrypted 1: {encrypted1}")
    print(f"Encrypted 2: {encrypted2}")
    print(f"Consistent: {encrypted1 == encrypted2}")
    
    return encrypted1 == encrypted2

def test_database_operations():
    """Test database operations step by step"""
    print("\n🗄️ Testing database operations...")
    
    # Clear any existing test data
    test_user_id = f"debug_user_{int(time.time())}"
    test_api_key = f"free_debug_{int(time.time())}"
    
    print(f"Test user ID: {test_user_id}")
    print(f"Test API key: {test_api_key}")
    
    # Step 1: Add key to database
    print("\n1. Adding key to database...")
    success = db_manager.add_api_key(test_api_key, test_user_id, "free")
    print(f"Add result: {success}")
    
    # Step 2: Get key data
    print("\n2. Getting key data...")
    data = db_manager.get_api_key_data(test_api_key)
    if data:
        print(f"Found data: {data}")
        print(f"User ID: {data.get('user_id')}")
        print(f"Plan: {data.get('plan')}")
        print(f"API Key: {data.get('api_key')}")
    else:
        print("❌ No data found!")
    
    # Step 3: Try to find by encrypted key
    print("\n3. Testing encrypted key lookup...")
    encrypted_key = key_encryption.encrypt_api_key(test_api_key)
    print(f"Encrypted key: {encrypted_key}")
    
    # Direct database query
    import sqlite3
    conn = sqlite3.connect("api_keys.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM api_keys WHERE api_key = ?", (encrypted_key,))
    row = cursor.fetchone()
    if row:
        print(f"✅ Found by encrypted key: {dict(row)}")
    else:
        print("❌ Not found by encrypted key")
    
    cursor.execute("SELECT * FROM api_keys WHERE api_key = ?", (test_api_key,))
    row = cursor.fetchone()
    if row:
        print(f"✅ Found by plain key: {dict(row)}")
    else:
        print("❌ Not found by plain key")
    
    conn.close()

if __name__ == "__main__":
    print("🚀 Debugging Encryption Issues")
    print("=" * 50)
    
    # Test 1: Encryption consistency
    consistent = test_encryption_consistency()
    
    # Test 2: Database operations
    test_database_operations()
    
    if consistent:
        print("\n✅ Encryption is consistent")
    else:
        print("\n❌ Encryption is NOT consistent - this is the problem!")

