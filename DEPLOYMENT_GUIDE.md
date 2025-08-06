# 🚀 Deploy Code Graveyard API to Heroku

## Step 1: Install Heroku CLI
1. Go to https://devcenter.heroku.com/articles/heroku-cli
2. Download and install Heroku CLI for Windows

## Step 2: Login to Heroku
```bash
heroku login
```

## Step 3: Create Heroku App
```bash
# Navigate to your backend folder
cd "C:\Users\Vansh\Desktop\code graveyard\backend"

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - CodeInspiration API"

# Create Heroku app (replace 'your-app-name' with something unique)
heroku create code-graveyard-api-2024

# Deploy to Heroku
git push heroku main
```

## Step 4: Test Your Live API
After deployment, your API will be available at:
```
https://code-graveyard-api-2024.herokuapp.com
```

Test it:
```bash
# Check health
curl https://code-graveyard-api-2024.herokuapp.com/health

# Test search with API key (active projects)
curl -X POST https://code-graveyard-api-2024.herokuapp.com/search \
  -H "Content-Type: application/json" \
  -H "X-API-Key: demo_free_12345" \
  -d '{"query": "react todo", "max_results": 2, "search_mode": "active"}'

# Test search for abandoned repos
curl -X POST https://code-graveyard-api-2024.herokuapp.com/search \
  -H "Content-Type: application/json" \
  -H "X-API-Key: demo_free_12345" \
  -d '{"query": "react todo", "max_results": 2, "search_mode": "graveyard"}'
```

## Step 5: Configure Domain (Optional)
- Buy domain: codeinspiration.dev
- Point to Heroku app
- Add SSL certificate (free with Heroku)

## Alternative: Railway (Even Easier)

1. Go to https://railway.app
2. Connect your GitHub repository
3. Deploy automatically
4. Get live URL instantly

## What You Get:
✅ **Live API** on the internet  
✅ **Professional HTTPS URL**  
✅ **Automatic scaling**  
✅ **Free tier available**  
✅ **Ready for customers**  

## Next Steps After Deployment:
1. **Add your API to RapidAPI marketplace**
2. **Create landing page** for sign-ups
3. **Set up Stripe** for payments
4. **Launch on ProductHunt**

Your API will be live and making money! 💰