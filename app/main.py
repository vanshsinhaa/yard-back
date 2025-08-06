"""
CodeInspiration API - Main Application
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

# Import routers
from app.api.search import router as search_router

# Import production features
from app.core.exceptions import CodeInspirationException, handle_exception
from app.core.rate_limiter import rate_limit_middleware
from app.core.logging import logging_middleware, api_logger

# Create FastAPI app
app = FastAPI(
    title="CodeInspiration API",
    description="API for finding inspiring GitHub repositories and learning from them",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
@app.middleware("http")
async def add_production_middleware(request: Request, call_next):
    """Add production middleware (logging and rate limiting)"""
    
    # Add request start time
    request.state.start_time = time.time()
    
    # Apply logging middleware
    response = await logging_middleware(request, call_next)
    
    # Apply rate limiting (only for search endpoints)
    if request.url.path.startswith("/api/v1/search"):
        response = await rate_limit_middleware(request, call_next)
    
    return response


# Global exception handler
@app.exception_handler(CodeInspirationException)
async def custom_exception_handler(request: Request, exc: CodeInspirationException):
    """Handle custom exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "code": exc.error_code,
                "status_code": exc.status_code,
                "details": exc.details
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    # Log the error
    api_logger.log_error(request, exc)
    
    # Return standardized error response
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "message": "An unexpected error occurred",
                "code": "INTERNAL_ERROR",
                "status_code": 500
            }
        }
    )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to CodeInspiration API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health",
        "features": [
            "GitHub repository search",
            "AI-powered analysis",
            "Semantic similarity scoring",
            "Learning insights generation"
        ]
    }


# Health check endpoint
@app.get("/api/v1/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "CodeInspiration API is running",
        "timestamp": time.time(),
        "version": "1.0.0"
    }


# Include routers
app.include_router(search_router, prefix="/api/v1", tags=["search"])


# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    print("🚀 CodeInspiration API starting up...")
    print("📊 Production features enabled:")
    print("   ✅ Error handling")
    print("   ✅ Rate limiting")
    print("   ✅ Request logging")
    print("   ✅ Performance monitoring")
    print("   ✅ CORS support")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    print("🛑 CodeInspiration API shutting down...") 