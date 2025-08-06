#!/usr/bin/env python3
"""
Simple search demo for CodeInspiration API
"""

import requests
import json

def test_search():
    """Show how to search with the API"""
    
    print("🔍 CodeInspiration API - Search Demo")
    print("=" * 50)
    
    # First, let's start with a simple working example
    api_url = "http://127.0.0.1:8004"  # Make sure server is running on this port
    
    # Search examples
    searches = [
        {
            "query": "react todo app",
            "max_results": 3,
            "sort_by": "stars",
            "min_stars": 10
        },
        {
            "query": "python machine learning",
            "max_results": 2,
            "sort_by": "updated",
            "min_stars": 5
        },
        {
            "query": "vue.js dashboard",
            "max_results": 1,
            "sort_by": "created",
            "min_stars": 0
        }
    ]
    
    print("📍 API URL:", api_url)
    print("📍 Search Endpoint:", f"{api_url}/search")
    print("📍 Interactive Docs:", f"{api_url}/docs")
    print()
    
    for i, search_data in enumerate(searches, 1):
        print(f"🔍 Search {i}: '{search_data['query']}'")
        print(f"   Parameters:")
        print(f"     • Max results: {search_data['max_results']}")
        print(f"     • Sort by: {search_data['sort_by']}")
        print(f"     • Min stars: {search_data['min_stars']}")
        
        try:
            # Make the search request
            response = requests.post(
                f"{api_url}/search",
                json=search_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success! Found {result['total_found']} repositories")
                print(f"   ⏱️ Response time: {result['search_time_ms']:.1f}ms")
                
                # Show first result
                if result['results']:
                    repo = result['results'][0]['repository']
                    summary = result['results'][0]
                    print(f"   📦 Top result: {repo['full_name']}")
                    print(f"   ⭐ Stars: {repo['stars']}")
                    print(f"   💬 Description: {repo['description']}")
                    print(f"   🔗 URL: {repo['html_url']}")
                    print(f"   📊 Similarity: {summary['similarity_score']:.2f}")
                    print(f"   💡 Key feature: {summary['key_features'][0]}")
                
            elif response.status_code == 429:
                print("   ⚠️ Rate limit exceeded - wait a minute and try again")
                
            elif response.status_code == 400:
                error = response.json()
                print(f"   ❌ Bad request: {error['error']['message']}")
                
            else:
                print(f"   ❌ Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Can't connect to API - server not running?")
            print(f"   💡 Start server with: python simple_production_api.py")
            break
            
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
        
        print()
    
    print("🎯 How to Search:")
    print("1. Start the server: python simple_production_api.py")
    print("2. Visit http://127.0.0.1:8004/docs for interactive interface")
    print("3. Or use curl/code like this demo")
    print("4. Try different queries like:")
    print("   • 'django rest api'")
    print("   • 'react native app'") 
    print("   • 'python data science'")
    print("   • 'nodejs express server'")

if __name__ == "__main__":
    test_search()