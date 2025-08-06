#!/usr/bin/env python3
"""
Final demonstration of the Production CodeInspiration API
"""

import requests
import json
import time

def demo_api():
    """Demonstrate all API capabilities"""
    
    base_url = "http://127.0.0.1:8005"
    
    print("🎯 CodeInspiration API - PRODUCTION DEMO")
    print("=" * 60)
    
    # Test 1: Root endpoint
    print("1️⃣ API Overview...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ API is live and ready!")
            print(f"📦 Version: {data['version']}")
            print(f"🚀 Features:")
            for feature in data['features']:
                print(f"    • {feature}")
        else:
            print(f"❌ API not responding: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return
    
    print()
    
    # Test 2: Health check
    print("2️⃣ Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ {health['message']}")
            print(f"📊 Status: {health['status']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    print()
    
    # Test 3: Search functionality
    print("3️⃣ Search Demo...")
    search_queries = [
        {"query": "react todo app", "max_results": 2},
        {"query": "python machine learning", "max_results": 3},
        {"query": "vue dashboard", "max_results": 1}
    ]
    
    for i, search_data in enumerate(search_queries, 1):
        print(f"\n   Search {i}: '{search_data['query']}'")
        try:
            response = requests.post(
                f"{base_url}/search",
                json=search_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Found {result['total_found']} repositories")
                print(f"   ⏱️ Response time: {result['search_time_ms']:.1f}ms")
                
                # Show first result
                if result['results']:
                    repo = result['results'][0]['repository']
                    print(f"   📦 Top result: {repo['full_name']} ({repo['stars']} ⭐)")
                    
                # Check rate limiting headers
                if 'X-RateLimit-Remaining' in response.headers:
                    print(f"   🚦 Rate limit remaining: {response.headers['X-RateLimit-Remaining']}")
                    
            else:
                print(f"   ❌ Search failed: {response.status_code}")
                print(f"   📄 Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Search error: {e}")
    
    print()
    
    # Test 4: Error handling
    print("4️⃣ Error Handling Demo...")
    try:
        invalid_search = {
            "query": "x",  # Too short
            "max_results": 50,  # Too many
            "sort_by": "invalid"  # Invalid
        }
        
        response = requests.post(
            f"{base_url}/search",
            json=invalid_search,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 400:
            error = response.json()
            print("✅ Error handling working perfectly!")
            print(f"📄 Error code: {error['error']['code']}")
            print(f"📄 Message: {error['error']['message']}")
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
    
    print()
    
    # Test 5: API Stats
    print("5️⃣ API Statistics...")
    try:
        response = requests.get(f"{base_url}/search/stats")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Statistics endpoint working!")
            print(f"🚦 Rate limit: {stats['rate_limit']['requests_per_minute']} requests/minute")
            print("📊 Active features:")
            for feature, enabled in stats['features'].items():
                status = "✅" if enabled else "❌"
                print(f"    {status} {feature.replace('_', ' ').title()}")
        else:
            print(f"❌ Stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Stats error: {e}")
    
    print()
    print("🎉 PRODUCTION API DEMO COMPLETE!")
    print("=" * 60)
    print()
    print("📋 WHAT YOU'VE BUILT:")
    print("✅ Professional REST API")
    print("✅ Rate limiting (60 req/min)")
    print("✅ Error handling & validation")
    print("✅ Structured JSON responses")
    print("✅ API documentation (/docs)")
    print("✅ Health monitoring")
    print("✅ CORS support")
    print()
    print("💰 MONETIZATION-READY:")
    print("🔑 Add API key authentication")
    print("📊 Implement usage tracking")
    print("💳 Set up pricing tiers")
    print("☁️ Deploy to cloud platform")
    print()
    print("🚀 NEXT STEPS:")
    print("1. Visit http://127.0.0.1:8005/docs for interactive API docs")
    print("2. Test different search queries")
    print("3. Add your GitHub API token for real data")
    print("4. Deploy to production!")

if __name__ == "__main__":
    demo_api()