# OAuth Handler Deployment Request for Hivelocity

## Hi DevOps Team! 👋

We need to deploy a secure OAuth handler service on our Hivelocity infrastructure to handle Google authentication without exposing client secrets to the frontend.

## 🎯 **What We Need**

Deploy a Node.js OAuth handler service that:
- Exchanges Google OAuth codes for tokens server-side
- Returns secure JWT session tokens
- Protects the Google Client Secret from frontend exposure

## 📦 **Files to Deploy**

1. **Main handler**: `src/oauth-api-handler.js` - The OAuth logic
2. **Express server**: Create `oauth-server.js` with this content:

```javascript
const express = require('express');
const { createExpressHandler } = require('./oauth-api-handler.js');

const app = express();
app.use(express.json());
app.use('/api', createExpressHandler());

const PORT = process.env.PORT || 3001;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`OAuth server running on port ${PORT}`);
});
```

## 🔧 **Deployment Steps**

### 1. **Choose Server** (I recommend Staten Island since it has lower load):
- Staten Island: `74.50.113.152`
- Tampa: `23.92.65.243`

### 2. **Setup Service**:
```bash
# Create directory
mkdir -p /opt/oauth-handler
cd /opt/oauth-handler

# Copy files
# - oauth-api-handler.js
# - oauth-server.js

# Install dependencies
npm init -y
npm install express node-fetch jsonwebtoken cors
```

### 3. **Create systemd service** at `/etc/systemd/system/oauth-handler.service`:
```ini
[Unit]
Description=OAuth Handler Service for Mento Dashboard
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/oauth-handler
Environment="NODE_ENV=production"
Environment="PORT=3001"
Environment="GOOGLE_CLIENT_ID=867263134607-vkkd9avs6a75gmjpzja17a9a0bbdle1.apps.googleusercontent.com"
Environment="GOOGLE_CLIENT_SECRET=GOCSPX-<ACTUAL_SECRET_HERE>"
Environment="JWT_SECRET=<GENERATE_RANDOM_32_CHAR_STRING>"
Environment="ALLOWED_ORIGINS=https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io,http://localhost:3000"
ExecStart=/usr/bin/node oauth-server.js
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 4. **Start Service**:
```bash
systemctl daemon-reload
systemctl enable oauth-handler
systemctl start oauth-handler
systemctl status oauth-handler
```

### 5. **Open Firewall Port** (if needed):
```bash
ufw allow 3001/tcp
```

### 6. **Test the endpoint**:
```bash
curl http://localhost:3001/api/oauth/google/exchange \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"code":"test","redirectUri":"https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io/auth/callback/google"}'
```

## 🔐 **Security Requirements**

1. **GOOGLE_CLIENT_SECRET**: Get the actual secret from our secure credentials storage
2. **JWT_SECRET**: Generate using: `openssl rand -hex 32`
3. **Ensure HTTPS**: If possible, setup nginx reverse proxy with SSL

## 📊 **Expected Result**

Once deployed, the service will be available at:
- `http://74.50.113.152:3001/api/oauth/google/exchange`

The frontend will call this endpoint to securely exchange OAuth codes without exposing secrets.

## 🚨 **Important Notes**

- This service handles authentication, so uptime is critical
- Monitor logs for any errors: `journalctl -u oauth-handler -f`
- The service should auto-restart on failure
- Consider setting up monitoring/alerts

## 📞 **Questions?**

The implementation follows OAuth 2.0 best practices. The complete documentation is in `SECURE_OAUTH_SETUP.md`.

Let me know if you need any clarification or run into issues!

Thanks! 🙏
