# Agent Forge State Generator

🤖 **AI-powered workflow state generator for Agent Forge platform**

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Rizkin/Solidus)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

## 🎯 Overview

A comprehensive FastAPI application that generates AI-powered workflow states for the Agent Forge platform. Features advanced AI integration, comprehensive validation, professional templates, and enterprise-ready deployment capabilities.

## ✨ Features

### 🤖 AI-Powered Generation
- **Claude AI Integration**: Advanced workflow state generation using Anthropic's Claude
- **Intelligent Fallbacks**: Rule-based generation when AI is unavailable
- **Pattern Recognition**: Automatically detects and optimizes workflow patterns
- **Smart Configuration**: AI-enhanced block configuration and connections

### 🔍 Comprehensive Validation
- **9-Validator System**: Complete Agent Forge compliance checking
  - Schema validation
  - Block type validation  
  - Starter block validation
  - Agent configuration validation
  - API integration validation
  - Edge connectivity validation
  - Workflow pattern validation
  - Position bounds validation
  - Sub-block structure validation
- **Real-time Feedback**: Instant validation with detailed error reporting
- **Marketplace Readiness**: Automated compliance checks for Agent Forge marketplace

### 🎨 Professional Templates
**8 Ready-to-Deploy Templates:**
1. **Lead Generation System** - Sales & Marketing automation
2. **Crypto Trading Bot** - Web3 Trading with risk management  
3. **Multi-Agent Research Team** - Collaborative AI research
4. **Customer Support Automation** - Ticket classification & response
5. **Web3 DeFi Automation** - Smart contract monitoring
6. **Data Processing Pipeline** - ETL processing and transformation
7. **Content Generation System** - AI-powered writing & publishing
8. **Multi-Channel Notifications** - Intelligent alerts across channels

### 🏗️ Enterprise Architecture
- **Database Integration**: Supabase with intelligent fallbacks to mock data
- **Serverless Ready**: Optimized for Vercel deployment
- **Environment Flexibility**: Works with or without external dependencies
- **Comprehensive Logging**: Structured logging for monitoring and debugging
- **Error Handling**: Graceful degradation and comprehensive error reporting

## 🚀 Live Demo

**Deployed on Vercel**: [https://solidus-olive.vercel.app/](https://solidus-olive.vercel.app/)

### Try the API:
```bash
# Get available templates
curl https://solidus-olive.vercel.app/api/templates

# Check health status
curl https://solidus-olive.vercel.app/api/health

# Get debug information
curl https://solidus-olive.vercel.app/api/debug

# View API documentation
open https://solidus-olive.vercel.app/docs
```

## 📡 API Endpoints

### Core Endpoints
- `GET /` - Welcome page with system status
- `GET /api/health` - Comprehensive health check
- `GET /api/templates` - List all workflow templates
- `GET /api/debug` - System debug information
- `GET /docs` - Interactive API documentation

### Workflow Management
- `POST /api/workflows/{id}/generate-state` - Generate AI-powered workflow states
- `POST /api/workflows/{id}/validate` - Validate workflow compliance
- `GET /api/workflows/{id}/state` - Retrieve workflow state
- `GET /api/workflows/{id}/marketplace-preview` - Marketplace readiness preview
- `POST /api/workflows/templates/{name}` - Create workflows from templates
- `GET /api/workflows/{id}/export` - Export workflows (JSON/YAML)
- `GET /api/block-types` - Agent Forge block type documentation

## 🎯 Workflow Templates

### Template Categories
- **Sales & Marketing**: Lead generation, CRM integration
- **Web3 Trading**: Crypto trading bots, DeFi automation
- **AI Automation**: Multi-agent teams, research workflows
- **Customer Service**: Support automation, ticket management
- **Data Processing**: ETL pipelines, transformation workflows
- **Content & Media**: AI writing, publishing automation
- **Communication**: Multi-channel notifications, alerts

### Template Usage Example
```bash
# Create a trading bot with custom parameters
curl -X POST https://solidus-olive.vercel.app/api/workflows/templates/trading_bot \
  -H "Content-Type: application/json" \
  -d '{
    "trading_pair": "ETH/USD",
    "stop_loss": -3,
    "take_profit": 8,
    "position_size": 0.05
  }'

# Create a lead generation system
curl -X POST https://solidus-olive.vercel.app/api/workflows/templates/lead_generation \
  -H "Content-Type: application/json" \
  -d '{
    "source": "facebook_ads",
    "crm_integration": "salesforce"
  }'
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

3. **Configure Environment Variables** (Optional):
   ```bash
   ANTHROPIC_API_KEY=your_anthropic_key  # For AI features
   SUPABASE_URL=your_supabase_url        # For database features
   SUPABASE_SERVICE_KEY=your_supabase_key
   ```

4. **Deploy**:
   - Click "Deploy"
   - Your app will be live at `https://your-project.vercel.app`

### Local Development
```bash
# Clone the repository
git clone https://github.com/Rizkin/Solidus.git
cd Solidus

# Install dependencies
pip install -r requirements.txt

# Configure environment (optional)
cp .env.example .env
# Edit .env with your API keys

# Start the server
uvicorn src.main:app --reload --port 8000

# Visit the API
open http://localhost:8000/docs
```

## 🔧 Configuration

### Environment Variables
```bash
# AI Integration (Optional - enables AI features)
ANTHROPIC_API_KEY=your_anthropic_api_key

# Database (Optional - uses mock data if not provided)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your_supabase_service_key

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Feature Modes
The application intelligently adapts based on available configuration:

- **Full Mode**: All features enabled (AI + Database)
- **AI Mode**: AI features only (mock database)
- **Basic Mode**: Templates and validation only
- **Minimal Mode**: Core API only

## 🧪 API Examples

### Generate AI Workflow State
```bash
curl -X POST https://solidus-olive.vercel.app/api/workflows/sample-workflow-123/generate-state \
  -H "Content-Type: application/json" \
  -d '{
    "complexity": "medium",
    "include_suggestions": true
  }'
