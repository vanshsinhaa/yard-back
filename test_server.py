#!/usr/bin/env python3
"""
Simple test script to start the server and test API endpoints
"""

import uvicorn
import requests
import time
import json

def test_api():
    """Test the API endpoints"""
    
    # Start the server
    print("🚀 Starting CodeInspiration API server...")
    
    # Test the root endpoint
    try:
        response = requests.get("http://127.0.0.1:8001/")
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"📄 Response: {response.json()}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
    
    # Test the health endpoint
    try:
        response = requests.get("http://127.0.0.1:8001/api/v1/health")
        print(f"✅ Health endpoint: {response.status_code}")
        print(f"📄 Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
    
    # Test the search endpoint
    try:
        search_data = {
            "query": "react todo app",
            "max_results": 3,
            "sort_by": "stars",
            "min_stars": 10
        }
        response = requests.post(
            "http://127.0.0.1:8001/api/v1/search",
            json=search_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Search endpoint: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"📄 Found {result.get('total_found', 0)} repositories")
        else:
            print(f"📄 Error: {response.text}")
    except Exception as e:
        print(f"❌ Search endpoint failed: {e}")

if __name__ == "__main__":
    # Start server in background
    config = uvicorn.Config("app.main:app", host="127.0.0.1", port=8001, log_level="info")
    server = uvicorn.Server(config)
    
    # Run server in a separate thread
    import threading
    server_thread = threading.Thread(target=server.run)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(5)
    
    # Test the API
    test_api()
    
    print("🎉 API testing complete!") 