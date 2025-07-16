#!/bin/bash

echo "🚀 Deploying agent_registry_v2.aleo"
echo "==================================="
echo ""

# Ensure we're in the right directory
cd "$(dirname "$0")"

echo "Current directory: $(pwd)"
echo ""

# Get private key
echo "Enter your Aleo private key:"
read -s PRIVATE_KEY
echo ""

# Build
echo "Building contract..."
leo build --network testnet || {
    echo "❌ Build failed"
    exit 1
}

# Deploy
echo "Deploying to Aleo testnet..."
leo deploy --private-key "$PRIVATE_KEY" --broadcast --yes

echo ""
echo "✅ Deployment initiated!"
echo "Check AleoScan in 2-3 minutes:"
echo "https://testnet.aleoscan.io/program?id=agent_registry_v2.aleo"
