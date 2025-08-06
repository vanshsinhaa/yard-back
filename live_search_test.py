#!/usr/bin/env python3
"""
Live search test - Use while server is running!
"""

import requests
import json

def search_now():
    """Search immediately with your running server"""
    
    print("🔍 LIVE SEARCH TEST")
    print("=" * 40)
    print("📍 Server: http://127.0.0.1:8004")
    print("📍 Status: Server should be running!")
    print()
    
    # Test search
    search_data = {
        "query": "python machine learning",
        "max_results": 2,
        "sort_by": "stars",
        "min_stars": 5
    }
    
    print(f"🔍 Searching for: '{search_data['query']}'")
    
    try:
        response = requests.post(
            "http://127.0.0.1:8004/search",
            json=search_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS! Found {result['total_found']} repositories")
            print(f"⏱️ Search time: {result['search_time_ms']:.1f}ms")
            print()
            
            # Show results
            for i, item in enumerate(result['results'], 1):
                repo = item['repository']
                print(f"📦 Result {i}: {repo['full_name']}")
                print(f"   ⭐ Stars: {repo['stars']}")
                print(f"   💬 Description: {repo['description']}")
                print(f"   🔗 URL: {repo['html_url']}")
                print(f"   🎯 Similarity: {item['similarity_score']:.2f}")
                print(f"   💡 Key Features:")
                for feature in item['key_features']:
                    print(f"      • {feature}")
                print()
            
            print("🎉 YOUR API IS WORKING PERFECTLY!")
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Can't connect - make sure server is running on port 8004")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    search_now()