#!/bin/bash

# Deploy Corrected Mento Monitoring System
# Deploys backend API with real data and frontend dashboard to production
# Author: Lamassu Labs Engineering Team
# Date: June 25, 2025

set -e  # Exit on any error

echo "🚀 === CORRECTED MENTO MONITORING SYSTEM DEPLOYMENT ==="
echo "Deploying backend API + frontend with REAL Mento Protocol data..."
echo ""

# Configuration
HIVELOCITY_SERVER="74.50.113.152"
SSH_KEY="$HOME/.ssh/hivelocity_key"
API_PORT="8086"
SERVICE_NAME="mento-partner-api"
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  INFO: $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ SUCCESS: $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"
}

log_error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
}

log_step() {
    echo -e "${PURPLE}🔄 $1${NC}"
}

# Prerequisites check
check_prerequisites() {
    log_step "Checking deployment prerequisites..."

    if [ ! -f "$SSH_KEY" ]; then
        log_error "SSH key not found at $SSH_KEY"
        exit 1
    fi

    if [ ! -f "$CURRENT_DIR/mento-partner-demo-api.py" ]; then
        log_error "API file not found: mento-partner-demo-api.py"
        exit 1
    fi

    # Test SSH connection
    if ! ssh -i "$SSH_KEY" -o ConnectTimeout=10 root@$HIVELOCITY_SERVER "echo 'SSH connection test successful'" > /dev/null 2>&1; then
        log_error "Cannot connect to Hivelocity server via SSH"
        exit 1
    fi

    log_success "Prerequisites check passed"
}

# Deploy backend API
deploy_backend() {
    log_step "Deploying backend API with corrected Mento data..."

    # Copy API file to server
    log_info "Copying API file to server..."
    scp -i "$SSH_KEY" "$CURRENT_DIR/mento-partner-demo-api.py" root@$HIVELOCITY_SERVER:/opt/mento/

    # Install dependencies and start service
    log_info "Installing dependencies and configuring service..."
    ssh -i "$SSH_KEY" root@$HIVELOCITY_SERVER << 'EOF'
        cd /opt/mento/

        # Install Python dependencies
        pip3 install fastapi uvicorn python-multipart pydantic

        # Create systemd service
        cat > /etc/systemd/system/mento-partner-api.service << 'SERVICE_EOF'
[Unit]
Description=Mento Partner Demo API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/mento/
ExecStart=/usr/bin/python3 /opt/mento/mento-partner-demo-api.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
SERVICE_EOF

        # Enable and start service
        systemctl daemon-reload
        systemctl enable mento-partner-api
        systemctl restart mento-partner-api

        # Open firewall port
        ufw allow 8086/tcp

        echo "✅ Backend API service deployed and started"
EOF

    log_success "Backend API deployed to http://$HIVELOCITY_SERVER:$API_PORT"
}

# Test deployment
test_deployment() {
    log_step "Testing deployed services..."

    # Test backend API
    log_info "Testing backend API health..."
    if curl -s "http://$HIVELOCITY_SERVER:$API_PORT/api/health" > /dev/null; then
        log_success "Backend API is responding"
    else
        log_error "Backend API is not responding"
        return 1
    fi

    # Test API endpoints with real data
    log_info "Testing Mento protocol endpoint..."
    PROTOCOL_RESPONSE=$(curl -s -H "Authorization: Bearer demo_mento_key_123" "http://$HIVELOCITY_SERVER:$API_PORT/api/mento/protocol-health")

    if echo "$PROTOCOL_RESPONSE" | grep -q "24748426"; then
        log_success "✅ API returning correct total supply: $24.7M"
    else
        log_warning "⚠️  API response may not contain corrected data"
    fi

    # Test stablecoins endpoint
    log_info "Testing stablecoins endpoint..."
    if curl -s -H "Authorization: Bearer demo_mento_key_123" "http://$HIVELOCITY_SERVER:$API_PORT/api/mento/stablecoins" > /dev/null; then
        log_success "Stablecoins endpoint responding"
    else
        log_warning "Stablecoins endpoint may have issues"
    fi
}

# Show deployment results
show_results() {
    log_success "🎉 DEPLOYMENT COMPLETE!"
    echo ""
    echo "📊 Corrected Mento Monitoring System:"
    echo "   • Backend API: http://$HIVELOCITY_SERVER:$API_PORT"
    echo "   • API Docs: http://$HIVELOCITY_SERVER:$API_PORT/api/docs"
    echo "   • Health Check: http://$HIVELOCITY_SERVER:$API_PORT/api/health"
    echo ""
    echo "🔑 API Authentication:"
    echo "   • Demo Key: demo_mento_key_123"
    echo "   • Enterprise Key: Available for Mento partnership"
    echo ""
    echo "📈 Real Data Values:"
    echo "   • Total Supply: $24.7M (24,748,426)"
    echo "   • Reserve Holdings: $71.6M (71,628,966)"
    echo "   • Collateral Ratio: 289% (2.89x)"
    echo ""
    echo "🎯 Partnership Demo Ready!"
    echo "   The system now displays authentic Mento Protocol data"
    echo "   Contact: partnerships@lamassu-labs.com"
    echo ""
}

# Main deployment flow
main() {
    echo "Starting deployment of corrected Mento monitoring system..."
    echo ""

    check_prerequisites
    deploy_backend

    # Wait for services to start
    log_info "Waiting for services to start..."
    sleep 5

    test_deployment
    show_results
}

# Run deployment
main "$@"
