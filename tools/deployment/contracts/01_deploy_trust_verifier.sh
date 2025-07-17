#!/bin/bash

# Deployment script for trust_verifier.aleo contract

echo "🚀 Deploying trust_verifier.aleo Contract"
echo ""

# Navigate to contract directory
cd "$(dirname "$0")/../../../src/contracts/trust_verifier" || exit 1

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
echo "Contract: trust_verifier.aleo"
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
<<<<<<< HEAD
echo "Check deployment status at: https://testnet.aleoscan.io/"
=======
echo "Check deployment status at: https://testnet.aleoscan.io/"
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
