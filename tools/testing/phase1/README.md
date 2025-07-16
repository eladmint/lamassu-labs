# TrustWrapper v3.0 Phase 1 - Test Runners

This directory contains test execution scripts for TrustWrapper v3.0 Phase 1 Week 1 validation.

## Available Test Runners

### 1. **run_week1_testing.py**
Comprehensive Week 1 integration testing orchestrator that executes:
- Unit tests (>90% coverage target)
- Integration tests (5 scenarios)
- Performance tests (1,000 RPS baseline)
- Security and fault tolerance tests

**Usage:**
```bash
python tools/testing/phase1/run_week1_testing.py
```

### 2. **run_simple_validation.py**
Simplified validation script for quick Phase 1 verification:
- Architecture validation (91.7% achieved)
- Implementation completeness check
- Basic functionality tests
- Bridge architecture validation
- Phase 1 achievements verification

**Usage:**
```bash
python tools/testing/phase1/run_simple_validation.py
```

## Test Results

All test results and reports are stored in:
- `internal_docs/reports/sprint24-phase1/`

## Related Files

- **Test Suites**: `src/trustwrapper-v3/tests/`
- **Demo Files**: `tools/examples/trustwrapper-v3/`
- **Sprint Reports**: `internal_docs/reports/sprint24-phase1/`

---

*Last Updated: June 26, 2025 - Week 1 Testing Complete*
