# Leo & Aleo CLI Installation Guide

**Last Updated**: June 21, 2025
**Time Required**: 15-30 minutes
**Platform**: macOS (your system)

## Prerequisites Check

First, let's verify your system is ready:

```bash
# Check if you have Rust installed (required)
rustc --version

# If not installed, install Rust first:
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

## Step 1: Install Leo

Leo is the programming language for writing Aleo programs.

### Option A: Quick Install (Recommended)

```bash
# Download and run the Leo installer
curl -L https://install.aleo.org | bash

# Add Leo to your PATH
echo 'export PATH="$HOME/.aleo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify installation
leo --version
```

### Option B: Build from Source

```bash
# Clone the Leo repository
git clone https://github.com/AleoHQ/leo
cd leo

# Build and install
cargo install --path .

# Verify installation
leo --version
```

## Step 2: Install SnarkOS

SnarkOS is needed for deploying to the Aleo network.

```bash
# Install snarkOS
cargo install snarkos

# Verify installation
snarkos --version
```

## Step 3: Install Aleo SDK (Optional but Recommended)

```bash
# Install the Aleo development tools
cargo install aleo

# Verify installation
aleo --version
```

## Step 4: Verify Complete Installation

Run this verification script:

```bash
#!/bin/bash
echo "🔍 Checking Leo and Aleo installation..."
echo ""

# Check Leo
if command -v leo &> /dev/null; then
    echo "✅ Leo installed: $(leo --version)"
else
    echo "❌ Leo not found"
fi

# Check SnarkOS
if command -v snarkos &> /dev/null; then
    echo "✅ SnarkOS installed: $(snarkos --version)"
else
    echo "❌ SnarkOS not found"
fi

# Check Aleo
if command -v aleo &> /dev/null; then
    echo "✅ Aleo installed: $(aleo --version)"
else
    echo "⚠️  Aleo not found (optional)"
fi

echo ""
echo "📁 Leo installation path: $(which leo)"
```

## Step 5: Configure Your Environment

### Create Aleo Account (if you don't have one)

```bash
# Generate new Aleo account
snarkos account new

# You'll see output like:
# Private Key: APrivateKey1zkp8CZNn3yeCseEtxuVPbDCwSyhGW6yZKUYKfgXmcpoGPWH
# View Key: AViewKey1mSnpFFC8Mj4fXbK5YiWgZ3mjiV8CxA79bYNa8ymUpTrw
# Address: aleo1rhgdu77hgyqd3xjj8ucu3jj9r2krwz6mnzyd80gncr5fxcwlh5rsvzp9px

# IMPORTANT: Save these keys securely!
```

### Set Environment Variables

```bash
# Add to your ~/.zshrc or ~/.bash_profile
echo 'export ALEO_PRIVATE_KEY="YOUR_PRIVATE_KEY_HERE"' >> ~/.zshrc
echo 'export ALEO_NETWORK="testnet3"' >> ~/.zshrc
source ~/.zshrc
```

## Step 6: Test Your Installation

### Test Leo Compilation

```bash
cd /Users/eladm/Projects/token/tokenhunter/lamassu-labs

# Try compiling a contract
cd src/contracts
leo new test_project
cd test_project
leo build

# If successful, you'll see:
# ✅ Compiled 'test_project.aleo'
```

### Test Aleo Connection

```bash
# Check testnet status
curl https://api.explorer.aleo.org/v1/testnet3/latest/height

# Get testnet tokens (for deployment)
# Visit: https://faucet.aleo.org
# Enter your address to receive test tokens
```

## Troubleshooting

### Common Issues

#### 1. "leo: command not found"
```bash
# Make sure PATH is updated
echo $PATH | grep -q ".aleo/bin" || echo 'export PATH="$HOME/.aleo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### 2. "error: failed to fetch"
```bash
# Clear cargo cache and retry
rm -rf ~/.cargo/registry/cache
cargo clean
# Then reinstall
```

#### 3. "SSL certificate problem"
```bash
# Update certificates
brew install ca-certificates
# Or on Linux:
sudo apt-get update && sudo apt-get install ca-certificates
```

#### 4. Build fails with "linking with cc failed"
```bash
# On macOS, install Xcode command line tools
xcode-select --install
```

## Next Steps After Installation

Once everything is installed, you can proceed with deployment:

```bash
# 1. Navigate to project
cd /Users/eladm/Projects/token/tokenhunter/lamassu-labs

# 2. Run deployment script
./scripts/deploy_contracts.sh

# 3. Or compile contracts manually
cd src/contracts
./scripts/compile_leo.sh
```

## Verification Checklist

- [ ] Leo version 1.9.0 or higher installed
- [ ] SnarkOS installed and accessible
- [ ] Aleo account created and keys saved
- [ ] Environment variables set
- [ ] Test compilation successful
- [ ] Can connect to Aleo testnet

## Resources

- **Leo Documentation**: https://developer.aleo.org/leo
- **Installation Issues**: https://github.com/AleoHQ/leo/issues
- **Discord Support**: https://discord.gg/aleohq
- **Faucet**: https://faucet.aleo.org

---

Once you've completed these steps, you'll be ready to deploy the smart contracts!
