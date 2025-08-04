# Agent Forge State Generator

🤖 **AI-powered workflow state generator for Agent Forge platform**

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Rizkin/Solidus)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

## 🎯 Overview

A lightweight FastAPI application that generates AI-powered workflow states for the Agent Forge platform. Features template-based workflow creation, health monitoring, and serverless deployment support.

## ✨ Features

- **Template System**: 4 pre-built workflow templates (Trading Bot, Lead Generation, Multi-Agent Research, Web3 Automation)
- **Health Monitoring**: Built-in health check endpoints
- **Serverless Ready**: Optimized for Vercel deployment
- **CORS Enabled**: Ready for frontend integration
- **Agent Forge Compatible**: Designed for Agent Forge platform integration

## 🚀 Live Demo

**Deployed on Vercel**: [https://solidus-olive.vercel.app/](https://solidus-olive.vercel.app/)

### Try the API:
```bash
# Get available templates
curl https://solidus-olive.vercel.app/api/templates

# Check health status
curl https://solidus-olive.vercel.app/api/health

# Main endpoint
curl https://solidus-olive.vercel.app/
```

## 📡 API Endpoints

### Core Endpoints
- `GET /` - Welcome page with feature overview
- `GET /api/health` - System health check
- `GET /api/templates` - List available workflow templates

## 🎯 Workflow Templates

### Available Templates
1. **Crypto Trading Bot** - Automated trading with stop-loss and take-profit
2. **Lead Generation System** - Capture and qualify leads from multiple sources  
3. **Multi-Agent Research Team** - Collaborative AI agents for research tasks
4. **Web3 DeFi Automation** - Smart contract monitoring and DeFi operations

### Template Response Example
```json
{
  "templates": [
    {
      "name": "trading_bot",
      "display_name": "Crypto Trading Bot",
      "description": "Automated trading with stop-loss and take-profit",
      "category": "Web3 Trading",
      "status": "available"
    }
  ],
  "total_templates": 4,
  "deployment": "vercel-serverless"
}
```

## 🚀 Deploy to Vercel

### One-Click Deploy
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Rizkin/Solidus)

### Manual Deploy
1. **Fork this repository**
2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Import your forked repository
   - Vercel will auto-detect the FastAPI app

3. **Deploy**:
   - Click "Deploy"
   - Your app will be live at `https://your-project.vercel.app`

### Local Development
```bash
# Clone the repository
git clone https://github.com/Rizkin/Solidus.git
cd Solidus

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn src.main:app --reload --port 8000

# Visit the API
open http://localhost:8000
```

## 🔧 Project Structure

```
├── api/
│   └── index.py          # Vercel serverless entry point
├── src/
│   └── main.py           # Main FastAPI application
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
└── README.md            # This file
```

## 🛠️ Built With

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[Vercel](https://vercel.com/)** - Serverless deployment platform
- **Python 3.11+** - Programming language

## 📞 Usage After Deployment

Once deployed to Vercel, you can integrate with the Agent Forge platform:

### 1. Get Your Vercel URL
After deployment, you'll receive a URL like: `https://your-project.vercel.app`

### 2. Test the Endpoints
```bash
# Check if your deployment is working
curl https://your-project.vercel.app/api/health

# Get available templates for Agent Forge
curl https://your-project.vercel.app/api/templates
```

### 3. Integration with Agent Forge
Use your Vercel URL as the base endpoint in Agent Forge:
- **Base URL**: `https://your-project.vercel.app`
- **Templates Endpoint**: `/api/templates`
- **Health Check**: `/api/health`

### 4. Expected Response
Your deployment should return:
```json
{
  "name": "Agent Forge State Generator",
  "status": "operational",
  "deployment": "vercel-serverless",
  "message": "🚀 Agent Forge State Generator is running successfully on Vercel!"
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📜 License

MIT License - see the LICENSE file for details.

---

**Built for the Agent Forge community** 🚀
