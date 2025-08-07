#!/usr/bin/env python3
"""
Test script for API key encryption
"""
from encryption import key_encryption

def test_encryption():
    """Test the encryption system"""
    print("🔐 Testing API key encryption...")
    
    # Test key
    test_key = "test_api_key_12345"
    
    # Encrypt
    encrypted = key_encryption.encrypt_api_key(test_key)
    print(f"🔐 Original: {test_key}")
    print(f"🔐 Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = key_encryption.decrypt_api_key(encrypted)
    print(f"🔐 Decrypted: {decrypted}")
    
    # Verify
    if test_key == decrypted:
        print("✅ Encryption/decryption working correctly!")
    else:
        print("❌ Encryption/decryption failed!")
    
    # Test detection
    print(f"🔍 Is encrypted: {key_encryption.is_encrypted(encrypted)}")
    print(f"🔍 Is encrypted: {key_encryption.is_encrypted(test_key)}")

if __name__ == "__main__":
    test_encryption() 