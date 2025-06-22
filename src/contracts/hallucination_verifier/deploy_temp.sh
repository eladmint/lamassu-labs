#!/bin/bash

# Temporary deployment script for hallucination_verifier contract
# This script will prompt for your private key securely

set -e

echo "🚀 Aleo Contract Deployment for hallucination_verifier"
echo ""
echo "Please enter your Aleo private key (it will be hidden):"
echo "It should start with 'APrivateKey1zkp...'"
echo ""

# Read private key securely
read -s PRIVATE_KEY

# Verify private key format
if [[ ! "$PRIVATE_KEY" =~ ^APrivateKey1zkp ]]; then
    echo "❌ Invalid private key format. It should start with 'APrivateKey1zkp'"
    exit 1
fi

echo ""
echo "✅ Private key accepted"
echo ""

# Get account address
echo "Deriving your account address..."
ADDRESS=$(echo "$PRIVATE_KEY" | aleo account import | grep "Address" | awk '{print $2}')
echo "Your address: $ADDRESS"
echo ""

# Deploy the contract
echo "Deploying hallucination_verifier.aleo to testnet..."
echo ""

# Use Aleo CLI to deploy
aleo deploy --network testnet --private-key "$PRIVATE_KEY" --fee 1000000

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Please save the transaction ID shown above for your records."