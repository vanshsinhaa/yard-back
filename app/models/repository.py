from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class Repository(BaseModel):
    """GitHub repository data model for inspiration search"""
    id: int
    name: str
    full_name: str
    description: Optional[str] = None
    html_url: str
    stargazers_count: int = Field(alias="stars")
    language: Optional[str] = None
    updated_at: datetime
    created_at: datetime
    pushed_at: datetime
    archived: bool = False
    disabled: bool = False
    fork: bool = False
    readme_content: Optional[str] = None
    last_commit_date: Optional[datetime] = None
    inspiration_score: Optional[float] = None
    
    class Config:
        populate_by_name = True

class SearchRequest(BaseModel):
    """Request model for repository search"""
    query: str = Field(..., description="User's project idea or search query")
    max_results: int = Field(default=5, ge=1, le=20, description="Maximum number of results to return")
    sort_by: str = Field(default="stars", description="Sort criteria (stars, updated, created)")
    min_stars: int = Field(default=0, description="Minimum star count filter")
    search_mode: str = Field(default="active", description="Search mode: 'active' for thriving projects, 'graveyard' for abandoned repos, 'all' for both")

class RepositorySummary(BaseModel):
    """Repository with AI-generated analysis and learning insights"""
    repository: Repository
    summary: str = Field(..., description="AI-generated summary of what the repository does")
    key_features: List[str] = Field(..., description="Key features and technologies used")
    learning_insights: List[str] = Field(..., description="What you can learn from this repository")
    implementation_tips: List[str] = Field(..., description="Tips for implementing similar features")
    similarity_score: float = Field(..., description="Similarity score between user query and repository")

class SearchResponse(BaseModel):
    """Response model for repository search"""
    query: str
    results: List[RepositorySummary]
    total_found: int
    search_time_ms: float
    search_mode: str = Field(..., description="Search mode used: active, graveyard, or all") 