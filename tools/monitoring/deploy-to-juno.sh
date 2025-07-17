#!/bin/bash

# Deployment script for Juno satellite on ICP

<<<<<<< HEAD
echo "🚀 Deploying enhanced Mento Protocol monitoring dashboard to Juno satellite..."
=======
echo "🚀 Deploying Lamassu Labs monitoring dashboard to Juno satellite..."
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
echo "Satellite ID: cmhvu-6iaaa-aaaal-asg5q-cai"
echo ""

# Check if Juno CLI is installed
if ! command -v juno &> /dev/null; then
    echo "❌ Juno CLI not found. Please install it first:"
    echo "   npm install -g @junobuild/cli"
    exit 1
fi

<<<<<<< HEAD
# Check if updated dashboard exists
if [ ! -f "dist/mento-dashboard.html" ]; then
    echo "❌ Updated dashboard not found. Please ensure dist/mento-dashboard.html exists."
    exit 1
fi

# Copy the main dashboard as index.html for default access
echo "📦 Preparing dashboard files..."
cp dist/mento-dashboard.html dist/index.html

# Verify data file exists
if [ ! -f "dist/mento_dashboard_data.json" ]; then
    echo "⚠️  Warning: mento_dashboard_data.json not found. Dashboard will use live API only."
fi

# Deploy to Juno
echo ""
echo "🌐 Deploying enhanced dashboard to Internet Computer..."
=======
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
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
cd dist
juno deploy

# Get the deployment URL
<<<<<<< HEAD
DEPLOYMENT_URL="https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io"
=======
DEPLOYMENT_URL="https://bvxuo-uaaaa-aaaal-asgua-cai.icp0.io"
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

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
<<<<<<< HEAD
echo "📝 To update monitoring data, use the Juno SDK or API"
=======
echo "📝 To update monitoring data, use the Juno SDK or API"
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
