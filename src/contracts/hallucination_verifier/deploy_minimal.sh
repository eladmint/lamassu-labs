#!/bin/bash

# Minimal deployment script

echo "🚀 Aleo Minimal Deployment"
echo ""

# Get private key
echo "Enter your private key (hidden):"
read -s PRIVATE_KEY

echo ""
echo "Deploying hallucination_verifier.aleo..."
echo ""

# Deploy with minimal required parameters
aleo deploy --private-key "$PRIVATE_KEY" --fee 3000000 --endpoint "https://api.explorer.aleo.org/v1/testnet3/transaction/broadcast" hallucination_verifier.aleo

echo ""
echo "Done! Check transaction ID above."