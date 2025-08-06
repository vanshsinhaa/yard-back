"""
Logging configuration for CodeInspiration API
"""

import logging
import time
from typing import Dict, Any
from fastapi import Request, Response
from datetime import datetime


# Configure logging
def setup_logging():
    """Setup logging configuration"""
    
    # Create logger
    logger = logging.getLogger("codeinspiration")
    logger.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger


# Global logger instance
logger = setup_logging()


class APILogger:
    """API request/response logger"""
    
    def __init__(self):
        self.logger = logger
    
    def log_request(self, request: Request, start_time: float):
        """Log incoming request"""
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        self.logger.info(
            f"Request: {request.method} {request.url.path} "
            f"from {client_ip} "
            f"User-Agent: {user_agent}"
        )
    
    def log_response(self, request: Request, response: Response, start_time: float):
        """Log response details"""
        duration = time.time() - start_time
        status_code = response.status_code
        
        # Log level based on status code
        if status_code >= 500:
            log_level = self.logger.error
        elif status_code >= 400:
            log_level = self.logger.warning
        else:
            log_level = self.logger.info
        
        log_level(
            f"Response: {request.method} {request.url.path} "
            f"-> {status_code} ({duration:.3f}s)"
        )
    
    def log_error(self, request: Request, error: Exception):
        """Log error details"""
        client_ip = request.client.host if request.client else "unknown"
        
        self.logger.error(
            f"Error: {request.method} {request.url.path} "
            f"from {client_ip} - {type(error).__name__}: {str(error)}"
        )
    
    def log_search_query(self, query: str, results_count: int, duration: float):
        """Log search query details"""
        self.logger.info(
            f"Search: '{query}' -> {results_count} results ({duration:.3f}s)"
        )
    
    def log_api_usage(self, endpoint: str, client_id: str, success: bool):
        """Log API usage for analytics"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"API Usage: {endpoint} by {client_id} -> {status}")


# Global API logger instance
api_logger = APILogger()


async def logging_middleware(request: Request, call_next):
    """Logging middleware for all requests"""
    start_time = time.time()
    
    # Log request
    api_logger.log_request(request, start_time)
    
    try:
        # Process request
        response = await call_next(request)
        
        # Log response
        api_logger.log_response(request, response, start_time)
        
        return response
        
    except Exception as e:
        # Log error
        api_logger.log_error(request, e)
        raise


def log_metrics(metric_name: str, value: float, tags: Dict[str, str] = None):
    """Log metrics for monitoring"""
    tags_str = " ".join([f"{k}={v}" for k, v in (tags or {}).items()])
    logger.info(f"METRIC: {metric_name}={value} {tags_str}")


def log_performance(operation: str, duration: float, details: Dict[str, Any] = None):
    """Log performance metrics"""
    details_str = ""
    if details:
        details_str = " " + " ".join([f"{k}={v}" for k, v in details.items()])
    
    logger.info(f"PERFORMANCE: {operation} took {duration:.3f}s{details_str}") 