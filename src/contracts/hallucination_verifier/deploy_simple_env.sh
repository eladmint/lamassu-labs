#!/bin/bash

# Simple deployment with .env file

echo "🚀 Simple Deployment with .env Configuration"
echo ""

# Get private key
echo "Enter your private key:"
read -s PRIVATE_KEY

echo ""
echo "Using .env file configuration..."
echo "Network: testnet"
echo "Endpoint: https://api.explorer.provable.com/v1"
echo ""

# Simple Leo deploy with .env
leo deploy --private-key "$PRIVATE_KEY" --broadcast --yes

echo ""
<<<<<<< HEAD
echo "Deployment completed!"
=======
echo "Deployment completed!"
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
