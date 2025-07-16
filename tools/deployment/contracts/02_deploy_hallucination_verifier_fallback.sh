#!/bin/bash

# Final working deployment script

echo "🚀 Final Deployment Attempt - Alternative Endpoint"
echo ""

# Get private key
echo "Enter your private key:"
read -s PRIVATE_KEY

echo ""
echo "Trying deployment with alternative settings..."
echo ""

# Try with different endpoint and explicit consensus version
echo "Attempt 1: Using explorer.provable.com endpoint..."
leo deploy \
  --private-key "$PRIVATE_KEY" \
  --network testnet \
  --endpoint "https://api.explorer.provable.com/v1" \
  --consensus-version "v2.0" \
  --broadcast \
  --yes

if [ $? -ne 0 ]; then
    echo ""
    echo "Attempt 1 failed. Trying with testnet3 endpoint..."
    echo ""

    # Try with testnet3 specific endpoint
    leo deploy \
      --private-key "$PRIVATE_KEY" \
      --network testnet \
      --endpoint "https://api.explorer.aleo.org/v1/testnet3" \
      --consensus-version "v2.0" \
      --broadcast \
      --yes
fi

if [ $? -ne 0 ]; then
    echo ""
    echo "Alternative: Deploy without broadcast (offline mode)..."
    echo ""

    # Try offline deployment first
    leo deploy \
      --private-key "$PRIVATE_KEY" \
      --network testnet \
      --save ./deployment_output \
      --offline \
      --yes

    if [ $? -eq 0 ]; then
        echo "✅ Deployment transaction created successfully!"
        echo "📁 Transaction saved to: ./deployment_output"
        echo ""
        echo "To broadcast manually:"
        echo "1. Go to https://aleo.tools/"
        echo "2. Use 'Broadcast Transaction' feature"
        echo "3. Upload the transaction file from ./deployment_output"
    fi
fi

echo ""
echo "Deployment attempts completed!"
