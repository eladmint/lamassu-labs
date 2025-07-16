# LangChain Integration Testing Suite

Comprehensive testing suite for TrustWrapper LangChain integration following ADR-005 testing strategy.

## 📋 Test Structure

### Unit Tests (`unit/langchain/`)
- **`test_langchain_config.py`**: Configuration system testing
- **`test_trustwrapper_callbacks.py`**: Direct callback testing
- **Coverage Target**: >90% for LangChain integration components
- **Focus**: Individual component functionality and edge cases

### Integration Tests (`integration/langchain/`)
- **`test_trustwrapper_langchain_integration.py`**: Full integration testing
- **`test_langchain_integration.py`**: LangChain framework integration
- **Focus**: Component interactions and data flow
- **Dependencies**: Real TrustWrapper components with mock LLMs

### Performance Tests (`performance/langchain/`)
- **`test_langchain_performance_benchmarks.py`**: Comprehensive performance testing
- **Target**: <100ms overhead for standard verification
- **Focus**: Latency, throughput, memory usage, concurrent load

## 🚀 Quick Start

### Run All Tests
```bash
python tools/testing/run_langchain_tests.py --all
```

### Run Specific Test Suites
```bash
# Unit tests only
python tools/testing/run_langchain_tests.py --unit

# Integration tests only
python tools/testing/run_langchain_tests.py --integration

# Performance tests only
python tools/testing/run_langchain_tests.py --performance

# Quick smoke tests
python tools/testing/run_langchain_tests.py --smoke
```

### Run Individual Test Files
```bash
# Run specific unit test
pytest tools/testing/unit/langchain/test_langchain_config.py -v

# Run integration tests with markers
pytest tools/testing/integration/langchain/ -m "integration" -v

# Run performance tests
pytest tools/testing/performance/langchain/ -m "performance" -v
```

## 📊 Test Categories

### Test Markers
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.performance` - Performance tests
- `@pytest.mark.slow` - Tests taking >1 second
- `@pytest.mark.langchain` - LangChain specific tests

### Test Scenarios

#### Unit Tests
- Configuration validation
- Callback method testing
- Error handling
- Edge cases

#### Integration Tests
- End-to-end verification flows
- Compliance mode testing
- Real-world scenarios (financial, healthcare, customer service)
- Statistics and monitoring

#### Performance Tests
- Baseline vs. TrustWrapper overhead
- Concurrent load testing
- Memory usage validation
- Cache performance benefits
- Large response handling

## 📈 Performance Targets

Based on ADR-005 testing strategy:

| Metric | Target | Test |
|--------|--------|------|
| **Verification Overhead** | <100ms | `test_overhead_within_target` |
| **Concurrent Load** | 10+ requests | `test_concurrent_load_performance` |
| **Memory Usage** | <100MB for 10 instances | `test_memory_usage_reasonable` |
| **Individual Test Speed** | <1s average | All unit tests |
| **Cache Benefit** | Measurable improvement | `test_cache_performance_benefit` |

## 🔧 Dependencies

### Required
- `pytest` - Test framework
- `asyncio` - Async testing support
- Python 3.8+ - Minimum version

### Optional
- `langchain` - For real LangChain integration testing
- `psutil` - For memory usage testing
- `pytest-asyncio` - Enhanced async test support

### Install Dependencies
```bash
pip install pytest pytest-asyncio psutil
pip install langchain  # For full integration testing
```

## 📋 Test Configuration

Configuration via `pytest_langchain.ini`:
- Async mode enabled
- Comprehensive markers defined
- Timeout protection (300s)
- Verbose output by default

## 🧪 Writing New Tests

### Unit Test Template
```python
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent / "src"))

from src.integrations.langchain import TrustWrapperCallback, TrustWrapperConfig

class TestNewFeature:
    @pytest.fixture
    def config(self):
        return TrustWrapperConfig()

    def test_new_functionality(self, config):
        callback = TrustWrapperCallback(config)
        # Your test logic here
        assert True
```

### Integration Test Template
```python
import pytest
import asyncio

class TestNewIntegration:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_integration_scenario(self):
        # Your integration test logic here
        assert True
```

### Performance Test Template
```python
import pytest
import time

class TestNewPerformance:
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_performance_scenario(self):
        start_time = time.perf_counter()
        # Your performance test logic here
        end_time = time.perf_counter()

        latency_ms = (end_time - start_time) * 1000
        assert latency_ms < 100  # Your performance target
```

## 📊 Test Reports

### Console Output
The test runner provides detailed console output with:
- Real-time test progress
- Performance metrics
- Success/failure summary
- Actionable recommendations

### Coverage Reports
```bash
# Generate coverage report
pytest --cov=src/integrations/langchain --cov-report=html

# View coverage
open htmlcov/index.html
```

## 🔍 Debugging Tests

### Verbose Output
```bash
python tools/testing/run_langchain_tests.py --all
```

### Debug Individual Tests
```bash
pytest tools/testing/unit/langchain/test_langchain_config.py::TestTrustWrapperConfig::test_default_config -v -s
```

### Debug Performance Issues
```bash
pytest tools/testing/performance/langchain/ -v -s --tb=long
```

## ✅ Test Quality Standards

Following ADR-005 requirements:

### Coverage Standards
- **Line Coverage**: >90% for integration components
- **Branch Coverage**: >85% for conditional logic
- **Function Coverage**: 100% for public APIs

### Performance Standards
- **Unit Test Speed**: <100ms per test average
- **Integration Test Speed**: <5 seconds per test average
- **Full Test Suite**: <10 minutes total execution

### Quality Standards
- **Test Reliability**: <1% flaky test rate
- **Clear Assertions**: Every test has meaningful assertions
- **Proper Fixtures**: Reusable test setup and teardown
- **Documentation**: Clear test descriptions and comments

## 🚨 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure src is in Python path
export PYTHONPATH="/Users/eladm/Projects/token/tokenhunter/lamassu-labs/src:$PYTHONPATH"
```

#### LangChain Not Found
```bash
# Install LangChain for full integration testing
pip install langchain langchain-community
```

#### Async Test Issues
```bash
# Ensure pytest-asyncio is installed
pip install pytest-asyncio
```

#### Performance Test Variance
Performance tests may show variance in different environments. Focus on relative performance and trend analysis rather than absolute numbers.

## 📚 Related Documentation

- **[ADR-005: Testing Strategy](../../memory-bank/adrs/ADR-005-testing-strategy.md)** - Overall testing approach
- **[ADR-007: LangChain Integration](../../memory-bank/adrs/ADR-007-langchain-integration-architecture.md)** - Integration architecture
- **[LangChain Integration Guide](../../docs/integration/langchain/LANGCHAIN_INTEGRATION_GUIDE.md)** - Usage documentation
- **[Performance Optimization Guide](../../docs/deployment/PERFORMANCE_OPTIMIZATION_GUIDE.md)** - Performance tuning

---

**Need help?** Check the troubleshooting section above or refer to the main project documentation.
