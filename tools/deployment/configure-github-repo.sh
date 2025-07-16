#!/bin/bash

# Configure GitHub repository settings
# Run this after pushing code to GitHub

REPO_OWNER="eladmint"
REPO_NAME="trustwrapper-eliza-plugin"
REPO_URL="https://github.com/$REPO_OWNER/$REPO_NAME"

echo "🔧 Configuring GitHub repository settings..."
echo "Repository: $REPO_URL"
echo ""

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "⚠️  GitHub CLI not found. Install with: brew install gh"
    echo "   Or configure manually at: $REPO_URL/settings"
    exit 1
fi

# Login check
if ! gh auth status &> /dev/null; then
    echo "🔐 Please login to GitHub CLI first:"
    echo "   gh auth login"
    exit 1
fi

# Set repository description
echo "📝 Setting repository description..."
gh repo edit $REPO_OWNER/$REPO_NAME \
  --description "Universal AI verification plugin for Eliza framework - Build trustworthy AI agents with zero-knowledge proofs"

# Set homepage
echo "🏠 Setting homepage..."
gh repo edit $REPO_OWNER/$REPO_NAME \
  --homepage "https://trustwrapper.io"

# Add topics
echo "🏷️  Adding repository topics..."
gh repo edit $REPO_OWNER/$REPO_NAME \
  --add-topic eliza-plugin \
  --add-topic ai-agents \
  --add-topic verification \
  --add-topic zero-knowledge-proof \
  --add-topic trustwrapper \
  --add-topic typescript \
  --add-topic blockchain \
  --add-topic ai-safety \
  --add-topic defi \
  --add-topic trading-bots

# Enable issues and projects
echo "📋 Enabling features..."
gh repo edit $REPO_OWNER/$REPO_NAME \
  --enable-issues \
  --enable-projects

echo ""
echo "✅ Repository configuration complete!"
echo ""
echo "🔐 To enable automated npm publishing:"
echo "1. Generate npm token: https://www.npmjs.com/settings/YOUR_USERNAME/tokens"
echo "2. Add to repository secrets:"
echo "   gh secret set NPM_TOKEN --body YOUR_TOKEN_HERE"
echo ""
echo "📦 To publish to npm manually:"
echo "   npm login"
echo "   npm publish --access public"
echo ""
echo "🎉 Repository ready for community engagement!"
echo "   $REPO_URL"
