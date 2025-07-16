#!/bin/bash

# Deploy remaining TrustWrapper contracts to Aleo testnet
# This script deploys agent_registry_v2 and trust_verifier_v2

set -e  # Exit on error

echo "🚀 TrustWrapper Contract Deployment Script"
echo "=========================================="
echo ""
echo "This script will deploy:"
echo "1. agent_registry_v2.aleo"
echo "2. trust_verifier_v2.aleo"
echo ""
echo "Prerequisites:"
echo "- Aleo account with at least 30 testnet credits"
echo "- Private key starting with APrivateKey1zkp..."
echo ""

# Get private key once for both deployments
echo "Enter your Aleo private key:"
read -s PRIVATE_KEY
echo ""

# Validate private key format
if [[ ! "$PRIVATE_KEY" =~ ^APrivateKey1zkp ]]; then
    echo "❌ Error: Invalid private key format. Must start with APrivateKey1zkp"
    exit 1
fi

echo "✅ Private key validated"
echo ""

# Get the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"

# Deploy agent_registry_v2
echo "📋 Step 1/2: Deploying agent_registry_v2.aleo"
echo "============================================="
cd "$PROJECT_ROOT/src/contracts/agent_registry"

echo "Building contract..."
leo build --network testnet || {
    echo "❌ Build failed for agent_registry_v2"
    exit 1
}

echo "Deploying to Aleo testnet..."
DEPLOY_OUTPUT=$(leo deploy --private-key "$PRIVATE_KEY" --broadcast --yes 2>&1)
echo "$DEPLOY_OUTPUT"

# Extract transaction ID from output
AGENT_TX_ID=$(echo "$DEPLOY_OUTPUT" | grep -oE 'at1[a-z0-9]{58}' | head -1)
if [ ! -z "$AGENT_TX_ID" ]; then
    echo ""
    echo "✅ agent_registry_v2.aleo deployed!"
    echo "Transaction ID: $AGENT_TX_ID"
    echo "View on AleoScan: https://testnet.aleoscan.io/transaction?id=$AGENT_TX_ID"
    echo ""
else
    echo "⚠️  Could not extract transaction ID. Check deployment output above."
fi

# Wait a bit between deployments
echo "Waiting 10 seconds before next deployment..."
sleep 10

# Deploy trust_verifier_v2
echo "📋 Step 2/2: Deploying trust_verifier_v2.aleo"
echo "=============================================="
cd "$PROJECT_ROOT/src/contracts/trust_verifier"

echo "Building contract..."
leo build --network testnet || {
    echo "❌ Build failed for trust_verifier_v2"
    exit 1
}

echo "Deploying to Aleo testnet..."
DEPLOY_OUTPUT=$(leo deploy --private-key "$PRIVATE_KEY" --broadcast --yes 2>&1)
echo "$DEPLOY_OUTPUT"

# Extract transaction ID from output
TRUST_TX_ID=$(echo "$DEPLOY_OUTPUT" | grep -oE 'at1[a-z0-9]{58}' | head -1)
if [ ! -z "$TRUST_TX_ID" ]; then
    echo ""
    echo "✅ trust_verifier_v2.aleo deployed!"
    echo "Transaction ID: $TRUST_TX_ID"
    echo "View on AleoScan: https://testnet.aleoscan.io/transaction?id=$TRUST_TX_ID"
    echo ""
else
    echo "⚠️  Could not extract transaction ID. Check deployment output above."
fi

# Summary
echo ""
echo "🎉 Deployment Summary"
echo "===================="
echo ""
echo "✅ Deployed Contracts:"
echo "1. hallucination_verifier.aleo (previously deployed)"
echo "   TX: at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt"
echo "   View: https://testnet.aleoscan.io/program?id=hallucination_verifier.aleo"
echo ""

if [ ! -z "$AGENT_TX_ID" ]; then
    echo "2. agent_registry_v2.aleo"
    echo "   TX: $AGENT_TX_ID"
    echo "   View: https://testnet.aleoscan.io/transaction?id=$AGENT_TX_ID"
    echo ""
fi

if [ ! -z "$TRUST_TX_ID" ]; then
    echo "3. trust_verifier_v2.aleo"
    echo "   TX: $TRUST_TX_ID"
    echo "   View: https://testnet.aleoscan.io/transaction?id=$TRUST_TX_ID"
    echo ""
fi

echo "Next steps:"
echo "1. Wait 2-3 minutes for transactions to be confirmed"
echo "2. Search for contract names on AleoScan:"
echo "   - agent_registry_v2.aleo"
echo "   - trust_verifier_v2.aleo"
echo "3. Update documentation with deployment details"
echo ""

# Save deployment info
cd "$PROJECT_ROOT"
echo "Saving deployment information..."
cat > LATEST_DEPLOYMENT.md << EOF
# Latest Deployment Information
**Date**: $(date)

## agent_registry_v2.aleo
- Transaction: $AGENT_TX_ID
- Explorer: https://testnet.aleoscan.io/transaction?id=$AGENT_TX_ID

## trust_verifier_v2.aleo
- Transaction: $TRUST_TX_ID
- Explorer: https://testnet.aleoscan.io/transaction?id=$TRUST_TX_ID
EOF

echo "✅ Deployment information saved to LATEST_DEPLOYMENT.md"
echo ""
echo "🏁 Deployment script completed!"
