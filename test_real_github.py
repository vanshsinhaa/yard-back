#!/usr/bin/env python3
"""
Simple test for real GitHub API (no async)
"""

import requests
import json

def test_github_search():
    """Test real GitHub API directly"""
    
    print("🔍 Testing REAL GitHub API")
    print("=" * 40)
    
    # Test search
    query = "liquid glass ui"
    url = "https://api.github.com/search/repositories"
    
    params = {
        "q": f"{query} stars:>=5",
        "sort": "stars",
        "order": "desc",
        "per_page": 3
    }
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "CodeInspiration-API/1.0"
    }
    
    print(f"🔍 Searching GitHub for: '{query}'")
    print(f"📍 URL: {url}")
    print(f"📋 Query: {params['q']}")
    print()
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            total_count = data.get("total_count", 0)
            items = data.get("items", [])
            
            print(f"✅ SUCCESS! Found {total_count} total repositories")
            print(f"📦 Showing first {len(items)} results:")
            print()
            
            for i, repo in enumerate(items, 1):
                print(f"🏆 Result {i}: {repo['full_name']}")
                print(f"   ⭐ Stars: {repo['stargazers_count']:,}")
                print(f"   💬 Description: {repo.get('description', 'No description')}")
                print(f"   🔗 URL: {repo['html_url']}")
                print(f"   💻 Language: {repo.get('language', 'Unknown')}")
                print(f"   📅 Updated: {repo['updated_at'][:10]}")
                print(f"   👥 Forks: {repo['forks_count']:,}")
                print()
            
            print("🎉 REAL GITHUB DATA IS WORKING!")
            print()
            print("💡 Difference from mock data:")
            print("   ✅ Real repository names and descriptions")
            print("   ✅ Actual star counts and statistics") 
            print("   ✅ Real GitHub URLs you can visit")
            print("   ✅ Genuine project information")
            
        elif response.status_code == 403:
            print("❌ Rate limit exceeded - GitHub API limits requests")
            print("💡 Solution: Add GitHub token or wait an hour")
            
        elif response.status_code == 422:
            print("❌ Invalid search query")
            
        else:
            print(f"❌ GitHub API error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_github_search()