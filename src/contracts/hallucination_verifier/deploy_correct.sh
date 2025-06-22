#!/bin/bash

# Correct deployment script for hallucination_verifier

echo "🚀 Aleo Contract Deployment"
echo "=========================="
echo ""
echo "This will deploy hallucination_verifier.aleo to testnet"
echo ""

# Check if we're in the right directory
if [ ! -f "build/main.aleo" ]; then
    echo "❌ Error: build/main.aleo not found"
    echo "Please run 'leo build --network testnet' first"
    exit 1
fi

echo "✅ Found compiled contract: build/main.aleo"
echo ""

# Get private key
echo "Please enter your Aleo private key:"
echo "(starts with APrivateKey1zkp...)"
read -s PRIVATE_KEY

if [[ ! "$PRIVATE_KEY" =~ ^APrivateKey1zkp ]]; then
    echo ""
    echo "❌ Invalid private key format"
    exit 1
fi

echo ""
echo "✅ Private key accepted"

# Derive address
echo ""
echo "Deriving your account address..."
ADDRESS=$(echo "$PRIVATE_KEY" | aleo account import 2>&1 | grep "Address" | awk '{print $2}')
echo "Your address: $ADDRESS"

# Deployment confirmation
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Ready to deploy:"
echo "  Contract: hallucination_verifier.aleo"
echo "  Network: testnet"
echo "  Account: $ADDRESS"
echo "  Fee: ~3-10 credits"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Type 'deploy' to proceed:"
read CONFIRM

if [[ "$CONFIRM" != "deploy" ]]; then
    echo "Deployment cancelled"
    exit 0
fi

# Set environment variables
export NETWORK=testnet
export PRIVATE_KEY="$PRIVATE_KEY"

# Deploy using the correct syntax
echo ""
echo "🚀 Deploying contract..."
echo ""

# The correct aleo deploy syntax
aleo deploy --private-key "$PRIVATE_KEY" --fee 3000000 hallucination_verifier.aleo

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Deployment command completed!"
    echo ""
    echo "⚠️  IMPORTANT: Save the transaction ID from above!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Copy the transaction ID"
    echo "2. Wait 1-2 minutes for confirmation"
    echo "3. Check deployment at:"
    echo "   https://aleoscan.io/transaction/[YOUR_TX_ID]"
    echo "   https://aleo.tools/"
else
    echo ""
    echo "❌ Deployment failed. Check the error message above."
    echo ""
    echo "Common issues:"
    echo "- Insufficient balance (need 3-10 credits)"
    echo "- Network connectivity"
    echo "- Invalid private key"
fi