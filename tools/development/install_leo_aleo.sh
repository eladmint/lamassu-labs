#!/bin/bash

# Leo & Aleo Installation Script
# This script installs all necessary tools for Aleo development

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Leo & Aleo Installation Script${NC}"
echo -e "${GREEN}=================================${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

if ! command_exists rustc; then
    echo -e "${RED}❌ Rust is not installed. Please install Rust first:${NC}"
    echo "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
    exit 1
else
    echo -e "${GREEN}✅ Rust is installed: $(rustc --version)${NC}"
fi

# Update Rust to latest
echo -e "\n${YELLOW}📦 Updating Rust to latest version...${NC}"
rustup update

# Install Leo
echo -e "\n${YELLOW}📦 Installing Leo...${NC}"
if command_exists leo; then
    echo -e "${GREEN}✅ Leo is already installed: $(leo --version)${NC}"
    echo -e "${YELLOW}   Updating to latest version...${NC}"
fi

# Download and install Leo
curl -L https://install.aleo.org | bash

# Add to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.aleo/bin:"* ]]; then
    echo -e "\n${YELLOW}🔧 Adding Leo to PATH...${NC}"
    echo 'export PATH="$HOME/.aleo/bin:$PATH"' >> ~/.zshrc
    export PATH="$HOME/.aleo/bin:$PATH"
    echo -e "${GREEN}✅ Added to ~/.zshrc${NC}"
fi

# Install SnarkOS
echo -e "\n${YELLOW}📦 Installing SnarkOS...${NC}"
if command_exists snarkos; then
    echo -e "${GREEN}✅ SnarkOS is already installed: $(snarkos --version)${NC}"
else
    cargo install snarkos
fi

# Install Aleo SDK (optional)
echo -e "\n${YELLOW}📦 Installing Aleo SDK...${NC}"
if command_exists aleo; then
    echo -e "${GREEN}✅ Aleo SDK is already installed: $(aleo --version)${NC}"
else
    cargo install aleo
fi

# Verify installations
echo -e "\n${GREEN}🔍 Verifying installations...${NC}"
echo -e "${GREEN}=================================${NC}"

# Source the updated PATH
source ~/.zshrc 2>/dev/null || source ~/.bash_profile 2>/dev/null || true

# Check Leo
if command_exists leo || [ -f "$HOME/.aleo/bin/leo" ]; then
    LEO_VERSION=$($HOME/.aleo/bin/leo --version 2>/dev/null || leo --version 2>/dev/null || echo "Unknown")
    echo -e "${GREEN}✅ Leo installed: $LEO_VERSION${NC}"
else
    echo -e "${RED}❌ Leo installation may have failed${NC}"
fi

# Check SnarkOS
if command_exists snarkos; then
    echo -e "${GREEN}✅ SnarkOS installed: $(snarkos --version)${NC}"
else
    echo -e "${RED}❌ SnarkOS not found${NC}"
fi

# Check Aleo
if command_exists aleo; then
    echo -e "${GREEN}✅ Aleo SDK installed: $(aleo --version)${NC}"
else
    echo -e "${YELLOW}⚠️  Aleo SDK not found (optional)${NC}"
fi

# Create or check Aleo account
echo -e "\n${YELLOW}🔑 Aleo Account Setup${NC}"
echo -e "${GREEN}=================================${NC}"

if [ -z "$ALEO_PRIVATE_KEY" ]; then
    echo -e "${YELLOW}No ALEO_PRIVATE_KEY found in environment.${NC}"
    echo -e "${YELLOW}Would you like to create a new account? (y/n)${NC}"
    read -r create_account
    
    if [[ $create_account == "y" || $create_account == "Y" ]]; then
        echo -e "\n${YELLOW}Creating new Aleo account...${NC}"
        snarkos account new
        echo -e "\n${RED}⚠️  IMPORTANT: Save the above keys securely!${NC}"
        echo -e "${YELLOW}Add to your ~/.zshrc:${NC}"
        echo 'export ALEO_PRIVATE_KEY="YOUR_PRIVATE_KEY_HERE"'
        echo 'export ALEO_NETWORK="testnet3"'
    fi
else
    echo -e "${GREEN}✅ ALEO_PRIVATE_KEY is already set${NC}"
fi

# Final instructions
echo -e "\n${GREEN}🎉 Installation Complete!${NC}"
echo -e "${GREEN}=================================${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Close and reopen your terminal, or run:"
echo "   source ~/.zshrc"
echo ""
echo "2. Verify Leo is accessible:"
echo "   leo --version"
echo ""
echo "3. If you created a new account, add your keys to ~/.zshrc"
echo ""
echo "4. Get testnet tokens from: https://faucet.aleo.org"
echo ""
echo "5. Deploy contracts:"
echo "   cd /Users/eladm/Projects/token/tokenhunter/lamassu-labs"
echo "   ./scripts/deploy_contracts.sh"
echo ""
echo -e "${GREEN}Happy building on Aleo! 🚀${NC}"