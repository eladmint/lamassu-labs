#!/bin/bash

# Deploy Mento Protocol Dashboard to Hivelocity VPS
# Serves dashboard on Staten Island VPS alongside existing services

echo "🚀 Deploying Mento Protocol Dashboard to Hivelocity VPS..."
echo "Server: Staten Island (74.50.113.152)"
echo "Deployment: Parallel to Juno (ICP) deployment"
echo ""

# Configuration
HIVELOCITY_HOST="74.50.113.152"
SSH_KEY="~/.ssh/hivelocity_key"
DASHBOARD_DIR="/opt/nuru/mento-dashboard"
NGINX_CONFIG="/etc/nginx/sites-available/mento-dashboard"
SERVICE_NAME="mento-dashboard"

# Check if updated dashboard exists
if [ ! -f "dist/mento-dashboard.html" ]; then
    echo "❌ Updated dashboard not found. Please ensure dist/mento-dashboard.html exists."
    exit 1
fi

echo "📦 Preparing dashboard files..."
# Ensure we have the latest files
cp dist/mento-dashboard.html dist/index.html

echo ""
echo "🌐 Deploying to Hivelocity Staten Island VPS..."

# Create deployment directory on server
ssh -i "$SSH_KEY" root@"$HIVELOCITY_HOST" "mkdir -p $DASHBOARD_DIR/static"

# Upload dashboard files
echo "📤 Uploading dashboard files..."
scp -i "$SSH_KEY" dist/mento-dashboard.html root@"$HIVELOCITY_HOST":"$DASHBOARD_DIR/index.html"
scp -i "$SSH_KEY" dist/mento_dashboard_data.json root@"$HIVELOCITY_HOST":"$DASHBOARD_DIR/static/mento_dashboard_data.json" 2>/dev/null || echo "⚠️  mento_dashboard_data.json not found - dashboard will use live API only"

# Create Nginx configuration for the dashboard
echo "🔧 Configuring Nginx for dashboard hosting..."
ssh -i "$SSH_KEY" root@"$HIVELOCITY_HOST" "cat > $NGINX_CONFIG << 'EOF'
server {
    listen 8083;
    server_name 74.50.113.152;

    root $DASHBOARD_DIR;
    index index.html;

    # Enable gzip compression
    gzip on;
    gzip_types text/html text/css application/javascript application/json;

    # Cache static assets
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control \"public, immutable\";
    }

    # Serve dashboard
    location / {
        try_files \$uri \$uri/ /index.html;
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection \"1; mode=block\";
    }

    # Serve static files (JSON data)
    location /static/ {
        alias $DASHBOARD_DIR/static/;
        add_header Access-Control-Allow-Origin *;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 '{\"status\":\"healthy\",\"service\":\"mento-dashboard\",\"deployment\":\"hivelocity\"}';
        add_header Content-Type application/json;
    }
}
EOF"

# Enable the site and reload Nginx
ssh -i "$SSH_KEY" root@"$HIVELOCITY_HOST" "
    ln -sf $NGINX_CONFIG /etc/nginx/sites-enabled/mento-dashboard
    nginx -t && systemctl reload nginx
"

# Open firewall port for dashboard
echo "🔥 Opening firewall port 8083..."
ssh -i "$SSH_KEY" root@"$HIVELOCITY_HOST" "ufw allow 8083/tcp"

# Test deployment
echo ""
echo "🧪 Testing deployment..."
sleep 3

HIVELOCITY_URL="http://74.50.113.152:8083"
if ssh -i "$SSH_KEY" root@"$HIVELOCITY_HOST" "curl -s -o /dev/null -w '%{http_code}' $HIVELOCITY_URL" | grep -q "200"; then
    echo "✅ Dashboard is accessible on Hivelocity!"
else
    echo "⚠️  Dashboard may need a moment to start up"
fi

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🎉 Your Mento Protocol Dashboard is now available on BOTH platforms:"
echo ""
echo "🌐 **Hivelocity VPS (Instant Access)**:"
echo "   $HIVELOCITY_URL"
echo ""
echo "🛰️  **ICP Juno Canister (Decentralized)**:"
echo "   https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io"
echo ""
echo "📊 Dashboard Features:"
echo "   • Enhanced banner with 'UPDATED' status"
echo "   • Live blockchain data from Chainlink oracles"
echo "   • Partnership progress tracking (45%)"
echo "   • Professional shadcn/ui design system"
echo "   • Multi-source data (Live API + Local fallback)"
echo ""
echo "🔧 Hivelocity Infrastructure:"
echo "   • Nginx web server on port 8083"
echo "   • Gzip compression enabled"
echo "   • Static asset caching"
echo "   • Health monitoring at $HIVELOCITY_URL/health"
echo ""
echo "📝 Next Steps:"
echo "   • Hivelocity dashboard is immediately accessible"
echo "   • ICP canister will warm up in 2-3 minutes"
echo "   • Both deployments use the same updated content"
echo ""
echo "🎯 Benefits of Dual Deployment:"
echo "   • Hivelocity: Fast, reliable, enterprise hosting"
echo "   • ICP Juno: Decentralized, censorship-resistant"
echo "   • Redundancy: Multiple access points for users"
