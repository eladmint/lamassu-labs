#!/bin/bash

# Manual Leo Installation Script
# Alternative method for installing Leo

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔧 Manual Leo Installation${NC}"
echo -e "${GREEN}========================${NC}"
echo ""

# Method 1: Direct binary download
echo -e "${YELLOW}Method 1: Trying direct binary download...${NC}"

# Create directories
mkdir -p ~/.leo/bin

# Detect platform
OS=$(uname -s)
ARCH=$(uname -m)

if [ "$OS" = "Darwin" ] && [ "$ARCH" = "arm64" ]; then
    PLATFORM="apple-darwin"
    echo -e "${GREEN}✅ Detected: macOS ARM64 (Apple Silicon)${NC}"
elif [ "$OS" = "Darwin" ] && [ "$ARCH" = "x86_64" ]; then
    PLATFORM="apple-darwin"
    echo -e "${GREEN}✅ Detected: macOS x86_64${NC}"
elif [ "$OS" = "Linux" ] && [ "$ARCH" = "x86_64" ]; then
    PLATFORM="unknown-linux-gnu"
    echo -e "${GREEN}✅ Detected: Linux x86_64${NC}"
else
    echo -e "${RED}❌ Unsupported platform: $OS $ARCH${NC}"
    exit 1
fi

# Download Leo binary
LEO_VERSION="v1.9.3"  # Latest stable version
DOWNLOAD_URL="https://github.com/AleoHQ/leo/releases/download/${LEO_VERSION}/leo-x86_64-${PLATFORM}.zip"

echo -e "${YELLOW}Downloading Leo ${LEO_VERSION}...${NC}"
echo "URL: $DOWNLOAD_URL"

cd /tmp
curl -L -o leo.zip "$DOWNLOAD_URL" || {
    echo -e "${RED}❌ Download failed. Trying alternative method...${NC}"
    
    # Method 2: Build from source
    echo -e "${YELLOW}Method 2: Building from source...${NC}"
    
    # Clone repository
    if [ -d "leo" ]; then
        rm -rf leo
    fi
    
    git clone https://github.com/AleoHQ/leo.git
    cd leo
    
    # Checkout stable version
    git checkout tags/${LEO_VERSION}
    
    # Build with cargo
    echo -e "${YELLOW}Building Leo (this may take several minutes)...${NC}"
    cargo build --release
    
    # Copy binary
    cp target/release/leo ~/.leo/bin/
    
    echo -e "${GREEN}✅ Built from source successfully${NC}"
}

# If download succeeded, extract
if [ -f "/tmp/leo.zip" ]; then
    echo -e "${YELLOW}Extracting Leo...${NC}"
    unzip -o leo.zip
    
    # Find and move the leo binary
    if [ -f "leo" ]; then
        chmod +x leo
        mv leo ~/.leo/bin/
        echo -e "${GREEN}✅ Leo binary installed${NC}"
    else
        echo -e "${RED}❌ Leo binary not found in archive${NC}"
        exit 1
    fi
fi

# Update PATH
echo -e "\n${YELLOW}Updating PATH...${NC}"

# Add to .zshrc if not already there
if ! grep -q "export PATH=\"\$HOME/.leo/bin:\$PATH\"" ~/.zshrc; then
    echo 'export PATH="$HOME/.leo/bin:$PATH"' >> ~/.zshrc
    echo -e "${GREEN}✅ Added to ~/.zshrc${NC}"
fi

# Also add to .bash_profile for compatibility
if [ -f ~/.bash_profile ] && ! grep -q "export PATH=\"\$HOME/.leo/bin:\$PATH\"" ~/.bash_profile; then
    echo 'export PATH="$HOME/.leo/bin:$PATH"' >> ~/.bash_profile
    echo -e "${GREEN}✅ Added to ~/.bash_profile${NC}"
fi

# Export for current session
export PATH="$HOME/.leo/bin:$PATH"

# Verify installation
echo -e "\n${YELLOW}Verifying installation...${NC}"

if [ -f "$HOME/.leo/bin/leo" ]; then
    echo -e "${GREEN}✅ Leo binary found at: $HOME/.leo/bin/leo${NC}"
    
    # Make it executable
    chmod +x "$HOME/.leo/bin/leo"
    
    # Test execution
    if "$HOME/.leo/bin/leo" --help >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Leo is working!${NC}"
        
        # Show version
        echo -e "\n${GREEN}Leo installation complete!${NC}"
        echo -e "Version info:"
        "$HOME/.leo/bin/leo" --help | head -5
    else
        echo -e "${RED}❌ Leo binary exists but won't execute${NC}"
        echo "Trying to diagnose..."
        file "$HOME/.leo/bin/leo"
        ldd "$HOME/.leo/bin/leo" 2>/dev/null || true
    fi
else
    echo -e "${RED}❌ Leo installation failed${NC}"
fi

# Cleanup
rm -f /tmp/leo.zip

echo -e "\n${YELLOW}Next steps:${NC}"
echo "1. Run: source ~/.zshrc"
echo "2. Test: leo --help"
echo "3. If leo command not found, use full path: ~/.leo/bin/leo --help"