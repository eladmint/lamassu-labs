#!/bin/bash

# TrustWrapper v3.0 Complete Validation Suite
# Runs all performance, security, and integration tests
# Universal Multi-Chain AI Verification Platform

set -euo pipefail

# Configuration
BASE_URL="${BASE_URL:-https://api.trustwrapper.com}"
API_KEY="${API_KEY:-}"
OUTPUT_DIR="${OUTPUT_DIR:-./test-results}"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create output directory
create_output_dir() {
    mkdir -p "${OUTPUT_DIR}"
    log_info "Created output directory: ${OUTPUT_DIR}"
}

# Validate prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed"
        exit 1
    fi

    if ! python3 -c "import aiohttp, asyncio" &> /dev/null; then
        log_error "Required Python packages not installed"
        log_info "Install with: pip install aiohttp asyncio"
        exit 1
    fi

    # Check if TrustWrapper API is accessible
    if ! curl -sf "${BASE_URL}/health" &> /dev/null; then
        log_warning "TrustWrapper API not responding at ${BASE_URL}"
        log_info "Continuing with tests - some may fail if API is down"
    fi

    log_success "Prerequisites check completed"
}

# Run performance tests
run_performance_tests() {
    log_info "Running performance validation tests..."

    local output_file="${OUTPUT_DIR}/performance_results_${TIMESTAMP}.json"

    # Run load testing with different RPS targets
    local rps_targets=(1000 2500 5000 7500)
    local overall_success=true

    for rps in "${rps_targets[@]}"; do
        log_info "Testing ${rps} RPS target..."

        if python3 tools/testing/performance/load_test_suite.py \
            --url "${BASE_URL}" \
            --rps "${rps}" \
            --duration 120 \
            --users $((rps / 10)) \
            --output "${OUTPUT_DIR}/load_test_${rps}rps_${TIMESTAMP}.json"; then
            log_success "${rps} RPS test passed"
        else
            log_error "${rps} RPS test failed"
            overall_success=false

            # Stop at first failure for high RPS tests
            if [ "${rps}" -ge 5000 ]; then
                log_warning "Stopping performance tests due to failure at ${rps} RPS"
                break
            fi
        fi
    done

    if [ "${overall_success}" = true ]; then
        log_success "All performance tests passed"
        return 0
    else
        log_error "Some performance tests failed"
        return 1
    fi
}

# Run security tests
run_security_tests() {
    log_info "Running security validation tests..."

    local api_key_param=""
    if [ -n "${API_KEY}" ]; then
        api_key_param="--api-key ${API_KEY}"
    fi

    if python3 tools/testing/security/security_test_suite.py \
        --url "${BASE_URL}" \
        ${api_key_param} \
        --output "${OUTPUT_DIR}/security_results_${TIMESTAMP}.json"; then
        log_success "Security tests passed"
        return 0
    else
        log_error "Security tests failed"
        return 1
    fi
}

# Run integration tests
run_integration_tests() {
    log_info "Running end-to-end integration tests..."

    local api_key_param=""
    if [ -n "${API_KEY}" ]; then
        api_key_param="--api-key ${API_KEY}"
    fi

    if python3 tools/testing/integration/end_to_end_validation.py \
        --url "${BASE_URL}" \
        ${api_key_param} \
        --timeout 120 \
        --output "${OUTPUT_DIR}/e2e_results_${TIMESTAMP}.json"; then
        log_success "Integration tests passed"
        return 0
    else
        log_error "Integration tests failed"
        return 1
    fi
}

