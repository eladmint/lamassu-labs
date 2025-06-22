# Testing Deployed Aleo Contracts

**Date**: June 22, 2025

## Issue: Executing Deployed Contracts

When contracts are deployed, executing them requires specific syntax. Here are the methods:

## Method 1: Local Testing (Leo Run)

Test your functions locally before on-chain execution:

```bash
cd /Users/eladm/Projects/token/tokenhunter/lamassu-labs/agent_registry_simple

# Test locally
leo run register_agent 7777field 1000000u64 9000u32 250u32 150u32
```

## Method 2: On-Chain Execution (Aleo CLI)

For deployed contracts, use the Aleo CLI:

```bash
# Set environment
export ALEO_PRIVATE_KEY="YOUR_PRIVATE_KEY"

# Execute on testnet
aleo execute agent_registry_simple.aleo register_agent \
  --inputs "7777field 1000000u64 9000u32 250u32 150u32" \
  --network testnet \
  --private-key $ALEO_PRIVATE_KEY \
  --endpoint https://api.explorer.provable.com/v1
```

## Method 3: Using Aleo SDK/API

```bash
# Query the program first
curl -X GET "https://api.explorer.provable.com/v1/testnet/program/agent_registry_simple.aleo"

# Execute via API (requires more setup)
```

## Viewing Your Deployed Programs

1. **Aleo Explorer**: https://explorer.aleo.org/
   - Search: `agent_registry_simple.aleo`
   - Search: `trust_verifier_test.aleo`

2. **API Query**:
```bash
# Get program info
curl https://api.explorer.provable.com/v1/testnet/program/agent_registry_simple.aleo
```

## Common Issues

1. **"Failed to parse program name"**: This occurs when trying to use `leo execute` on deployed programs
2. **Solution**: Use `leo run` for local testing or `aleo execute` for on-chain execution

## Next Steps

1. Test functions locally with `leo run`
2. View your programs on the explorer
3. Set up proper API integration for production use