#!/bin/bash

# Push TrustWrapper Eliza Plugin to GitHub
# Run this script from the trustwrapper-eliza-plugin directory

echo "🚀 Pushing TrustWrapper Eliza Plugin to GitHub..."
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -d ".git" ]; then
    echo "❌ Error: Please run this script from the trustwrapper-eliza-plugin directory"
    echo "cd /Users/eladm/Projects/trustwrapper-eliza-plugin"
    exit 1
fi

# Add remote origin (skip if already exists)
echo "📡 Adding GitHub remote..."
git remote add origin https://github.com/eladmint/trustwrapper-eliza-plugin.git 2>/dev/null || echo "✓ Remote 'origin' already exists"

# Verify remote
echo ""
echo "🔍 Verifying remote configuration..."
git remote -v

# Push to GitHub
echo ""
echo "📤 Pushing to GitHub..."
git push -u origin main

# Check result
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Code pushed to GitHub"
    echo ""
    echo "🎉 Your repository is now live at:"
    echo "   https://github.com/eladmint/trustwrapper-eliza-plugin"
    echo ""
    echo "📋 Next steps:"
    echo "1. Add repository description and topics on GitHub"
    echo "2. Enable GitHub Pages if needed"
    echo "3. Configure repository settings"
    echo "4. Add NPM_TOKEN secret for automated publishing"
    echo "5. Publish to npm with: npm publish --access public"
else
    echo ""
    echo "❌ Push failed. Common issues:"
    echo "1. Authentication: You may need to login with 'gh auth login'"
    echo "2. Permissions: Ensure you have write access to the repository"
    echo "3. Branch name: Your default branch might be 'master' instead of 'main'"
    echo ""
    echo "Try: git push -u origin master"
fi
