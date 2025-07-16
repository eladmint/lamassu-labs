# Aleo Smart Contract Deployment Commands

**Date**: June 22, 2025
**Network**: Aleo Testnet

## Prerequisites Completed ✅

- [x] Leo CLI installed (v2.7.1)
- [x] Aleo CLI installed
- [x] Account created: `aleo176m09rv6qslzx0r7uyuerz3keq346lkdqhwtk2w8ffsk4rdsxyrqj9xx5m`
- [x] Testnet tokens received
- [x] Contracts compiled successfully

## Deployment Commands

### 1. Deploy Agent Registry Contract

```bash
cd /Users/eladm/Projects/token/tokenhunter/lamassu-labs/test_build/agent_registry_test

# Set up environment
cat > .env << EOF
NETWORK=testnet
PRIVATE_KEY=YOUR_PRIVATE_KEY_HERE
ENDPOINT=https://api.explorer.provable.com/v1
EOF

# Deploy
leo deploy --network testnet
```

### 2. Deploy Trust Verifier Contract

```bash
cd /Users/eladm/Projects/token/tokenhunter/lamassu-labs/trust_verifier_test

# Set up environment
cat > .env << EOF
NETWORK=testnet
PRIVATE_KEY=YOUR_PRIVATE_KEY_HERE
ENDPOINT=https://api.explorer.provable.com/v1
EOF

# Build first
leo build

# Deploy
leo deploy --network testnet
```

## After Deployment

1. **Save the program IDs** (e.g., `agent_registry_test.aleo`, `trust_verifier_test.aleo`)
2. **Save the transaction IDs** for verification
3. **Update integration tests** with deployed addresses
4. **Test contract interactions** using Leo CLI

## Testing Deployed Contracts

### Test Agent Registration

```bash
leo execute register_agent \
  1234field \
  "{accuracy: 8500u32, latency: 200u32, tasks_completed: 150u32, success_rate: 9000u32}" \
  1000000u64 \
  100u32 \
  --network testnet
```

### Test Execution Verification

```bash
leo execute verify_execution \
  5678field \
  1234field \
  999field \
  999field \
  100u32 \
  --network testnet
```

## Monitoring

Use the contract monitor to track your deployed contracts:

```bash
cd /Users/eladm/Projects/token/tokenhunter/lamassu-labs
python monitoring/contract_monitor.py --network testnet
```
