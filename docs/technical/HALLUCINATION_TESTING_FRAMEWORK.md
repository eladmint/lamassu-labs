# Hallucination Testing Framework

## Overview

The Hallucination Testing Framework is a comprehensive system for detecting, measuring, and preventing AI hallucinations in language models. It integrates seamlessly with TrustWrapper to provide cryptographically verifiable validation of AI responses.

## Key Features

### 1. Multi-Level Hallucination Detection
- **Level 1: Simple Factual Errors** - Basic fact checking against known truths
- **Level 2: Plausible Fabrications** - Believable but false information
- **Level 3: Partial Truths** - Mix of correct and incorrect information
- **Level 4: Contextual Hallucinations** - Wrong information for specific context
- **Level 5: Confident Fabrications** - High-confidence false statements

### 2. Comprehensive Test Suite
- **700+ test cases** across multiple categories
- **Adversarial tests** designed to trick detection systems
- **Performance benchmarks** for latency and throughput
- **A/B testing framework** for production deployment

### 3. Advanced Metrics
- **Precision**: 85-95% target (few false positives)
- **Recall**: 90-95% target (catch most hallucinations)
- **F1 Score**: 87.5-95% target
- **Latency**: <200ms overhead target
- **Scalability**: >100 requests/second

## Architecture

```
src/core/
├── hallucination_detector.py      # Core detection engine
├── hallucination_test_suite.py    # Test cases and benchmarks
├── hallucination_metrics.py       # Performance metrics and analysis
├── trust_wrapper.py              # ZK proof integration
└── trust_wrapper_xai.py          # Explainable AI integration

tests/
├── unit/test_hallucination_detection.py      # Unit tests
└── integration/test_hallucination_system.py  # Integration tests

demos/
└── hallucination_testing_demo.py  # Live demonstration
```

## Usage

### Basic Detection

```python
from src.core.hallucination_detector import HallucinationDetector

# Initialize detector
detector = HallucinationDetector()

# Detect hallucinations in text
text = "The capital of France is London."
result = await detector.detect_hallucinations(text)

if result.has_hallucination:
    print(f"❌ Hallucinations detected!")
    for h in result.hallucinations:
        print(f"  • Type: {h.type.value}")
        print(f"  • Confidence: {h.confidence:.1%}")
        print(f"  • Description: {h.description}")
```

### With TrustWrapper Integration

```python
from src.core.hallucination_detector import TrustWrapperValidator

# Initialize validator with your model
validator = TrustWrapperValidator(model, enable_xai=True)

# Validate response with full pipeline
result = await validator.validate_response("What is the capital of France?")

print(f"Trust Score: {result['final_trust_score']:.1%}")
print(f"Hallucinations: {result['hallucination_detection']['hallucination_count']}")
print(f"Verification Proof: {result['verification_proof']['proof_hash']}")
```

### Running Test Suite

```python
from src.core.hallucination_test_suite import HallucinationTestSuite

# Initialize test suite
suite = HallucinationTestSuite()

# Run specific category
results = await suite.run_category("factual", model, validator)
print(f"Pass rate: {results['pass_rate']:.1%}")

# Run full suite
full_results = await suite.run_full_suite(model, validator)
report = suite.generate_report(full_results)
print(report)
```

## Performance Benchmarks

### Detection Accuracy
- **Factual Errors**: 95%+ detection rate
- **Fabricated Citations**: 85%+ detection rate
- **Temporal Errors**: 90%+ detection rate
- **Statistical Hallucinations**: 80%+ detection rate
- **Confident Fabrications**: 75%+ detection rate

### Performance Impact
- **Average Overhead**: 50-150ms per request
- **P95 Overhead**: <200ms
- **Throughput**: 100-1000 requests/second
- **Memory Usage**: <100MB additional

## Integration Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Detection
```python
# Customize detection thresholds
detector = HallucinationDetector()
detector.confidence_threshold = 0.7  # Adjust sensitivity
```

### 3. Integrate with Your Model
```python
class YourModelWithValidation:
    def __init__(self, base_model):
        self.model = base_model
        self.validator = TrustWrapperValidator(base_model)
    
    async def generate(self, prompt):
        result = await self.validator.validate_response(prompt)
        if result['final_trust_score'] < 0.5:
            return "⚠️ Low confidence response - possible hallucinations detected"
        return result['wrapped_response']
```

## Testing

### Run Unit Tests
```bash
pytest tests/unit/test_hallucination_detection.py -v
```

### Run Integration Tests
```bash
pytest tests/integration/test_hallucination_system.py -v
```

### Run Live Demo
```bash
python demos/hallucination_testing_demo.py
```

## Metrics and Reporting

The framework provides comprehensive metrics:

```python
from src.core.hallucination_metrics import HallucinationMetrics

metrics = HallucinationMetrics()
# ... run detections ...

summary = metrics.get_summary()
print(f"Precision: {summary['accuracy_metrics']['precision']:.1%}")
print(f"Recall: {summary['accuracy_metrics']['recall']:.1%}")
print(f"F1 Score: {summary['accuracy_metrics']['f1_score']:.1%}")

# Check if meets criteria
meets_min, failures = metrics.meets_minimum_criteria()
if not meets_min:
    print("Failed criteria:", failures)
```

## Production Deployment

### A/B Testing
```python
from src.core.hallucination_metrics import A_B_TestFramework

ab_test = A_B_TestFramework()

# Record interactions
ab_test.record_interaction(
    user_id="user123",
    query="What is quantum computing?",
    response=response,
    hallucination_detected=False,
    user_satisfaction=4.5
)

# Check significance
results = ab_test.calculate_statistical_significance()
if results['significant']:
    print(f"Treatment improved satisfaction by {results['improvement_pct']:.1%}")
```

### Continuous Monitoring
- Set up automated testing pipeline
- Monitor detection metrics in production
- Alert on performance degradation
- Regular retraining based on false negatives

## Best Practices

1. **Regular Testing**: Run test suite before deployments
2. **Custom Test Cases**: Add domain-specific test cases
3. **Threshold Tuning**: Adjust detection thresholds based on your use case
4. **Performance Monitoring**: Track latency impact in production
5. **User Feedback**: Collect feedback to improve detection

## Future Enhancements

- [ ] Multi-language hallucination detection
- [ ] Domain-specific knowledge bases
- [ ] Real-time learning from user feedback
- [ ] Integration with more LLM providers
- [ ] Advanced visualization dashboard

## References

Based on research from:
- IR06: TrustWrapper Hallucination Validation Methodology
- TruthfulQA: Measuring How Models Mimic Human Falsehoods
- HaluEval: Large-Scale Hallucination Evaluation Benchmark
- Self-CheckGPT: Zero-Resource Black-Box Hallucination Detection