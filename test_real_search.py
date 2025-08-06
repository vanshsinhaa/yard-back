#!/usr/bin/env python3
"""
Test the real data search API
"""

import requests

def test_real_search():
    """Test the real GitHub search"""
    
    print("🔍 Testing REAL GitHub Data API")
    print("=" * 50)
    
    # Test search
    search_data = {
        "query": "liquid glass ui",
        "max_results": 2,
        "sort_by": "stars",
        "min_stars": 5
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:8005/search",
            json=search_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS! Found {result['total_found']} repositories")
            print(f"⏱️ Search time: {result['search_time_ms']:.1f}ms")
            print()
            
            for i, item in enumerate(result['results'], 1):
                repo = item['repository']
                print(f"📦 Result {i}: {repo['full_name']}")
                print(f"   ⭐ Stars: {repo['stars']:,}")
                print(f"   💬 Description: {repo['description']}")
                print(f"   🔗 URL: {repo['html_url']}")
                print(f"   💻 Language: {repo['language']}")
                print(f"   🍴 Forks: {repo['forks']:,}")
                print(f"   👀 Watchers: {repo['watchers']:,}")
                print(f"   🎯 Similarity: {item['similarity_score']:.2f}")
                print()
                print("   🔍 Key Features:")
                for feature in item['key_features']:
                    print(f"      • {feature}")
                print()
                print("   💡 Learning Insights:")
                for insight in item['learning_insights'][:2]:  # Show first 2
                    print(f"      • {insight}")
                print()
            
            print("🎉 YOUR API NOW USES REAL GITHUB DATA!")
            print()
            print("💰 Comparison:")
            print("   Before: Mock/fake repository names")
            print("   Now: REAL GitHub repositories you can visit!")
            print()
            print("🚀 Visit http://127.0.0.1:8005/docs to try more searches!")
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_real_search()