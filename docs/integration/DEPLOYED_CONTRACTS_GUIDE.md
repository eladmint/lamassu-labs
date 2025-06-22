# 🔗 Integration Guide: Deployed Aleo Contracts

**Status**: ✅ LIVE ON ALEO TESTNET  
**Date**: June 22, 2025  
**Contracts**: `agent_registry_simple.aleo`, `trust_verifier_test.aleo`

## 📍 Contract Addresses & Details

### agent_registry_simple.aleo
- **Purpose**: Register and verify AI agents with hidden performance metrics
- **Deployment Cost**: 4.689950 credits
- **Network**: Aleo Testnet (testnet3)
- **Account**: `aleo176m09rv6qslzx0r7uyuerz3keq346lkdqhwtk2w8ffsk4rdsxyrqj9xx5m`

### trust_verifier_test.aleo
- **Purpose**: Verify AI execution results with zero-knowledge proofs
- **Deployment Cost**: 7.412275 credits  
- **Network**: Aleo Testnet (testnet3)
- **Account**: Same as above

## 🚀 Quick Start Integration

### Prerequisites
```bash
# Install Leo CLI
curl -L https://raw.githubusercontent.com/AleoHQ/leo/main/install.sh | sh

# Set up environment
export ALEO_PRIVATE_KEY="your_private_key"
export ALEO_NETWORK="testnet"
export ENDPOINT="https://api.explorer.provable.com/v1"
```

### Python Integration Example
```python
from src.zk.leo_integration import LeoProofGenerator
from src.zk.aleo_client import AleoClient

# Initialize clients
leo_generator = LeoProofGenerator(
    contract_path="./contracts/agent_registry_simple",
    private_key="your_private_key",
    view_key="your_view_key"
)

aleo_client = AleoClient(
    network="testnet",
    private_key="your_private_key"
)

# Register an AI agent
async def register_ai_agent(agent_id, stake, accuracy, tasks):
    # Generate proof locally
    proof = await leo_generator.generate_proof(
        function_name="register_agent",
        inputs={
            "agent_id": f"{agent_id}field",
            "stake_amount": f"{stake}u64",
            "accuracy": f"{accuracy}u32",
            "tasks_completed": f"{tasks}u32",
            "current_height": "150u32"
        }
    )
    
    # Submit to blockchain
    tx_id = await aleo_client.submit_transaction(
        program_id="agent_registry_simple.aleo",
        function_name="register_agent",
        inputs=proof['inputs'],
        fee=0.5
    )
    
    return tx_id
```

## 🔧 Contract Functions

### agent_registry_simple.aleo

#### register_agent
```leo
transition register_agent(
    public agent_id: field,          // Unique identifier
    public stake_amount: u64,        // Stake in microcredits
    private accuracy: u32,           // Hidden accuracy score
    private tasks_completed: u32,    // Hidden task count
    public current_height: u32       // Block height
) -> VerificationResult
```

**Usage**: Register a new AI agent with performance metrics kept private

#### verify_agent
```leo
transition verify_agent(
    public agent_id: field,
    public min_score: u32
) -> bool
```

**Usage**: Verify an agent meets minimum performance requirements

### trust_verifier_test.aleo

#### verify_execution
```leo
transition verify_execution(
    public execution_id: field,      // Unique execution ID
    public agent_id: field,          // Agent that executed
    private expected_output: field,  // Hidden expected result
    private actual_output: field,    // Hidden actual result
    public timestamp: u32            // Execution timestamp
) -> VerificationResult
```

**Usage**: Verify AI execution correctness without revealing outputs

#### batch_verify
```leo
transition batch_verify(
    public batch_id: field,
    public executions: [field; 10]
) -> bool
```

**Usage**: Verify multiple executions efficiently

## 🧪 Testing Locally

### Test Registration
```bash
cd test_build/agent_registry_simple
leo run register_agent 7777field 1000000u64 9000u32 250u32 150u32

# Expected output:
# {
#   agent_id: 7777field,
#   score: 9250u32,
#   verified: true,
#   timestamp: 150u32
# }
```

### Test Verification
```bash
cd test_build/trust_verifier_test
leo run verify_execution 1234field 7777field 999field 999field 200u32

# Expected output:
# {
#   agent_id: 7777field,
#   score: 10000u32,
#   verified: true,
#   timestamp: 200u32
# }
```

## 🌐 On-Chain Execution

