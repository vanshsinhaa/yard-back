#!/usr/bin/env python3
"""
View database contents
"""

import sqlite3
import time
from datetime import datetime

def view_database():
    """View all database contents"""
    
    try:
        # Connect to database
        conn = sqlite3.connect('api_keys.db')
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        cursor = conn.cursor()
        
        print("🗄️  DATABASE CONTENTS")
        print("=" * 50)
        
        # Show tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📋 Tables: {[table[0] for table in tables]}")
        print()
        
        # Show API keys
        print("🔑 API KEYS TABLE")
        print("-" * 30)
        cursor.execute("SELECT * FROM api_keys ORDER BY created_at DESC")
        api_keys = cursor.fetchall()
        
        if api_keys:
            for i, key_data in enumerate(api_keys, 1):
                created_date = datetime.fromtimestamp(key_data['created_at']).strftime('%Y-%m-%d %H:%M:%S')
                email = key_data['email'] if 'email' in key_data.keys() else 'Not set'
                print(f"{i}. API Key: {key_data['api_key']}")
                print(f"   User ID: {key_data['user_id']}")
                print(f"   Email: {email}")
                print(f"   Plan: {key_data['plan']}")
                print(f"   Active: {key_data['active']}")
                print(f"   Created: {created_date}")
                print(f"   Hourly Usage: {key_data['current_hour_requests']}/{key_data['requests_per_hour']}")
                print(f"   Monthly Usage: {key_data['current_month_requests']}/{key_data['requests_per_month']}")
                print()
        else:
            print("No API keys found")
        
        # Show usage logs
        print("📊 USAGE LOGS TABLE")
        print("-" * 30)
        cursor.execute("SELECT * FROM usage_logs ORDER BY timestamp DESC LIMIT 10")
        usage_logs = cursor.fetchall()
        
        if usage_logs:
            for i, log in enumerate(usage_logs, 1):
                log_date = datetime.fromtimestamp(log['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                print(f"{i}. API Key: {log['api_key'][:20]}...")
                print(f"   Endpoint: {log['endpoint']}")
                print(f"   Response Time: {log['response_time']:.2f}s" if log['response_time'] else "   Response Time: N/A")
                print(f"   Timestamp: {log_date}")
                print()
        else:
            print("No usage logs found")
        
        # Show statistics
        print("📈 STATISTICS")
        print("-" * 30)
        cursor.execute("SELECT COUNT(*) as total_keys FROM api_keys")
        total_keys = cursor.fetchone()['total_keys']
        
        cursor.execute("SELECT COUNT(*) as total_logs FROM usage_logs")
        total_logs = cursor.fetchone()['total_logs']
        
        cursor.execute("SELECT plan, COUNT(*) as count FROM api_keys GROUP BY plan")
        plan_stats = cursor.fetchall()
        
        print(f"Total API Keys: {total_keys}")
        print(f"Total Usage Logs: {total_logs}")
        print("Plan Distribution:")
        for plan in plan_stats:
            print(f"  {plan['plan']}: {plan['count']} keys")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error viewing database: {e}")

if __name__ == "__main__":
    view_database() 