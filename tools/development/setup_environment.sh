#!/bin/bash

# Aleo Environment Setup for Puzzle Wallet Users
# Run this script after adding your keys from Puzzle Wallet

echo "🔧 Setting up Aleo environment for Lamassu Labs..."

# Check if Aleo CLI is available
if ! command -v aleo &> /dev/null; then
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Verify Aleo CLI
if ! command -v aleo &> /dev/null; then
    echo "❌ Aleo CLI not found. Please ensure it's installed."
    exit 1
fi

echo "✅ Aleo CLI found: $(which aleo)"

# Check environment variables
if [ -z "$ALEO_PRIVATE_KEY" ]; then
    echo "⚠️  ALEO_PRIVATE_KEY not set."
    echo "Please export your private key from Puzzle Wallet and add to ~/.zshrc:"
    echo 'export ALEO_PRIVATE_KEY="your-private-key-here"'
    echo 'export ALEO_ADDRESS="your-address-here"'
    echo 'export ALEO_NETWORK="testnet3"'
    echo ""
    echo "Then run: source ~/.zshrc"
    echo ""
    exit 1
fi

echo "✅ Environment variables configured"
echo "   Address: $ALEO_ADDRESS"
echo "   Network: $ALEO_NETWORK"

# Test contract compilation
echo ""
echo "🧪 Testing contract compilation..."

cd /Users/eladm/Projects/token/tokenhunter/lamassu-labs

# Test agent registry contract compilation
if [ -f "src/contracts/agent_registry_v2.leo" ]; then
    echo "Testing agent_registry_v2 compilation..."
    mkdir -p build/agent_registry_v2
    cp src/contracts/agent_registry_v2.leo build/agent_registry_v2/main.leo
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Create program.json for agent registry
    cat > build/agent_registry_v2/program.json << EOF
{
    "program": "agent_registry_v2.aleo",
    "version": "1.0.0",
    "description": "AI Agent Registry with Performance Verification",
    "license": "MIT"
}
EOF
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    cd build/agent_registry_v2
    if aleo build; then
        echo "✅ agent_registry_v2 compilation successful!"
    else
        echo "❌ agent_registry_v2 compilation failed"
    fi
    cd ../../
fi

# Test trust verifier contract compilation
if [ -f "src/contracts/trust_verifier_v2.leo" ]; then
    echo "Testing trust_verifier_v2 compilation..."
    mkdir -p build/trust_verifier_v2
    cp src/contracts/trust_verifier_v2.leo build/trust_verifier_v2/main.leo
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Create program.json for trust verifier
    cat > build/trust_verifier_v2/program.json << EOF
{
    "program": "trust_verifier_v2.aleo",
    "version": "1.0.0",
    "description": "AI Execution Trust Verification",
    "license": "MIT"
}
EOF
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    cd build/trust_verifier_v2
    if aleo build; then
        echo "✅ trust_verifier_v2 compilation successful!"
    else
        echo "❌ trust_verifier_v2 compilation failed"
    fi
    cd ../../
fi

echo ""
echo "🎉 Setup complete! Ready for deployment."
echo ""
echo "Next steps:"
echo "1. Get testnet tokens: https://faucet.aleo.org"
echo "2. Deploy contracts: ./scripts/deploy_contracts.sh"
<<<<<<< HEAD
echo "3. Run tests: python -m pytest tests/integration/"
=======
echo "3. Run tests: python -m pytest tests/integration/"
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
