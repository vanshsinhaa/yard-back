#!/usr/bin/env python3
"""
GitHub Token Setup Script
Helps you get a GitHub Personal Access Token for higher API limits
"""

import os
import webbrowser

def setup_github_token():
    """Guide user through GitHub token setup"""
    
    print("🔑 GitHub Token Setup")
    print("=" * 50)
    print()
    print("GitHub API has rate limits:")
    print("❌ Unauthenticated: 60 requests/hour (you've hit this)")
    print("✅ Authenticated: 5,000 requests/hour")
    print()
    print("To get a GitHub Personal Access Token:")
    print()
    print("1. Go to GitHub Settings > Developer settings > Personal access tokens")
    print("2. Click 'Generate new token (classic)'")
    print("3. Give it a name like 'CodeInspiration API'")
    print("4. Select scopes: 'public_repo' (for public repository access)")
    print("5. Click 'Generate token'")
    print("6. Copy the token (you won't see it again!)")
    print()
    
    # Open GitHub token page
    open_github = input("Open GitHub token page in browser? (y/n): ").lower()
    if open_github == 'y':
        webbrowser.open("https://github.com/settings/tokens")
    
    print()
    print("Once you have your token:")
    print("1. Create a .env file in this directory")
    print("2. Add: GITHUB_TOKEN=your_token_here")
    print("3. Restart the API server")
    print()
    
    # Check if .env exists
    if os.path.exists('.env'):
        print("✅ .env file exists")
        with open('.env', 'r') as f:
            content = f.read()
            if 'GITHUB_TOKEN' in content:
                print("✅ GITHUB_TOKEN found in .env")
            else:
                print("❌ GITHUB_TOKEN not found in .env")
                print("Add: GITHUB_TOKEN=your_token_here")
    else:
        print("❌ .env file not found")
        print("Create .env file with: GITHUB_TOKEN=your_token_here")
    
    print()
    print("After adding the token, restart your API server!")
    print("The API will then use 5,000 requests/hour instead of 60!")

if __name__ == "__main__":
    setup_github_token() 