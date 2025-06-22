#!/bin/bash

# Test the deployed contract with a real transaction

echo "🧪 Testing Deployed Contract"
echo "=============================="
echo ""
echo "Contract: hallucination_verifier.aleo"
echo "Deployment TX: at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt"
echo ""

# Get private key
echo "Enter your private key to execute a test transaction:"
read -s PRIVATE_KEY

echo ""
echo "Executing verify_response function..."
echo ""

# Execute the verify_response function with test data
leo execute verify_response \
  12345field \
  67890field \
  95u8 \
  3u8 \
  1u8 \
  aleo176m09rv6qslzx0r7uyuerz3keq346lkdqhwtk2w8ffsk4rdsxyrqj9xx5m \
  --private-key "$PRIVATE_KEY" \
  --broadcast \
  --yes

echo ""
echo "Test transaction completed!"