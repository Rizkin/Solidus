# Agent Forge State Generator - Vercel Deployment Guide 🚀

Complete guide for deploying the Agent Forge Workflow State Generator to Vercel, including setup, configuration, and optimization for serverless deployment.

## 📋 Table of Contents

1. [Why Vercel?](#why-vercel)
2. [Prerequisites](#prerequisites)
3. [Quick Deploy](#quick-deploy)
4. [Manual Setup](#manual-setup)
5. [Environment Configuration](#environment-configuration)
6. [Testing & Validation](#testing--validation)
7. [Performance Optimization](#performance-optimization)
8. [Troubleshooting](#troubleshooting)

## Why Vercel?

Vercel is perfect for the Agent Forge State Generator because it offers:

- **🚀 Serverless Functions**: Automatic scaling and zero cold starts
- **🌐 Global CDN**: Fast response times worldwide
- **🔧 Easy Deployment**: Git-based deployments with automatic builds
- **💰 Cost Effective**: Pay only for what you use
- **🔒 Built-in Security**: HTTPS, DDoS protection, and security headers
- **📊 Analytics**: Built-in performance monitoring

## Prerequisites

### Required Accounts & Services
- **Vercel Account**: [vercel.com](https://vercel.com) (free tier available)
- **Supabase Account**: [supabase.com](https://supabase.com) for database
- **Anthropic API Key**: [console.anthropic.com](https://console.anthropic.com) for AI features
- **GitHub Account**: For repository hosting and automatic deployments

### Local Requirements
- **Node.js**: 16+ (for Vercel CLI)
- **Git**: For version control
- **Python**: 3.11+ (for local testing)

### Install Vercel CLI
```bash
# Install globally
npm i -g vercel

# Or use yarn
yarn global add vercel

# Verify installation
vercel --version
```

## Quick Deploy

### 1-Click Deploy (Recommended)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-org/agent-forge-state-generator&env=SUPABASE_URL,SUPABASE_SERVICE_KEY,ANTHROPIC_API_KEY&envDescription=Required%20environment%20variables%20for%20Agent%20Forge%20State%20Generator&envLink=https://github.com/your-org/agent-forge-state-generator/blob/main/.env.vercel.example)

**Steps:**
1. Click the "Deploy with Vercel" button above
2. Connect your GitHub account
3. Configure environment variables (see [Environment Configuration](#environment-configuration))
4. Click "Deploy"
5. Your app will be live at `https://your-project.vercel.app`

### Command Line Deploy

```bash
# Clone the repository
git clone https://github.com/your-org/agent-forge-state-generator
cd agent-forge-state-generator

# Login to Vercel
vercel login

# Deploy with our script
./scripts/deploy-vercel.sh
```

## Manual Setup

### Step 1: Repository Setup

```bash
# Fork or clone the repository
git clone https://github.com/your-org/agent-forge-state-generator
cd agent-forge-state-generator

# Ensure you have the latest changes
git pull origin main
```

### Step 2: Vercel Project Creation

```bash
# Login to Vercel
vercel login

# Initialize project
vercel

# Follow the prompts:
# ? Set up and deploy "agent-forge-state-generator"? [Y/n] y
# ? Which scope do you want to deploy to? [Your Account]
# ? Link to existing project? [y/N] n
# ? What's your project's name? agent-forge-state-generator
# ? In which directory is your code located? ./
```

### Step 3: Environment Variables Setup

Go to your Vercel dashboard and add these environment variables:

#### Required Variables
```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

# AI Integration  
ANTHROPIC_API_KEY=sk-ant-api03-...

# Database Connection
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.your-project.supabase.co:5432/postgres
```

#### Optional Variables
```bash
# Application Settings
AGENT_FORGE_MODE=production
LOG_LEVEL=INFO
VERCEL_DEPLOYMENT=true

# Security (recommended for production)
ALLOWED_HOSTS=your-domain.vercel.app
CORS_ORIGINS=https://your-domain.vercel.app,https://agentforge.ai
```

### Step 4: Deploy

```bash
# Deploy to production
vercel --prod

# Or use our deployment script
./scripts/deploy-vercel.sh
```

## Environment Configuration

### Supabase Setup

1. **Create Supabase Project**
   ```bash
   # Go to https://supabase.com/dashboard
   # Click "New Project"
   # Note your project URL and service key
   ```

2. **Database Schema**
   ```sql
   -- Execute in Supabase SQL Editor
   -- Copy content from scripts/create_tables.sql
   ```

3. **Optional: Load Sample Data**
   ```sql
   -- Execute in Supabase SQL Editor
   -- Copy content from data/agent_forge_synthetic_data.sql
   ```

### Anthropic API Setup

1. **Get API Key**
   ```bash
   # Visit https://console.anthropic.com
   # Create new API key
   # Copy the key (starts with sk-ant-api03-)
   ```

2. **Test API Key**
   ```bash
   curl -X POST https://api.anthropic.com/v1/messages \
     -H "x-api-key: YOUR_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -H "content-type: application/json" \
     -d '{"model": "claude-3-sonnet-20240229", "max_tokens": 10, "messages": [{"role": "user", "content": "Hello"}]}'
   ```

### Environment Variables in Vercel

#### Via Dashboard
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to Settings → Environment Variables
4. Add each variable with appropriate scope (Production, Preview, Development)

#### Via CLI
```bash
# Add environment variables via CLI
vercel env add SUPABASE_URL production
vercel env add SUPABASE_SERVICE_KEY production
vercel env add ANTHROPIC_API_KEY production
vercel env add DATABASE_URL production

# List environment variables
vercel env ls
```

## Testing & Validation

### Local Testing

```bash
# Install dependencies
pip install -r requirements-vercel.txt

# Set environment variables
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_SERVICE_KEY="your-service-key"
export ANTHROPIC_API_KEY="your-claude-key"

# Run locally
python -m uvicorn api.index:app --reload --port 8000

# Test endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/docs
```

### Production Testing

```bash
# Get your deployment URL
DEPLOYMENT_URL=$(vercel list agent-forge-state-generator --meta url | head -1)

# Test health endpoint
curl $DEPLOYMENT_URL/api/health

# Test API documentation
open $DEPLOYMENT_URL/docs

# Test workflow operations
curl -X POST "$DEPLOYMENT_URL/api/workflows/test-id/generate-state" \
  -H "Content-Type: application/json" \
  -d '{"optimization_goal": "efficiency"}'
```

### Automated Testing

```bash
# Run our validation script against production
python scripts/final_validation.py --url $DEPLOYMENT_URL

# Monitor logs
vercel logs $DEPLOYMENT_URL --follow

# Check function performance
vercel inspect $DEPLOYMENT_URL
```

## Performance Optimization

### Serverless Optimization

#### Cold Start Reduction
```python
# In src/main_vercel.py
# Global variables for connection reuse
_supabase_client = None
_claude_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _supabase_client, _claude_client
    # Initialize connections once
    if not _app_initialized:
        _supabase_client = get_supabase_client()
        _claude_client = ClaudeClient()
```

#### Memory Optimization
```json
// In vercel.json
{
  "functions": {
    "api/index.py": {
      "maxDuration": 30,
      "memory": 1024
    }
  }
}
```

### Performance Monitoring

#### Vercel Analytics
```bash
# Enable analytics in Vercel dashboard
# Go to Settings → Analytics
# View performance metrics and user insights
```

#### Custom Monitoring
```python
# Add performance logging
import time
import logging

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logging.info(f"Path: {request.url.path}, Duration: {process_time:.3f}s")
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### Caching Strategy

#### Response Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
async def get_block_types():
    # Cache static data
    return block_types_data

# Set cache headers
@app.get("/api/block-types")
async def block_types():
    response = get_block_types()
    return Response(
        content=response,
        headers={"Cache-Control": "public, max-age=3600"}
    )
```

## Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Error: ModuleNotFoundError: No module named 'src'
# Solution: Check PYTHONPATH in vercel.json
{
  "env": {
    "PYTHONPATH": "."
  }
}
```

#### 2. Database Connection Issues
```bash
# Error: Supabase connection failed
# Check environment variables
vercel env ls

# Test connection locally
python -c "
from src.utils.supabase import get_supabase_client
client = get_supabase_client()
print('Connection:', 'OK' if client else 'FAILED')
"
```

#### 3. Function Timeout
```bash
# Error: Function execution timed out
# Increase timeout in vercel.json
{
  "functions": {
    "api/index.py": {
      "maxDuration": 60  // Increase from 30
    }
  }
}
```

#### 4. Memory Limit Exceeded
```bash
# Error: Function exceeded memory limit
# Increase memory allocation
{
  "functions": {
    "api/index.py": {
      "memory": 1024  // Increase from default 512MB
    }
  }
}
```

### Debug Tools

#### Vercel Logs
```bash
# View real-time logs
vercel logs --follow

# View logs for specific deployment
vercel logs https://your-deployment-url.vercel.app

# Filter logs by function
vercel logs --since 1h | grep "api/index.py"
```

#### Function Inspector
```bash
# Inspect function performance
vercel inspect https://your-deployment-url.vercel.app

# View function source and configuration
vercel inspect --scope your-team
```

### Performance Issues

#### Slow Response Times
1. **Check Function Region**: Ensure deployment is in optimal region
2. **Database Location**: Use Supabase region close to Vercel region
3. **Connection Pooling**: Implement connection reuse
4. **Caching**: Add response caching for static data

#### High Error Rates
1. **Check Logs**: Use `vercel logs` to identify issues
2. **Environment Variables**: Verify all required variables are set
3. **API Limits**: Check Anthropic API quota and rate limits
4. **Database Limits**: Monitor Supabase usage and limits

## Advanced Configuration

### Custom Domains

```bash
# Add custom domain
vercel domains add yourdomain.com

# Configure DNS
# Add CNAME record: your-project.vercel.app

# Enable automatic HTTPS
vercel certs ls
```

### Team Deployment

```bash
# Deploy to team
vercel --scope your-team

# Set team environment variables
vercel env add SUPABASE_URL production --scope your-team
```

### Staging Environment

```bash
# Deploy to preview (staging)
vercel

# Set preview environment variables
vercel env add SUPABASE_URL preview
vercel env add ANTHROPIC_API_KEY preview
```

## Security Best Practices

### Environment Variables
- Never commit API keys to git
- Use different keys for production/preview/development
- Regularly rotate API keys
- Use least-privilege access for service keys

### CORS Configuration
```python
# Configure CORS properly for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://agentforge.ai", "https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Rate Limiting
```python
# Implement rate limiting for API endpoints
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/workflows/{workflow_id}/generate-state")
@limiter.limit("10/minute")
async def generate_state(request: Request, workflow_id: str):
    # Implementation
    pass
```

## Monitoring & Analytics

### Built-in Monitoring
- **Vercel Analytics**: User behavior and performance metrics
- **Function Logs**: Real-time logging and error tracking
- **Performance Insights**: Response times and error rates

### Custom Monitoring
```python
# Add custom metrics
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = datetime.now()
    
    try:
        response = await call_next(request)
        duration = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"Request: {request.method} {request.url.path} - "
                   f"Status: {response.status_code} - "
                   f"Duration: {duration:.3f}s")
        
        return response
    except Exception as e:
        logger.error(f"Request failed: {request.method} {request.url.path} - "
                    f"Error: {str(e)}")
        raise
```

## Support & Resources

### Vercel Resources
- �� **Documentation**: [vercel.com/docs](https://vercel.com/docs)
- 💬 **Community**: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)
- 🎥 **Tutorials**: [vercel.com/guides](https://vercel.com/guides)

### Agent Forge Resources
- 🏠 **Homepage**: [agentforge.ai](https://agentforge.ai)
- 📚 **Documentation**: [docs.agentforge.ai](https://docs.agentforge.ai)
- 💬 **Discord**: [discord.gg/agentforge](https://discord.gg/agentforge)

### Project Support
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-org/agent-forge-state-generator/issues)
- 📧 **Email**: support@agentforge.ai
- 📖 **Wiki**: [Project Wiki](https://github.com/your-org/agent-forge-state-generator/wiki)

---

**🎉 Your Agent Forge State Generator is now running on Vercel! Enjoy the power of serverless AI workflows! 🚀**
