# 🚀 CodeInspiration API - Production Deployment Guide

## 📋 **Production Features Added**

### ✅ **Completed Features**
- **Database Integration**: SQLite for persistent API key storage
- **User Registration**: Dynamic API key generation
- **Authentication System**: Plan-based rate limiting
- **Real GitHub Data**: Live repository search and analysis
- **Health Monitoring**: `/health` endpoint for monitoring
- **Production Logging**: Structured logging with file rotation
- **Docker Containerization**: Production-ready container
- **Environment Configuration**: Secure environment variable management

## 🛠️ **Quick Start**

### **1. Prerequisites**
- Docker Desktop installed and running
- Python 3.11+ (for local development)
- OpenAI API key
- GitHub Personal Access Token

### **2. Environment Setup**
```bash
# Copy environment template
cp env.example .env

# Edit .env with your API keys
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here
```

### **3. Docker Deployment**
```bash
# Windows
deploy.bat

# Linux/Mac
./deploy.sh
```

### **4. Local Development**
```bash
# Install dependencies
pip install -r requirements.txt

# Start server
python authenticated_api.py
```

## 📊 **API Endpoints**

### **Authentication Required**
- `POST /register` - Register new user
- `POST /keys/generate` - Generate API key
- `POST /search` - Search repositories
- `GET /usage` - Get usage statistics

### **Public Endpoints**
- `GET /health` - Health check
- `GET /plans` - Pricing plans
- `GET /docs` - API documentation

## 🔐 **Authentication**

### **API Key Format**
```
X-API-Key: your_api_key_here
```

### **API Keys**
- Register at `/register` endpoint to get your API key
- Use the key in `X-API-Key` header for all requests

### **Plan Limits**
- **Free**: 100/hour, 1,000/month
- **Pro**: 1,000/hour, 10,000/month  
- **Enterprise**: 10,000/hour, 100,000/month

## 📈 **Monitoring**

### **Health Check**
```bash
curl http://localhost:8006/health
```

### **Logs**
- **API Logs**: `logs/api.log`
- **Error Logs**: `logs/errors.log`
- **Database**: `api_keys.db`

### **Database View**
```bash
python view_database.py
```

## 🐳 **Docker Commands**

### **Build Image**
```bash
docker build -t codeinspiration-api .
```

### **Run Container**
```bash
docker run -p 8006:8006 --env-file .env codeinspiration-api
```

### **Docker Compose**
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 **Configuration**

### **Environment Variables**
| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | Yes |
| `GITHUB_TOKEN` | GitHub token for repository access | Yes |
| `PORT` | Server port (default: 8006) | No |
| `DEBUG` | Debug mode (default: false) | No |

### **Database**
- **Type**: SQLite
- **Location**: `api_keys.db`
- **Tables**: `api_keys`, `usage_logs`

## 📝 **Usage Examples**

### **Register User**
```bash
curl -X POST http://localhost:8006/register \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "myuser",
    "email": "user@example.com",
    "plan": "free"
  }'
```

### **Search Repositories**
```bash
curl -X POST http://localhost:8006/search \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "react todo app",
    "max_results": 5,
    "sort_by": "stars",
    "min_stars": 10,
    "search_mode": "active"
  }'
```

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Docker not running**
   ```bash
   # Start Docker Desktop first
   ```

2. **Missing API keys**
   ```bash
   # Check .env file
   cat .env
   ```

3. **Port already in use**
   ```bash
   # Change port in .env
   PORT=8007
   ```

4. **Database issues**
   ```bash
   # View database
   python view_database.py
   ```

### **Logs**
```bash
# View API logs
tail -f logs/api.log

# View error logs  
tail -f logs/errors.log
```

## 🔒 **Security**

### **Production Checklist**
- [ ] Use strong API keys
- [ ] Enable HTTPS in production
- [ ] Set up proper firewall rules
- [ ] Monitor rate limits
- [ ] Regular security updates
- [ ] Database backups

### **API Key Security**
- Store keys securely
- Rotate keys regularly
- Monitor usage patterns
- Set up alerts for abuse

## 📞 **Support**

### **API Documentation**
- Swagger UI: `http://localhost:8006/docs`
- ReDoc: `http://localhost:8006/redoc`

### **Health Monitoring**
- Health endpoint: `http://localhost:8006/health`
- Database status included in health check

---

**Version**: 1.0.0  
**Last Updated**: August 2025