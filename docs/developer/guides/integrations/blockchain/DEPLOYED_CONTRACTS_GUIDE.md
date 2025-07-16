# 🔗 Integration Guide: Deployed Aleo Contracts

**Status**: ✅ LIVE ON ALEO TESTNET
**Date**: June 23, 2025
**Contracts**: 3 contracts successfully deployed

## 📍 Contract Addresses & Details

### hallucination_verifier.aleo ✅ DEPLOYED
- **Purpose**: ZK-verified AI hallucination detection
- **Contract ID**: `hallucination_verifier.aleo`
- **Transaction**: [`at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt`](https://testnet.aleoscan.io/transaction?id=at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt)
- **Deployment Cost**: 8.633225 credits
- **Network**: Aleo Testnet (testnet3)
- **Explorer**: [View on AleoScan](https://testnet.aleoscan.io/program?id=hallucination_verifier.aleo)
- **Account**: `aleo176m09rv6qslzx0r7uyuerz3keq346lkdqhwtk2w8ffsk4rdsxyrqj9xx5m`

### agent_registry_v2.aleo ✅ DEPLOYED
- **Purpose**: AI agent registration and performance tracking
- **Contract ID**: `agent_registry_v2.aleo`
- **Transaction**: [`at1hyqa37uskww30l4trcwf6kmzfdhhszjv982cmtdsszy8ml7h959qgfq8h9`](https://testnet.aleoscan.io/transaction?id=at1hyqa37uskww30l4trcwf6kmzfdhhszjv982cmtdsszy8ml7h959qgfq8h9)
- **Deployment Cost**: 16.723925 credits
- **Network**: Aleo Testnet (testnet3)
- **Explorer**: [View on AleoScan](https://testnet.aleoscan.io/program?id=agent_registry_v2.aleo)
- **Account**: Same as above

### trust_verifier_v2.aleo ✅ DEPLOYED
- **Purpose**: AI execution verification and trust scoring
- **Contract ID**: `trust_verifier_v2.aleo`
- **Transaction**: [`at1d3ukp45tuvkp0khq8tdt4qtd3y40lx5qz65kdg0yre3rq726k5xqvrc4dz`](https://testnet.aleoscan.io/transaction?id=at1d3ukp45tuvkp0khq8tdt4qtd3y40lx5qz65kdg0yre3rq726k5xqvrc4dz)
- **Deployment Cost**: 9.629775 credits
- **Network**: Aleo Testnet (testnet3)
- **Explorer**: [View on AleoScan](https://testnet.aleoscan.io/program?id=trust_verifier_v2.aleo)
- **Account**: Same as above

### Total Deployment Summary
- **Total Contracts**: 3/3 deployed
- **Total Cost**: 34.986925 credits
- **Status**: All contracts are live and verified!

## 💰 Pricing & Usage

### Smart Contracts: FREE Forever
- ✅ **No fees charged by TrustWrapper** - We believe in open infrastructure
- ✅ **Pay only Aleo network gas fees** - Typically ~0.001-0.002 credits per transaction
- ✅ **Unlimited usage** - No rate limits or restrictions
- ✅ **Open source** - Inspect, fork, and modify as needed

### Need High-Volume or Enterprise Features?
While our smart contracts are free, we offer premium API services for organizations needing:
- High-performance batch processing (>1K verifications/month)
- Analytics dashboards and compliance reports
- SLA guarantees and dedicated support
- Custom integrations and white-label solutions

**[View API Pricing →](../PRICING.md)** | **[Contact Sales →](https://trustwrapper.ai/contact-sales)**

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
    contract_path="./contracts/hallucination_verifier",
    private_key="your_private_key",
    view_key="your_view_key"
)

aleo_client = AleoClient(
    network="testnet",
    private_key="your_private_key"
)

# Example 1: Verify AI Response
async def verify_ai_response(response_hash, model_hash, trust_score, evidence_count):
    # Generate proof locally
    proof = await leo_generator.generate_proof(
        function_name="verify_response",
        inputs={
            "response_text": f"{response_hash}field",
            "ai_model_hash": f"{model_hash}field",
            "trust_score": f"{trust_score}u8",
            "verification_method": "1u8",
            "evidence_count": f"{evidence_count}u8",
            "verifier_address": "aleo176m09rv6qslzx0r7uyuerz3keq346lkdqhwtk2w8ffsk4rdsxyrqj9xx5m"
        }
    )

    # Submit to blockchain
    tx_id = await aleo_client.submit_transaction(
        program_id="hallucination_verifier.aleo",
        function_name="verify_response",
        inputs=proof['inputs'],
        fee=0.5
    )

    return tx_id

# Example 2: Register an AI agent
async def register_ai_agent(agent_id, stake, performance_data):
    tx_id = await aleo_client.submit_transaction(
        program_id="agent_registry_v2.aleo",
        function_name="register_agent",
        inputs={
            "agent_id": f"{agent_id}field",
            "stake_amount": f"{stake}u64",
            "performance_data": performance_data,
            "registration_fee": "150u32"
        },
        fee=0.5
    )

    return tx_id
```

## 🔧 Contract Functions

### hallucination_verifier.aleo

#### verify_response
```leo
transition verify_response(
    response_text: field,           // Hash of the response text
    ai_model_hash: field,          // Hash identifying the AI model
    trust_score: u8,               // Calculated trust score (0-100)
    verification_method: u8,        // Method used for verification
    evidence_count: u8,            // Number of evidence items
    public verifier_address: address  // Address of the verifier
) -> (VerifiedResponse, field)
```

**Usage**: Verify an AI response for hallucinations with zero-knowledge proof

#### record_hallucination_evidence
```leo
transition record_hallucination_evidence(
    verification_id: field,         // ID from verify_response
    evidence_type: u8,             // Type of hallucination detected
    confidence: u8,                // Confidence in detection (0-100)
    detection_method: u8,          // Detection method used
    evidence_data: field           // Hash of evidence details
) -> HallucinationEvidence
```

**Usage**: Record specific hallucination evidence for a verified response

### agent_registry_v2.aleo

#### register_agent
```leo
transition register_agent(
    agent_id: field,               // Unique agent identifier
    stake_amount: u64,             // Stake in microcredits
    performance_data: PerformanceMetrics,  // Agent performance metrics
    registration_fee: u32          // Registration fee
) -> AgentRecord
```

**Usage**: Register a new AI agent with performance tracking

#### update_agent_performance
```leo
transition update_agent_performance(
    agent_id: field,
    new_metrics: PerformanceMetrics,
    timestamp: u32
) -> AgentRecord
```

**Usage**: Update agent performance metrics on-chain

### trust_verifier_v2.aleo

#### verify_execution
```leo
transition verify_execution(
    execution_data: ExecutionData,  // Execution details struct
    proof_hash: field,             // ZK proof of execution
    public verifier: address       // Verifier address
) -> (VerificationResult, field)
```

**Usage**: Verify AI execution with trust scoring

#### batch_verify_executions
```leo
transition batch_verify_executions(
    executions: [ExecutionData; 5],
    trust_scores: [u8; 5],
    public verifier: address
) -> [field; 5]
```

**Usage**: Batch verify multiple executions efficiently

## 🧪 Testing Locally

### Test Hallucination Verification
```bash
cd src/contracts/hallucination_verifier
leo run verify_response 123field 456field 85u8 1u8 5u8 aleo176m09rv6qslzx0r7uyuerz3keq346lkdqhwtk2w8ffsk4rdsxyrqj9xx5m

# Expected output:
# {
#   response_hash: 123field,
#   model_hash: 456field,
#   trust_score: 85u8,
#   verified: true,
#   verification_id: <generated_id>
# }
```

### Test Agent Registration
```bash
cd src/contracts/agent_registry
leo run register_agent 7777field 1000000u64 "{accuracy_rate: 9000u32, success_rate: 8500u32, avg_latency_ms: 250u32, total_executions: 1000u32}" 150u32

# Expected output:
# {
#   agent_id: 7777field,
#   stake_amount: 1000000u64,
#   performance_score: 8750u32,
#   registered: true
# }
```

### Test Trust Verification
```bash
cd src/contracts/trust_verifier
leo run verify_execution "{agent_id: 123field, execution_id: 456field, result_hash: 789field, confidence: 8500u32, timestamp: 1234u32}" 999field aleo176m09rv6qslzx0r7uyuerz3keq346lkdqhwtk2w8ffsk4rdsxyrqj9xx5m

# Expected output:
# {
#   execution_id: 456field,
#   trust_score: 85u8,
#   verified: true,
#   verification_id: <generated_id>
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
# Execute hallucination verification on-chain
aleo execute hallucination_verifier.aleo verify_response \
  --inputs "123field 456field 85u8 1u8 5u8 aleo176m09rv6qslzx0r7uyuerz3keq346lkdqhwtk2w8ffsk4rdsxyrqj9xx5m" \
  --network testnet \
  --private-key $ALEO_PRIVATE_KEY \
  --endpoint $ENDPOINT

# Execute agent registration on-chain
aleo execute agent_registry_v2.aleo register_agent \
  --inputs "8888field 2000000u64 {accuracy_rate: 9000u32, success_rate: 8500u32, avg_latency_ms: 250u32, total_executions: 1000u32} 150u32" \
  --network testnet \
  --private-key $ALEO_PRIVATE_KEY \
  --endpoint $ENDPOINT

# Check transaction status
aleo query transaction <tx_id> --network testnet --endpoint $ENDPOINT
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
      'agent_registry_v2.aleo',
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
        program_id="agent_registry_v2.aleo",
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
        program_id="trust_verifier_v2.aleo",
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
