#!/bin/bash

# Script to check Aleo account balance

echo "🔍 Aleo Account Balance Checker"
echo ""
echo "Please enter your Aleo address (starts with 'aleo1...'):"
read ADDRESS

if [[ ! "$ADDRESS" =~ ^aleo1 ]]; then
    echo "❌ Invalid address format. It should start with 'aleo1'"
    exit 1
fi

echo ""
echo "Checking balance for: $ADDRESS"
echo ""

# Try multiple API endpoints
echo "Trying Aleo API endpoints..."

# Try the Aleo API
echo "1. Checking via api.explorer.aleo.org..."
RESPONSE=$(curl -s "https://api.explorer.aleo.org/v1/testnet3/program/credits.aleo/mapping/account/$ADDRESS")
if [[ $RESPONSE == *"error"* ]] || [[ -z "$RESPONSE" ]]; then
    echo "   No data from explorer API"
else
    echo "   Response: $RESPONSE"
fi

# Try alternative endpoint
echo ""
echo "2. Checking via Aleo RPC..."
# Using snarkOS RPC endpoint
BALANCE=$(curl -s -X POST "https://api.explorer.aleo.org/v1/testnet3" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"getBalance\",\"params\":[\"$ADDRESS\"]}" 2>/dev/null)

if [[ ! -z "$BALANCE" ]]; then
    echo "   Balance info: $BALANCE"
fi

echo ""
echo "💡 You can also check your balance at:"
echo "   https://aleo.tools/account?address=$ADDRESS"
echo "   https://aleoscan.io/address?a=$ADDRESS"
echo ""