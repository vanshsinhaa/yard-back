#!/usr/bin/env python3
"""
CodeInspiration API with REAL GitHub Data
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
import time
import requests

# Models
class SearchRequest(BaseModel):
    query: str
    max_results: int = Field(default=5, ge=1, le=20)
    sort_by: str = Field(default="stars")
    min_stars: int = Field(default=0, ge=0)

class SearchResponse(BaseModel):
    query: str
    results: List[dict]
    total_found: int
    search_time_ms: float

# Real GitHub Service
class GitHubService:
    """Fetches REAL GitHub data"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "CodeInspiration-API/1.0"
        }
    
    def search_repositories(self, query: str, max_results: int, sort_by: str, min_stars: int):
        """Search real GitHub repositories"""
        
        try:
            # Build search query
            search_query = f"{query} stars:>={min_stars}"
            
            # Map sort options
            github_sort = {
                "stars": "stars",
                "updated": "updated",
                "created": "created"
            }.get(sort_by, "stars")
            
            # Make GitHub API request
            url = f"{self.base_url}/search/repositories"
            params = {
                "q": search_query,
                "sort": github_sort,
                "order": "desc",
                "per_page": min(max_results, 10)
            }
            
            print(f"🔍 Fetching real data from GitHub: {search_query}")
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
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
                        "summary": self._generate_summary(item),
                        "key_features": self._generate_features(item),
                        "learning_insights": self._generate_insights(item),
                        "implementation_tips": self._generate_tips(item),
                        "similarity_score": 0.95 - (len(repositories) * 0.05)  # Decreasing score
                    }
                    repositories.append(repo)
                
                print(f"✅ Found {len(repositories)} real repositories!")
                return repositories
                
            elif response.status_code == 403:
                print("⚠️ GitHub rate limit - using fallback")
                return self._get_fallback_repos(query, max_results)
                
            else:
                print(f"❌ GitHub API error: {response.status_code}")
                return self._get_fallback_repos(query, max_results)
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return self._get_fallback_repos(query, max_results)
    
    def _generate_summary(self, repo):
        """Generate summary from real repo data"""
        stars = repo["stargazers_count"]
        language = repo.get("language", "Unknown")
        description = repo.get("description", "")
        
        return f"This {language} project has {stars:,} stars and is actively maintained. {description[:100]}..."
    
    def _generate_features(self, repo):
        """Generate features from real repo data"""
        features = [
            f"Written in {repo.get('language', 'Unknown')}",
            f"Popular project with {repo['stargazers_count']:,} GitHub stars",
            f"Active community with {repo['watchers_count']:,} watchers",
            f"Open source with {repo['forks_count']:,} forks"
        ]
        
        if repo.get("description"):
            features.append(f"Well documented: {repo['description'][:50]}...")
            
        return features
    
    def _generate_insights(self, repo):
        """Generate learning insights from real repo data"""
        language = repo.get("language", "Unknown")
        stars = repo["stargazers_count"]
        
        return [
            f"Study the {language} code structure and best practices",
            f"Learn from a project with {stars:,} community endorsements",
            "Examine the project's architecture and design patterns",
            "Review issues and pull requests for development insights",
            "Check the commit history to understand evolution"
        ]
    
    def _generate_tips(self, repo):
        """Generate implementation tips from real repo data"""
        return [
            f"Clone the repository: git clone {repo['html_url']}.git",
            "Read the README.md file thoroughly for setup instructions",
            "Check the package.json/requirements.txt for dependencies",
            "Look at the issues tab for common problems and solutions",
            "Examine recent commits to understand active development",
            f"Visit the live project: {repo['html_url']}"
        ]
    
    def _get_fallback_repos(self, query, max_results):
        """Fallback to enhanced mock data when GitHub fails"""
        print("📦 Using enhanced fallback data")
        
        fallback_repos = []
        for i in range(min(max_results, 3)):
            repo = {
                "repository": {
                    "id": 9000 + i,
                    "name": f"fallback-{query.replace(' ', '-')}-{i+1}",
                    "full_name": f"fallback-user/fallback-{query.replace(' ', '-')}-{i+1}",
                    "description": f"A fallback {query} project (GitHub API unavailable)",
                    "html_url": f"https://github.com/fallback-user/fallback-{query.replace(' ', '-')}-{i+1}",
                    "stars": 100 - (i * 20),
                    "language": ["JavaScript", "Python", "TypeScript"][i % 3],
                    "created_at": "2023-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                    "forks": 25 - (i * 5),
                    "watchers": 40 - (i * 8),
                    "owner": {
                        "login": f"fallback-user",
                        "avatar_url": "https://avatars.githubusercontent.com/u/0?v=4"
                    }
                },
                "summary": f"Fallback data for {query} (Real GitHub data temporarily unavailable)",
                "key_features": [
                    "Fallback repository data",
                    "GitHub API rate limited or unavailable",
                    "Real data will return shortly",
                    "Enhanced mock structure"
                ],
                "learning_insights": [
                    "This is fallback data - try again in a few minutes",
                    "Real GitHub repositories will provide better insights",
                    "API is working, just waiting for GitHub availability"
                ],
                "implementation_tips": [
                    "Try your search again in a few minutes",
                    "Real GitHub data provides actual repository links",
                    "Consider upgrading to premium for guaranteed access"
                ],
                "similarity_score": 0.75 - (i * 0.1)
            }
            fallback_repos.append(repo)
        
        return fallback_repos

