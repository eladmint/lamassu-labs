#!/bin/bash

# Deploy script for Mento Live API with Chainlink integration
# This updates the existing API to use live data

echo "🚀 Deploying Mento Live API with Chainlink Integration"
echo "======================================================="

# Check if running on Hivelocity VPS
if [[ $(hostname) == *"hivelocity"* ]] || [[ $(hostname -I | grep "74.50.113.152") ]]; then
    echo "✅ Running on Hivelocity VPS"
    IS_PRODUCTION=true
else
    echo "📍 Running locally for testing"
    IS_PRODUCTION=false
fi

# Install dependencies
echo -e "\n📦 Installing dependencies..."
if [ -f "package.json" ]; then
    npm install ethers node-cache
else
    # Create package.json if it doesn't exist
    cat > package.json << EOF
{
  "name": "mento-live-api",
  "version": "1.0.0",
  "description": "Mento Protocol Live API with Chainlink",
  "main": "chainlink_oracle_service.js",
  "dependencies": {
    "ethers": "^5.7.2",
    "node-cache": "^5.1.2",
    "express": "^4.18.2",
    "cors": "^2.8.5"
  }
}
EOF
    npm install
fi

# Test Chainlink connection
echo -e "\n🔗 Testing Chainlink connection..."
node chainlink_live_demo.js

# Python dependencies for live API
echo -e "\n🐍 Setting up Python environment..."
pip install fastapi uvicorn httpx

if [ "$IS_PRODUCTION" = true ]; then
    echo -e "\n🚀 Deploying to production..."

    # Stop existing API service
    sudo systemctl stop mento-api || true

    # Copy new API file
    sudo cp mento_api_live.py /opt/mento-monitoring/api/

    # Update systemd service to use port 8087 for testing
    sudo tee /etc/systemd/system/mento-api-live.service > /dev/null << EOF
[Unit]
Description=Mento Live API with Chainlink
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/mento-monitoring/api
ExecStart=/usr/bin/python3 -m uvicorn mento_api_live:app --host 0.0.0.0 --port 8087
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    # Reload and start service
    sudo systemctl daemon-reload
    sudo systemctl enable mento-api-live
    sudo systemctl start mento-api-live

    # Check status
    sleep 2
    sudo systemctl status mento-api-live --no-pager

    echo -e "\n✅ Live API deployed on port 8087"
    echo "   Test: curl http://74.50.113.152:8087/api/mento/live-dashboard-data"

else
    echo -e "\n🧪 Starting local test server..."
    echo "   API will run on: http://localhost:8087"
    echo "   Press Ctrl+C to stop"

    # Run in background for testing
    python3 mento_api_live.py &
    API_PID=$!

    # Wait a moment for startup
    sleep 3

    # Test the API
    echo -e "\n📊 Testing live data endpoint..."
    curl -s http://localhost:8087/api/mento/live-dashboard-data | jq '.'

    echo -e "\n💡 To integrate with dashboard:"
    echo "1. Update dashboard to use port 8087 instead of 8086"
    echo "2. Look for 'is_live_data: true' flag in response"
    echo "3. Dashboard will show real Chainlink prices"

    # Keep running
    echo -e "\nPress Enter to stop the test server..."
    read
    kill $API_PID
fi

echo -e "\n✅ Deployment complete!"
