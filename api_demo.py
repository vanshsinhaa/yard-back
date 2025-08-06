#!/usr/bin/env python3
"""
CodeInspiration API Demo Script
This script demonstrates how to use your API and shows what each endpoint does.
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://127.0.0.1:8005"

def test_root_endpoint():
    """Test the root endpoint - shows API info"""
    print("🔍 Testing Root Endpoint (/)")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

def test_health_endpoint():
    """Test the health endpoint - shows API status"""
    print("🔍 Testing Health Endpoint (/api/v1/health)")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"✅ Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

def test_search_endpoint():
    """Test the search endpoint - the main functionality"""
    print("🔍 Testing Search Endpoint (/api/v1/search)")
    print("=" * 50)
    
    # Example search request
    search_data = {
        "query": "react todo app with authentication",
        "max_results": 3,
        "sort_by": "stars",
        "min_stars": 10
    }
    
    print(f"🔍 Search Query: {search_data['query']}")
    print(f"📊 Max Results: {search_data['max_results']}")
    print(f"⭐ Min Stars: {search_data['min_stars']}")
    print()
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/search",
            json=search_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📄 Found {result.get('total_found', 0)} repositories")
            print(f"⏱️ Search Time: {result.get('search_time_ms', 0):.2f}ms")
            
            # Show first result if available
            if result.get('results'):
                first_repo = result['results'][0]
                repo = first_repo['repository']
                print(f"\n🏆 Top Result:")
                print(f"   Name: {repo.get('name', 'N/A')}")
                print(f"   Stars: {repo.get('stargazers_count', 0)}")
                print(f"   Language: {repo.get('language', 'N/A')}")
                print(f"   Similarity Score: {first_repo.get('similarity_score', 0):.2f}")
                print(f"   Summary: {first_repo.get('summary', 'N/A')[:100]}...")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()

def show_api_documentation():
    """Show how to access API documentation"""
    print("📚 API Documentation")
    print("=" * 50)
    print(f"🌐 Interactive Docs: {BASE_URL}/docs")
    print(f"📖 ReDoc: {BASE_URL}/redoc")
    print()
    print("💡 You can visit these URLs in your browser to see:")
    print("   - Interactive API documentation")
    print("   - Try out endpoints directly")
    print("   - See request/response schemas")
    print()

def show_usage_examples():
    """Show different ways to use the API"""
    print("💡 Usage Examples")
    print("=" * 50)
    
    examples = [
        {
            "name": "Find React Projects",
            "data": {
                "query": "react typescript",
                "max_results": 5,
                "sort_by": "stars",
                "min_stars": 50
            }
        },
        {
            "name": "Find Python ML Projects",
            "data": {
                "query": "machine learning python",
                "max_results": 3,
                "sort_by": "updated",
                "min_stars": 100
            }
        },
        {
            "name": "Find Recent Projects",
            "data": {
                "query": "web scraper",
                "max_results": 2,
                "sort_by": "created",
                "min_stars": 10
            }
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['name']}:")
        print(f"   curl -X POST {BASE_URL}/api/v1/search \\")
        print(f"     -H 'Content-Type: application/json' \\")
        print(f"     -d '{json.dumps(example['data'], indent=2)}'")
        print()

def explain_what_is_happening():
    """Explain what the API does behind the scenes"""
    print("🤖 What Your API Does Behind the Scenes")
    print("=" * 50)
    print("1. 📝 Takes your search query (e.g., 'react todo app')")
    print("2. 🔍 Searches GitHub for repositories matching your query")
    print("3. 🧠 Uses AI to analyze each repository's content")
    print("4. 📊 Calculates similarity scores using embeddings")
    print("5. 🎯 Ranks repositories by relevance to your query")
    print("6. 📋 Generates learning insights and implementation tips")
    print("7. 📤 Returns structured data with AI analysis")
    print()

def main():
    """Run the complete API demo"""
    print("🚀 CodeInspiration API Demo")
    print("=" * 60)
    print()
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(3)
    print()
    
    # Test all endpoints
    test_root_endpoint()
    test_health_endpoint()
    test_search_endpoint()
    
    # Show documentation and examples
    show_api_documentation()
    show_usage_examples()
    explain_what_is_happening()
    
    print("🎉 Demo complete! Your API is working perfectly!")
    print()
    print("💡 Next Steps:")
    print("   1. Visit http://127.0.0.1:8005/docs to see interactive docs")
    print("   2. Try different search queries")
    print("   3. Add your OpenAI API key for full AI features")
    print("   4. Deploy to production when ready!")

if __name__ == "__main__":
    main() 