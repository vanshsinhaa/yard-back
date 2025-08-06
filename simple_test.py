#!/usr/bin/env python3
"""
Minimal test to check if FastAPI app can start
"""

from fastapi import FastAPI
import uvicorn

# Create a simple FastAPI app
app = FastAPI(title="Test API")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("🚀 Starting simple test server...")
    uvicorn.run(app, host="127.0.0.1", port=8003) 