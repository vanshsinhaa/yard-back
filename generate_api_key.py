#!/usr/bin/env python3
"""
Quick API Key Generator for Code Graveyard API
Usage: python generate_api_key.py [plan] [email]
"""

import sys
from secure_key_manager import secure_key_manager

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_api_key.py [plan] [email]")
        print("Plans: free, pro, enterprise")
        print("Example: python generate_api_key.py pro user@example.com")
        return
    
    plan = sys.argv[1]
    email = sys.argv[2]
    
    if plan not in ["free", "pro", "enterprise"]:
        print("❌ Invalid plan. Use: free, pro, or enterprise")
        return
    
    print(f"🔑 Generating {plan} API key for {email}...")
    print()
    
    try:
        api_key = secure_key_manager.generate_api_key(plan, email)
        
        print("✅ API Key Generated Successfully!")
        print("=" * 50)
        print(f"🔑 API Key: {api_key}")
        print(f"📧 Email: {email}")
        print(f"💎 Plan: {plan}")
        print()
        print("📋 Usage Instructions:")
        print(f"   Header: X-API-Key: {api_key}")
        print(f"   Example: curl -H 'X-API-Key: {api_key}' https://api.codegraveyard.com/search")
        print()
        print("⚠️  IMPORTANT: Save this key securely - it cannot be retrieved again!")
        
    except Exception as e:
        print(f"❌ Error generating key: {e}")

if __name__ == "__main__":
    main()