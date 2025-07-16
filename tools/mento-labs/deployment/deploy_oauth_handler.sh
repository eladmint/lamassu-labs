#!/bin/bash

# OAuth Handler Deployment Script for Hivelocity Staten Island VPS
# Target: 74.50.113.152:3001

set -e

echo "🚀 Starting OAuth Handler deployment to Hivelocity..."

# Configuration
VPS_IP="74.50.113.152"
SSH_KEY="~/.ssh/hivelocity_key"
SERVICE_DIR="/opt/oauth-handler"
SERVICE_NAME="oauth-handler"

# Get Google Client Secret from .env file
GOOGLE_CLIENT_SECRET=$(grep "GOOGLE_OAUTH_CLIENT_SECRET" /Users/eladm/Projects/token/tokenhunter/.env | cut -d'=' -f2 | tr -d '"')
if [ -z "$GOOGLE_CLIENT_SECRET" ]; then
    echo "❌ Error: GOOGLE_OAUTH_CLIENT_SECRET not found in .env file"
    exit 1
fi

echo "✅ Found Google Client Secret in .env file"

# Generated JWT Secret
JWT_SECRET="4e08f8a65671451252a888a545d0db2c1e5459dc93e984f4f1dc7bf4c44703e3"

echo "📦 Deploying OAuth handler to $VPS_IP..."

# Create deployment package
TEMP_DIR=$(mktemp -d)
cp src/oauth-api-handler-commonjs.js "$TEMP_DIR/"
cp src/oauth-server.js "$TEMP_DIR/"

# Create package.json
cat > "$TEMP_DIR/package.json" << EOF
{
  "name": "oauth-handler",
  "version": "1.0.0",
  "description": "OAuth Handler Service for Mento Dashboard",
  "main": "oauth-server.js",
  "scripts": {
    "start": "node oauth-server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "node-fetch": "^2.6.7",
    "jsonwebtoken": "^9.0.0",
    "cors": "^2.8.5"
  }
}
EOF

# Deploy files to VPS
echo "📁 Creating service directory on VPS..."
ssh -i $SSH_KEY root@$VPS_IP "mkdir -p $SERVICE_DIR"

echo "📤 Copying files to VPS..."
scp -i $SSH_KEY "$TEMP_DIR"/* root@$VPS_IP:$SERVICE_DIR/

echo "📦 Installing Node.js dependencies on VPS..."
ssh -i $SSH_KEY root@$VPS_IP "cd $SERVICE_DIR && npm install"

# Create systemd service file
echo "⚙️ Creating systemd service..."
ssh -i $SSH_KEY root@$VPS_IP "cat > /etc/systemd/system/$SERVICE_NAME.service << 'EOF'
[Unit]
Description=OAuth Handler Service for Mento Dashboard
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$SERVICE_DIR
Environment=\"NODE_ENV=production\"
Environment=\"PORT=3001\"
Environment=\"GOOGLE_CLIENT_ID=867263134607-vkkd9avs6a75gmjpzja17a9a0bbdle1.apps.googleusercontent.com\"
Environment=\"GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET\"
Environment=\"JWT_SECRET=$JWT_SECRET\"
Environment=\"ALLOWED_ORIGINS=https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io,http://localhost:3000\"
ExecStart=/usr/bin/node oauth-server.js
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF"

# Configure firewall
echo "🔥 Configuring firewall..."
ssh -i $SSH_KEY root@$VPS_IP "ufw allow 3001/tcp"

# Start the service
echo "🚀 Starting OAuth handler service..."
ssh -i $SSH_KEY root@$VPS_IP "systemctl daemon-reload"
ssh -i $SSH_KEY root@$VPS_IP "systemctl enable $SERVICE_NAME"
ssh -i $SSH_KEY root@$VPS_IP "systemctl start $SERVICE_NAME"

# Check service status
echo "📊 Checking service status..."
ssh -i $SSH_KEY root@$VPS_IP "systemctl status $SERVICE_NAME --no-pager"

# Test the endpoint
echo "🧪 Testing OAuth endpoint..."
HEALTH_CHECK=$(ssh -i $SSH_KEY root@$VPS_IP "curl -s -o /dev/null -w '%{http_code}' http://localhost:3001/api/oauth/google/exchange -X POST -H 'Content-Type: application/json' -d '{\"code\":\"test\",\"redirectUri\":\"https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io/auth/callback/google\"}' || echo '000'")

if [ "$HEALTH_CHECK" = "400" ]; then
    echo "✅ OAuth service is responding correctly (400 expected for test data)"
elif [ "$HEALTH_CHECK" = "000" ]; then
    echo "❌ OAuth service is not responding"
    exit 1
else
    echo "⚠️ OAuth service responded with code: $HEALTH_CHECK"
fi

# Show service logs
echo "📋 Recent service logs:"
ssh -i $SSH_KEY root@$VPS_IP "journalctl -u $SERVICE_NAME --no-pager -n 10"

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "🎉 OAuth Handler deployment completed successfully!"
echo ""
echo "📍 Service Details:"
echo "   URL: http://74.50.113.152:3001/api/oauth/google/exchange"
echo "   Status: systemctl status $SERVICE_NAME"
echo "   Logs: journalctl -u $SERVICE_NAME -f"
echo "   Restart: systemctl restart $SERVICE_NAME"
echo ""
echo "🧪 Test the service:"
echo "curl http://74.50.113.152:3001/api/oauth/google/exchange \\"
echo "  -X POST \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"code\":\"test\",\"redirectUri\":\"https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io/auth/callback/google\"}'"
echo ""
