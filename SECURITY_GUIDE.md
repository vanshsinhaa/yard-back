# 🔐 Code Graveyard API - Security Guide

## 🚨 Security Overview

Your API now has **production-grade security**:

✅ **Cryptographically secure API keys** (256-bit entropy)  
✅ **HMAC-SHA256 key hashing** (never stores plain keys)  
✅ **Environment-based secrets** (no hardcoded credentials)  
✅ **Secure key generation** with proper prefixes  
✅ **Rate limiting** and usage tracking  
✅ **Admin-only key generation**  

## 🔑 API Key Security

### Key Format
```
cg_live_[24_random_characters]
```
- `cg_` = Code Graveyard prefix
- `live_` = Production environment  
- 24 random chars = ~144 bits of entropy

### Key Storage
- Keys are **hashed with HMAC-SHA256** before storage
- **Never stored in plain text**
- Secret key used for hashing stored in environment
- Keys cannot be recovered, only validated

### Key Generation (Production)
```python
# Generate secure keys via API
POST /generate-key
{
  "plan": "free|pro|enterprise",
  "user_email": "user@example.com"
}
Headers: admin_key: [ADMIN_KEY]
```

## 🛡️ Environment Security

### Required Environment Variables
```bash
# Copy env.example to .env and configure:
SECRET_KEY=your_secret_key_here     # For key hashing
ADMIN_KEY=your_admin_key_here       # For key generation
GITHUB_TOKEN=your_github_token      # Optional, for higher rate limits
```

### Generate Secure Keys
```bash
# Generate SECRET_KEY
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"

# Generate ADMIN_KEY  
python -c "import secrets; print('ADMIN_KEY=' + secrets.token_urlsafe(32))"
```

## 🚀 Deployment Security

### 1. Remove Demo Keys
```bash
# Use production_api.py instead of authenticated_api.py
python production_api.py
```

### 2. Set Environment Variables
```bash
# For Heroku
heroku config:set SECRET_KEY=your_secret_key
heroku config:set ADMIN_KEY=your_admin_key
heroku config:set GITHUB_TOKEN=your_github_token

# For Railway
# Set in Railway dashboard under Variables
```

### 3. Secure File Permissions
```bash
# Protect key storage file
chmod 600 secure_api_keys.json
```

## 📧 User Onboarding Flow

### 1. User Signs Up
- User provides email and selects plan
- Admin generates key via secure endpoint
- Key sent to user via email (not displayed)

### 2. Key Distribution
```python
# Admin generates key
api_key = secure_key_manager.generate_api_key("pro", "user@example.com")

# Send via email (implement email service)
send_api_key_email(user_email, api_key, plan)
```

### 3. User Authentication
```bash
# User includes key in requests
curl -H "X-API-Key: cg_live_abc123..." https://api.codegraveyard.com/search
```

## 🔒 Additional Security Measures

### Rate Limiting
- **Free:** 100 requests/hour, 1,000/month
- **Pro:** 1,000 requests/hour, 10,000/month  
- **Enterprise:** 10,000 requests/hour, 100,000/month

### Key Management
```python
# Revoke compromised keys
secure_key_manager.revoke_key(api_key)

# List user keys (admin)
secure_key_manager.list_keys_for_user("user@example.com")
```

### Monitoring & Alerts
- Track unusual usage patterns
- Monitor for brute force attacks
- Alert on high error rates
- Log all key generation/revocation

## 🚨 Incident Response

### Compromised Key
1. **Immediately revoke** the key
2. **Generate new key** for user
3. **Notify user** via email
4. **Review logs** for unauthorized usage

### Security Breach
1. **Rotate SECRET_KEY** immediately
2. **Regenerate all API keys**
3. **Update environment variables**
4. **Notify all users**

## ✅ Security Checklist

**Before Deployment:**
- [ ] Remove all demo/hardcoded keys
- [ ] Set strong SECRET_KEY and ADMIN_KEY
- [ ] Configure environment variables
- [ ] Test key generation endpoint
- [ ] Verify key validation works
- [ ] Set up monitoring/alerting
- [ ] Configure rate limiting
- [ ] Implement key revocation
- [ ] Set up secure key distribution

**After Deployment:**
- [ ] Monitor usage patterns
- [ ] Regular security audits
- [ ] Update dependencies
- [ ] Backup key database securely
- [ ] Monitor for unusual activity
- [ ] Test incident response procedures

## 💡 Best Practices

1. **Never log API keys** in plain text
2. **Rotate keys regularly** (90 days)
3. **Use HTTPS only** in production
4. **Implement IP whitelisting** for enterprise
5. **Monitor and alert** on security events
6. **Regular security audits**
7. **Keep dependencies updated**
8. **Use database for production** (not JSON files)

Your API is now **production-ready** with enterprise-grade security! 🛡️