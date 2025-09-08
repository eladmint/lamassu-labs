# TrustWrapper Eliza Plugin Deployment Request for OpenXAI

## Hi DevOps Team! 👋

Great work on Sprint 9 completion! 🎉 OAuth service on port 3001 is perfect timing.

We need to deploy our TrustWrapper Eliza plugin on OpenXAI infrastructure for testing before NPM publication. This builds on your existing infrastructure work.

## 🎯 **What We're Deploying**

**TrustWrapper Eliza Verification Plugin** - An AI agent plugin that provides:
- Trading decision verification
- AI skill performance validation
- Compliance report generation
- Real-time blockchain data integration

## 📦 **Plugin Location**

```
/Users/eladm/Projects/token/tokenhunter/trustwrapper-testing/
├── src/
│   ├── index.ts                 # Main plugin entry
│   ├── actions/                 # Verification actions
│   ├── providers/               # Data providers
│   ├── evaluators/              # Response evaluators
│   └── services/                # Core services
├── package.json
├── tsconfig.json
└── README.md
```

## 🚀 **Deployment Steps**

### 1. **Deploy to OpenXAI Infrastructure**

Since we already have OpenXAI integration on Tampa VPS (23.92.65.243) and OAuth service on port 3001, we can integrate with existing infrastructure:

```bash
# SSH into Tampa OpenXAI server
ssh root@23.92.65.243  # Password: YS6OaT2uruHa

# Create plugin directory
mkdir -p /opt/trustwrapper-eliza-plugin
cd /opt/trustwrapper-eliza-plugin

# Copy plugin files
# Copy entire trustwrapper-testing directory content

# Install dependencies
npm install
npm run build
```

### 2. **Create Test Eliza Agent**

Create `/opt/eliza-test-agent/index.js`:

```javascript
const { ElizaAgent } = require('@ai16z/eliza-core');
const { trustWrapperPlugin } = require('../trustwrapper-eliza-plugin/dist');

// Test agent configuration
const testAgent = new ElizaAgent({
    name: "TrustWrapperTestBot",
    plugins: [trustWrapperPlugin],
    settings: {
        trustwrapper: {
            apiKey: process.env.TRUSTWRAPPER_API_KEY || "tw_test_key",
            baseUrl: "https://api.trustwrapper.com",
            primaryChain: "ethereum"
        }
    }
});

// Start agent
async function start() {
    try {
        await testAgent.start();
        console.log('TrustWrapper Eliza Plugin Test Agent Started!');

        // Test verification action
        const result = await testAgent.execute({
            action: "VERIFY_TRADING_DECISION",
            params: {
                token: "ETH",
                action: "BUY",
                amount: 1000,
                reason: "Testing plugin deployment"
            }
        });

        console.log('Test Result:', result);
    } catch (error) {
        console.error('Test failed:', error);
    }
}

start();
```

### 3. **Create systemd Service**

Create `/etc/systemd/system/eliza-test-agent.service`:

```ini
[Unit]
Description=TrustWrapper Eliza Plugin Test Agent
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/eliza-test-agent
Environment="NODE_ENV=production"
Environment="TRUSTWRAPPER_API_KEY=tw_test_key"
ExecStart=/usr/bin/node index.js
StandardOutput=journal
StandardError=journal
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 4. **Run Tests**

```bash
# Start the test agent
systemctl daemon-reload
systemctl start eliza-test-agent
systemctl status eliza-test-agent

# Check logs
journalctl -u eliza-test-agent -f

# Run integration tests
cd /opt/trustwrapper-eliza-plugin
npm test
```

### 5. **Create HTTP Test Endpoint**

Create `/opt/eliza-test-api/server.js`:

```javascript
const express = require('express');
const { trustWrapperPlugin } = require('../trustwrapper-eliza-plugin/dist');

const app = express();
app.use(express.json());

// Test endpoint for plugin actions
app.post('/test/verify-trade', async (req, res) => {
    try {
        const { token, action, amount } = req.body;

        // Simulate plugin execution
        const result = await trustWrapperPlugin.actions[0].handler(
            { /* mock runtime */ },
            { content: { token, action, amount } }
        );

        res.json({ success: true, result });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.listen(3002, () => {
    console.log('Eliza Plugin Test API running on port 3002');
    console.log('Integrating with existing OAuth service on port 3001');
});
```

## 🧪 **Testing Plan**

### 1. **Unit Tests**
```bash
cd /opt/trustwrapper-eliza-plugin
npm test
```

### 2. **Integration Tests**
```bash
# Test trading verification
curl -X POST http://localhost:3002/test/verify-trade \
  -H "Content-Type: application/json" \
  -d '{"token":"ETH","action":"BUY","amount":1000}'
```

### 3. **Live Agent Test**
- Deploy test agent with real Eliza framework
- Test all three actions (trading, skill, compliance)
- Monitor performance and errors

## 📊 **Success Criteria**

- [ ] Plugin builds without errors
- [ ] All unit tests pass
- [ ] Integration with Eliza framework works
- [ ] API endpoints respond correctly
- [ ] No memory leaks after 24h running
- [ ] Performance metrics acceptable (<100ms response time)

## 🚀 **After Successful Testing**

Once tests pass on OpenXAI:

1. **Prepare for NPM**:
```bash
cd /opt/trustwrapper-eliza-plugin
npm version 1.0.0
npm pack
# This creates trustwrapper-eliza-verification-plugin-1.0.0.tgz
```

2. **Test NPM Package**:
```bash
# In a test directory
npm install ../trustwrapper-eliza-plugin/trustwrapper-eliza-verification-plugin-1.0.0.tgz
# Verify it works
```

3. **Publish to NPM** (after approval):
```bash
npm login
npm publish --access public
```

## 📋 **Deployment Checklist**

- [ ] Copy plugin files to Tampa OpenXAI server
- [ ] Install dependencies and build
- [ ] Create test agent
- [ ] Run unit tests
- [ ] Test integration with Eliza
- [ ] Monitor for 24 hours
- [ ] Prepare NPM package
- [ ] Get approval for NPM publication

## 🔐 **Security Notes**

- Use test API keys for initial testing
- Don't expose real TrustWrapper API keys in logs
- Ensure proper error handling
- Monitor resource usage

## 📞 **Questions?**

The plugin integrates with the Eliza AI agent framework to provide blockchain verification services. Full documentation is in the `trustwrapper-testing/README.md` file.

Let me know if you need any clarification or run into issues during deployment!

Thanks! 🙏

---

**Priority**: High - Strategic partnership with Senpi AI depends on this
**Timeline**: ASAP for testing, NPM publication after successful tests
