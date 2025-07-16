#!/bin/bash

# TrustWrapper v3.0 Kubernetes Deployment Script
# Universal Multi-Chain AI Verification Platform
# Production deployment automation

set -euo pipefail

# Configuration
NAMESPACE="trustwrapper"
DOCKER_IMAGE="trustwrapper/v3"
KUBECTL_CONTEXT="${KUBECTL_CONTEXT:-production}"
ENVIRONMENT="${ENVIRONMENT:-production}"

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

# Verify prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is not installed"
        exit 1
    fi

    if ! command -v docker &> /dev/null; then
        log_error "docker is not installed"
        exit 1
    fi

    if ! kubectl cluster-info &> /dev/null; then
        log_error "Unable to connect to Kubernetes cluster"
        exit 1
    fi

    log_success "Prerequisites check passed"
}

# Build and push Docker image
build_and_push_image() {
    log_info "Building TrustWrapper v3.0 Docker image..."

    cd "$(dirname "$0")/.."

    # Build optimized production image
    docker build \
        -f src/trustwrapper/v3/Dockerfile.production \
        -t "${DOCKER_IMAGE}:latest" \
        -t "${DOCKER_IMAGE}:$(date +%Y%m%d-%H%M%S)" \
        .

    log_success "Docker image built successfully"

    # Push to registry (assuming registry is configured)
    if [[ "${PUSH_IMAGE:-true}" == "true" ]]; then
        log_info "Pushing image to registry..."
        docker push "${DOCKER_IMAGE}:latest"
        log_success "Image pushed successfully"
    fi
}

# Deploy to Kubernetes
deploy_kubernetes() {
    log_info "Deploying TrustWrapper v3.0 to Kubernetes..."

    # Set kubectl context
    kubectl config use-context "${KUBECTL_CONTEXT}"

    # Create namespace
    log_info "Creating namespace..."
    kubectl apply -f k8s/namespace.yaml

    # Wait for namespace to be ready
    kubectl wait --for=condition=Active namespace/${NAMESPACE} --timeout=60s

    # Apply secrets (template - replace with actual secrets management)
    log_warning "Please ensure secrets are properly configured before deployment"

    # Deploy application
    log_info "Deploying application components..."
    kubectl apply -f k8s/trustwrapper-deployment.yaml
    kubectl apply -f k8s/ingress.yaml
    kubectl apply -f k8s/monitoring.yaml

    log_success "Kubernetes manifests applied"
}

# Wait for deployment to be ready
wait_for_deployment() {
    log_info "Waiting for deployment to be ready..."

    kubectl wait --for=condition=available \
        --timeout=300s \
        deployment/trustwrapper-v3 \
        -n ${NAMESPACE}

    log_success "Deployment is ready"
}

# Verify deployment health
verify_deployment() {
    log_info "Verifying deployment health..."

    # Check pod status
    kubectl get pods -n ${NAMESPACE} -l app=trustwrapper

    # Check service status
    kubectl get services -n ${NAMESPACE}

    # Check HPA status
    kubectl get hpa -n ${NAMESPACE}

    # Test health endpoint
    if kubectl get ingress -n ${NAMESPACE} trustwrapper-ingress &> /dev/null; then
        INGRESS_IP=$(kubectl get ingress -n ${NAMESPACE} trustwrapper-ingress -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
        if [[ -n "${INGRESS_IP}" ]]; then
            log_info "Testing health endpoint..."
            if curl -f "http://${INGRESS_IP}/health" &> /dev/null; then
                log_success "Health endpoint is responding"
            else
                log_warning "Health endpoint is not responding yet"
            fi
        fi
    fi

    log_success "Deployment verification completed"
}

# Performance test
run_performance_test() {
    log_info "Running basic performance test..."

    # Port forward for testing
    kubectl port-forward -n ${NAMESPACE} service/trustwrapper-service 8080:80 &
    PF_PID=$!

    sleep 5

    # Basic load test
    if command -v ab &> /dev/null; then
        log_info "Running Apache Bench test..."
        ab -n 100 -c 10 http://localhost:8080/health
    else
        log_warning "Apache Bench not available, skipping performance test"
    fi

    # Cleanup port forward
    kill $PF_PID 2>/dev/null || true

    log_success "Performance test completed"
}

# Rollback function
rollback_deployment() {
    log_warning "Rolling back deployment..."
    kubectl rollout undo deployment/trustwrapper-v3 -n ${NAMESPACE}
    kubectl rollout status deployment/trustwrapper-v3 -n ${NAMESPACE}
    log_success "Rollback completed"
}

# Main deployment function
main() {
    log_info "Starting TrustWrapper v3.0 deployment..."

    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-build)
                SKIP_BUILD=true
                shift
                ;;
            --skip-tests)
                SKIP_TESTS=true
                shift
                ;;
            --rollback)
                rollback_deployment
                exit 0
                ;;
            --verify-only)
                verify_deployment
                exit 0
                ;;
            *)
                log_error "Unknown option $1"
                exit 1
                ;;
        esac
    done

    # Execute deployment steps
    check_prerequisites

    if [[ "${SKIP_BUILD:-false}" != "true" ]]; then
        build_and_push_image
    fi

    deploy_kubernetes
    wait_for_deployment
    verify_deployment

    if [[ "${SKIP_TESTS:-false}" != "true" ]]; then
        run_performance_test
    fi

    log_success "TrustWrapper v3.0 deployment completed successfully!"
    log_info "Access your deployment:"
    log_info "  - API: http://api.trustwrapper.com"
    log_info "  - Monitoring: Check Grafana dashboard"
    log_info "  - Logs: kubectl logs -n ${NAMESPACE} -l app=trustwrapper -f"
}

# Error handling
trap 'log_error "Deployment failed at line $LINENO"' ERR

# Run main function
main "$@"
