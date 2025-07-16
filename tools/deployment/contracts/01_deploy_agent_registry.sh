#!/bin/bash

# Deployment script for agent_registry.aleo contract

echo "🚀 Deploying agent_registry.aleo Contract"
echo ""

# Navigate to contract directory
cd "$(dirname "$0")/../../../src/contracts/agent_registry" || exit 1

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
NETWORK=testnet
ENDPOINT=https://api.explorer.provable.com/v1
EOF
fi

# Get private key
echo "Enter your private key (starting with APrivateKey1zkp...):"
read -s PRIVATE_KEY

echo ""
echo "Using configuration:"
echo "Network: testnet"
echo "Endpoint: https://api.explorer.provable.com/v1"
echo "Contract: agent_registry.aleo"
echo ""

# Build the contract
echo "Building contract..."
leo build --network testnet || {
    echo "❌ Build failed"
    exit 1
}

# Deploy
echo "Deploying to Aleo testnet..."
leo deploy --private-key "$PRIVATE_KEY" --broadcast --yes

echo ""
echo "✅ Deployment completed!"
echo "Check deployment status at: https://testnet.aleoscan.io/"
