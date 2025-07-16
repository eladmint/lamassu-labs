#!/bin/bash
# Deploy TrustWrapper Backend to Hivelocity VPS (Tampa)
# This script deploys the minimal TrustWrapper API for Senpi integration

set -e

echo "🚀 Deploying TrustWrapper Backend to Hivelocity VPS"
echo "=================================================="

# Configuration
VPS_HOST="23.92.65.243"
VPS_USER="root"
VPS_PASSWORD="YS6OaT2uruHa"
DEPLOY_PATH="/opt/trustwrapper"
SERVICE_NAME="trustwrapper-api"
PORT=3000

# Create deployment package
echo "📦 Creating deployment package..."
mkdir -p deploy-package
cp -r ../backend/* deploy-package/
cp -r ../plugin-trustwrapper-verification deploy-package/

# Create systemd service file
cat > deploy-package/trustwrapper-api.service << EOF
[Unit]
Description=TrustWrapper API Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$DEPLOY_PATH
ExecStart=/usr/bin/node $DEPLOY_PATH/server.js
Restart=always
RestartSec=10
Environment=NODE_ENV=production
Environment=PORT=$PORT
Environment=NOWNODES_API_KEY=$NOWNODES_API_KEY

[Install]
WantedBy=multi-user.target
EOF

# Create deployment script
cat > deploy-package/setup.sh << 'EOF'
#!/bin/bash
set -e

echo "Setting up TrustWrapper API on server..."

# Install Node.js if not present
if ! command -v node &> /dev/null; then
    echo "Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Install PM2 for process management
if ! command -v pm2 &> /dev/null; then
    echo "Installing PM2..."
    npm install -g pm2
fi

# Install dependencies
cd /opt/trustwrapper
npm install --production

# Build TypeScript files
npm run build || echo "Build step skipped (no TypeScript compiler)"

# Setup PM2
pm2 delete trustwrapper-api || true
pm2 start server.js --name trustwrapper-api --env production
pm2 save
pm2 startup systemd -u root --hp /root

# Setup nginx reverse proxy if available
if command -v nginx &> /dev/null; then
    echo "Configuring nginx..."
    cat > /etc/nginx/sites-available/trustwrapper << NGINX_EOF
server {
    listen 80;
    server_name trustwrapper.api;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
NGINX_EOF

    ln -sf /etc/nginx/sites-available/trustwrapper /etc/nginx/sites-enabled/
    nginx -t && systemctl reload nginx
fi

echo "✅ TrustWrapper API setup complete!"
EOF

chmod +x deploy-package/setup.sh

# Deploy via SSH
echo "🚀 Deploying to VPS at $VPS_HOST..."

# Note: In production, use SSH keys instead of password
# For now, we'll prepare the files and provide manual instructions

echo ""
echo "📋 Manual Deployment Instructions:"
echo "=================================="
echo ""
echo "1. Copy files to VPS:"
echo "   scp -r deploy-package/* root@$VPS_HOST:$DEPLOY_PATH/"
echo ""
echo "2. SSH into the VPS:"
echo "   ssh root@$VPS_HOST"
echo "   Password: $VPS_PASSWORD"
echo ""
echo "3. Run the setup script:"
echo "   cd $DEPLOY_PATH"
echo "   chmod +x setup.sh"
echo "   ./setup.sh"
echo ""
echo "4. Verify the service is running:"
echo "   pm2 status"
echo "   curl http://localhost:$PORT/v1/health"
echo ""
echo "5. Access the API:"
echo "   External: http://$VPS_HOST:$PORT/v1"
echo ""
echo "🔐 Security Notes:"
echo "- Configure firewall: ufw allow $PORT"
echo "- Set up SSL certificate with Let's Encrypt"
echo "- Use environment variables for sensitive data"
echo ""
echo "✅ Deployment package ready in ./deploy-package/"