### ✅ Successfully Tested On-Chain (June 22, 2025)

#### Example Transactions
1. **register_agent**: `at1er2w65mshfc4qsrqyrugcwtwzmmyky5vemd58vg77vv7zlmq05rql6lkp9`
   - Fee: 0.001620 credits
   - Registered agent 7777field with performance metrics

2. **verify_execution**: `at1q3zwac0p33e4799te4c8fx9njnpvd2mfut62xq4u5nc6uvctmggsj3rq0j`  
   - Fee: 0.001740 credits
   - Verified execution for agent 7777field

### Important Notes
1. **Network Propagation**: Allow 30+ minutes after deployment for full propagation
2. **Gas Fees**: Keep ~20 credits in account for transaction fees (actual: ~0.0017 per tx)
3. **Network Name**: Use "testnet" for CLI commands (not "testnet3")
4. **Transaction Confirmation**: May take 1-2 minutes to appear in explorer

### Execute On-Chain
```bash
# Execute register_agent on-chain
leo execute register_agent 8888field 2000000u64 8500u32 300u32 175u32 \
  --network testnet \
  --private-key $ALEO_PRIVATE_KEY \
  --endpoint $ENDPOINT

# Check transaction status
leo query transaction <tx_id> --network testnet --endpoint $ENDPOINT
```

## 🔗 JavaScript/TypeScript Integration

```typescript
import { Account, ProgramManager } from '@aleohq/sdk';

class TrustWrapperClient {
  private account: Account;
  private programManager: ProgramManager;
  
  constructor(privateKey: string) {
    this.account = new Account({ privateKey });
    this.programManager = new ProgramManager(
      'https://api.explorer.provable.com/v1',
      this.account
    );
  }
  
  async registerAgent(
    agentId: string,
    stake: number,
    accuracy: number,
    tasksCompleted: number
  ): Promise<string> {
    const inputs = [
      `${agentId}field`,
      `${stake}u64`,
      `${accuracy}u32`,
      `${tasksCompleted}u32`,
      '150u32'
    ];
    
    const tx = await this.programManager.execute(
      'agent_registry_simple.aleo',
      'register_agent',
      inputs,
      0.5 // fee in credits
    );
    
    return tx;
  }
}
```

## 🛡️ Security Considerations

1. **Private Keys**: Never expose private keys in code
2. **Input Validation**: Validate all inputs before proof generation
3. **Error Handling**: Handle network errors and failed proofs gracefully
4. **Rate Limiting**: Implement rate limiting to prevent spam

## 📊 Monitoring & Analytics

### Query Agent Status
```python
async def get_agent_status(agent_id):
    # Query on-chain state
    result = await aleo_client.query_mapping(
        program_id="agent_registry_simple.aleo",
        mapping_name="agents",
        key=f"{agent_id}field"
    )
    return result
```

### Track Verifications
```python
async def get_verification_count(agent_id):
    # Query verification history
    count = await aleo_client.query_mapping(
        program_id="trust_verifier_test.aleo",
        mapping_name="verification_count",
        key=f"{agent_id}field"
    )
    return count
```

## 🚨 Troubleshooting

### Common Issues

1. **"Network testnet3 not found"**
   - Solution: Use "testnet" instead of "testnet3" in CLI commands

2. **"owner is a reserved keyword"**
   - Solution: Use simplified contracts without owner field

3. **404 Error on execution**
   - Solution: Wait for network propagation (5-10 minutes)

4. **"Insufficient balance"**
   - Solution: Ensure account has credits for gas fees

### Debug Commands
```bash
# Check account balance
leo account balance --network testnet

# View transaction details
leo query transaction <tx_id> --network testnet

# Test local execution
leo run <function_name> <inputs>
```

## 📚 Additional Resources

- [Aleo Developer Docs](https://developer.aleo.org/)
- [Leo Language Guide](https://developer.aleo.org/leo/)
- [TrustWrapper Architecture](../architecture/TECHNICAL_ARCHITECTURE.md)
- [Security Audit](../ALEO_SECURITY_AUDIT.md)

## 🆘 Support

For integration support:
- GitHub Issues: [lamassu-labs/trustwrapper](https://github.com/lamassu-labs/trustwrapper)
- Documentation: [Technical Deep Dive](../TECHNICAL_DEEP_DIVE.md)
- Examples: See `examples/` directory

---

**Remember**: These contracts are live on testnet. Always test locally first before on-chain execution!