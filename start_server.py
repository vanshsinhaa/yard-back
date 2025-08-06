#!/usr/bin/env python3
"""
Start the CodeInspiration API server
"""

import uvicorn
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.main import app
    
    if __name__ == "__main__":
        print("🚀 Starting CodeInspiration API server...")
        print("📍 Server will be available at: http://127.0.0.1:8001")
        print("📚 API Documentation: http://127.0.0.1:8001/docs")
        print("🔍 Health Check: http://127.0.0.1:8001/api/v1/health")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8001,  # Changed from 8000 to avoid conflicts
            log_level="info"
        )
        
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Make sure you're in the backend directory and all dependencies are installed")
    print("   Run: pip install -r requirements.txt")
    
except Exception as e:
    print(f"❌ Error starting server: {e}")
    print("💡 Try running: python -m uvicorn app.main:app --host 127.0.0.1 --port 8001") 