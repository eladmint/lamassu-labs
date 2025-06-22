# Lamassu Labs Development Tools

Internal development tools for TrustWrapper ZK-verified AI hallucination detection system.

## Directory Structure

- **testing/** - Test utilities and development test scripts
- **analysis/** - Data analysis and research tools
- **debugging/** - System debugging utilities  
- **deployment/** - Deployment verification tools
- **development/** - Development environment setup

## Testing Tools

Located in `testing/` directory:
- `test_enhanced_detector.py` - Enhanced hallucination detector tests
- `test_gemini_access.py` - Google Gemini API integration tests
- `test_hallucination_detection.py` - Core detection system tests
- `prove_trustwrapper_works.py` - Complete system validation
- `simple_hallucination_test.py` - Basic functionality tests

## Usage

All tools should be run from the Lamassu Labs root directory:

```bash
# Run enhanced detector tests
python tools/testing/test_enhanced_detector.py

# Validate complete system
python tools/testing/prove_trustwrapper_works.py

# Run simple functionality test
python tools/testing/simple_hallucination_test.py
```

## Security Note

These are internal development tools. Do not expose to end users or include in public distributions.