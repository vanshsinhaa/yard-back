"""
Custom exceptions and error handling for CodeInspiration API
"""

from fastapi import HTTPException, status
from typing import Any, Dict, Optional


class CodeInspirationException(Exception):
    """Base exception for CodeInspiration API"""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class GitHubAPIError(CodeInspirationException):
    """Raised when GitHub API returns an error"""
    
    def __init__(self, message: str, status_code: int = status.HTTP_502_BAD_GATEWAY):
        super().__init__(
            message=message,
            status_code=status_code,
            error_code="GITHUB_API_ERROR"
        )


class OpenAIAPIError(CodeInspirationException):
    """Raised when OpenAI API returns an error"""
    
    def __init__(self, message: str, status_code: int = status.HTTP_502_BAD_GATEWAY):
        super().__init__(
            message=message,
            status_code=status_code,
            error_code="OPENAI_API_ERROR"
        )


class EmbeddingError(CodeInspirationException):
    """Raised when embedding generation fails"""
    
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="EMBEDDING_ERROR"
        )


class SearchError(CodeInspirationException):
    """Raised when search operation fails"""
    
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="SEARCH_ERROR"
        )


class ValidationError(CodeInspirationException):
    """Raised when request validation fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="VALIDATION_ERROR",
            details=details
        )


class RateLimitError(CodeInspirationException):
    """Raised when rate limit is exceeded"""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_ERROR"
        )


def create_error_response(
    message: str,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    error_code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create a standardized error response"""
    
    error_response = {
        "error": {
            "message": message,
            "code": error_code or "INTERNAL_ERROR",
            "status_code": status_code
        }
    }
    
    if details:
        error_response["error"]["details"] = details
    
    return error_response


def handle_exception(exc: Exception) -> HTTPException:
    """Convert custom exceptions to HTTPException"""
    
    if isinstance(exc, CodeInspirationException):
        return HTTPException(
            status_code=exc.status_code,
            detail=create_error_response(
                message=exc.message,
                status_code=exc.status_code,
                error_code=exc.error_code,
                details=exc.details
            )
        )
    
    # Handle other exceptions
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=create_error_response(
            message="An unexpected error occurred",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_ERROR"
        )
    ) 