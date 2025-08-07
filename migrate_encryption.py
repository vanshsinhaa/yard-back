#!/usr/bin/env python3
"""
Migration script to encrypt existing API keys
"""
import sqlite3
from encryption import key_encryption

def migrate_existing_keys():
    """Migrate existing plain text API keys to encrypted format"""
    print("🔐 Starting API key encryption migration...")
    
    try:
        # Connect to database
        conn = sqlite3.connect("api_keys.db")
        cursor = conn.cursor()
        
        # Get all API keys
        cursor.execute("SELECT api_key FROM api_keys")
        rows = cursor.fetchall()
        
        if not rows:
            print("✅ No API keys found to migrate")
            return
        
        print(f"📊 Found {len(rows)} API keys to check...")
        
        migrated_count = 0
        for row in rows:
            api_key = row[0]
            
            # Check if key is already encrypted
            if key_encryption.is_encrypted(api_key):
                print(f"✅ Key already encrypted: {api_key[:10]}...")
                continue
            
            # Encrypt the key
            encrypted_key = key_encryption.encrypt_api_key(api_key)
            
            # Update in database
            cursor.execute("""
                UPDATE api_keys SET api_key = ? WHERE api_key = ?
            """, (encrypted_key, api_key))
            
            migrated_count += 1
            print(f"🔐 Encrypted key: {api_key[:10]}... -> {encrypted_key[:20]}...")
        
        conn.commit()
        print(f"✅ Migration complete! Encrypted {migrated_count} keys")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_existing_keys() 