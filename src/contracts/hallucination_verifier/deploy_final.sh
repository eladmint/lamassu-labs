#!/bin/bash

# Final deployment script - should work now

echo "🚀 Final Deployment Attempt"
echo ""

# Verify files exist
if [ ! -f "hallucination_verifier.aleo" ]; then
    echo "Copying compiled contract..."
    cp build/main.aleo hallucination_verifier.aleo
fi

echo "✅ Contract file ready: hallucination_verifier.aleo"
echo ""

# Get private key
echo "Enter your private key:"
read -s PRIVATE_KEY

echo ""
echo "Deploying to Aleo testnet..."
echo ""

# Deploy with the correct file in place
aleo deploy --private-key "$PRIVATE_KEY" --fee 3000000 hallucination_verifier.aleo

echo ""
echo "Deployment attempt completed!"
echo "Look for transaction ID above!"