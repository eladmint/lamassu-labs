# TrustWrapper Test Suite

Comprehensive testing framework for the TrustWrapper zero-knowledge proof system.

## Overview

This test suite provides comprehensive validation of TrustWrapper functionality, including:
- Core wrapper functionality
- Zero-knowledge proof generation
- Leo smart contract integration
- Aleo blockchain verification
- Performance benchmarks
- Integration scenarios

## Test Structure

```
tests/
├── README.md                    # This file
├── pytest.ini                   # Pytest configuration
├── requirements-test.txt        # Testing dependencies
├── run_tests.py                # Automated test runner
├── test_trust_wrapper.py       # Core functionality tests
├── test_leo_integration.py     # Blockchain integration tests
├── test_demos.py              # Demo validation tests
└── test_performance.py        # Performance benchmark tests
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r tests/requirements-test.txt
```

### 2. Run All Tests

```bash
# Basic test run
python tests/run_tests.py

# Verbose output
python tests/run_tests.py -v

# With coverage report
python tests/run_tests.py -c

# Continuous testing mode
python tests/run_tests.py -w
```

### 3. Run Specific Tests

```bash
# Run only trust wrapper tests
pytest tests/test_trust_wrapper.py -v

# Run specific test by name
python tests/run_tests.py -k "test_execution_proof"

# Run tests with specific marker
pytest -m "not slow"
```

## Test Categories

### Core Tests (`test_trust_wrapper.py`)
- **Wrapper Initialization**: Agent wrapping and hash generation
- **Execution Tests**: Synchronous and asynchronous execution
- **Proof Generation**: Zero-knowledge proof creation
- **Error Handling**: Failed execution scenarios
- **Performance**: Overhead and efficiency tests

### Integration Tests (`test_leo_integration.py`)
- **Leo Proof Generation**: Aleo blockchain proof creation
- **Contract Integration**: Leo smart contract interaction
- **Verification**: On-chain proof verification
- **End-to-End**: Complete verification flow

### Demo Tests (`test_demos.py`)
- **Demo Imports**: Validate demo modules
- **Demo Execution**: Test demo functionality
- **Example Agents**: Verify example implementations

### Performance Tests (`test_performance.py`)
- **Wrapper Overhead**: Measure performance impact
- **Proof Generation Speed**: Benchmark proof creation
- **Scalability**: Large-scale execution tests
- **Memory Usage**: Memory efficiency validation

## Test Markers

Tests are marked with categories for selective execution:

- `@pytest.mark.slow` - Long-running tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.performance` - Performance benchmarks
- `@pytest.mark.blockchain` - Blockchain interaction tests

Run specific categories:
```bash
# Skip slow tests
pytest -m "not slow"

# Only integration tests
pytest -m integration
```

## Coverage Reports

Generate coverage reports:

```bash
# Terminal report
python tests/run_tests.py -c

# HTML report
pytest --cov=src --cov-report=html
# Open coverage_html/index.html in browser
```

## Continuous Testing

Watch for file changes and auto-run tests:

```bash
python tests/run_tests.py -w
```

This monitors:
- Source files in `src/`
- Test files in `tests/`
- Runs tests automatically on changes

## Test Examples

### Testing a Custom Agent

```python
def test_custom_agent_wrapping():
    """Test wrapping a custom agent"""
    class MyAgent:
        def execute(self, data):
            return {"processed": data}
    
    agent = MyAgent()
    wrapper = ZKTrustWrapper(agent)
    
    result = wrapper.verified_execute("test_data")
    
    assert result.verified is True
    assert result.result["processed"] == "test_data"
    assert result.proof.success is True
```

### Testing Async Execution

```python
@pytest.mark.asyncio
async def test_async_agent():
    """Test async agent execution"""
    class AsyncAgent:
        async def execute(self, data):
            await asyncio.sleep(0.1)
            return {"async_result": data}
    
    agent = AsyncAgent()
    wrapper = ZKTrustWrapper(agent)
    
    result = await wrapper.verified_execute_async("test")
    
    assert result.proof.execution_time >= 100  # At least 100ms
```

### Testing Blockchain Integration

```python
@pytest.mark.blockchain
async def test_blockchain_verification():
    """Test blockchain proof verification"""
    wrapper = ZKTrustWrapper(agent, enable_blockchain=True)
    
    result = await wrapper.verified_execute_with_blockchain(data)
    
    assert result.blockchain_proof is not None
    assert result.blockchain_proof["status"] == "confirmed"
```

## Debugging Tests

### Run with detailed output
```bash
pytest -vv -s tests/test_trust_wrapper.py
```

### Run with debugger
```bash
pytest --pdb tests/test_trust_wrapper.py
```

### Run specific test with print statements
```bash
pytest -s -k "test_name" tests/test_file.py
```

## Test Results

Test results are saved as JSON reports:
- Location: `tests/test_report_<timestamp>.json`
- Contains: Test outcomes, durations, coverage metrics

Example report structure:
```json
{
  "timestamp": "2025-06-21T10:30:00",
  "tests": {
    "Core TrustWrapper Tests": {
      "passed": true,
      "duration": 2.34,
      "summary": "25 passed in 2.34s"
    }
  },
  "summary": {
    "total_suites": 4,
    "passed_suites": 4,
    "success_rate": 100.0
  }
}
```

## Writing New Tests

1. Create test file: `test_<feature>.py`
2. Import required modules:
   ```python
   import pytest
   from src.core.trust_wrapper import ZKTrustWrapper
   ```
3. Write test class or functions:
   ```python
   class TestNewFeature:
       def test_feature_behavior(self):
           # Test implementation
           assert expected == actual
   ```
4. Run your tests:
   ```bash
   pytest tests/test_<feature>.py -v
   ```

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Clear Names**: Use descriptive test names
3. **Assertions**: Use specific assertions with messages
4. **Mocking**: Mock external dependencies
5. **Coverage**: Aim for >80% code coverage
6. **Documentation**: Document complex test scenarios

## Troubleshooting

### Import Errors
- Ensure project root is in PYTHONPATH
- Check `sys.path` additions in test files

### Async Test Issues
- Use `@pytest.mark.asyncio` decorator
- Ensure `pytest-asyncio` is installed

### Coverage Not Working
- Check `pytest.ini` configuration
- Verify source paths in coverage settings

### Slow Tests
- Mark slow tests with `@pytest.mark.slow`
- Use `-m "not slow"` to skip during development

## Contributing

When adding new features:
1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Add appropriate test markers
4. Update this README if needed
5. Run full test suite before committing

Happy Testing! 🧪✨