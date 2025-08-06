# CodeInspiration API

A FastAPI-based service for finding inspiring GitHub repositories and learning from them. This application helps developers discover relevant repositories that can provide inspiration, learning opportunities, and implementation guidance for their own projects.

## Features

- **Semantic Search**: Find repositories similar to your project idea using AI-powered embeddings
- **Quality Filtering**: Focus on repositories with good documentation and active development
- **Learning Insights**: AI-generated analysis of key features, learning opportunities, and implementation tips
- **Flexible Search**: Sort by stars, update date, or creation date with customizable filters

## Architecture

### Core Services

1. **GitHub Search Service** (`github_search.py`)
   - Searches GitHub repositories based on user queries
   - Filters by quality criteria (stars, documentation, activity)
   - Calculates inspiration scores based on repository metrics

2. **Embedding Service** (`embed_and_store.py`)
   - Generates semantic embeddings for repository content
   - Uses FAISS for efficient similarity search
   - Supports multiple embedding models and index types

3. **Summarization Service** (`summarize.py`)
   - Generates AI-powered analysis of repositories
   - Provides key features, learning insights, and implementation tips
   - Requires OpenAI API key for full functionality

### API Endpoints

- `POST /api/v1/search` - Search for inspiring repositories
- `GET /api/v1/health` - Health check endpoint

## Search Request Format

```json
{
  "query": "react todo app with authentication",
  "max_results": 5,
  "sort_by": "stars",
  "min_stars": 10
}
```

## Search Response Format

```json
{
  "query": "react todo app with authentication",
  "results": [
    {
      "repository": {
        "id": 123456,
        "name": "awesome-todo-app",
        "full_name": "user/awesome-todo-app",
        "description": "A modern React todo app with authentication",
        "html_url": "https://github.com/user/awesome-todo-app",
        "stars": 150,
        "language": "JavaScript",
        "inspiration_score": 0.85
      },
      "summary": "A modern React todo application with user authentication...",
      "key_features": [
        "React with TypeScript",
        "Firebase Authentication",
        "Material-UI components"
      ],
      "learning_insights": [
        "Clean component architecture",
        "State management patterns",
        "Authentication flow implementation"
      ],
      "implementation_tips": [
        "Start with a simple authentication setup",
        "Use React Context for state management",
        "Implement proper error handling"
      ],
      "similarity_score": 0.92
    }
  ],
  "total_found": 1,
  "search_time_ms": 1250.5
}
```

## Configuration

The application uses environment variables for configuration. Key settings include:

- `OPENAI_API_KEY`: Required for AI summarization features
- `GITHUB_TOKEN`: Optional GitHub API token for higher rate limits
- `MIN_STARS_FOR_INSPIRATION`: Minimum star count for quality filtering (default: 10)
- `EMBEDDING_MODEL_NAME`: Sentence transformer model for embeddings (default: "all-MiniLM-L6-v2")

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables (optional):
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export GITHUB_TOKEN="your-github-token"
   ```

3. Run the application:
   ```bash
   python -m app.main
   ```

## Usage Examples

### Basic Search
```bash
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning image classification",
    "max_results": 3
  }'
```

### Advanced Search with Filters
```bash
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "python web scraper",
    "max_results": 5,
    "sort_by": "updated",
    "min_stars": 50
  }'
```

## Pivot from CodeGraveyard

This application was pivoted from a "dead repository finder" to an "inspiration search engine". Key changes include:

- **Removed abandonment criteria** - No longer filters for inactive repositories
- **Added quality metrics** - Focuses on well-documented, active projects
- **Changed AI analysis** - From "why it failed" to "what you can learn"
- **Enhanced search parameters** - Added sorting and filtering options
- **Updated response format** - Learning insights instead of revival suggestions

## Future Enhancements

- **Academic Paper Integration**: Search and analyze research papers alongside repositories
- **Technology Stack Analysis**: Automatic detection and comparison of tech stacks
- **Community Insights**: Integration with GitHub discussions and issues
- **Personalized Recommendations**: User preference learning and customization
- **Visual Analytics**: Charts and graphs showing repository trends and patterns

Copyright © 2025 Vansh Sinha. All rights reserved.
