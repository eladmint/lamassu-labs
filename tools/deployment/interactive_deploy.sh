#!/bin/bash

# Interactive deployment helper for TrustWrapper contracts

echo "🚀 TrustWrapper Interactive Deployment Helper"
echo "==========================================="
echo ""
echo "This helper will guide you through deploying the remaining contracts."
echo ""
echo "📋 Current Status:"
echo "✅ hallucination_verifier.aleo - DEPLOYED"
echo "⏳ agent_registry_v2.aleo - READY TO DEPLOY"
echo "⏳ trust_verifier_v2.aleo - READY TO DEPLOY"
echo ""
echo "Choose an option:"
echo "1) Deploy agent_registry_v2.aleo only"
echo "2) Deploy trust_verifier_v2.aleo only"
echo "3) Deploy both contracts"
echo "4) Exit"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "Deploying agent_registry_v2.aleo..."
        cd src/contracts/agent_registry
        ./../../tools/deployment/contracts/01_deploy_agent_registry.sh
        ;;
    2)
        echo ""
        echo "Deploying trust_verifier_v2.aleo..."
        cd src/contracts/trust_verifier
        ./../../tools/deployment/contracts/01_deploy_trust_verifier.sh
        ;;
    3)
        echo ""
        echo "Deploying both contracts..."
        ./deploy_remaining_contracts.sh
        ;;
    4)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac
