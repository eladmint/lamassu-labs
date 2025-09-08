# Chainlink Live Data Integration Guide

## 🎯 Quick Start: Making the Dashboard Show Live Data

### Option 1: Quick Test (Recommended)
1. **Deploy the live API** (on Hivelocity VPS):
   ```bash
   cd partnerships/mento-labs/backend
   ./deploy_live_api.sh
   ```

2. **Update dashboard to use new endpoint**:
   - Change API URL from `:8086` to `:8087`
   - The dashboard will automatically show live data
   - Look for `is_live_data: true` in the response

### Option 2: Full Integration
1. **Get actual Chainlink contract addresses**:
   - Visit: https://data.chain.link
   - Select "Celo" network
   - Find addresses for: CELO/USD, ETH/USD, EUR/USD, etc.

2. **Update the contract addresses** in `chainlink_oracle_service.js`:
   ```javascript
   const CHAINLINK_FEEDS = {
     'CELO/USD': '0x[ACTUAL_ADDRESS_HERE]',
     'ETH/USD': '0x[ACTUAL_ADDRESS_HERE]',
     // ... add all needed feeds
   };
   ```

3. **Install Web3 dependencies** (for real blockchain reads):
   ```bash
   npm install web3 @chainlink/contracts
   ```

4. **Deploy to production**

## 📊 What You Get with Live Data

### Current (Demo Data):
- Static values from JSON file
- Updates every 30 seconds (but same data)
- Good for demos but not "real"

### With Chainlink Integration:
- **Real-time prices** from the same oracles Mento uses
- **Live collateralization ratios** based on actual market prices
- **Dynamic health scores** that change with market conditions
- **Automatic alerts** when ratios drop below thresholds
- **"Live Data" badge** on dashboard showing data source

## 🔗 Free Chainlink Access Details

### How It Works:
```javascript
// No API key needed - just read from blockchain!
const provider = new ethers.providers.JsonRpcProvider("https://rpc.ankr.com/celo");
const priceFeed = new ethers.Contract(feedAddress, aggregatorABI, provider);
const [roundId, price] = await priceFeed.latestRoundData();
```

### Best Free RPCs (tested):
1. **Ankr**: `https://rpc.ankr.com/celo` (61ms latency)
2. **ENVIO**: `https://celo.rpc.hypersync.xyz/` (125ms)
3. **dRPC**: `https://celo.drpc.org/` (150ms)

### Cost:
- **Chainlink**: FREE (just read contracts)
- **RPC calls**: FREE up to reasonable limits
- **Only cost**: Gas for contract reads (~$0.0001 per read)

## 🚀 Implementation Steps

### Backend (30 minutes):
1. Install dependencies: `npm install ethers node-cache`
2. Deploy `chainlink_oracle_service.js`
3. Update API to use oracle service
4. Test with: `node chainlink_live_demo.js`

### Frontend (10 minutes):
1. Change API endpoint to `:8087`
2. Add "Live Data" indicator when `is_live_data: true`
3. Show last oracle update timestamp
4. That's it! Auto-refresh already works

## 📈 Business Impact

### For Partnership Demo:
- **Before**: "We built a monitoring dashboard with realistic data"
- **After**: "We built a LIVE monitoring dashboard using YOUR EXACT ORACLES"

### Technical Advantages:
- Same data source as Mento Protocol
- Real-time updates (not hourly cached)
- No vendor lock-in or API keys
- Demonstrates deep blockchain integration

## 🧪 Testing Commands

### Test Chainlink connection:
```bash
node chainlink_live_demo.js
```

### Test live API:
```bash
# Start API
python3 mento_api_live.py

# Test endpoint
curl http://localhost:8087/api/mento/live-dashboard-data | jq
```

### Deploy to Hivelocity:
```bash
./deploy_live_api.sh
```

## 🎯 Next Steps

1. **Get real Chainlink addresses** from https://data.chain.link
2. **Run test locally** to verify everything works
3. **Deploy to production** (port 8087 for testing)
4. **Update dashboard** to use live endpoint
5. **Demo to Mento Labs** with truly live data!

## 💡 Pro Tips

- Cache oracle data for 30-60 seconds to reduce RPC calls
- Use multiple RPC endpoints for redundancy
- Show confidence indicators when multiple oracles agree
- Add historical charts showing price movements
- Implement alerts for significant changes

## 🔗 Resources

- **Chainlink Docs**: https://docs.chain.link/data-feeds
- **Celo RPCs**: https://docs.celo.org/network
- **Our Research**: `/partnerships/mento-labs/research/CHAINLINK_ORACLE_INTEGRATION_RESEARCH.md`
- **Mento Adoption**: https://www.mento.org/blog/mento-adopts-the-chainlink-data-standard-to-power-decentralized-stablecoins
