# Aleo Smart Contract Examples

This directory contains practical examples demonstrating how to use the Aleo smart contracts and TrustWrapper integration.

## Prerequisites

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   export ALEO_PRIVATE_KEY="APrivateKey1zkp..."  # Your Aleo private key
   export ALEO_NETWORK="testnet3"                 # or "mainnet"
   ```

3. **Deploy Contracts** (if not already deployed)
   ```bash
   ./scripts/deploy_contracts.sh
   ```

## Available Examples

### 1. 🤖 Register AI Agent (`register_agent.py`)
Demonstrates how to register an AI agent with hidden performance metrics using zero-knowledge proofs.

```bash
python examples/register_agent.py
```

**What it shows:**
- Connecting to Aleo network
- Creating private performance metrics
- Generating registration proof
- Submitting to blockchain
- Maintaining metric privacy

### 2. 🔍 Verify Execution (`verify_execution.py`)
Shows how to create ZK proofs of agent execution without revealing implementation details.

```bash
python examples/verify_execution.py
```

**What it shows:**
- Single execution verification
- Batch execution verification
- Metrics commitment generation
- Proof integrity checking

### 3. 🛡️ TrustWrapper Integration (`trustwrapper_integration.py`)
Complete example of wrapping existing AI agents with the TrustWrapper system.

```bash
python examples/trustwrapper_integration.py
```

**What it shows:**
- Basic agent wrapping
- Performance monitoring with 13.99x optimization
- Multi-agent marketplace
- Full Aleo integration

### 4. ⚡ Performance Optimization (`performance_optimization.py`)
Demonstrates the TrustWrapper Performance Module for enterprise-grade verification speed.

```bash
python examples/performance_optimization.py
```

**What it shows:**
- Baseline vs optimized verification performance
- 13.99x speed improvement demonstration
- Zero memory overhead optimization
- Real-time verification capabilities

## Quick Start

### Minimal Example
```python
from src.core.trust_wrapper import ZKTrustWrapper

# Your existing AI agent
agent = YourAIAgent()

# Wrap it with trust
trusted_agent = ZKTrustWrapper(agent)

# Use normally - now with ZK proofs!
result = await trusted_agent.verified_execute("your input")
print(f"Result: {result.result}")
print(f"Proof: {result.proof.proof_hash}")
```

## Common Patterns

### 1. Agent Registration Pattern
```python
# Define private metrics
metrics = {
    'accuracy': 9500,        # 95%
    'latency': 250,         # ms
    'tasks_completed': 1000,
    'success_rate': 9800    # 98%
}

# Register with hidden metrics
proof = await generator.generate_proof(
    function_name='register_agent',
    inputs={'agent_id': 'my_agent'},
    private_inputs={'metrics': metrics}
)
```

### 2. Execution Verification Pattern
```python
# Generate execution proof
proof = await generator.generate_execution_proof(
    agent_hash="agent_001",
    execution_time=1500,
    success=True,
    metrics_commitment="0xabc..."
)

# Verify on-chain
verified = await generator.verify_proof(proof)
```

### 3. Batch Processing Pattern
```python
# Batch multiple executions
proofs = await generator.generate_batch_proof(
    agent_hash="agent_001",
    execution_times=[1200, 1500, 1800],
    success_flags=[True, True, False],
    batch_size=3
)
```

## Best Practices

1. **Environment Setup**
   - Always use environment variables for keys
   - Never commit private keys to git
   - Use testnet for development

2. **Error Handling**
   ```python
   try:
       result = await trusted_agent.verified_execute(input)
   except Exception as e:
       logger.error(f"Execution failed: {e}")
       # Handle gracefully
   ```

3. **Performance Optimization**
   - Enable TrustWrapper Performance Module for 13.99x faster verification
   - Batch verifications when possible
   - Cache proof generation for repeated inputs
   - Monitor gas costs

4. **Security**
   - Validate all inputs before proof generation
   - Use secure random for any nonces
   - Regularly rotate keys

## Troubleshooting

### "Leo not installed" Error
```bash
curl -L https://install.aleo.org | bash
source ~/.bashrc
```

### "Insufficient balance" Error
- For testnet: Use faucet at https://faucet.aleo.org
- For mainnet: Ensure account has credits

### "Connection timeout" Error
- Check network connectivity
- Verify ALEO_NETWORK is correct
- Try alternative RPC endpoint

## Next Steps

1. **Explore the Contracts**
   - `src/contracts/agent_registry_v2.leo`
   - `src/contracts/trust_verifier_v2.leo`

2. **Read the Documentation**
   - [Deployment Guide](../docs/ALEO_DEPLOYMENT_GUIDE.md)
   - [Security Audit](../docs/ALEO_SECURITY_AUDIT.md)
   - [API Reference](../docs/API_QUICK_REFERENCE.md)

3. **Build Your Own**
   - Fork the examples
   - Modify for your use case
   - Deploy to production

## Support

- GitHub Issues: [lamassu-labs/trustwrapper](https://github.com/lamassu-labs/trustwrapper)
- Discord: [Aleo Discord](https://discord.gg/aleo)
- Documentation: [Aleo Developer Docs](https://developer.aleo.org)