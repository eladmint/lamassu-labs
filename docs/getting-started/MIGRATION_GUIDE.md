# 🚀 Migration Guide: From Basic to Full Stack

**Level up your AI agents with progressive trust enhancement**

## 📋 Overview

This guide shows you how to progressively add trust layers to your AI agents:

1. **Basic** → Performance verification only
2. **Enhanced** → Add explainable AI
3. **Complete** → Add quality consensus
4. **Advanced** → Custom validators and blockchain

## 🎯 Migration Paths

```
Your Agent → [Layer 1: Performance] → [Layer 2: XAI] → [Layer 3: Quality] → Advanced Features
            └─ Basic Trust ─┘        └─ Enhanced ─┘   └─ Complete ─┘      └─ Enterprise ─┘
```

## 📊 Layer 1: Basic Performance Verification

### Starting Point
```python
# Your existing agent
class MyAgent:
    def execute(self, data):
        # Your agent logic
        return process_data(data)
```

### Add Basic Trust
```python
from src.core.trust_wrapper import ZKTrustWrapper

# Wrap your agent (one line!)
trusted_agent = ZKTrustWrapper(MyAgent(), "MyAgent")

# Use it
result = trusted_agent.verified_execute(data)
print(f"Speed: {result.metrics.execution_time_ms}ms")
print(f"Success: {result.metrics.success}")
print(f"Proof: {result.proof.proof_hash}")
```

### What You Get
- ⚡ Execution time tracking
- ✅ Success/failure monitoring
- 🔐 Basic ZK proof generation
- 📊 Performance baselines

## 🧠 Layer 2: Add Explainable AI

### When to Upgrade
- Your agent makes complex decisions
- Users ask "why did it do that?"
- Compliance requires transparency
- You need confidence scores

### Migration Steps
```python
# Before: Basic wrapper
from src.core.trust_wrapper import ZKTrustWrapper
basic_agent = ZKTrustWrapper(MyAgent(), "MyAgent")

# After: Add XAI layer
from src.core.trust_wrapper_xai import ZKTrustWrapperXAI
xai_agent = ZKTrustWrapperXAI(MyAgent(), "MyAgent")

# Use enhanced features
result = xai_agent.verified_execute(data)
print(f"Explanation: {result.explanation}")
print(f"Confidence: {result.trust_score:.1%}")
print(f"Key factors: {result.explanation.feature_importance}")
```

### New Capabilities
- 🧠 SHAP/LIME explanations
- 📊 Feature importance scores
- 🎯 Confidence percentages
- 💭 Decision reasoning

### Code Changes Required
```python
# If your agent uses ML models, expose them:
class MyMLAgent:
    def __init__(self):
        self.model = load_model()
    
    def get_model(self):  # Add this method
        return self.model
    
    def execute(self, data):
        return self.model.predict(data)
```

## ✅ Layer 3: Add Quality Consensus

### When to Upgrade
- Output quality varies
- Need validation guarantees
- Multiple stakeholders involved
- Anti-gaming required

### Migration Steps
```python
# Before: XAI wrapper
from src.core.trust_wrapper_xai import ZKTrustWrapperXAI
xai_agent = ZKTrustWrapperXAI(MyAgent(), "MyAgent")

# After: Full stack with quality
from src.core.trust_wrapper_quality import QualityVerifiedWrapper
quality_agent = QualityVerifiedWrapper(MyAgent(), "MyAgent")

# Use complete stack
result = quality_agent.verified_execute(data)
print(f"Quality verified: {result.quality_verified}")
print(f"Consensus: {result.consensus_score:.1%}")
print(f"Validators: {len(result.validator_results)}")
```

### New Capabilities
- ✅ Multiple validator verification
- 📊 Consensus scoring
- 🛡️ Anti-gaming protection
- 📈 Quality metrics

### Custom Validators
```python
# Add domain-specific validators
class MyCustomValidator:
    def validate(self, input_data, output):
        # Your validation logic
        score = calculate_quality_score(output)
        passed = score > 0.8
        confidence = 0.95
        issues = [] if passed else ["Low quality score"]
        return passed, confidence, issues

# Use custom validator
quality_agent = QualityVerifiedWrapper(
    MyAgent(), 
    "MyAgent",
    validators=[MyCustomValidator()]
)
```

## 🔧 Advanced Features

### Async Support
```python
# Sync agent
class SyncAgent:
    def execute(self, data):
        return process(data)

# Make it async-compatible
class AsyncAgent:
    async def execute_async(self, data):
        return await async_process(data)
    
    def execute(self, data):
        # Fallback for sync calls
        return asyncio.run(self.execute_async(data))
```

### Blockchain Integration
```python
# Enable on-chain verification
from src.core.blockchain import AleoVerifier

quality_agent = QualityVerifiedWrapper(
    MyAgent(),
    "MyAgent",
    blockchain_verifier=AleoVerifier(
        network="testnet",
        contract_address="trust_verifier.aleo"
    )
)
```

### Performance Optimization
```python
# Batch processing for efficiency
results = await quality_agent.batch_execute([
    data1, data2, data3, data4
])

# Caching for repeated queries
quality_agent.enable_caching(ttl_seconds=300)
```

## 📊 Migration Checklist

### Phase 1: Basic Trust ✓
- [ ] Wrap agent with ZKTrustWrapper
- [ ] Verify performance metrics work
- [ ] Check proof generation
- [ ] Establish baselines

### Phase 2: Add Explainability ✓
- [ ] Upgrade to ZKTrustWrapperXAI
- [ ] Expose model if using ML
- [ ] Test explanations make sense
- [ ] Verify confidence scores

### Phase 3: Add Quality ✓
- [ ] Upgrade to QualityVerifiedWrapper
- [ ] Test default validators
- [ ] Add custom validators if needed
- [ ] Verify consensus scoring

### Phase 4: Advanced Features ✓
- [ ] Add async support if needed
- [ ] Enable blockchain verification
- [ ] Optimize performance
- [ ] Add monitoring

## 🚨 Common Migration Issues

### Issue 1: Import Errors
```python
# Problem
ImportError: cannot import name 'ZKTrustWrapper'

# Solution
# Make sure you're in the project directory
cd trustwrapper
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

### Issue 2: Async Compatibility
```python
# Problem
RuntimeError: no running event loop

# Solution
# Add async support to your agent
class MyAgent:
    async def execute_async(self, data):
        return self.execute(data)
```

### Issue 3: Validator Failures
```python
# Problem
All validators rejecting output

# Solution
# Start with lenient validators
validator = MyValidator(threshold=0.5)  # Lower threshold
# Gradually increase as you improve
```

## 📈 Performance Impact

| Layer | Overhead | Use When |
|-------|----------|----------|
| Basic | ~50ms | Always - minimal cost |
| + XAI | +100ms | Need explanations |
| + Quality | +50ms | Need validation |
| **Total** | ~200ms | Full trust stack |

## 🎯 Best Practices

1. **Start Simple**: Begin with basic wrapper
2. **Add Incrementally**: One layer at a time
3. **Test Each Layer**: Verify before adding more
4. **Monitor Performance**: Track overhead
5. **Custom Validators**: Add domain expertise

## 🆘 Getting Help

- **Documentation**: [API Reference](API_QUICK_REFERENCE.md)
- **Examples**: Check `demos/` directory
- **Community**: GitHub discussions
- **Support**: support@trustwrapper.ai

---

**Ready to migrate?** Start with [Quick Start](QUICK_START.md) and work your way up!