# ADR-003: TrustWrapper Integration Pattern

**Date**: June 21, 2025  
**Status**: Accepted  
**Author**: Claude  
**Deciders**: Architecture Team

## Context

TrustWrapper needs to integrate with multiple components:
1. Existing AI agents (any implementation)
2. Leo smart contracts for ZK proofs
3. Aleo blockchain for verification
4. Multiple verification layers (ZK, XAI, Quality)

We need a clean, extensible pattern that:
- Wraps any AI agent without modification
- Supports multiple proof types
- Handles async blockchain operations
- Maintains performance
- Provides good developer experience

## Decision

We will use a **Decorator Pattern** with **Async Pipeline Architecture** for TrustWrapper integration.

### Core Architecture
```python
class ZKTrustWrapper:
    def __init__(self, agent: Any, **config):
        self.agent = agent
        self.config = config
        self.pipeline = self._build_pipeline()
    
    async def verified_execute(self, *args, **kwargs):
        # Pre-execution
        context = await self.pipeline.pre_execute(*args, **kwargs)
        
        # Agent execution
        result = await self._execute_agent(*args, **kwargs)
        
        # Post-execution verification
        verified = await self.pipeline.post_execute(result, context)
        
        return VerifiedResult(result, verified)
```

## Rationale

### Why Decorator Pattern?

1. **Non-Invasive**: No changes to existing agents
2. **Composable**: Stack multiple wrappers
3. **Flexible**: Easy to add/remove features
4. **Standard**: Well-understood pattern

### Why Async Pipeline?

1. **Performance**: Non-blocking blockchain calls
2. **Scalability**: Parallel proof generation
3. **Modularity**: Clean separation of concerns
4. **Extensibility**: Easy to add stages

### Alternative Patterns Considered

#### 1. Inheritance
```python
class VerifiedAgent(BaseAgent):  # Bad
    def execute(self):
        result = super().execute()
        # Add verification
```
**Rejected**: Requires modifying existing agents

#### 2. Proxy Pattern
```python
class AgentProxy:  # Okay
    def __init__(self, agent):
        self._agent = agent
    def __getattr__(self, name):
        # Intercept calls
```
**Rejected**: More complex, less transparent

#### 3. Middleware Chain
```python
middleware = [  # Good but complex
    AuthMiddleware(),
    VerificationMiddleware(),
    LoggingMiddleware()
]
```
**Rejected**: Overkill for current needs

## Implementation Details

### 1. Pipeline Stages

```python
class VerificationPipeline:
    stages = [
        MetricsCollectionStage(),      # Collect execution metrics
        ProofGenerationStage(),        # Generate ZK proofs
        BlockchainSubmissionStage(),   # Submit to Aleo
        VerificationStage(),           # Verify on-chain
        XAIEnrichmentStage(),         # Add explanations
        QualityConsensusStage()       # Quality verification
    ]
```

### 2. Configuration System

```python
wrapper = ZKTrustWrapper(
    agent=my_agent,
    enable_zk_proofs=True,
    enable_xai=True,
    enable_quality_consensus=False,
    contract_id='trust_verifier_v2.aleo',
    network='testnet3'
)
```

### 3. Error Handling

```python
class VerificationError(Exception):
    pass

class ProofGenerationError(VerificationError):
    pass

class BlockchainError(VerificationError):
    pass

# Graceful degradation
try:
    proof = await generate_proof()
except ProofGenerationError:
    # Continue without proof
    logger.warning("Proof generation failed")
```

### 4. Caching Strategy

```python
@lru_cache(maxsize=1000)
def get_cached_proof(input_hash: str) -> Optional[Proof]:
    # Cache proofs for repeated inputs
    pass

# Time-based cache for blockchain data
@ttl_cache(ttl=300)  # 5 minutes
async def get_contract_state():
    pass
```

## Consequences

### Positive
- **Clean Integration**: One-line agent wrapping
- **Backward Compatible**: Works with any agent
- **Performance**: Async operations, caching
- **Extensible**: Easy to add new verification types
- **Testable**: Each stage independently testable

### Negative
- **Complexity**: Pipeline adds abstraction layer
- **Debugging**: More layers to trace through
- **Memory**: Wrapper objects add overhead
- **Learning Curve**: Developers need to understand pattern

### Neutral
- **Dependencies**: Requires async agent methods
- **Configuration**: Many options to understand
- **Monitoring**: Need metrics at each stage

## Usage Examples

### Basic Usage
```python
# Wrap any agent
agent = MyAIAgent()
trusted = ZKTrustWrapper(agent)

# Use normally
result = await trusted.verified_execute(input_data)
print(f"Result: {result.result}")
print(f"Proof: {result.proof}")
```

### Advanced Configuration
```python
# Custom pipeline
wrapper = ZKTrustWrapper(
    agent=agent,
    pipeline_stages=[
        CustomMetricsStage(),
        FastProofStage(),
        CachedVerificationStage()
    ]
)
```

### Multiple Wrappers
```python
# Stack multiple verifications
agent = BaseAgent()
zk_agent = ZKTrustWrapper(agent)
xai_agent = XAIWrapper(zk_agent)
quality_agent = QualityWrapper(xai_agent)
```

## Migration Path

### Phase 1: Basic Wrapper (Complete)
- Simple decorator implementation
- Single verification type
- Synchronous operations

### Phase 2: Async Pipeline (Current)
- Full async support
- Multiple stages
- Error handling

### Phase 3: Advanced Features (Future)
- Dynamic pipeline configuration
- Plugin system
- Performance optimizations

## Testing Strategy

```python
# Unit tests for each stage
async def test_proof_generation_stage():
    stage = ProofGenerationStage()
    result = await stage.process(mock_data)
    assert result.proof is not None

# Integration tests
async def test_full_pipeline():
    agent = MockAgent()
    wrapper = ZKTrustWrapper(agent)
    result = await wrapper.verified_execute("test")
    assert result.proof.verified

# Performance tests
async def test_pipeline_performance():
    # Measure overhead
    pass
```

## References

1. [Decorator Pattern](https://refactoring.guru/design-patterns/decorator)
2. [Async/Await Best Practices](https://docs.python.org/3/library/asyncio.html)
3. [Pipeline Pattern](https://www.enterpriseintegrationpatterns.com/patterns/messaging/PipesAndFilters.html)
4. [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

## Review Triggers

- Major agent integration issues
- Performance bottlenecks identified
- New verification requirements
- Significant pattern improvements in ecosystem

## Approval

- **Proposed by**: Claude (AI Assistant)
- **Reviewed by**: Architecture Team
- **Approved by**: [Pending]
- **Implementation Status**: In Production