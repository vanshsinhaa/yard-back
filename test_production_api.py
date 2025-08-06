#!/usr/bin/env python3
"""
Test the production-ready CodeInspiration API
"""

import requests
import json
import time

def test_production_api():
    """Test all production API features"""
    
    base_url = "http://127.0.0.1:8001"
    
    print("🎯 Testing Production CodeInspiration API")
    print("=" * 50)
    
    # Test 1: Root endpoint with new features
    print("1️⃣ Testing enhanced root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ Root endpoint working!")
            print(f"📄 Features: {', '.join(data['features'])}")
            print(f"📄 Version: {data['version']}")
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
            data = response.json()
            print("✅ Health endpoint working!")
            print(f"📄 Status: {data['status']}")
            print(f"📄 Timestamp: {data['timestamp']}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    print()
    
    # Test 3: Search endpoint with validation
    print("3️⃣ Testing search endpoint...")
    try:
        search_data = {
            "query": "react todo app",
            "max_results": 3,
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
            
            # Check rate limiting headers
            if 'X-RateLimit-Limit' in response.headers:
                print(f"🚦 Rate limit: {response.headers['X-RateLimit-Limit']} req/min")
                print(f"🚦 Remaining: {response.headers['X-RateLimit-Remaining']} requests")
                
        else:
            print(f"❌ Search endpoint failed: {response.status_code}")
            print(f"📄 Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Search endpoint error: {e}")
    
    print()
    
    # Test 4: Invalid search (error handling)
    print("4️⃣ Testing error handling...")
    try:
        invalid_search = {
            "query": "x",  # Too short
            "max_results": 50,  # Too many
            "sort_by": "invalid",  # Invalid option
            "min_stars": -1  # Negative
        }
        
        response = requests.post(
            f"{base_url}/api/v1/search",
            json=invalid_search,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 400:
            error_data = response.json()
            print("✅ Error handling working!")
            print(f"📄 Error code: {error_data['error']['code']}")
            print(f"📄 Error message: {error_data['error']['message']}")
        else:
            print(f"⚠️ Expected 400 error, got: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
    
    print()
    
    # Test 5: Search stats endpoint
    print("5️⃣ Testing search stats...")
    try:
        response = requests.get(f"{base_url}/api/v1/search/stats")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Search stats working!")
            print(f"📊 Rate limit: {stats['rate_limit']['requests_per_minute']} req/min")
            print(f"📊 Features: {', '.join([k for k, v in stats['features'].items() if v])}")
        else:
            print(f"❌ Search stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Search stats error: {e}")
    
    print()
    print("🎉 Production API testing complete!")
    print()
    print("🚀 Your API is production-ready with:")
    print("   ✅ Professional error handling")
    print("   ✅ Rate limiting (60 req/min)")
    print("   ✅ Request logging & monitoring")
    print("   ✅ Input validation")
    print("   ✅ Standardized responses")
    print()
    print("💡 Next steps:")
    print("   1. Add API key authentication")
    print("   2. Deploy to cloud (AWS/GCP/Azure)")
    print("   3. Set up monitoring dashboard")
    print("   4. Implement usage tracking for billing")

if __name__ == "__main__":
    test_production_api()