#!/usr/bin/env python3
"""
Minimal CodeInspiration API for testing
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="CodeInspiration API (Test)",
    description="Minimal test version of the API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple models
class SearchRequest(BaseModel):
    query: str
    max_results: int = 5
    sort_by: str = "stars"
    min_stars: int = 0

class Repository(BaseModel):
    id: int
    name: str
    full_name: str
    description: Optional[str] = None
    html_url: str
    stars: int
    language: Optional[str] = None

class SearchResponse(BaseModel):
    query: str
    results: List[Repository]
    total_found: int
    search_time_ms: float

# Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to CodeInspiration API (Test)",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "message": "CodeInspiration API is running"}

@app.post("/search", response_model=SearchResponse)
async def search_repositories(request: SearchRequest):
    """Mock search endpoint for testing"""
    
    # Mock response for testing
    mock_repos = [
        Repository(
            id=1,
            name="test-todo-app",
            full_name="user/test-todo-app",
            description="A test React todo application",
            html_url="https://github.com/user/test-todo-app",
            stars=150,
            language="JavaScript"
        ),
        Repository(
            id=2,
            name="awesome-project",
            full_name="user/awesome-project",
            description="Another test project",
            html_url="https://github.com/user/awesome-project",
            stars=75,
            language="Python"
        )
    ]
    
    return SearchResponse(
        query=request.query,
        results=mock_repos,
        total_found=len(mock_repos),
        search_time_ms=100.0
    )

if __name__ == "__main__":
    print("🚀 Starting Minimal CodeInspiration API...")
    print("📍 Server will be available at: http://127.0.0.1:8002")
    print("📚 API Documentation: http://127.0.0.1:8002/docs")
    print("🔍 Health Check: http://127.0.0.1:8002/health")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8002,
        log_level="info"
    ) 