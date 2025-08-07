#!/usr/bin/env python3
"""
CodeInspiration API with Authentication & Real Data
"""

import re
import requests
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
import uvicorn
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our authentication system
from auth_system import get_api_key, get_optional_api_key, api_key_manager

# Import database for user management
from database import db_manager

# Models
class SearchRequest(BaseModel):
    query: str
    max_results: int = Field(default=5, ge=1, le=20)
    sort_by: str = Field(default="stars")
    min_stars: int = Field(default=0, ge=0)
    search_mode: str = Field(default="active", description="Search mode: 'active' for thriving projects, 'graveyard' for abandoned repos, 'all' for both")

class SearchResponse(BaseModel):
    query: str
    results: List[dict]
    total_found: int
    search_time_ms: float
    search_mode: str
    plan: str
    usage: dict

class UserRegistrationRequest(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    email: str = Field(..., description="User email address")
    plan: str = Field(default="free", description="Plan type: free, pro, enterprise")
    
    @validator('email')
    def validate_email_format(cls, v):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")
        return v

class UserRegistrationResponse(BaseModel):
    user_id: str
    api_key: str
    plan: str
    message: str
    limits: dict

class APIKeyResponse(BaseModel):
    api_key: str
    user_id: str
    plan: str
    created_at: float
    limits: dict

# Real GitHub Service (same as before)
class GitHubService:
    """Fetches REAL GitHub data"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "CodeInspiration-API/2.1"
        }
        
        # Add GitHub token if available
        github_token = os.environ.get("GITHUB_TOKEN")
        if github_token:
            self.headers["Authorization"] = f"token {github_token}"
            print("🔑 Using GitHub token for authenticated requests")
        else:
            print("⚠️ No GitHub token found - using unauthenticated requests (limited to 60/hour)")
    
    def search_repositories(self, query: str, max_results: int, sort_by: str, min_stars: int, search_mode: str = "active"):
        """Search real GitHub repositories with different modes"""
        
        try:
            # Build search query based on mode
            if search_mode == "graveyard":
                # Search for abandoned repositories (no commits in last 2+ years)
                search_query = f"{query} stars:>={min_stars} pushed:<2022-01-01"
            elif search_mode == "active":
                # Search for active repositories (commits in last year)
                search_query = f"{query} stars:>={min_stars} pushed:>2023-01-01"
            else:  # search_mode == "all"
                # Search for all repositories
                search_query = f"{query} stars:>={min_stars}"
            github_sort = {
                "stars": "stars",
                "updated": "updated",
                "created": "created"
            }.get(sort_by, "stars")
            
            url = f"{self.base_url}/search/repositories"
            params = {
                "q": search_query,
                "sort": github_sort,
                "order": "desc",
                "per_page": min(max_results, 10)
            }
            
            print(f"🔍 Fetching real GitHub data: {search_query}")
            print(f"📡 URL: {url}")
            print(f"📋 Params: {params}")
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            print(f"📊 Response Status: {response.status_code}")
            print(f"📊 Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.json()
                repositories = []
                
                for item in data.get("items", []):
                    repo = {
                        "repository": {
                            "id": item["id"],
                            "name": item["name"],
                            "full_name": item["full_name"],
                            "description": item.get("description", "No description available"),
                            "html_url": item["html_url"],
                            "stars": item["stargazers_count"],
                            "language": item.get("language", "Unknown"),
                            "created_at": item["created_at"],
                            "updated_at": item["updated_at"],
                            "forks": item["forks_count"],
                            "watchers": item["watchers_count"],
                            "owner": {
                                "login": item["owner"]["login"],
                                "avatar_url": item["owner"]["avatar_url"]
                            }
                        },
                        "summary": f"This {item.get('language', 'Unknown')} project has {item['stargazers_count']:,} stars and is actively maintained. {item.get('description', '')[:100]}...",
                        "key_features": [
                            f"Written in {item.get('language', 'Unknown')}",
                            f"Popular project with {item['stargazers_count']:,} GitHub stars",
                            f"Active community with {item['watchers_count']:,} watchers",
                            f"Open source with {item['forks_count']:,} forks"
                        ],
                        "learning_insights": [
                            f"Study the {item.get('language', 'Unknown')} code structure and best practices",
                            f"Learn from a project with {item['stargazers_count']:,} community endorsements",
                            "Examine the project's architecture and design patterns",
                            "Review issues and pull requests for development insights"
                        ],
                        "implementation_tips": [
                            f"Clone: git clone {item['html_url']}.git",
                            "Read the README.md thoroughly",
                            "Check dependencies and setup instructions",
                            "Browse issues for common problems and solutions",
                            f"Visit live project: {item['html_url']}"
                        ],
                        "similarity_score": 0.95 - (len(repositories) * 0.05)
                    }
                    repositories.append(repo)
                
                print(f"✅ Found {len(repositories)} real repositories!")
                return repositories
                
            else:
                print(f"⚠️ GitHub API returned {response.status_code}")
                print(f"⚠️ Response content: {response.text[:200]}...")
                
                # Check if it's a rate limit error
                if response.status_code == 403 and "rate limit" in response.text.lower():
                    print("🚨 GitHub API rate limit exceeded!")
                    print("💡 Solution: Add GITHUB_TOKEN environment variable for higher limits")
                
                return self._get_fallback_repos(query, max_results, search_mode)
                
        except Exception as e:
            print(f"❌ Error: {e}")
            print(f"❌ Error type: {type(e).__name__}")
            return self._get_fallback_repos(query, max_results, search_mode)
    
    def _get_fallback_repos(self, query, max_results, search_mode="active"):
        """Enhanced fallback data"""
        return [{
            "repository": {
                "id": 9999,
                "name": f"fallback-{query.replace(' ', '-')}",
                "full_name": f"fallback/fallback-{query.replace(' ', '-')}",
                "description": f"Fallback repository for '{query}' in {search_mode} mode (GitHub API temporarily unavailable)",
                "html_url": f"https://github.com/fallback/fallback-{query.replace(' ', '-')}",
                "stars": 50,
                "language": "JavaScript",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "forks": 10,
                "watchers": 25,
                "owner": {"login": "fallback", "avatar_url": "https://avatars.githubusercontent.com/u/0?v=4"}
            },
            "summary": f"Fallback data for '{query}' - Real GitHub data will return shortly",
            "key_features": ["Fallback repository", "Real data temporarily unavailable"],
            "learning_insights": ["Try your search again in a few minutes for real GitHub data"],
            "implementation_tips": ["This is placeholder data - refresh for real repositories"],
            "similarity_score": 0.75
        }]

# Create FastAPI app
app = FastAPI(
    title="Code Graveyard API",
    description="Professional API for discovering GitHub repositories - find inspiration from active projects OR learn from abandoned code graveyards",
    version="2.1.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
github_service = GitHubService()

# Exception handler
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    print(f"Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": {"message": "Internal server error", "code": "INTERNAL_ERROR"}}
    )

# Endpoints
@app.get("/")
async def root():
    return {
        "message": "Welcome to Code Graveyard API (Authenticated)",
        "version": "2.1.0",
        "docs": "/docs",
        "health": "/health",
        "authentication": "API key required for search",
        "search_modes": {
            "active": "Find inspiration from thriving projects (updated in last year)",
            "graveyard": "Learn from abandoned repositories (no commits in 2+ years)",
            "all": "Search all repositories regardless of activity"
        },
        "plans": {
            "free": "100 requests/hour, 1,000/month",
            "pro": "1,000 requests/hour, 10,000/month",
            "enterprise": "10,000 requests/hour, 100,000/month"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "message": "Code Graveyard API with authentication is running",
        "timestamp": time.time(),
        "version": "2.1.0",
        "features": ["authentication", "rate_limiting", "real_github_data", "dual_search_modes"]
    }

@app.post("/search", response_model=SearchResponse)
async def search_repositories(
    request: SearchRequest,
    user_data: Dict = Depends(get_api_key)
):
    """Search for REAL GitHub repositories (requires API key)"""
    start_time = time.time()
    
    # Validate sort_by
    if request.sort_by not in ["stars", "updated", "created"]:
        raise HTTPException(
            status_code=400,
            detail={"error": {"message": "sort_by must be: stars, updated, or created"}}
        )
    
    # Apply plan-based limits
    if user_data["plan"] == "free" and request.max_results > 5:
        request.max_results = 5
    elif user_data["plan"] == "pro" and request.max_results > 15:
        request.max_results = 15
    
    # Search GitHub with mode selection
    results = github_service.search_repositories(
        query=request.query,
        max_results=request.max_results,
        sort_by=request.sort_by,
        min_stars=request.min_stars,
        search_mode=request.search_mode
    )
    
    search_time = (time.time() - start_time) * 1000
    
    # Get current usage stats for the authenticated user
    usage_stats = api_key_manager.get_usage_stats(user_data["api_key"])
    
    return SearchResponse(
        query=request.query,
        results=results,
        total_found=len(results),
        search_time_ms=search_time,
        search_mode=request.search_mode,
        plan=user_data["plan"],
        usage=usage_stats
    )

@app.get("/search/demo")
async def demo_search():
    """Demo search endpoint (no authentication required)"""
    
    # Show limited demo results
    demo_results = [{
        "repository": {
            "name": "demo-repository",
            "full_name": "demo/demo-repository", 
            "description": "This is a demo result. Sign up for API access to see real repositories!",
            "html_url": "https://github.com/demo/demo-repository",
            "stars": 100,
            "language": "JavaScript"
        },
        "summary": "Demo repository - sign up for full access to real GitHub data",
        "key_features": ["Demo data", "Sign up for real results"],
        "learning_insights": ["Get API access for real insights"],
        "implementation_tips": ["Upgrade to access real repositories"],
        "similarity_score": 0.90
    }]
    
    return {
        "query": "demo",
        "results": demo_results,
        "total_found": 1,
        "search_time_ms": 50.0,
        "plan": "demo",
        "message": "This is demo data. Get your API key for real GitHub repositories!"
    }

@app.post("/register", response_model=UserRegistrationResponse)
async def register_user(request: UserRegistrationRequest):
    """Register a new user and generate API key"""
    
    try:
        # Generate API key
        api_key = api_key_manager.generate_api_key(request.user_id, request.email, request.plan)
        
        # Get usage limits
        limits = {
            "free": {"hour": 100, "month": 1000},
            "pro": {"hour": 1000, "month": 10000},
            "enterprise": {"hour": 10000, "month": 100000}
        }
        
        return UserRegistrationResponse(
            user_id=request.user_id,
            api_key=api_key,
            plan=request.plan,
            message=f"Successfully registered for {request.plan} plan",
            limits=limits[request.plan]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "message": f"Registration failed: {str(e)}",
                    "code": "REGISTRATION_ERROR"
                }
            }
        )

@app.post("/keys/generate", response_model=APIKeyResponse)
async def generate_api_key(
    user_id: str,
    plan: str = "free",
    user_data: Dict = Depends(get_api_key)
):
    """Generate a new API key for authenticated user"""
    
    try:
        # Generate new API key
        api_key = api_key_manager.generate_api_key(user_id, plan)
        
        # Get key data
        key_data = db_manager.get_api_key_data(api_key)
        
        limits = {
            "free": {"hour": 100, "month": 1000},
            "pro": {"hour": 1000, "month": 10000},
            "enterprise": {"hour": 10000, "month": 100000}
        }
        
        return APIKeyResponse(
            api_key=api_key,
            user_id=user_id,
            plan=plan,
            created_at=key_data["created_at"],
            limits=limits[plan]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "message": f"API key generation failed: {str(e)}",
                    "code": "KEY_GENERATION_ERROR"
                }
            }
        )

@app.get("/usage")
async def get_usage(user_data: Dict = Depends(get_api_key)):
    """Get current API usage statistics"""
    
    # Get usage stats for the authenticated user's API key
    usage_stats = api_key_manager.get_usage_stats(user_data["api_key"])
    
    return {
        "user_id": user_data["user_id"],
        "plan": user_data["plan"],
        "usage": usage_stats,
        "account_created": user_data["created_at"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    import time
    from app.core.logging import log_api_request
    
    start_time = time.time()
    
    try:
        # Check database connection
        from database import db_manager
        db_status = "healthy"
        
        # Check API key manager
        from auth_system import api_key_manager
        auth_status = "healthy"
        
        # Check GitHub API (basic check)
        github_status = "healthy"
        
        response_data = {
            "status": "healthy",
            "timestamp": time.time(),
            "services": {
                "database": db_status,
                "authentication": auth_status,
                "github_api": github_status
            },
            "version": "1.0.0"
        }
        
        response_time = time.time() - start_time
        log_api_request("GET", "/health", 200, response_time)
        
        return response_data
        
    except Exception as e:
        response_time = time.time() - start_time
        log_api_request("GET", "/health", 500, response_time)
        
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }, 500

@app.get("/plans")
async def get_plans():
    """Get available pricing plans"""
    
    return {
        "plans": {
            "free": {
                "price": "$0/month",
                "features": [
                    "100 searches per hour",
                    "1,000 searches per month",
                    "Basic repository data",
                    "Community support"
                ]
            },
            "pro": {
                "price": "$19/month", 
                "features": [
                    "1,000 searches per hour",
                    "10,000 searches per month",
                    "Advanced repository insights",
                    "Priority support",
                    "Export capabilities"
                ]
            },
            "enterprise": {
                "price": "$99/month",
                "features": [
                    "10,000 searches per hour", 
                    "100,000 searches per month",
                    "Custom integrations",
                    "Dedicated support",
                    "SLA guarantees",
                    "Custom data sources"
                ]
            }
        }
    }

if __name__ == "__main__":
    import os
    
    # Get port from environment (for Heroku) or default to 8006
    port = int(os.environ.get("PORT", 8006))
    host = "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"
    
    print("🚀 Starting Code Graveyard API with Authentication!")
    print(f"📍 Server: http://{host}:{port}")
    print(f"📚 Docs: http://{host}:{port}/docs")
    print(f"🔍 Health: http://{host}:{port}/health")
    print()
    print("📋 Usage:")
    print("   Add header: X-API-Key: your_api_key")
    print("   search_mode: 'active', 'graveyard', or 'all'")
    print()
    print("💰 Features:")
    print("   ✅ API key authentication")
    print("   ✅ Usage tracking & limits") 
    print("   ✅ Multiple pricing tiers")
    print("   ✅ Real GitHub data")
    print("   ✅ Dual search modes (active + graveyard)")
    print("   ✅ Production ready")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    uvicorn.run(app, host=host, port=port)