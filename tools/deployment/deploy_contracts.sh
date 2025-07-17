#!/bin/bash

# Aleo Contract Deployment Script
# Deploys both agent_registry and trust_verifier contracts to Aleo network

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
CONTRACTS_DIR="$(dirname "$0")/../../src/contracts"
NETWORK="${ALEO_NETWORK:-testnet3}"
PRIVATE_KEY="${ALEO_PRIVATE_KEY}"

echo -e "${GREEN}🚀 Aleo Contract Deployment Script${NC}"
echo -e "Network: ${YELLOW}$NETWORK${NC}"
echo ""

# Check dependencies
check_dependencies() {
    echo -e "${YELLOW}Checking dependencies...${NC}"
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Check for Aleo CLI (can substitute for Leo)
    if ! command -v aleo &> /dev/null; then
        # Add cargo bin to PATH if not there
        export PATH="$HOME/.cargo/bin:$PATH"
    fi
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    if ! command -v aleo &> /dev/null; then
        echo -e "${RED}❌ Aleo CLI is not installed. Please install it first:${NC}"
        echo "cargo install aleo"
        exit 1
    fi
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    if ! command -v snarkos &> /dev/null; then
        echo -e "${RED}❌ SnarkOS is not installed. Please install it first:${NC}"
        echo "cargo install snarkos"
        exit 1
    fi
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    if [ -z "$PRIVATE_KEY" ]; then
        echo -e "${RED}❌ ALEO_PRIVATE_KEY environment variable not set${NC}"
        echo "Please set your Aleo private key:"
        echo "export ALEO_PRIVATE_KEY=APrivateKey1zkp..."
        exit 1
    fi
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    echo -e "${GREEN}✅ All dependencies satisfied${NC}"
}

# Compile contract
compile_contract() {
    local contract_name=$1
    local contract_dir="$CONTRACTS_DIR/$contract_name"
<<<<<<< HEAD

    echo -e "\n${YELLOW}Compiling $contract_name...${NC}"

=======
    
    echo -e "\n${YELLOW}Compiling $contract_name...${NC}"
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Copy the Leo file to the contract directory
    cp "$CONTRACTS_DIR/${contract_name}_v2.leo" "$contract_dir/src/main.leo" 2>/dev/null || {
        mkdir -p "$contract_dir/src"
        cp "$CONTRACTS_DIR/${contract_name}_v2.leo" "$contract_dir/src/main.leo"
    }
<<<<<<< HEAD

    cd "$contract_dir"

=======
    
    cd "$contract_dir"
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Build the contract using Aleo CLI
    aleo build || {
        echo -e "${RED}❌ Failed to compile $contract_name${NC}"
        return 1
    }
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    echo -e "${GREEN}✅ Successfully compiled $contract_name${NC}"
    return 0
}

# Deploy contract
deploy_contract() {
    local contract_name=$1
    local contract_dir="$CONTRACTS_DIR/$contract_name"
<<<<<<< HEAD

    echo -e "\n${YELLOW}Deploying $contract_name to $NETWORK...${NC}"

    cd "$contract_dir"

=======
    
    echo -e "\n${YELLOW}Deploying $contract_name to $NETWORK...${NC}"
    
    cd "$contract_dir"
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Deploy using Aleo CLI
    aleo deploy --network "$NETWORK" --private-key "$PRIVATE_KEY" || {
        echo -e "${RED}❌ Failed to deploy $contract_name${NC}"
        return 1
    }
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Get deployment info
    local program_id="${contract_name}_v2.aleo"
    echo -e "${GREEN}✅ Successfully deployed $contract_name${NC}"
    echo -e "Program ID: ${YELLOW}$program_id${NC}"
<<<<<<< HEAD

    # Save deployment info
    echo "$program_id" > "$contract_dir/deployment_${NETWORK}.txt"

=======
    
    # Save deployment info
    echo "$program_id" > "$contract_dir/deployment_${NETWORK}.txt"
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    return 0
}

# Verify deployment
verify_deployment() {
    local contract_name=$1
    local program_id="${contract_name}_v2.aleo"
<<<<<<< HEAD

    echo -e "\n${YELLOW}Verifying deployment of $program_id...${NC}"

=======
    
    echo -e "\n${YELLOW}Verifying deployment of $program_id...${NC}"
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Query the program from the network
    snarkos developer scan --network "$NETWORK" --program "$program_id" || {
        echo -e "${RED}❌ Failed to verify $contract_name deployment${NC}"
        return 1
    }
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    echo -e "${GREEN}✅ Deployment verified on $NETWORK${NC}"
    return 0
}

# Main deployment flow
main() {
    echo -e "${GREEN}Starting Aleo contract deployment...${NC}"
<<<<<<< HEAD

    # Check dependencies
    check_dependencies

    # Deploy contracts
    local contracts=("agent_registry" "trust_verifier")
    local deployed_contracts=()

=======
    
    # Check dependencies
    check_dependencies
    
    # Deploy contracts
    local contracts=("agent_registry" "trust_verifier")
    local deployed_contracts=()
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    for contract in "${contracts[@]}"; do
        echo -e "\n${GREEN}═══════════════════════════════════${NC}"
        echo -e "${GREEN}Processing $contract${NC}"
        echo -e "${GREEN}═══════════════════════════════════${NC}"
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        if compile_contract "$contract"; then
            if deploy_contract "$contract"; then
                verify_deployment "$contract"
                deployed_contracts+=("$contract")
            fi
        fi
    done
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Summary
    echo -e "\n${GREEN}═══════════════════════════════════${NC}"
    echo -e "${GREEN}Deployment Summary${NC}"
    echo -e "${GREEN}═══════════════════════════════════${NC}"
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    if [ ${#deployed_contracts[@]} -eq ${#contracts[@]} ]; then
        echo -e "${GREEN}✅ All contracts deployed successfully!${NC}"
        echo -e "\nDeployed contracts:"
        for contract in "${deployed_contracts[@]}"; do
            echo -e "  - ${YELLOW}${contract}_v2.aleo${NC}"
        done
    else
        echo -e "${YELLOW}⚠️  Some contracts failed to deploy${NC}"
        echo -e "Successfully deployed: ${#deployed_contracts[@]}/${#contracts[@]}"
    fi
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    echo -e "\n${GREEN}Next steps:${NC}"
    echo "1. Save the program IDs for use in your application"
    echo "2. Update your .env files with the deployed addresses"
    echo "3. Test the contracts using the Leo CLI or SDK"
    echo ""
}

# Run main function
<<<<<<< HEAD
main "$@"
=======
main "$@"
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
