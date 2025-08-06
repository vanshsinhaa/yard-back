"""
Search API endpoints for CodeInspiration
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
import time

from app.models.repository import SearchRequest, SearchResponse
from app.services.github_search import GitHubSearchService
from app.services.summarize import SummarizationService
from app.core.exceptions import (
    ValidationError, 
    GitHubAPIError, 
    OpenAIAPIError, 
    SearchError
)
from app.core.logging import api_logger, log_performance

# Initialize services (mock for now)
# github_service = GitHubSearchService()
# summarization_service = SummarizationService()

router = APIRouter()


def validate_search_request(request: SearchRequest) -> SearchRequest:
    """Validate search request parameters"""
    
    # Validate query
    if not request.query or len(request.query.strip()) < 2:
        raise ValidationError(
            "Search query must be at least 2 characters long",
            details={"query": request.query}
        )
    
    # Validate max_results
    if request.max_results < 1 or request.max_results > 20:
        raise ValidationError(
            "max_results must be between 1 and 20",
            details={"max_results": request.max_results}
        )
    
    # Validate sort_by
    valid_sort_options = ["stars", "updated", "created"]
    if request.sort_by not in valid_sort_options:
        raise ValidationError(
            f"sort_by must be one of: {', '.join(valid_sort_options)}",
            details={"sort_by": request.sort_by}
        )
    
    # Validate min_stars
    if request.min_stars < 0:
        raise ValidationError(
            "min_stars must be non-negative",
            details={"min_stars": request.min_stars}
        )
    
    return request


@router.post("/search", response_model=SearchResponse)
async def search_repositories(request: SearchRequest):
    """
    Search for inspiring GitHub repositories
    
    This endpoint searches GitHub for repositories matching your query,
    analyzes them using AI, and returns learning insights.
    """
    
    start_time = time.time()
    
    try:
        # Validate request
        validated_request = validate_search_request(request)
        
        # Log search attempt
        api_logger.log_search_query(
            query=validated_request.query,
            results_count=0,  # Will be updated after search
            duration=0
        )
        
        # Mock GitHub search results for now
        mock_repositories = [
            {
                "id": 1,
                "name": f"awesome-{validated_request.query.replace(' ', '-')}",
                "full_name": f"developer/awesome-{validated_request.query.replace(' ', '-')}",
                "description": f"An awesome {validated_request.query} project with great features",
                "html_url": f"https://github.com/developer/awesome-{validated_request.query.replace(' ', '-')}",
                "stars": 150,
                "language": "JavaScript",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            },
            {
                "id": 2,
                "name": f"best-{validated_request.query.replace(' ', '-')}-example",
                "full_name": f"coder/best-{validated_request.query.replace(' ', '-')}-example",
                "description": f"Best practices for {validated_request.query} development",
                "html_url": f"https://github.com/coder/best-{validated_request.query.replace(' ', '-')}-example",
                "stars": 89,
                "language": "Python",
                "created_at": "2023-06-01T00:00:00Z",
                "updated_at": "2024-02-01T00:00:00Z"
            }
        ]
        
        # Limit results
        repositories = mock_repositories[:validated_request.max_results]
        
        if not repositories:
            return SearchResponse(
                query=validated_request.query,
                results=[],
                total_found=0,
                search_time_ms=(time.time() - start_time) * 1000
            )
        
        # Generate mock summaries for each repository
        results = []
        for repo in repositories:
            results.append({
                "repository": repo,
                "summary": f"This is an excellent {validated_request.query} project that demonstrates best practices and modern development techniques.",
                "key_features": [
                    f"Modern {validated_request.query} implementation",
                    "Clean and maintainable code",
                    "Comprehensive documentation",
                    "Active community support"
                ],
                "learning_insights": [
                    f"Learn how to structure a {validated_request.query} project",
                    "Understand modern development patterns",
                    "See real-world implementation examples"
                ],
                "implementation_tips": [
                    "Start with the basic setup",
                    "Follow the project's coding standards",
                    "Review the documentation thoroughly",
                    "Check the issues for common problems"
                ],
                "similarity_score": 0.85
            })
        
        # Calculate total time
        total_time = (time.time() - start_time) * 1000
        
        # Log successful search
        api_logger.log_search_query(
            query=validated_request.query,
            results_count=len(results),
            duration=total_time / 1000
        )
        
        # Log performance metrics
        log_performance(
            operation="search_repositories",
            duration=total_time / 1000,
            details={
                "query": validated_request.query,
                "results_count": len(results),
                "max_results": validated_request.max_results
            }
        )
        
        return SearchResponse(
            query=validated_request.query,
            results=results,
            total_found=len(results),
            search_time_ms=total_time
        )
        
    except ValidationError as e:
        # Re-raise validation errors
        raise e
        
    except GitHubAPIError as e:
        # Log GitHub API errors
        api_logger.log_error(None, e)
        raise e
        
    except OpenAIAPIError as e:
        # Log OpenAI API errors
        api_logger.log_error(None, e)
        raise e
        
    except Exception as e:
        # Log unexpected errors
        api_logger.log_error(None, e)
        raise SearchError(f"Search failed: {str(e)}")


@router.get("/search/stats")
async def get_search_stats():
    """Get search statistics and API usage info"""
    
    return {
        "total_searches": 0,  # TODO: Implement counter
        "average_response_time_ms": 0,  # TODO: Implement tracking
        "rate_limit": {
            "requests_per_minute": 60,
            "remaining_requests": 60  # TODO: Implement tracking
        },
        "features": {
            "github_search": True,
            "ai_analysis": True,
            "semantic_search": False  # TODO: Implement
        }
    } 