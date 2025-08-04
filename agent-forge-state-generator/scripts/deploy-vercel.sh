#!/bin/bash
# Agent Forge State Generator - Vercel Deployment Script

set -e

echo "🚀 Agent Forge State Generator - Vercel Deployment"
echo "=================================================="

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI is not installed."
    echo "   Install with: npm i -g vercel"
    echo "   Or visit: https://vercel.com/cli"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json not found. Please run this script from the project root."
    exit 1
fi

# Environment variables check
echo "🔧 Environment variables setup..."

if [ ! -f ".env.vercel.example" ]; then
    echo "❌ .env.vercel.example not found."
    exit 1
fi

echo "📝 Please ensure you have configured these environment variables in Vercel:"
echo "   1. Go to your Vercel project dashboard"
echo "   2. Navigate to Settings > Environment Variables"
echo "   3. Add the following variables from .env.vercel.example:"
echo ""
cat .env.vercel.example | grep -E "^[A-Z_]+" | sed 's/=.*//' | sed 's/^/   - /'
echo ""

read -p "Have you configured all environment variables in Vercel? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "⚠️  Please configure environment variables first, then run this script again."
    echo "   Visit: https://vercel.com/docs/concepts/projects/environment-variables"
    exit 1
fi

# Git status check
echo "📦 Checking git status..."

if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  You have uncommitted changes. It's recommended to commit them first."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "📝 Please commit your changes and run this script again."
        exit 1
    fi
fi

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."

# First deployment or update
echo "🔍 Checking if this is a new project..."

if vercel list | grep -q "agent-forge-state-generator"; then
    echo "📦 Updating existing deployment..."
    vercel --prod
else
    echo "🆕 Creating new deployment..."
    vercel --prod
fi

# Get deployment URL
DEPLOYMENT_URL=$(vercel list agent-forge-state-generator --meta url | head -1)

echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Your Agent Forge State Generator is now live at:"
echo "   $DEPLOYMENT_URL"
echo ""
echo "🔍 Test your deployment:"
echo "   curl $DEPLOYMENT_URL/api/health"
echo "   open $DEPLOYMENT_URL/docs"
echo ""
echo "📊 Monitor your deployment:"
echo "   vercel logs $DEPLOYMENT_URL"
echo "   vercel inspect $DEPLOYMENT_URL"
echo ""
echo "🎉 Happy coding with Agent Forge on Vercel!"
