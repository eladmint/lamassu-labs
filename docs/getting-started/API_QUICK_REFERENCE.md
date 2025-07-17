# 🚀 TrustWrapper API Quick Reference

**Add trust to ANY AI agent in 3 lines of code!**

## 📦 Installation

```bash
# Clone the repository and use locally
git clone https://github.com/eladmint/lamassu-labs.git
cd lamassu-labs
pip install -r requirements.txt
```

## 🎯 Basic Usage

### Layer 1: Performance Verification
```python
from src.core.trust_wrapper import ZKTrustWrapper

# Your existing agent
agent = YourAIAgent()

# Add trust in one line!
trusted_agent = ZKTrustWrapper(agent, "MyAgent")

# Use normally - returns VerifiedResult
result = trusted_agent.verified_execute(input_data)

# Access results
print(result.result)           # Original agent output
print(result.metrics)          # Execution metrics
print(result.proof)            # ZK proof
print(result.verified)         # True/False
```

### Layer 2: Add Explainability (XAI)
```python
from src.core.trust_wrapper_xai import create_xai_wrapper

# Create XAI-enhanced wrapper
xai_agent = create_xai_wrapper(agent, "MyAgent")

# Execute with explanations
result = xai_agent.verified_execute(input_data)

# Access XAI features
print(result.explanation.top_features)      # Feature importance
print(result.explanation.confidence_score)  # 0.0-1.0
print(result.explanation.decision_reasoning) # Why this decision
print(result.trust_score)                   # Overall trust score
```

### Layer 3: Add Quality Consensus
```python
from src.core.trust_wrapper_quality import create_quality_wrapper

# Create quality-verified wrapper
quality_agent = create_quality_wrapper(agent, "MyAgent")

# Execute with quality validation
result = quality_agent.verified_execute(input_data)

# Access quality metrics
print(result.quality_verified)     # True/False
print(result.consensus_score)      # 0.0-1.0
print(result.validator_results)    # Individual validator results
```

## 🔧 Full Stack Example

```python
# Combine all three layers for maximum trust!
from src.core.trust_wrapper import ZKTrustWrapper
from src.core.trust_wrapper_xai import ZKTrustWrapperXAI
from src.core.trust_wrapper_quality import QualityVerifiedWrapper

# Your agent
agent = YourComplexAIAgent()

# Layer 1: Performance
perf_agent = ZKTrustWrapper(agent, "ComplexAgent")

# Layer 2: Add XAI
xai_agent = ZKTrustWrapperXAI(perf_agent, "ComplexAgent-XAI")

# Layer 3: Add Quality
trusted_agent = QualityVerifiedWrapper(xai_agent, "ComplexAgent-Full")

# Use with complete trust!
result = trusted_agent.verified_execute(complex_data)
```

## 📊 Data Structures

### VerifiedResult
```python
@dataclass
class VerifiedResult:
    result: Any              # Original agent output
    metrics: ExecutionMetrics # Performance metrics
    proof: ZKProof           # Zero-knowledge proof
    verified: bool = True    # Verification status
    
    # XAI additions (if using XAI wrapper)
    explanation: Optional[Explanation] = None
    trust_score: Optional[float] = None
    
    # Quality additions (if using Quality wrapper)
    quality_verified: Optional[bool] = None
    consensus_score: Optional[float] = None
    validator_results: Optional[Dict] = None
```

### ExecutionMetrics
```python
@dataclass
class ExecutionMetrics:
    execution_time_ms: int   # Execution time
    success: bool           # Success status
    input_hash: str         # Input data hash
    output_hash: str        # Output data hash
    timestamp: int          # Unix timestamp
    agent_name: str         # Agent identifier
    agent_version: str      # Version tracking
    error_message: Optional[str] = None
```

### ZKProof
```python
@dataclass
class ZKProof:
    proof_hash: str              # Proof identifier
    metrics_commitment: str      # Metrics hash
    timestamp: int              # Generation time
    aleo_tx_hash: Optional[str] # Blockchain tx
```

## 🎨 Common Patterns

### Async Execution
```python
# For async agents
result = await trusted_agent.verified_execute_async(data)
```

### Custom Validators
```python
from src.core.trust_wrapper_quality import QualityVerifiedWrapper

class MyValidator:
    def validate(self, input_data, output):
        # Your validation logic
        passed = len(output) > 0
        confidence = 0.95
        issues = []
        return passed, confidence, issues

# Use custom validator
wrapper = QualityVerifiedWrapper(
    agent, 
    "MyAgent",
    validators=[MyValidator()]
)
```

### Error Handling
```python
result = trusted_agent.verified_execute(data)

if not result.metrics.success:
    print(f"Execution failed: {result.metrics.error_message}")
    # Proof still generated for failed executions!
    
if result.quality_verified == False:
    print(f"Quality check failed: {result.consensus_score}")
    # Output still returned, but marked as low quality
```

## ⚡ Performance Tips

1. **Minimize Overhead**: Each layer adds ~50-150ms
2. **Batch Operations**: Process multiple inputs together
3. **Cache Results**: Proofs are deterministic for same input
4. **Async When Possible**: Better concurrency

## 🔗 Integration Examples

### With FastAPI
```python
from fastapi import FastAPI
app = FastAPI()

trusted_agent = ZKTrustWrapper(agent)

@app.post("/analyze")
async def analyze(data: dict):
    result = await trusted_agent.verified_execute_async(data)
    return {
        "output": result.result,
        "proof": result.proof.proof_hash,
        "metrics": result.metrics.to_dict()
    }
```

### With Agent Marketplace
```python
# Register wrapped agent
marketplace.register_agent(
    agent=trusted_agent,
    capabilities=["nlp", "analysis"],
    trust_features=["zk-proof", "xai", "quality"]
)
```

## 🛡️ Security Considerations

1. **Private Inputs**: Inputs are hashed, not revealed
2. **Proof Verification**: Verify proofs on Aleo blockchain
3. **Rate Limiting**: Built-in rate limiting support
4. **Anti-Gaming**: Quality consensus prevents manipulation

## 📚 Full Documentation

- [Technical Deep Dive](./TECHNICAL_DEEP_DIVE.md)
- [Integration Guide](./guides/INTEGRATION_GUIDE.md) *(coming soon)*
- [Examples](../demo/README.md)

---

**Remember**: TrustWrapper adds trust without changing your agent code!