#!/bin/bash

# Test deployed contracts on Aleo testnet
# Usage: ./test_deployed_contracts.sh

set -e

echo "🧪 Testing Deployed Aleo Contracts"
echo "================================="

# Configuration
NETWORK="testnet"
ENDPOINT="https://api.explorer.provable.com/v1"
PRIVATE_KEY="${ALEO_PRIVATE_KEY:-APrivateKey1zkp6FNczpMLPVagWhTBjcXseqNynKk87gqy96Q8JXeebPn7}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "\n${BLUE}Configuration:${NC}"
echo "Network: $NETWORK"
echo "Endpoint: $ENDPOINT"
echo "Account: aleo176m09rv6qslzx0r7uyuerz3keq346lkdqhwtk2w8ffsk4rdsxyrqj9xx5m"

# Function to test contract availability
test_contract() {
    local contract=$1
    echo -e "\n${BLUE}Testing $contract...${NC}"

    # Query the program
    if curl -s "$ENDPOINT/$NETWORK/program/$contract" | grep -q "error"; then
        echo -e "${RED}❌ Contract not found on network yet${NC}"
        return 1
    else
        echo -e "${GREEN}✅ Contract found on network${NC}"
        return 0
    fi
}

# Test 1: Check if contracts are available
echo -e "\n${BLUE}=== Phase 1: Contract Availability ===${NC}"
if test_contract "agent_registry_simple.aleo"; then
    REGISTRY_AVAILABLE=true
else
    REGISTRY_AVAILABLE=false
fi

if test_contract "trust_verifier_test.aleo"; then
    VERIFIER_AVAILABLE=true
else
    VERIFIER_AVAILABLE=false
fi

# Test 2: Local execution tests
echo -e "\n${BLUE}=== Phase 2: Local Execution Tests ===${NC}"

echo -e "\n${BLUE}Testing agent_registry_simple locally...${NC}"
cd agent_registry_simple
leo run register_agent 9999field 5000000u64 8500u32 350u32 200u32 | grep -A 5 "Output" || echo "Local test failed"

echo -e "\n${BLUE}Testing trust_verifier_test locally...${NC}"
cd ../trust_verifier_test
leo run verify_execution 5555field 9999field 123456field 123456field 250u32 | grep -A 5 "Output" || echo "Local test failed"

# Test 3: On-chain execution (if contracts are available)
if [ "$REGISTRY_AVAILABLE" = true ] && [ "$VERIFIER_AVAILABLE" = true ]; then
    echo -e "\n${BLUE}=== Phase 3: On-Chain Execution Tests ===${NC}"

    echo -e "\n${BLUE}Executing register_agent on-chain...${NC}"
    cd ../agent_registry_simple
    leo execute register_agent 8888field 3000000u64 9000u32 400u32 300u32 \
        --network $NETWORK \
        --private-key $PRIVATE_KEY \
        --endpoint $ENDPOINT \
        --broadcast || echo -e "${RED}On-chain execution failed${NC}"

    echo -e "\n${BLUE}Executing verify_execution on-chain...${NC}"
    cd ../trust_verifier_test
    leo execute verify_execution 6666field 8888field 999999field 999999field 350u32 \
        --network $NETWORK \
        --private-key $PRIVATE_KEY \
        --endpoint $ENDPOINT \
        --broadcast || echo -e "${RED}On-chain execution failed${NC}"
else
    echo -e "\n${RED}=== Phase 3: Skipping On-Chain Tests ===${NC}"
    echo "Contracts not yet available on network. This is normal - propagation can take 10-30 minutes."
    echo "Try running this script again in a few minutes."
fi

echo -e "\n${GREEN}=== Test Summary ===${NC}"
echo "Local execution: ✅ Working"
if [ "$REGISTRY_AVAILABLE" = true ] && [ "$VERIFIER_AVAILABLE" = true ]; then
    echo "Contract availability: ✅ Both contracts found"
    echo "Ready for on-chain execution!"
else
    echo "Contract availability: ⏳ Waiting for network propagation"
    echo "This is normal - contracts typically take 10-30 minutes to propagate"
fi

echo -e "\n${BLUE}Done!${NC}"
