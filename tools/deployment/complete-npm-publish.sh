#!/bin/bash

# Complete npm publication for TrustWrapper Eliza Plugin

echo "📦 Completing npm publication for TrustWrapper..."
echo "=================================================="

cd /Users/eladm/Projects/trustwrapper-eliza-plugin

# Check if we're in the right place
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run from the plugin directory."
    exit 1
fi

echo "✅ Found package.json"

# Check npm login status
echo "🔐 Checking npm authentication..."
npm whoami &> /dev/null

if [ $? -ne 0 ]; then
    echo "🔑 Please login to npm:"
    echo "   If you don't have an account, create one at: https://www.npmjs.com/signup"
    echo ""
    npm login
else
    echo "✅ Already logged in to npm as: $(npm whoami)"
fi

# Final package validation
echo ""
echo "🔍 Running final validation..."
if [ -f "scripts/validate-package.js" ]; then
    node scripts/validate-package.js
fi

# Publish to npm
echo ""
echo "🚀 Publishing to npm registry..."
npm publish --access public

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! Package published to npm!"
    echo ""
    echo "📦 Package URL: https://www.npmjs.com/package/@trustwrapper/eliza-verification-plugin"
    echo "📚 Installation: npm install @trustwrapper/eliza-verification-plugin"
    echo ""
    echo "✅ TrustWrapper Eliza Plugin is now LIVE!"
    echo ""
    echo "🚀 Ready for community launch!"
else
    echo ""
    echo "❌ npm publish failed. Common solutions:"
    echo "1. Version conflict: Update version in package.json"
    echo "2. Authentication: Run 'npm login' again"
    echo "3. Scope permissions: Ensure you have access to @trustwrapper scope"
    echo ""
    echo "Try running: npm version patch && npm publish --access public"
fi

echo ""
echo "🎯 Next Steps:"
echo "1. 🐦 Create launch announcement on Twitter/X"
echo "2. 💬 Post in Eliza Discord community"
echo "3. 📝 Write technical blog post on dev.to"
echo "4. 🚀 Submit to Product Hunt"
echo "5. 📧 Direct outreach to AI agent developers"
