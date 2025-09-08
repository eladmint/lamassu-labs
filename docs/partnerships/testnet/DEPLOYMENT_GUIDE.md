# Celo Alfajores Testnet Deployment Guide

## Quick Setup for Real Deployment

### 1. Environment Setup

```bash
# Set your Celo private key (separate from Aleo PRIVATE_KEY)
export CELO_PRIVATE_KEY="your_celo_private_key_here"

# OR create a .env file
echo "CELO_PRIVATE_KEY=your_celo_private_key_here" > .env
```

### 2. Get Testnet CELO

Visit: https://faucet.celo.org
- Enter your wallet address
- Request testnet CELO tokens
- Wait for confirmation

### 3. Run Deployment

```bash
# Test connection first
python test_connection.py

# Deploy simple oracle
python deploy_simple.py

# OR deploy production-ready oracle
python deploy_oracle_real.py
```

## Key Changes Made

**Security Enhancement**: Changed from `PRIVATE_KEY` to `CELO_PRIVATE_KEY` to avoid conflicts with existing Aleo private keys in the project.

**Environment Separation**:
- `PRIVATE_KEY` - Used by Lamassu Labs Aleo contracts
- `CELO_PRIVATE_KEY` - Used by Mento Labs Celo integration

## Deployment Scripts

1. **`deploy_simple.py`** - Basic oracle deployment with comprehensive testing
2. **`deploy_oracle_real.py`** - Production-ready deployment with advanced error handling
3. **`test_connection.py`** - Test Celo Alfajores connectivity

## Ready for Real Deployment

✅ Web3 connectivity confirmed
✅ Scripts updated with proper environment variables
✅ No conflicts with existing Aleo keys
✅ Comprehensive error handling and validation

## Next Steps

1. Set your `CELO_PRIVATE_KEY` environment variable
2. Get testnet CELO from the faucet
3. Run the deployment script
4. Update sprint documentation with actual deployment results
