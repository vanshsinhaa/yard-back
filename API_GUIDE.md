# 🚀 CodeInspiration API Guide

## 🎯 **What Your API Does**

Your **CodeInspiration API** is a smart search engine that helps developers find inspiring GitHub repositories. Here's what it does:

### **Behind the Scenes:**
1. **Takes your search query** (e.g., "react todo app")
2. **Searches GitHub** for repositories matching your query
3. **Uses AI** to analyze each repository's content
4. **Calculates similarity scores** using embeddings
5. **Ranks repositories** by relevance to your query
6. **Generates learning insights** and implementation tips
7. **Returns structured data** with AI analysis

---

## 🚀 **How to Start Your API**

### **Step 1: Start the Server**
```bash
cd backend
python start_server.py
```

### **Step 2: Verify It's Working**
Open your browser and go to: `http://127.0.0.1:8000/`

You should see:
```json
{
  "message": "Welcome to CodeInspiration API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/api/v1/health"
}
```

---

## 📚 **API Endpoints**

### **1. Root Endpoint (`/`)**
- **URL**: `http://127.0.0.1:8000/`
- **Method**: GET
- **Purpose**: Shows API information
- **Response**: Basic API details

### **2. Health Check (`/api/v1/health`)**
- **URL**: `http://127.0.0.1:8000/api/v1/health`
- **Method**: GET
- **Purpose**: Check if API is running
- **Response**: Health status

### **3. Search Repositories (`/api/v1/search`)**
- **URL**: `http://127.0.0.1:8000/api/v1/search`
- **Method**: POST
- **Purpose**: Main functionality - search for repositories
- **Request Body**: JSON with search parameters

---

## 🔍 **How to Use the Search API**

### **Basic Search Request:**
```json
{
  "query": "react todo app with authentication",
  "max_results": 5,
  "sort_by": "stars",
  "min_stars": 10
}
```

### **Parameters Explained:**
- **`query`**: Your search term (required)
- **`max_results`**: Number of results to return (1-20, default: 5)
- **`sort_by`**: Sort criteria (`stars`, `updated`, `created`, default: `stars`)
- **`min_stars`**: Minimum star count filter (default: 0)

### **Example Response:**
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

---

## 🧪 **How to Test Your API**

### **Method 1: Using Your Browser**
1. Start the server: `python start_server.py`
2. Open browser: `http://127.0.0.1:8000/docs`
3. Click "Try it out" on any endpoint
4. Enter your search parameters
5. Click "Execute"

### **Method 2: Using curl (Command Line)**
```bash
# Test root endpoint
curl http://127.0.0.1:8000/

# Test health endpoint
curl http://127.0.0.1:8000/api/v1/health

# Test search endpoint
curl -X POST "http://127.0.0.1:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "react todo app",
    "max_results": 3,
    "sort_by": "stars",
    "min_stars": 10
  }'
```

### **Method 3: Using Python**
```python
import requests

# Test search
search_data = {
    "query": "python web scraper",
    "max_results": 3,
    "sort_by": "stars",
    "min_stars": 50
}

response = requests.post(
    "http://127.0.0.1:8000/api/v1/search",
    json=search_data,
    headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    result = response.json()
    print(f"Found {result['total_found']} repositories")
    for repo in result['results']:
        print(f"- {repo['repository']['name']}: {repo['repository']['stars']} stars")
else:
    print(f"Error: {response.text}")
```

---

## 💡 **Example Use Cases**

### **1. Find React Projects**
```json
{
  "query": "react typescript",
  "max_results": 5,
  "sort_by": "stars",
  "min_stars": 50
}
```

### **2. Find Python ML Projects**
```json
{
  "query": "machine learning python",
  "max_results": 3,
  "sort_by": "updated",
  "min_stars": 100
}
```

### **3. Find Recent Projects**
```json
{
  "query": "web scraper",
  "max_results": 2,
  "sort_by": "created",
  "min_stars": 10
}
```

---

## 🔧 **Troubleshooting**

### **Server Won't Start:**
1. Make sure you're in the `backend` directory
2. Check if port 8000 is already in use
3. Try a different port: `uvicorn.run(app, port=8001)`

### **API Returns Errors:**
1. Check if all dependencies are installed: `pip install -r requirements.txt`
2. Make sure your search query is valid
3. Check the server logs for error messages

### **No Results Found:**
1. Try a broader search query
2. Lower the `min_stars` requirement
3. Check if GitHub API is accessible

---

## 🚀 **Next Steps**

### **1. Add OpenAI API Key (Optional)**
For full AI features, add your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### **2. Deploy to Production**
- Choose a cloud provider (AWS, GCP, Heroku)
- Set up environment variables
- Configure domain and SSL

### **3. Build a Frontend**
- Create a web interface
- Add user accounts
- Implement advanced features

### **4. Monetize Your API**
- Add API key authentication
- Implement rate limiting
- Create pricing tiers

---

## 🎉 **Congratulations!**

Your **CodeInspiration API** is now working! You have:

✅ **A working API server**  
✅ **GitHub repository search**  
✅ **AI-powered analysis**  
✅ **Semantic similarity scoring**  
✅ **Interactive documentation**  
✅ **Health monitoring**  

**You're ready to help developers find inspiration and learn from great code!** 🚀 