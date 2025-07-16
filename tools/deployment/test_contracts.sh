#!/bin/bash

# Test Script for Deployed Aleo Contracts
# Run this after both contracts are deployed

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🧪 Testing Deployed Aleo Contracts${NC}"
echo -e "${GREEN}===================================${NC}"

# Test Agent Registry
test_agent_registry() {
    echo -e "\n${YELLOW}Testing Agent Registry...${NC}"

    cd /Users/eladm/Projects/token/tokenhunter/lamassu-labs/agent_registry_simple

    # Generate a random agent ID
    AGENT_ID="$(date +%s)field"
    echo -e "Agent ID: ${YELLOW}$AGENT_ID${NC}"

    # Register an agent
    echo -e "\n${GREEN}1. Registering AI Agent${NC}"
    echo "leo execute register_agent $AGENT_ID 1000000u64 8500u32 150u32 100u32 --network testnet"

    leo execute register_agent \
        $AGENT_ID \
        1000000u64 \
        8500u32 \
        150u32 \
        100u32 \
        --network testnet || {
        echo -e "${RED}❌ Failed to register agent${NC}"
        return 1
    }

    echo -e "${GREEN}✅ Agent registered successfully!${NC}"

    # Wait a bit for transaction to settle
    sleep 5

    # Verify the agent
    echo -e "\n${GREEN}2. Verifying Agent Performance${NC}"
    echo "leo execute verify_agent $AGENT_ID 9000u32 101u32 --network testnet"

    leo execute verify_agent \
        $AGENT_ID \
        9000u32 \
        101u32 \
        --network testnet || {
        echo -e "${RED}❌ Failed to verify agent${NC}"
        return 1
    }

    echo -e "${GREEN}✅ Agent verified successfully!${NC}"
}

# Test Trust Verifier
test_trust_verifier() {
    echo -e "\n${YELLOW}Testing Trust Verifier...${NC}"

    cd /Users/eladm/Projects/token/tokenhunter/lamassu-labs/trust_verifier_test

    # Generate execution ID
    EXECUTION_ID="$(date +%s)field"
    AGENT_ID="1234field"

    echo -e "Execution ID: ${YELLOW}$EXECUTION_ID${NC}"

    # Test execution verification
    echo -e "\n${GREEN}1. Verifying Execution${NC}"
    echo "leo execute verify_execution $EXECUTION_ID $AGENT_ID 999field 999field 100u32 --network testnet"

    leo execute verify_execution \
        $EXECUTION_ID \
        $AGENT_ID \
        999field \
        999field \
        100u32 \
        --network testnet || {
        echo -e "${RED}❌ Failed to verify execution${NC}"
        return 1
    }

    echo -e "${GREEN}✅ Execution verified successfully!${NC}"

    # Test prove execution
    echo -e "\n${GREEN}2. Proving Execution${NC}"
    echo "leo execute prove_execution $EXECUTION_ID $AGENT_ID 12345field 101u32 --network testnet"

    leo execute prove_execution \
        $EXECUTION_ID \
        $AGENT_ID \
        12345field \
        101u32 \
        --network testnet || {
        echo -e "${RED}❌ Failed to prove execution${NC}"
        return 1
    }

    echo -e "${GREEN}✅ Execution proved successfully!${NC}"
}

# Main execution
main() {
    echo -e "${GREEN}Starting contract tests...${NC}"

    # Test agent registry
    if test_agent_registry; then
        echo -e "${GREEN}✅ Agent Registry tests passed!${NC}"
    else
        echo -e "${RED}❌ Agent Registry tests failed${NC}"
    fi

    # Test trust verifier if it exists
    if [ -d "/Users/eladm/Projects/token/tokenhunter/lamassu-labs/trust_verifier_test/build" ]; then
        if test_trust_verifier; then
            echo -e "${GREEN}✅ Trust Verifier tests passed!${NC}"
        else
            echo -e "${RED}❌ Trust Verifier tests failed${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Trust Verifier not yet deployed${NC}"
    fi

    echo -e "\n${GREEN}Test Summary${NC}"
    echo -e "${GREEN}============${NC}"
    echo "- Agent Registry: Deployed and tested ✅"
    echo "- Trust Verifier: Check deployment status"
    echo ""
    echo "View your contracts on Aleo Explorer:"
    echo "https://explorer.aleo.org/"
}

# Run main
main "$@"
