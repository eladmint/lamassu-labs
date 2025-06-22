# Aleo Smart Contract Deployment Guide

**Service**: Smart Contracts  
**Network**: Aleo testnet  
**Status**: ✅ Production Ready  
**Date**: June 22, 2025

## 📋 Deployment Overview

This guide covers deployment of TrustWrapper smart contracts to Aleo blockchain.

### ✅ Successfully Deployed Contracts

#### hallucination_verifier.aleo
- **Deployment TX**: `at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt`
- **Cost**: 8.633225 credits
- **Date**: June 22, 2025
- **Status**: ✅ Live and verified

## 🚀 Deployment Process

### Prerequisites

1. **Aleo CLI Tools**:
   ```bash
   # Install Leo
   cargo install leo-lang
   
   # Install Aleo CLI
   cargo install aleo
   ```

2. **Testnet Credits**: Minimum 10 credits for deployment

3. **Private Key**: Aleo account private key starting with `APrivateKey1zkp...`

### Standard Deployment Scripts

Located in `scripts/contracts/`:

#### 01_deploy_hallucination_verifier.sh (Primary)
- **Purpose**: Standard deployment with .env configuration
- **Requirements**: .env file with NETWORK and ENDPOINT
- **Usage**: Interactive, prompts for private key
- **Success Rate**: ✅ Verified working

#### 02_deploy_hallucination_verifier_fallback.sh (Fallback)
- **Purpose**: Multiple endpoint fallback deployment
- **Features**: Tries multiple endpoints, offline mode
- **Usage**: When primary deployment fails
- **Capabilities**: Creates offline transaction if needed

#### 03_test_hallucination_verifier.sh (Testing)
- **Purpose**: Execute test transaction on deployed contract
- **Function**: Calls `verify_response` with test data
- **Usage**: Verify contract functionality post-deployment

### Deployment Commands

```bash
# Navigate to project root
cd /path/to/lamassu-labs

# Deploy contract (recommended)
./scripts/contracts/01_deploy_hallucination_verifier.sh

# Or deploy with fallback options
./scripts/contracts/02_deploy_hallucination_verifier_fallback.sh

# Test deployed contract
./scripts/contracts/03_test_hallucination_verifier.sh
```

## 🔧 Configuration

### .env File Setup
Create `.env` in contract directory:
```bash
NETWORK=testnet
ENDPOINT=https://api.explorer.provable.com/v1
```

### Network Endpoints
- **Primary**: `https://api.explorer.provable.com/v1`
- **Secondary**: `https://api.explorer.aleo.org/v1`
- **Testnet3**: `https://api.explorer.aleo.org/v1/testnet3`

## 📊 Deployment Results

### Live Deployment (June 22, 2025)

```
📦 Deployment Summary for hallucination_verifier.aleo
──────────────────────────────────────────────
  Total Variables:      90,472
  Total Constraints:    69,337

💰 Cost Breakdown (credits)
  Transaction Storage:  3.638000
  Program Synthesis:    3.995225
  Namespace:            1.000000
  Priority Fee:         0.000000
  Total Fee:            8.633225
──────────────────────────────────────────────

✉️ Broadcasted transaction with:
  - transaction ID: 'at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt'
  - fee ID: 'au1p690uyap60ah3c0zl4tfyffswq7xclq9s5lrtwlw5ug266ahxgrq25pgdu'

✅ Deployment confirmed!
```

## 🔍 Verification

### Check Deployment Status
1. **Transaction ID**: `at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt`
2. **Aleo Tools**: https://aleo.tools/
3. **Account**: `aleo176m09rv6qslzx0r7uyuerz3keq346lkdqhwtk2w8ffsk4rdsxyrqj9xx5m`

### Test Contract Function
```bash
leo execute verify_response \
  12345field \
  67890field \
  95u8 \
  3u8 \
  1u8 \
  aleo176m09rv6qslzx0r7uyuerz3keq346lkdqhwtk2w8ffsk4rdsxyrqj9xx5m
```

## 🚨 Troubleshooting

### Common Issues

1. **Endpoint Errors**:
   ```
   Error: Failed to get consensus version
   ```
   **Solution**: Use different endpoint or add `--consensus-version v2.0`

2. **File Not Found**:
   ```
   Error: Program could not be found
   ```
   **Solution**: Ensure compiled `.aleo` file exists in directory

3. **Insufficient Credits**:
   ```
   Error: Insufficient balance
   ```
   **Solution**: Get more testnet credits or reduce fee

### Recovery Steps

1. **Check Balance**: Visit https://aleo.tools/ with your address
2. **Retry Deployment**: Use fallback script with different endpoint
3. **Offline Mode**: Create transaction offline, broadcast manually

## 📚 Related Documentation

- **[Aleo Blockchain Integration](../../hackathon/ALEO_BLOCKCHAIN_INTEGRATION.md)** - Complete integration details
- **[Smart Contract Source](../../../src/contracts/README.md)** - Contract documentation
- **[Project Standards](../../compliance/standards/PROJECT_STRUCTURE_STANDARDS.md)** - Organization standards

## 🏆 Production Notes

- **Status**: ✅ Production verified deployment
- **Network**: Aleo testnet (ready for mainnet)
- **Security**: Private key handling follows best practices
- **Monitoring**: Transaction IDs logged for audit trail
- **Backup**: All deployment scripts version controlled