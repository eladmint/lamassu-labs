# Aleo Smart Contract Deployment Guide

**Last Updated**: June 21, 2025
**Version**: 2.0 (Security Enhanced)
**Network**: Aleo Testnet3 / Mainnet

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Contract Overview](#contract-overview)
4. [Compilation Process](#compilation-process)
5. [Deployment Steps](#deployment-steps)
6. [Post-Deployment Verification](#post-deployment-verification)
7. [Integration Guide](#integration-guide)
8. [Troubleshooting](#troubleshooting)
9. [Security Checklist](#security-checklist)

## Prerequisites

### Required Software

1. **Leo Language**
   ```bash
   curl -L https://install.aleo.org | bash
   source ~/.bashrc
   leo --version  # Should show 1.9.0 or higher
   ```

2. **SnarkOS** (for deployment)
   ```bash
   cargo install snarkos
   snarkos --version
   ```

3. **Python 3.8+** (for integration)
   ```bash
   python --version
   pip install aleo-python-sdk
   ```

### Required Accounts

1. **Aleo Account**
   - Generate new account: `leo account new`
   - Save private key securely
   - Fund account with testnet tokens: https://faucet.aleo.org

2. **Environment Variables**
   ```bash
   export ALEO_PRIVATE_KEY="APrivateKey1zkp..."
   export ALEO_NETWORK="testnet3"  # or "mainnet"
   ```

## Environment Setup

### 1. Clone Repository
```bash
git clone https://github.com/lamassu-labs/trustwrapper
cd lamassu-labs
```

### 2. Install Dependencies
```bash
# Python dependencies
pip install -r requirements.txt

# Verify Leo installation
leo --version
```

### 3. Configure Network
```bash
# For testnet
export ALEO_NETWORK="testnet3"
export ALEO_NODE_URL="https://api.testnet3.aleo.org"

# For mainnet
export ALEO_NETWORK="mainnet"
export ALEO_NODE_URL="https://api.aleo.org"
```

## Contract Overview

### 1. **agent_registry_v2.aleo**
- **Purpose**: AI agent registration with ZK performance verification
- **Key Features**:
  - Private performance metrics
  - Staking mechanism with lock periods
  - Owner-only updates
  - Safe math operations
  - Withdrawal functionality

### 2. **trust_verifier_v2.aleo**
- **Purpose**: Simple execution verification for AI agents
- **Key Features**:
  - Private execution metrics
  - Batch verification support
  - Proof integrity checks
  - Comprehensive validation

## Compilation Process

### Automated Compilation
```bash
# Compile all contracts
./scripts/compile_leo.sh

# Compile specific contract
cd src/contracts/agent_registry
leo build
```

### Manual Compilation
```bash
# 1. Navigate to contract directory
cd src/contracts/agent_registry

# 2. Initialize Leo project (if needed)
leo new agent_registry --path .

# 3. Copy contract code
cp ../agent_registry_v2.leo src/main.leo

# 4. Build contract
leo build

# 5. Check output
ls build/
```

### Compilation Output
- `build/main.aleo` - Compiled bytecode
- `build/main.prover` - Prover files
- `build/main.verifier` - Verifier files

## Deployment Steps

### 1. Pre-deployment Checks

```bash
# Check account balance
snarkos account balance $ALEO_PRIVATE_KEY

# Verify network connection
curl -X GET "$ALEO_NODE_URL/testnet3/latest/height"

# Test compilation
./scripts/compile_leo.sh
```

### 2. Automated Deployment

```bash
# Deploy all contracts
./scripts/deploy_contracts.sh

# Monitor deployment
tail -f deployment.log
```

### 3. Manual Deployment

```bash
# Navigate to contract
cd src/contracts/agent_registry

# Deploy to testnet
leo deploy --network testnet3

# Deploy to mainnet (requires credits)
leo deploy --network mainnet --fee 1000000
```

### 4. Record Deployment Info

Save deployment details:
```json
{
  "network": "testnet3",
  "contracts": {
    "agent_registry_v2.aleo": {
      "address": "aleo1...",
      "transaction": "at1...",
      "block_height": 1234567,
      "deployed_at": "2025-06-21T10:00:00Z"
    },
    "trust_verifier_v2.aleo": {
      "address": "aleo1...",
      "transaction": "at1...",
      "block_height": 1234568,
      "deployed_at": "2025-06-21T10:05:00Z"
    }
  }
}
```

## Post-Deployment Verification

### 1. Verify Contract Deployment
```bash
# Check contract exists
snarkos developer scan --network testnet3 --program agent_registry_v2.aleo

# Get contract details
curl -X GET "$ALEO_NODE_URL/testnet3/program/agent_registry_v2.aleo"
```

### 2. Test Contract Functions
```python
# Python test script
from src.zk.leo_integration import LeoProofGenerator
from src.zk.aleo_client import AleoClient

async def test_deployment():
    client = AleoClient(network='testnet3')
    generator = LeoProofGenerator('agent_registry_v2.aleo')

    # Test registration
    result = await generator.generate_execution_proof(
        agent_hash="test_agent_001",
        execution_time=1500,
        success=True
    )

    print(f"Proof generated: {result}")
```

### 3. Monitor Contract Activity
```bash
# Watch for transactions
snarkos developer scan --network testnet3 --program agent_registry_v2.aleo --watch

# Check specific transaction
snarkos transaction get --network testnet3 --id "at1..."
```

## Integration Guide

### 1. Python Integration
```python
# Initialize integration
from src.zk.leo_integration import LeoProofGenerator
from src.zk.aleo_client import AleoClient

# Configure client
client = AleoClient(
    network='testnet3',
    private_key=os.getenv('ALEO_PRIVATE_KEY')
)

# Create proof generator
generator = LeoProofGenerator('trust_verifier_v2.aleo')
generator.client = client

# Generate and submit proof
proof = await generator.generate_execution_proof(
    agent_hash="agent_001",
    execution_time=1234,
    success=True
)
```

### 2. Environment Configuration
```bash
# .env file
ALEO_NETWORK=testnet3
ALEO_PRIVATE_KEY=APrivateKey1zkp...
AGENT_REGISTRY_ADDRESS=aleo1...
TRUST_VERIFIER_ADDRESS=aleo1...
```

### 3. Error Handling
```python
try:
    result = await client.submit_transaction(tx_data)
except Exception as e:
    if "insufficient balance" in str(e):
        print("Need more credits")
    elif "network error" in str(e):
        print("Retry with backoff")
    else:
        raise
```

## Troubleshooting

### Common Issues

1. **Compilation Errors**
   ```
   Error: Type mismatch
   Solution: Check Leo syntax, ensure types match
   ```

2. **Deployment Failures**
   ```
   Error: Insufficient balance
   Solution: Get testnet tokens from faucet
   ```

3. **Network Timeouts**
   ```
   Error: Connection timeout
   Solution: Check network, use different RPC endpoint
   ```

### Debug Commands
```bash
# Check Leo installation
leo --version
which leo

# Verify network
curl -X GET "$ALEO_NODE_URL/testnet3/latest/height"

# Test account
snarkos account balance $ALEO_PRIVATE_KEY

# Clean build
rm -rf build/ && leo build
```

## Security Checklist

### Pre-Deployment
- [ ] Security audit completed
- [ ] All HIGH risk issues fixed
- [ ] Safe math implemented
- [ ] Access control added
- [ ] Withdrawal functions tested
- [ ] Input validation comprehensive

### Deployment
- [ ] Use dedicated deployment account
- [ ] Verify contract bytecode
- [ ] Check gas estimates
- [ ] Deploy to testnet first
- [ ] Monitor initial transactions

### Post-Deployment
- [ ] Verify all functions work
- [ ] Check access control
- [ ] Test edge cases
- [ ] Monitor for unusual activity
- [ ] Document all addresses
- [ ] Backup deployment data

## Mainnet Deployment Checklist

### Requirements
- [ ] All tests passing (100%)
- [ ] Security audit passed
- [ ] Testnet deployment successful
- [ ] 1+ week of testnet testing
- [ ] Documentation complete
- [ ] Emergency procedures ready

### Process
1. Final code review
2. Update to mainnet configuration
3. Calculate deployment costs
4. Deploy during low-traffic period
5. Immediate verification
6. Monitor for 24 hours

### Post-Mainnet
- [ ] Update all documentation
- [ ] Notify users of addresses
- [ ] Set up monitoring alerts
- [ ] Regular security reviews

## Support & Resources

- **Aleo Documentation**: https://developer.aleo.org
- **Leo Language Guide**: https://leo-lang.org
- **Discord Support**: https://discord.gg/aleo
- **GitHub Issues**: https://github.com/lamassu-labs/trustwrapper/issues

## Version History

- **v2.0** (Current): Security enhanced contracts with audit fixes
- **v1.0**: Initial hackathon version (DO NOT USE IN PRODUCTION)