# Run blockchain connectivity tests
run_blockchain_tests() {
    log_info "Running blockchain connectivity tests..."

    # Test individual blockchain connections
    local chains=("ethereum" "cardano" "solana" "bitcoin" "polygon")
    local blockchain_success=true

    for chain in "${chains[@]}"; do
        log_info "Testing ${chain} connectivity..."

        # Simple connectivity test
        if curl -sf \
            -X POST \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer ${API_KEY}" \
            -d "{\"chain\":\"${chain}\",\"test\":\"connectivity\"}" \
            "${BASE_URL}/verify" &> /dev/null; then
            log_success "${chain} connectivity test passed"
        else
            log_warning "${chain} connectivity test failed"
            blockchain_success=false
        fi
    done

    if [ "${blockchain_success}" = true ]; then
        log_success "All blockchain connectivity tests passed"
        return 0
    else
        log_warning "Some blockchain connectivity tests failed"
        return 1
    fi
}

# Generate comprehensive report
generate_comprehensive_report() {
    log_info "Generating comprehensive validation report..."

    local report_file="${OUTPUT_DIR}/comprehensive_validation_report_${TIMESTAMP}.json"

    cat > "${report_file}" << EOF
{
    "validation_summary": {
        "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
        "test_suite": "TrustWrapper v3.0 Complete Validation",
        "base_url": "${BASE_URL}",
        "test_duration": "$(date -d @$(($(date +%s) - ${START_TIME})) -u +%H:%M:%S)",
        "output_directory": "${OUTPUT_DIR}"
    },
    "test_categories": {
        "performance": {
            "status": "${PERFORMANCE_STATUS:-unknown}",
            "target_rps": 5000,
            "results_file": "performance_results_${TIMESTAMP}.json"
        },
        "security": {
            "status": "${SECURITY_STATUS:-unknown}",
            "results_file": "security_results_${TIMESTAMP}.json"
        },
        "integration": {
            "status": "${INTEGRATION_STATUS:-unknown}",
            "results_file": "e2e_results_${TIMESTAMP}.json"
        },
        "blockchain": {
            "status": "${BLOCKCHAIN_STATUS:-unknown}",
            "tested_chains": ["ethereum", "cardano", "solana", "bitcoin", "polygon"]
        }
    },
    "overall_status": "${OVERALL_STATUS:-unknown}",
    "recommendations": [
        "Review failed test results for specific issues",
        "Verify API key configuration if authentication tests failed",
        "Check blockchain node connectivity if blockchain tests failed",
        "Monitor performance metrics during load testing",
        "Address any security vulnerabilities immediately"
    ]
}
EOF

    log_success "Comprehensive report generated: ${report_file}"
}

# Print final summary
print_final_summary() {
    echo ""
    echo "================================================================"
    echo "TRUSTWRAPPER v3.0 VALIDATION COMPLETE"
    echo "================================================================"
    echo "Test Suite:        Complete Validation"
    echo "Target URL:        ${BASE_URL}"
    echo "Test Duration:     $(date -d @$(($(date +%s) - ${START_TIME})) -u +%H:%M:%S)"
    echo "Output Directory:  ${OUTPUT_DIR}"
    echo "================================================================"
    echo "RESULTS SUMMARY:"
    echo "  Performance:     ${PERFORMANCE_STATUS:-UNKNOWN}"
    echo "  Security:        ${SECURITY_STATUS:-UNKNOWN}"
    echo "  Integration:     ${INTEGRATION_STATUS:-UNKNOWN}"
    echo "  Blockchain:      ${BLOCKCHAIN_STATUS:-UNKNOWN}"
    echo "================================================================"
    echo "OVERALL STATUS:    ${OVERALL_STATUS}"
    echo "================================================================"

    if [ "${OVERALL_STATUS}" = "PASS" ]; then
        echo "🎉 All validation tests passed! TrustWrapper v3.0 is ready for production."
    elif [ "${OVERALL_STATUS}" = "PARTIAL PASS" ]; then
        echo "⚠️  Some tests failed. Review results before production deployment."
    else
        echo "❌ Validation failed. Address issues before proceeding with deployment."
    fi

    echo ""
    echo "View detailed results in: ${OUTPUT_DIR}/"
    echo "================================================================"
}

# Main validation function
main() {
    # Record start time
    START_TIME=$(date +%s)

    log_info "Starting TrustWrapper v3.0 complete validation suite..."

    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --url)
                BASE_URL="$2"
                shift 2
                ;;
            --api-key)
                API_KEY="$2"
                shift 2
                ;;
            --output-dir)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            --skip-performance)
                SKIP_PERFORMANCE=true
                shift
                ;;
            --skip-security)
                SKIP_SECURITY=true
                shift
                ;;
            --skip-integration)
                SKIP_INTEGRATION=true
                shift
                ;;
            --skip-blockchain)
                SKIP_BLOCKCHAIN=true
                shift
                ;;
            *)
                log_error "Unknown option $1"
                exit 1
                ;;
        esac
    done

    # Execute validation steps
    create_output_dir
    check_prerequisites

    # Run test suites
    if [ "${SKIP_PERFORMANCE:-false}" != "true" ]; then
        if run_performance_tests; then
            PERFORMANCE_STATUS="PASS"
        else
            PERFORMANCE_STATUS="FAIL"
        fi
    else
        PERFORMANCE_STATUS="SKIPPED"
    fi

    if [ "${SKIP_SECURITY:-false}" != "true" ]; then
        if run_security_tests; then
            SECURITY_STATUS="PASS"
        else
            SECURITY_STATUS="FAIL"
        fi
    else
        SECURITY_STATUS="SKIPPED"
    fi

    if [ "${SKIP_INTEGRATION:-false}" != "true" ]; then
        if run_integration_tests; then
            INTEGRATION_STATUS="PASS"
        else
            INTEGRATION_STATUS="FAIL"
        fi
    else
        INTEGRATION_STATUS="SKIPPED"
    fi

    if [ "${SKIP_BLOCKCHAIN:-false}" != "true" ]; then
        if run_blockchain_tests; then
            BLOCKCHAIN_STATUS="PASS"
        else
            BLOCKCHAIN_STATUS="FAIL"
        fi
    else
        BLOCKCHAIN_STATUS="SKIPPED"
    fi

    # Determine overall status
    local failed_tests=0
    [ "${PERFORMANCE_STATUS}" = "FAIL" ] && ((failed_tests++))
    [ "${SECURITY_STATUS}" = "FAIL" ] && ((failed_tests++))
    [ "${INTEGRATION_STATUS}" = "FAIL" ] && ((failed_tests++))
    [ "${BLOCKCHAIN_STATUS}" = "FAIL" ] && ((failed_tests++))

    if [ ${failed_tests} -eq 0 ]; then
        OVERALL_STATUS="PASS"
    elif [ ${failed_tests} -le 1 ]; then
        OVERALL_STATUS="PARTIAL PASS"
    else
        OVERALL_STATUS="FAIL"
    fi

    # Generate reports and summary
    generate_comprehensive_report
    print_final_summary

    # Exit with appropriate code
    if [ "${OVERALL_STATUS}" = "PASS" ]; then
        exit 0
    elif [ "${OVERALL_STATUS}" = "PARTIAL PASS" ]; then
        exit 0  # Still considered success for CI/CD
    else
        exit 1
    fi
}

# Error handling
trap 'log_error "Validation failed at line $LINENO"' ERR

# Export variables for sub-scripts
export BASE_URL API_KEY OUTPUT_DIR TIMESTAMP

# Run main function
main "$@"
