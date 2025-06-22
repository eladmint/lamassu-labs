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

# Check balance using curl to the API
curl -s "https://api.explorer.aleo.org/v1/testnet/address/$ADDRESS" | grep -E '"public_balance"|"private_balance"' || echo "Failed to fetch balance. Please check the address."

echo ""