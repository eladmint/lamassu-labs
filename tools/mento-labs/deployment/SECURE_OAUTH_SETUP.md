# Secure OAuth Setup Guide

This guide explains how to deploy the secure OAuth handler for production use with Google authentication.

## 🔐 Security Overview

The secure implementation:
- Never exposes the Google Client Secret to the frontend
- Exchanges OAuth codes server-side
- Returns secure session tokens (JWT) instead of raw access tokens
- Validates redirect URIs to prevent redirect attacks
- Implements CORS protection

## 🚀 Deployment Options

### Option 1: Hivelocity VPS (Recommended - Existing Infrastructure)

Since we already have Hivelocity VPS infrastructure, we can deploy the OAuth handler there:

1. **SSH into Hivelocity server**:
```bash
ssh -i ~/.ssh/hivelocity_key root@74.50.113.152  # Staten Island
# or
ssh root@23.92.65.243  # Tampa (Password: YS6OaT2uruHa)
```

2. **Create OAuth service directory**:
```bash
mkdir -p /opt/oauth-handler
cd /opt/oauth-handler
```

3. **Copy OAuth handler files**:
```bash
# Copy oauth-api-handler.js to server
# Install dependencies
npm init -y
npm install node-fetch jsonwebtoken express cors
```

4. **Create systemd service** `/etc/systemd/system/oauth-handler.service`:
```ini
[Unit]
Description=OAuth Handler Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/oauth-handler
Environment="NODE_ENV=production"
Environment="GOOGLE_CLIENT_ID=867263134607-vkkd9avs6a75gmjpzja17a9a0bbdle1.apps.googleusercontent.com"
Environment="GOOGLE_CLIENT_SECRET=<actual-secret-here>"
Environment="JWT_SECRET=<generate-32-char-random-string>"
Environment="ALLOWED_ORIGINS=https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io"
ExecStart=/usr/bin/node oauth-server.js
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

5. **Create Express server** `/opt/oauth-handler/oauth-server.js`:
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

6. **Start the service**:
```bash
systemctl daemon-reload
systemctl enable oauth-handler
systemctl start oauth-handler
systemctl status oauth-handler
```

7. **Configure nginx proxy** (if nginx is installed):
```nginx
location /api/oauth/ {
    proxy_pass http://localhost:3001/api/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_cache_bypass $http_upgrade;
}
```

8. **Update frontend endpoint**:
```javascript
getOAuthEndpoint() {
    return 'http://74.50.113.152:3001/api/oauth/google/exchange';
    // or with nginx: 'http://74.50.113.152/api/oauth/google/exchange'
}
```

### Option 2: Vercel (Quick Serverless Setup)

1. **Create a Vercel account** at https://vercel.com

2. **Create `api/oauth.js`** in your project:
```javascript
import handler from '../src/oauth-api-handler.js';
export default handler;
```

3. **Set environment variables** in Vercel dashboard:
```
GOOGLE_CLIENT_ID=867263134607-vkkd9avs6a75gmjpzja17a9a0bbdle1.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=<your-actual-secret>
JWT_SECRET=<generate-random-32-char-string>
ALLOWED_ORIGINS=https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io
```

4. **Deploy** and get your endpoint URL (e.g., `https://your-app.vercel.app/api/oauth`)

5. **Update** `mento_auth_integration.js`:
```javascript
getOAuthEndpoint() {
    return 'https://your-app.vercel.app/api/oauth';
}
```

### Option 2: Netlify Functions

1. **Create** `netlify/functions/oauth.js`:
```javascript
import handler from '../../src/oauth-api-handler.js';
exports.handler = async (event, context) => {
    const req = {
        method: event.httpMethod,
        headers: event.headers,
        body: JSON.parse(event.body)
    };
    const res = {
        status: (code) => ({
            json: (data) => ({
                statusCode: code,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
        }),
        setHeader: () => {}
    };
    return await handler(req, res);
};
```

2. **Deploy** and set environment variables in Netlify dashboard

### Option 3: ICP Canister (Fully Decentralized)

1. **Deploy the Motoko canister**:
```bash
dfx deploy oauth_handler --network ic
```

2. **Initialize admin and set secret**:
```bash
dfx canister --network ic call oauth_handler initAdmin
dfx canister --network ic call oauth_handler setClientSecret '("YOUR_SECRET")'
```

3. **Update** the secure callback to use canister

### Option 4: Express.js Backend

1. **Create** `server.js`:
```javascript
import express from 'express';
import { createExpressHandler } from './src/oauth-api-handler.js';

const app = express();
app.use(express.json());
app.use('/api', createExpressHandler());

app.listen(3001, () => {
    console.log('OAuth server running on port 3001');
});
```

2. **Run** with environment variables:
```bash
GOOGLE_CLIENT_SECRET=your-secret JWT_SECRET=your-jwt-secret node server.js
```

## 🔧 Google Cloud Console Setup

1. **Add authorized redirect URIs**:
   - `https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io/auth/callback/google`
   - `http://localhost:3000/auth/callback/google` (for development)

2. **Add authorized JavaScript origins**:
   - `https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io`
   - `http://localhost:3000` (for development)

## 🧪 Testing the Secure Flow

1. **Local Development**:
   - Run your OAuth backend on port 3001
   - Update `getOAuthEndpoint()` to point to `http://localhost:3001/api/oauth/google/exchange`
   - Test the authentication flow

2. **Production**:
   - Deploy your OAuth handler
   - Update the endpoint URL
   - Test with real Google accounts

## 📝 Implementation Checklist

- [ ] Deploy OAuth handler to chosen platform
- [ ] Set all required environment variables
- [ ] Update `getOAuthEndpoint()` with your endpoint URL
- [ ] Test authentication flow end-to-end
- [ ] Monitor error logs for any issues
- [ ] Set up proper CORS headers
- [ ] Implement rate limiting (optional but recommended)
- [ ] Add session management/cleanup

## 🚨 Security Best Practices

1. **Never commit secrets** to version control
2. **Use environment variables** for all sensitive data
3. **Implement rate limiting** to prevent abuse
4. **Log authentication attempts** for security monitoring
5. **Regularly rotate** your JWT secret
6. **Use HTTPS** for all endpoints
7. **Validate all inputs** server-side

## 🎯 Next Steps

1. Choose your deployment platform
2. Deploy the OAuth handler
3. Update the frontend with your endpoint
4. Test thoroughly
5. Monitor for any issues

For questions or issues, refer to the platform-specific documentation or open an issue in the repository.
