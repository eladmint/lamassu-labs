#!/bin/bash

echo "🚀 Deploying trust_verifier_v2.aleo"
echo "===================================="
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
<<<<<<< HEAD
echo "https://testnet.aleoscan.io/program?id=trust_verifier_v2.aleo"
=======
echo "https://testnet.aleoscan.io/program?id=trust_verifier_v2.aleo"
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
