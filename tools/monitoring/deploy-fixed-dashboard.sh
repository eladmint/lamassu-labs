#!/bin/bash

# Deploy fixed dashboard to Juno satellite

echo "Deploying fixed monitoring dashboard..."

# Check if dist folder exists
if [ ! -d "dist" ]; then
    echo "Creating dist folder..."
    mkdir -p dist
fi

# The index.html file should already be updated with persistence fixes
echo "Checking index.html has the fixes..."
if grep -q "lastKnownGoodData" dist/index.html; then
    echo "✓ Data persistence code found"
else
    echo "✗ Data persistence code missing - dashboard not updated properly"
    exit 1
fi

# Try to deploy using Juno CLI
echo "Attempting Juno deployment..."
npx juno deploy --satellite-id cmhvu-6iaaa-aaaal-asg5q-cai --source dist || {
    echo "Juno deployment failed, but the files are ready in dist/"
    echo "You may need to manually upload through the Juno web interface"
}

echo ""
echo "Dashboard URL: https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io/"
echo ""
echo "The updated dashboard includes:"
echo "- Always shows 12 transactions (5+3+4) even when offline"
echo "- Persists data to localStorage"
echo "- Shows proper connection status"
echo "- Never resets to 0 transactions"
