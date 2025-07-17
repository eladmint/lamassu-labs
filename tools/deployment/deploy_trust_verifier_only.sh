#!/bin/bash

# Deploy only trust_verifier_v2.aleo

echo "🚀 Deploying trust_verifier_v2.aleo"
echo "===================================="
echo ""

# Get the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to trust_verifier directory
cd "$SCRIPT_DIR/src/contracts/trust_verifier"

echo "Current directory: $(pwd)"
echo ""

# Get private key
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

# Build
echo "Building contract..."
leo build --network testnet || {
    echo "❌ Build failed"
    exit 1
}

# Deploy
echo "Deploying to Aleo testnet..."
DEPLOY_OUTPUT=$(leo deploy --private-key "$PRIVATE_KEY" --broadcast --yes 2>&1)
echo "$DEPLOY_OUTPUT"

# Extract transaction ID
TX_ID=$(echo "$DEPLOY_OUTPUT" | grep -oE 'at1[a-z0-9]{58}' | head -1)
if [ ! -z "$TX_ID" ]; then
    echo ""
    echo "✅ trust_verifier_v2.aleo deployed!"
    echo "Transaction ID: $TX_ID"
    echo "View on AleoScan: https://testnet.aleoscan.io/transaction?id=$TX_ID"
    echo ""
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Save deployment info
    cd "$SCRIPT_DIR"
    echo "## trust_verifier_v2.aleo" >> LATEST_DEPLOYMENT.md
    echo "- Transaction: $TX_ID" >> LATEST_DEPLOYMENT.md
    echo "- Explorer: https://testnet.aleoscan.io/transaction?id=$TX_ID" >> LATEST_DEPLOYMENT.md
    echo "" >> LATEST_DEPLOYMENT.md
else
    echo "⚠️  Could not extract transaction ID. Check deployment output above."
fi

echo ""
echo "📊 Deployment Summary So Far:"
echo "============================"
echo "✅ agent_registry_v2.aleo"
echo "   TX: at1hyqa37uskww30l4trcwf6kmzfdhhszjv982cmtdsszy8ml7h959qgfq8h9"
echo "   View: https://testnet.aleoscan.io/transaction?id=at1hyqa37uskww30l4trcwf6kmzfdhhszjv982cmtdsszy8ml7h959qgfq8h9"
echo ""
echo "⏳ trust_verifier_v2.aleo - Check transaction above"
echo ""
<<<<<<< HEAD
echo "🏁 Done!"
=======
echo "🏁 Done!"
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
