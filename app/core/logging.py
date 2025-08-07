"""
Logging configuration for CodeInspiration API
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path

def setup_logging():
    """Setup production-ready logging configuration"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler with color formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    root_logger.addHandler(console_handler)
    
    # File handler for all logs
    file_handler = logging.handlers.RotatingFileHandler(
        'logs/api.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(file_format)
    root_logger.addHandler(file_handler)
    
    # Error file handler
    error_handler = logging.handlers.RotatingFileHandler(
        'logs/errors.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_format)
    root_logger.addHandler(error_handler)
    
    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    return root_logger

def log_api_request(method: str, path: str, status_code: int, response_time: float, user_id: str = None):
    """Log API request details"""
    logger = logging.getLogger("api.requests")
    
    log_data = {
        "method": method,
        "path": path,
        "status_code": status_code,
        "response_time_ms": round(response_time * 1000, 2),
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if status_code >= 400:
        logger.error(f"API Request Error: {log_data}")
    else:
        logger.info(f"API Request: {log_data}")

def log_rate_limit_hit(api_key: str, user_id: str, plan: str):
    """Log rate limit violations"""
    logger = logging.getLogger("api.rate_limits")
    logger.warning(f"Rate limit hit - API Key: {api_key[:10]}..., User: {user_id}, Plan: {plan}")

def log_error(error: Exception, context: str = None):
    """Log errors with context"""
    logger = logging.getLogger("api.errors")
    logger.error(f"Error in {context}: {str(error)}", exc_info=True) 