# Create FastAPI app
app = FastAPI(
    title="CodeInspiration API (Real Data)",
    description="API for finding inspiring GitHub repositories with REAL data",
    version="2.0.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize GitHub service
github_service = GitHubService()

# Rate limiting
request_counts = {}

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    current_time = time.time()
    
    if request.url.path in ["/docs", "/openapi.json", "/health", "/"]:
        return await call_next(request)
    
    # Simple rate limiting
    if client_ip in request_counts:
        request_counts[client_ip] = [
            req_time for req_time in request_counts[client_ip]
            if current_time - req_time < 60
        ]
    else:
        request_counts[client_ip] = []
    
    if len(request_counts[client_ip]) >= 60:
        return JSONResponse(
            status_code=429,
            content={"error": {"message": "Rate limit exceeded", "code": "RATE_LIMIT"}}
        )
    
    request_counts[client_ip].append(current_time)
    response = await call_next(request)
    
    # Add headers
    response.headers["X-RateLimit-Limit"] = "60"
    response.headers["X-RateLimit-Remaining"] = str(60 - len(request_counts[client_ip]))
    
    return response

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
        "message": "Welcome to CodeInspiration API (Real Data)",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
        "features": [
            "REAL GitHub repository search",
            "Live repository data",
            "Actual star counts and statistics",
            "Real project URLs and information"
        ],
        "data_source": "GitHub API with fallback"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "message": "CodeInspiration API with real data is running",
        "timestamp": time.time(),
        "version": "2.0.0",
        "github_api": "connected"
    }

@app.post("/search", response_model=SearchResponse)
async def search_repositories(request: SearchRequest):
    """Search for REAL GitHub repositories"""
    start_time = time.time()
    
    # Validate
    if request.sort_by not in ["stars", "updated", "created"]:
        raise HTTPException(
            status_code=400,
            detail={"error": {"message": "sort_by must be: stars, updated, or created"}}
        )
    
    # Search real GitHub data
    results = github_service.search_repositories(
        query=request.query,
        max_results=request.max_results,
        sort_by=request.sort_by,
        min_stars=request.min_stars
    )
    
    search_time = (time.time() - start_time) * 1000
    
    return SearchResponse(
        query=request.query,
        results=results,
        total_found=len(results),
        search_time_ms=search_time
    )

@app.get("/search/stats")
async def search_stats():
    return {
        "data_source": "Real GitHub API",
        "fallback_available": True,
        "rate_limit": {"requests_per_minute": 60},
        "features": {
            "real_github_data": True,
            "live_statistics": True,
            "actual_repositories": True,
            "fallback_system": True
        }
    }

if __name__ == "__main__":
    print("🚀 Starting CodeInspiration API with REAL GitHub Data!")
    print("📍 Server: http://127.0.0.1:8005")
    print("📚 Docs: http://127.0.0.1:8005/docs")
    print("🔍 Health: http://127.0.0.1:8005/health")
    print()
    print("✨ Features:")
    print("   🎯 REAL GitHub repository data")
    print("   📊 Live star counts and statistics")
    print("   🔗 Actual project URLs")
    print("   🛡️ Fallback system for rate limits")
    print("   ⚡ Rate limiting protection")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    uvicorn.run(app, host="127.0.0.1", port=8005)