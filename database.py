import sqlite3
import time
import secrets
from typing import Dict, Optional, List
from contextlib import contextmanager
from encryption import key_encryption

class DatabaseManager:
    """Manages SQLite database for API keys and usage tracking"""
    
    def __init__(self, db_path: str = "api_keys.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Create API keys table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_keys (
                    api_key TEXT NOT NULL,
                    key_hash TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    email TEXT,
                    plan TEXT NOT NULL,
                    requests_per_hour INTEGER NOT NULL,
                    requests_per_month INTEGER NOT NULL,
                    current_hour_requests INTEGER DEFAULT 0,
                    current_month_requests INTEGER DEFAULT 0,
                    last_reset_hour REAL DEFAULT 0,
                    last_reset_month REAL DEFAULT 0,
                    active BOOLEAN DEFAULT 1,
                    created_at REAL NOT NULL
                )
            """)
            
            # Create usage logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usage_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    api_key TEXT NOT NULL,
                    endpoint TEXT NOT NULL,
                    response_time REAL,
                    timestamp REAL NOT NULL,
                    FOREIGN KEY (api_key) REFERENCES api_keys (api_key)
                )
            """)
            
            conn.commit()
    
    @contextmanager
    def _get_connection(self):
        """Get database connection with proper error handling"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        try:
            yield conn
        finally:
            conn.close()
    
    def add_api_key(self, api_key: str, user_id: str, email: str = None, plan: str = "free") -> bool:
        """Add a new API key to the database"""
        try:
            limits = {
                "free": {"hour": 100, "month": 1000},
                "pro": {"hour": 1000, "month": 10000},
                "enterprise": {"hour": 10000, "month": 100000}
            }
            
            # Create a hash of the API key for lookup
            import hashlib
            key_hash = hashlib.sha256(api_key.encode()).hexdigest()
            
            # Encrypt the API key before storing
            encrypted_key = key_encryption.encrypt_api_key(api_key)
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO api_keys (
                        api_key, key_hash, user_id, email, plan, requests_per_hour, requests_per_month,
                        current_hour_requests, current_month_requests, last_reset_hour,
                        last_reset_month, active, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, ?, ?, 1, ?)
                """, (
                    encrypted_key, key_hash, user_id, email, plan,
                    limits[plan]["hour"], limits[plan]["month"],
                    time.time(), time.time(), time.time()
                ))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False  # Key already exists
    
    def get_api_key_data(self, api_key: str) -> Optional[Dict]:
        """Get API key data from database"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Create hash of the API key for lookup
                import hashlib
                key_hash = hashlib.sha256(api_key.encode()).hexdigest()
                
                # Find by key hash
                cursor.execute("""
                    SELECT * FROM api_keys WHERE key_hash = ?
                """, (key_hash,))
                
                row = cursor.fetchone()
                if row:
                    data = dict(row)
                    # Return the original API key (not the encrypted one)
                    data["api_key"] = api_key
                    return data
                
                # If not found, try to find by plain text (for backward compatibility)
                cursor.execute("""
                    SELECT * FROM api_keys WHERE api_key = ?
                """, (api_key,))
                
                row = cursor.fetchone()
                if row:
                    data = dict(row)
                    # If this is a plain text key, encrypt it and add hash for future use
                    if not key_encryption.is_encrypted(data["api_key"]):
                        encrypted_key = key_encryption.encrypt_api_key(data["api_key"])
                        key_hash = hashlib.sha256(data["api_key"].encode()).hexdigest()
                        cursor.execute("""
                            UPDATE api_keys SET api_key = ?, key_hash = ? WHERE api_key = ?
                        """, (encrypted_key, key_hash, data["api_key"]))
                        conn.commit()
                    # Return the original API key
                    data["api_key"] = api_key
                    return data
                
                return None
        except Exception as e:
            print(f"❌ Database error: {e}")
            return None
    
    def update_usage(self, api_key: str, current_time: float = None) -> bool:
        """Update usage counters for an API key"""
        if current_time is None:
            current_time = time.time()
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Create hash of the API key for lookup
                import hashlib
                key_hash = hashlib.sha256(api_key.encode()).hexdigest()
                
                # Try to find by key hash first
                cursor.execute("""
                    SELECT * FROM api_keys WHERE key_hash = ?
                """, (key_hash,))
                
                row = cursor.fetchone()
                if not row:
                    # Try plain text for backward compatibility
                    cursor.execute("""
                        SELECT * FROM api_keys WHERE api_key = ?
                    """, (api_key,))
                    row = cursor.fetchone()
                
                if not row:
                    return False
                
                data = dict(row)
                
                # Reset counters if needed
                if current_time - data["last_reset_hour"] >= 3600:  # 1 hour
                    data["current_hour_requests"] = 0
                    data["last_reset_hour"] = current_time
                
                if current_time - data["last_reset_month"] >= 2592000:  # 30 days
                    data["current_month_requests"] = 0
                    data["last_reset_month"] = current_time
                
                # Increment counters
                data["current_hour_requests"] += 1
                data["current_month_requests"] += 1
                
                # Update database using the key hash
                cursor.execute("""
                    UPDATE api_keys SET 
                        current_hour_requests = ?,
                        current_month_requests = ?,
                        last_reset_hour = ?,
                        last_reset_month = ?
                    WHERE key_hash = ?
                """, (
                    data["current_hour_requests"],
                    data["current_month_requests"],
                    data["last_reset_hour"],
                    data["last_reset_month"],
                    key_hash
                ))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"❌ Usage update error: {e}")
            return False
    
    def log_usage(self, api_key: str, endpoint: str, response_time: float = None):
        """Log API usage for analytics"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # Store encrypted key in logs
                encrypted_key = key_encryption.encrypt_api_key(api_key)
                cursor.execute("""
                    INSERT INTO usage_logs (api_key, endpoint, response_time, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (encrypted_key, endpoint, response_time, time.time()))
                conn.commit()
        except Exception:
            pass  # Don't fail if logging fails
    
    def get_usage_stats(self, api_key: str) -> Optional[Dict]:
        """Get usage statistics for an API key"""
        data = self.get_api_key_data(api_key)
        if not data:
            return None
        
        return {
            "plan": data["plan"],
            "hourly_usage": {
                "used": data["current_hour_requests"],
                "limit": data["requests_per_hour"],
                "remaining": data["requests_per_hour"] - data["current_hour_requests"]
            },
            "monthly_usage": {
                "used": data["current_month_requests"],
                "limit": data["requests_per_month"],
                "remaining": data["requests_per_month"] - data["current_month_requests"]
            }
        }
    
    def get_all_api_keys(self):
        """Get all API keys from database (for testing)"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM api_keys WHERE active = 1")
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            print(f"❌ Error getting all keys: {e}")
            return []
    
    def create_demo_keys(self):
        """Create demo API keys for testing"""
        # Demo keys are now created through registration endpoint
        pass

# Global database instance
db_manager = DatabaseManager() 