"""
Encryption utilities for API key security
"""
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Optional

class KeyEncryption:
    """Handles encryption and decryption of API keys"""
    
    def __init__(self, secret_key: Optional[str] = None):
        """
        Initialize encryption with a secret key.
        If no key provided, will try to load from environment or generate new one.
        """
        if secret_key:
            self.secret_key = secret_key
        else:
            # Try to load from environment
            self.secret_key = os.environ.get('ENCRYPTION_KEY')
            
        if not self.secret_key:
            # Generate a new key and save to environment
            self.secret_key = self._generate_key()
            print("🔐 Generated new encryption key. Add to .env: ENCRYPTION_KEY=" + self.secret_key)
        
        # Create Fernet instance
        self.fernet = Fernet(self.secret_key.encode())
    
    def _generate_key(self) -> str:
        """Generate a new encryption key"""
        return Fernet.generate_key().decode()
    
    def encrypt_api_key(self, api_key: str) -> str:
        """Encrypt an API key"""
        try:
            encrypted = self.fernet.encrypt(api_key.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            print(f"❌ Encryption failed: {e}")
            return api_key  # Fallback to plain text
    
    def decrypt_api_key(self, encrypted_key: str) -> str:
        """Decrypt an API key"""
        try:
            # First decode from base64
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_key.encode())
            # Then decrypt
            decrypted = self.fernet.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            print(f"❌ Decryption failed: {e}")
            return encrypted_key  # Fallback to original
    
    def is_encrypted(self, key: str) -> bool:
        """Check if a key appears to be encrypted"""
        try:
            # Try to decode as base64
            base64.urlsafe_b64decode(key.encode())
            return True
        except:
            return False

# Global encryption instance
key_encryption = KeyEncryption() 