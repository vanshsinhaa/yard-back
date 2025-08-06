import httpx
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from dateutil import parser
import time

from app.core.config import settings
from app.models.repository import Repository

class GitHubSearchService:
    """Service for searching and fetching GitHub repositories for inspiration"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "CodeInspiration/1.0"
        }
        
        if settings.github_token:
            self.headers["Authorization"] = f"token {settings.github_token}"
    
    async def search_repositories(self, query: str, max_results: int = 20, 
                                sort_by: str = "stars", min_stars: int = 0, 
                                search_mode: str = "active") -> List[Repository]:
        """
        Search for repositories on GitHub based on query and mode
        
        Args:
            query: Search query string
            max_results: Maximum number of repositories to return
            sort_by: Sort criteria (stars, updated, created)
            min_stars: Minimum star count filter
            search_mode: 'active' for thriving projects, 'graveyard' for abandoned repos, 'all' for both
            
        Returns:
            List of Repository objects
        """
        search_url = f"{self.base_url}/search/repositories"
        
        # Build search query based on mode
        if search_mode == "graveyard":
            # Search for abandoned repositories (no commits in last 2+ years)
            github_query = f"{query} stars:>={min_stars} pushed:<2022-01-01"
        elif search_mode == "active":
            # Search for active repositories (commits in last year)
            github_query = f"{query} stars:>={min_stars} pushed:>2023-01-01"
        else:  # search_mode == "all"
            # Search for all repositories
            github_query = f"{query} stars:>={min_stars}"
        
        params = {
            "q": github_query,
            "sort": sort_by,
            "order": "desc",
            "per_page": min(max_results, 100)  # GitHub API limit
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(search_url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            repositories = []
            
            for repo_data in data.get("items", []):
                # Fetch additional details for each repository
                repo = await self._enrich_repository_data(repo_data)
                if repo:
                    repositories.append(repo)
                
                # Rate limiting
                await asyncio.sleep(settings.github_rate_limit_delay)
                
                if len(repositories) >= max_results:
                    break
            
            return repositories
    
    async def _enrich_repository_data(self, repo_data: Dict[str, Any]) -> Optional[Repository]:
        """
        Enrich repository data with README content and quality metrics
        
        Args:
            repo_data: Raw repository data from GitHub API
            
        Returns:
            Enriched Repository object or None if failed
        """
        try:
            # Check if repository meets quality criteria
            if not self._meets_quality_criteria(repo_data):
                return None
            
            # Fetch README content
            readme_content = await self._get_readme_content(
                repo_data["owner"]["login"], 
                repo_data["name"]
            )
            
            # Fetch last commit date
            last_commit_date = await self._get_last_commit_date(
                repo_data["owner"]["login"], 
                repo_data["name"]
            )
            
            # Calculate inspiration score
            inspiration_score = self._calculate_inspiration_score(
                repo_data, last_commit_date
            )
            
            return Repository(
                id=repo_data["id"],
                name=repo_data["name"],
                full_name=repo_data["full_name"],
                description=repo_data.get("description"),
                html_url=repo_data["html_url"],
                stargazers_count=repo_data["stargazers_count"],
                language=repo_data.get("language"),
                updated_at=parser.parse(repo_data["updated_at"]),
                created_at=parser.parse(repo_data["created_at"]),
                pushed_at=parser.parse(repo_data["pushed_at"]),
                archived=repo_data.get("archived", False),
                disabled=repo_data.get("disabled", False),
                fork=repo_data.get("fork", False),
                readme_content=readme_content,
                last_commit_date=last_commit_date,
                inspiration_score=inspiration_score
            )
            
        except Exception as e:
            print(f"Error enriching repository data: {e}")
            return None
    
    def _meets_quality_criteria(self, repo_data: Dict[str, Any]) -> bool:
        """
        Check if repository meets quality criteria for inspiration
        
        Args:
            repo_data: Repository data from GitHub API
            
        Returns:
            True if repository meets quality criteria
        """
        # Must have minimum stars for quality
        if repo_data["stargazers_count"] < settings.min_stars_for_inspiration:
            return False
        
        # Must not be archived or disabled
        if repo_data.get("archived", False) or repo_data.get("disabled", False):
            return False
        
        # Must have a description or README (indicates effort)
        if not repo_data.get("description") and not repo_data.get("has_wiki", False):
            return False
        
        return True
    
    async def _get_readme_content(self, owner: str, repo: str) -> Optional[str]:
        """
        Fetch README content for a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            README content as string or None if not found
        """
        try:
            readme_url = f"{self.base_url}/repos/{owner}/{repo}/readme"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(readme_url, headers=self.headers)
                
                if response.status_code == 200:
                    data = response.json()
                    # GitHub returns base64 encoded content
                    import base64
                    content = base64.b64decode(data["content"]).decode("utf-8")
                    return content
                else:
                    return None
                    
        except Exception as e:
            print(f"Error fetching README for {owner}/{repo}: {e}")
            return None
    
    async def _get_last_commit_date(self, owner: str, repo: str) -> Optional[datetime]:
        """
        Fetch the date of the last commit
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Last commit date or None if failed
        """
        try:
            commits_url = f"{self.base_url}/repos/{owner}/{repo}/commits"
            params = {"per_page": 1}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(commits_url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    commits = response.json()
                    if commits:
                        commit_date = parser.parse(commits[0]["commit"]["author"]["date"])
                        return commit_date
                
                return None
                
        except Exception as e:
            print(f"Error fetching last commit for {owner}/{repo}: {e}")
            return None
    
    def _calculate_inspiration_score(self, repo_data: Dict[str, Any], last_commit_date: Optional[datetime]) -> float:
        """
        Calculate inspiration score based on various factors
        
        Args:
            repo_data: Repository data
            last_commit_date: Last commit date
            
        Returns:
            Inspiration score between 0 and 1 (higher = more inspiring)
        """
        score = 0.0
        
        # Factor 1: Star count (30% weight) - more stars = more inspiring
        star_count = repo_data["stargazers_count"]
        star_score = min(star_count / 1000, 1.0)  # Normalize to 1000 stars
        score += star_score * 0.3
        
        # Factor 2: Recent activity (25% weight) - active repos are more inspiring
        if last_commit_date:
            days_since_commit = (datetime.now() - last_commit_date.replace(tzinfo=None)).days
            activity_score = max(0, 1 - (days_since_commit / 365))  # More recent = higher score
            score += activity_score * 0.25
        
        # Factor 3: Documentation quality (25% weight)
        has_description = 1.0 if repo_data.get("description") else 0.0
        has_wiki = 1.0 if repo_data.get("has_wiki", False) else 0.0
        has_readme = 1.0 if repo_data.get("has_readme", False) else 0.0
        doc_score = (has_description + has_wiki + has_readme) / 3
        score += doc_score * 0.25
        
        # Factor 4: Repository maturity (20% weight) - mature repos are more inspiring
        created_at = parser.parse(repo_data["created_at"])
        days_since_creation = (datetime.now() - created_at.replace(tzinfo=None)).days
        maturity_score = min(days_since_creation / 365, 1.0)  # Normalize to 1 year
        score += maturity_score * 0.2
        
        return min(score, 1.0)  # Cap at 1.0 