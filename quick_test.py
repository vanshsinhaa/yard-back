#!/usr/bin/env python3
"""
Quick test script to verify API functionality
"""

import requests
import json
import time

def test_api():
    """Test the API endpoints"""
    
    base_url = "http://127.0.0.1:8001"
    
    print("🧪 Testing CodeInspiration API")
    print("=" * 40)
    
    # Test 1: Root endpoint
    print("1️⃣ Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            print(f"📄 Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    print()
    
    # Test 2: Health endpoint
    print("2️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/v1/health")
        if response.status_code == 200:
            print("✅ Health endpoint working!")
            print(f"📄 Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    print()
    
    # Test 3: Search endpoint (basic test)
    print("3️⃣ Testing search endpoint...")
    try:
        search_data = {
            "query": "react todo app",
            "max_results": 2,
            "sort_by": "stars",
            "min_stars": 10
        }
        
        response = requests.post(
            f"{base_url}/api/v1/search",
            json=search_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Search endpoint working!")
            print(f"📄 Found {result.get('total_found', 0)} repositories")
            print(f"⏱️ Search time: {result.get('search_time_ms', 0):.2f}ms")
        else:
            print(f"❌ Search endpoint failed: {response.status_code}")
            print(f"📄 Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Search endpoint error: {e}")
    
    print()
    print("🎉 API testing complete!")
    print()
    print("💡 Next steps:")
    print("   1. Visit http://127.0.0.1:8001/docs for interactive docs")
    print("   2. Try different search queries")
    print("   3. Add your OpenAI API key for full features")

if __name__ == "__main__":
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(3)
    test_api() 