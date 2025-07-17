#!/bin/bash

# Simple deployment script for hallucination_verifier

echo "🚀 Simple Aleo Deployment Script"
echo ""
echo "This will deploy hallucination_verifier.aleo to testnet"
echo ""
echo "Prerequisites:"
echo "1. You need your Aleo private key (starts with APrivateKey1zkp...)"
echo "2. You need testnet credits in your account"
echo ""
echo "Press Enter to continue or Ctrl+C to cancel..."
read

# Get private key
echo ""
echo "Please paste your Aleo private key and press Enter:"
echo "(It will be hidden for security)"
read -s PRIVATE_KEY

if [[ ! "$PRIVATE_KEY" =~ ^APrivateKey1zkp ]]; then
    echo ""
    echo "❌ Invalid private key format"
    exit 1
fi

echo ""
echo "✅ Private key accepted"

# Show account info
echo ""
echo "Getting account information..."
ACCOUNT_INFO=$(echo "$PRIVATE_KEY" | aleo account import 2>&1)
echo "$ACCOUNT_INFO" | grep -E "Address|View"

# Confirm deployment
echo ""
echo "Ready to deploy hallucination_verifier.aleo"
echo "This will cost approximately 3-10 testnet credits"
echo ""
echo "Type 'yes' to proceed with deployment:"
read CONFIRM

if [[ "$CONFIRM" != "yes" ]]; then
    echo "Deployment cancelled"
    exit 0
fi

# Deploy
echo ""
echo "🚀 Starting deployment..."
echo ""

# Run deployment with explicit parameters
aleo deploy hallucination_verifier.aleo \
    --private-key "$PRIVATE_KEY" \
    --query "https://api.explorer.aleo.org/v1" \
    --network testnet \
    --broadcast "https://api.explorer.aleo.org/v1/testnet3/transaction/broadcast" \
    --fee 3000000 \
    --record "{
  owner: aleo176m09rv6qslzx0r7uyuerz3keq346lkdqhwtk2w8ffsk4rdsxyrqj9xx5m.private,
  microcredits: 50000000u64.private,
  _nonce: 0group.public
}"

echo ""
echo "✅ Deployment command executed!"
echo ""
echo "Check the output above for:"
echo "1. Transaction ID (save this!)"
echo "2. Any error messages"
echo "3. Deployment status"
echo ""
echo "You can verify deployment at:"
echo "https://aleo.tools/"
<<<<<<< HEAD
echo "https://aleoscan.io/"
=======
echo "https://aleoscan.io/"
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
