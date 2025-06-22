#!/bin/bash

# Check balance using snarkOS

echo "🔍 Checking Aleo Testnet Balance"
echo ""
echo "Enter your Aleo address:"
read ADDRESS

if [[ ! "$ADDRESS" =~ ^aleo1 ]]; then
    echo "❌ Invalid address"
    exit 1
fi

echo ""
echo "Checking balance using snarkOS..."
echo ""

# Use snarkos to query account
snarkos developer scan --network testnet --address "$ADDRESS" 2>&1 | grep -A5 -B5 "balance\|credits\|Credits" || echo "Could not fetch balance via snarkOS"

echo ""
echo "Alternative: Check your balance online at:"
echo "🌐 https://aleoscan.io/address?a=$ADDRESS"
echo ""