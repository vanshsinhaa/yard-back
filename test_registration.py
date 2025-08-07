#!/usr/bin/env python3
"""
Test user registration and API key generation
"""

import requests
import json

def test_registration():
    """Test user registration functionality"""
    base_url = "http://127.0.0.1:8006"
    
    print("🧪 Testing user registration...")
    
    # Test 1: Register a new user
    print("\n1. Testing user registration...")
    registration_data = {
        "user_id": "test_user_123",
        "email": "test@example.com",
        "plan": "free"
    }
    
    try:
        response = requests.post(
            f"{base_url}/register",
            json=registration_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ User registered successfully!")
            print(f"   User ID: {result['user_id']}")
            print(f"   API Key: {result['api_key'][:20]}...")
            print(f"   Plan: {result['plan']}")
            print(f"   Message: {result['message']}")
            
            # Save the API key for testing
            api_key = result['api_key']
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration request failed: {e}")
        return
    
    # Test 2: Test the new API key with search
    print("\n2. Testing API key with search...")
    search_data = {
        "query": "react todo app",
        "max_results": 2,
        "sort_by": "stars",
        "min_stars": 10
    }
    
    try:
        response = requests.post(
            f"{base_url}/search",
            json=search_data,
            headers={
                "Content-Type": "application/json",
                "X-API-Key": api_key
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Search successful with new API key!")
            print(f"   Found {result['total_found']} repositories")
            print(f"   Plan: {result['plan']}")
        else:
            print(f"❌ Search failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Search request failed: {e}")
    
    # Test 3: Check usage stats
    print("\n3. Testing usage statistics...")
    try:
        response = requests.get(
            f"{base_url}/usage",
            headers={"X-API-Key": api_key}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Usage stats retrieved!")
            print(f"   User ID: {result['user_id']}")
            print(f"   Plan: {result['plan']}")
            if result.get('usage'):
                usage = result['usage']
                print(f"   Hourly: {usage['hourly_usage']['used']}/{usage['hourly_usage']['limit']}")
                print(f"   Monthly: {usage['monthly_usage']['used']}/{usage['monthly_usage']['limit']}")
        else:
            print(f"❌ Usage stats failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Usage stats request failed: {e}")
    
    print("\n🎉 Registration test complete!")

if __name__ == "__main__":
    test_registration() 