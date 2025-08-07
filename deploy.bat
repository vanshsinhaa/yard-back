@echo off
echo 🚀 Deploying CodeInspiration API...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo ⚠️  No .env file found. Creating from example...
    copy env.example .env
    echo 📝 Please edit .env file with your API keys before continuing.
    echo    Required: OPENAI_API_KEY, GITHUB_TOKEN
    pause
    exit /b 1
)

REM Create necessary directories
if not exist logs mkdir logs
if not exist data mkdir data

REM Build and start the application
echo 🔨 Building Docker image...
docker-compose build

echo 🚀 Starting services...
docker-compose up -d

REM Wait for health check
echo ⏳ Waiting for service to be healthy...
for /l %%i in (1,1,30) do (
    curl -f http://localhost:8006/health >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Service is healthy!
        goto :healthy
    )
    echo ⏳ Waiting... (%%i/30)
    timeout /t 2 /nobreak >nul
)

:healthy
REM Show status
echo 📊 Deployment Status:
docker-compose ps

echo 🌐 API is running at: http://localhost:8006
echo 📚 API Documentation: http://localhost:8006/docs
echo 💚 Health Check: http://localhost:8006/health

echo ✅ Deployment complete!
pause 