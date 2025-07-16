#!/bin/bash

# Leo Contract Compilation Script
# Compiles Leo contracts without deploying

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
CONTRACTS_DIR="$(dirname "$0")/../src/contracts"

echo -e "${GREEN}🔨 Leo Contract Compilation Script${NC}"
echo ""

# Check if Leo is installed
if ! command -v leo &> /dev/null; then
    echo -e "${RED}❌ Leo is not installed. Please install it first:${NC}"
    echo "curl -L https://install.aleo.org | bash"
    exit 1
fi

# Compile a single contract
compile_contract() {
    local contract_file=$1
    local contract_name=$(basename "$contract_file" .leo)
    local contract_dir="$CONTRACTS_DIR/build_$contract_name"

    echo -e "\n${YELLOW}Compiling $contract_name...${NC}"

    # Create temporary build directory
    rm -rf "$contract_dir"
    mkdir -p "$contract_dir/src"

    # Initialize Leo project
    cd "$contract_dir"
    leo new "$contract_name" --path . > /dev/null 2>&1 || true

    # Copy contract file
    cp "$contract_file" "./src/main.leo"

    # Update program.json with correct program name
    cat > program.json <<EOF
{
  "program": "${contract_name}.aleo",
  "version": "1.0.0",
  "description": "Compiled from $contract_file",
  "license": "MIT"
}
EOF

    # Compile
    if leo build; then
        echo -e "${GREEN}✅ Successfully compiled $contract_name${NC}"
        echo -e "   Output: $contract_dir/build/"

        # Copy build artifacts back
        mkdir -p "$CONTRACTS_DIR/build"
        cp -r "build/." "$CONTRACTS_DIR/build/${contract_name}/" 2>/dev/null || true

        return 0
    else
        echo -e "${RED}❌ Failed to compile $contract_name${NC}"
        return 1
    fi
}

# Main compilation flow
main() {
    local success_count=0
    local fail_count=0

    # Find all Leo files
    echo -e "${YELLOW}Searching for Leo contracts...${NC}"
    local leo_files=($(find "$CONTRACTS_DIR" -name "*.leo" -type f))

    if [ ${#leo_files[@]} -eq 0 ]; then
        echo -e "${RED}No Leo files found in $CONTRACTS_DIR${NC}"
        exit 1
    fi

    echo -e "Found ${#leo_files[@]} Leo contracts"

    # Compile each contract
    for leo_file in "${leo_files[@]}"; do
        echo -e "\n${GREEN}═══════════════════════════════════${NC}"
        echo -e "${GREEN}Processing: $(basename "$leo_file")${NC}"
        echo -e "${GREEN}═══════════════════════════════════${NC}"

        if compile_contract "$leo_file"; then
            ((success_count++))
        else
            ((fail_count++))
        fi
    done

    # Summary
    echo -e "\n${GREEN}═══════════════════════════════════${NC}"
    echo -e "${GREEN}Compilation Summary${NC}"
    echo -e "${GREEN}═══════════════════════════════════${NC}"
    echo -e "Total contracts: ${#leo_files[@]}"
    echo -e "${GREEN}✅ Successful: $success_count${NC}"

    if [ $fail_count -gt 0 ]; then
        echo -e "${RED}❌ Failed: $fail_count${NC}"
    fi

    if [ $success_count -eq ${#leo_files[@]} ]; then
        echo -e "\n${GREEN}All contracts compiled successfully!${NC}"
        echo -e "\nBuild artifacts available in: $CONTRACTS_DIR/build/"
    fi

    # Cleanup temporary directories
    rm -rf "$CONTRACTS_DIR"/build_*
}

# Run main function
main "$@"
