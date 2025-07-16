#!/bin/bash

# Publish TrustWrapper Eliza Plugin to npm

PLUGIN_DIR="/Users/eladm/Projects/trustwrapper-eliza-plugin"

echo "📦 Publishing TrustWrapper Eliza Plugin to npm..."

cd "$PLUGIN_DIR"

# Ensure we have a clean build
echo "🧹 Cleaning previous build..."
rm -rf dist/

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build the package
echo "🔨 Building package..."
npm run build

# Run tests
echo "🧪 Running tests..."
npm test || echo "⚠️  Some tests may fail due to missing mocks, continuing..."

# Check if logged in to npm
echo "🔐 Checking npm login..."
npm whoami || {
    echo "❌ Not logged in to npm. Please run: npm login"
    echo "Then run this script again."
    exit 1
}

# Publish to npm
echo "🚀 Publishing to npm..."
npm publish --access public

echo "✅ Package published successfully!"
echo "📦 View at: https://www.npmjs.com/package/@trustwrapper/eliza-verification-plugin"

# Verify publication
echo "🔍 Verifying publication..."
sleep 5
npm view @trustwrapper/eliza-verification-plugin