```

### Validate Workflow
```bash
curl -X POST https://solidus-olive.vercel.app/api/workflows/sample-workflow-123/validate
```

### Export Workflow
```bash
curl https://solidus-olive.vercel.app/api/workflows/sample-workflow-123/export?format=json
```

## 🔧 Project Structure

```
├── api/
│   └── index.py              # Vercel serverless entry point
├── src/
│   ├── main.py              # Main FastAPI application
│   ├── api/
│   │   └── workflows.py     # Workflow API endpoints
│   ├── services/
│   │   ├── state_generator.py   # AI-powered state generation
│   │   ├── validation.py        # 9-validator compliance system
│   │   └── templates.py         # Professional workflow templates
│   ├── utils/
│   │   └── database_hybrid.py   # Database service with fallbacks
│   └── models/
│       ├── schemas.py           # Pydantic models
│       ├── connection.py        # Database connections
│       └── database.py          # Database models
├── requirements.txt         # Python dependencies
├── vercel.json             # Vercel configuration
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🛠️ Built With

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[Anthropic Claude](https://www.anthropic.com/)** - AI-powered state generation
- **[Supabase](https://supabase.com/)** - Database and backend services
- **[Vercel](https://vercel.com/)** - Serverless deployment platform
- **[Pydantic](https://pydantic.dev/)** - Data validation and serialization

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

# Generate a workflow state
curl -X POST https://your-project.vercel.app/api/workflows/templates/trading_bot \
  -H "Content-Type: application/json" \
  -d '{"trading_pair": "BTC/USD"}'
```

### 3. Integration with Agent Forge
Use your Vercel URL as the base endpoint in Agent Forge:
- **Base URL**: `https://your-project.vercel.app`
- **Templates Endpoint**: `/api/templates`
- **State Generation**: `/api/workflows/{id}/generate-state`
- **Validation**: `/api/workflows/{id}/validate`

### 4. Expected Response
Your deployment should return comprehensive workflow data:
```json
{
  "name": "Agent Forge State Generator",
  "status": "operational",
  "deployment": "vercel-serverless",
  "features": [
    "AI-powered workflow state generation",
    "Template-based workflow creation",
    "Multi-agent team support",
    "Web3 and DeFi automation",
    "Real-time validation",
    "Marketplace integration"
  ],
  "api_status": {
    "full_api": true,
    "endpoints": {
      "health": "/api/health",
      "docs": "/docs",
      "templates": "/api/templates",
      "workflows": "/api/workflows"
    }
  }
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

*Featuring AI-powered state generation, comprehensive validation, and professional workflow templates for the modern no-code automation platform.*
