#!/bin/bash

# Local Testing Script for Aleo Contracts
# This tests contracts locally without on-chain execution

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🧪 Testing Contracts Locally${NC}"
echo -e "${GREEN}=============================${NC}"

# Test Agent Registry
echo -e "\n${YELLOW}Testing Agent Registry Simple...${NC}"
cd /Users/eladm/Projects/token/tokenhunter/lamassu-labs/agent_registry_simple

echo "Running: leo run register_agent 7777field 1000000u64 9000u32 250u32 150u32"
leo run register_agent 7777field 1000000u64 9000u32 250u32 150u32

echo -e "\n${YELLOW}Testing verify_agent...${NC}"
echo "Running: leo run verify_agent 7777field 9500u32 151u32"
leo run verify_agent 7777field 9500u32 151u32

# Test Trust Verifier
echo -e "\n${YELLOW}Testing Trust Verifier...${NC}"
cd /Users/eladm/Projects/token/tokenhunter/lamassu-labs/trust_verifier_test

echo "Running: leo run verify_execution 5555field 7777field 999field 999field 200u32"
leo run verify_execution 5555field 7777field 999field 999field 200u32

echo "Running: leo run prove_execution 6666field 7777field 12345field 201u32"
leo run prove_execution 6666field 7777field 12345field 201u32

echo -e "\n${GREEN}✅ Local testing complete!${NC}"
echo -e "\nYour contracts are deployed at:"
echo "- agent_registry_simple.aleo"
echo "- trust_verifier_test.aleo"
echo ""
echo "View them at: https://explorer.aleo.org/"
