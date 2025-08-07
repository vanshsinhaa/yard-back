# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PORT=8006

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first (to leverage caching)
COPY requirements.txt .

# --- Split install into 2 steps (lightweight + heavy) ---

# Install light/fast packages
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    httpx==0.25.2 \
    requests==2.31.0 \
    python-dotenv==1.0.0 \
    python-multipart==0.0.6 \
    pydantic==2.5.0 \
    pydantic-settings==2.1.0 \
    python-dateutil==2.8.2

# Install heavier packages separately
RUN pip install --no-cache-dir \
    pandas==2.1.3 \
    "numpy>=1.24.0" \
    scikit-learn==1.3.2 \
    sentence-transformers==2.2.2 \
    faiss-cpu==1.7.4 \
    openai==1.3.7 \
    tiktoken==0.5.1

# Copy the actual app code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Expose port
EXPOSE 8006

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8006/health || exit 1

# Run the application
CMD ["python", "authenticated_api.py"]
