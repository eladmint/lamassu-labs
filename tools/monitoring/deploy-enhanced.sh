#!/bin/bash
set -e

echo "🚀 Deploying Enhanced TrustWrapper Dashboard v4.0"
echo "================================================="

# Build the enhanced React dashboard
echo "📦 Building enhanced dashboard with shadcn/ui..."
npm run build

# Copy static assets if they exist
if [ -d "static" ]; then
    echo "📂 Copying static assets..."
    cp -r static/* dist/
fi

# Deploy to Juno satellite
echo "🌍 Deploying to Juno satellite: cmhvu-6iaaa-aaaal-asg5q-cai"

# Use the global Juno CLI (updated version)
if command -v juno &> /dev/null; then
    juno deploy --version
    juno deploy
else
    echo "⚠️  Global Juno CLI not found, using npx..."
    npx @junobuild/cli@latest deploy
fi

echo ""
echo "✅ Enhanced Dashboard Deployment Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 URL: https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io"
echo "🎯 Dashboard: TrustWrapper v4.0 with React + shadcn/ui"
echo "🔧 Features: Real-time analytics, enhanced UX, unified design"
echo "📊 Integration: Coordinated with Sprint 4 unified UI system"
echo ""
echo "🎉 Ready for production use!"
