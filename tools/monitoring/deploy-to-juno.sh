#!/bin/bash

# Deployment script for Juno satellite on ICP

echo "🚀 Deploying Lamassu Labs monitoring dashboard to Juno satellite..."
echo "Satellite ID: cmhvu-6iaaa-aaaal-asg5q-cai"
echo ""

# Check if Juno CLI is installed
if ! command -v juno &> /dev/null; then
    echo "❌ Juno CLI not found. Please install it first:"
    echo "   npm install -g @junobuild/cli"
    exit 1
fi

# Build the project
echo "📦 Building project..."
./build-juno.sh

# Check if build was successful
if [ ! -d "dist" ]; then
    echo "❌ Build failed. No dist directory found."
    exit 1
fi

# Deploy to Juno
echo ""
echo "🌐 Deploying to Internet Computer..."
cd dist
juno deploy

# Get the deployment URL
DEPLOYMENT_URL="https://bvxuo-uaaaa-aaaal-asgua-cai.icp0.io"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🎉 Your monitoring dashboard is now live at:"
echo "   $DEPLOYMENT_URL"
echo ""
echo "📊 Datastore collections created:"
echo "   - monitoring_data"
echo "   - contract_metrics"
echo "   - alerts"
echo ""
echo "🔐 Access control:"
echo "   - Read: Public"
echo "   - Write: Managed (requires authentication)"
echo ""
echo "📝 To update monitoring data, use the Juno SDK or API"