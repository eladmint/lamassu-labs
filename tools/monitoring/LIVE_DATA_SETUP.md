# Live Aleo Dashboard Setup Guide

**Date**: June 23, 2025  
**Purpose**: Connect monitoring dashboard to live Aleo blockchain data

## 🚀 Quick Start

### Option 1: View Live Dashboard (Easiest)

```bash
# Start local server
python3 start-dashboard.py

# Dashboard will open automatically at:
# http://localhost:8080/dashboard-live.html
```

### Option 2: Open HTML Directly

Simply open `dashboard-live.html` in your browser. It will attempt to connect to Aleo APIs directly.

### Option 3: Deploy to ICP

```bash
# Update dist/index.html with live data code
cp dashboard-live.html dist/index.html

# Deploy to your satellite
./deploy-to-juno.sh
```

## 📊 Live Dashboard Features

### Real-Time Monitoring
- **Contract Health**: Live status updates every 60 seconds
- **Transaction Counts**: Actual blockchain data
- **Success Rates**: Calculated from real transactions
- **Activity Tracking**: Last transaction timestamps
- **Automatic Alerts**: Based on contract health

### Our Deployed Contracts
1. **hallucination_verifier.aleo**
   - TX: `at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt`
   - [View on AleoScan](https://testnet.aleoscan.io/program?id=hallucination_verifier.aleo)

2. **agent_registry_v2.aleo**
   - TX: `at1hyqa37uskww30l4trcwf6kmzfdhhszjv982cmtdsszy8ml7h959qgfq8h9`
   - [View on AleoScan](https://testnet.aleoscan.io/program?id=agent_registry_v2.aleo)

3. **trust_verifier_v2.aleo**
   - TX: `at1d3ukp45tuvkp0khq8tdt4qtd3y40lx5qz65kdg0yre3rq726k5xqvrc4dz`
   - [View on AleoScan](https://testnet.aleoscan.io/program?id=trust_verifier_v2.aleo)

## 🛠️ Technical Implementation

### Files Created

1. **`aleo-live-data.js`** - Client-side Aleo API integration
   - Automatic endpoint fallback
   - 30-second caching
   - Health status calculation
   - Alert generation

2. **`dashboard-live.html`** - Live monitoring dashboard
   - Real-time updates
   - Connection status indicator
   - Countdown to next refresh
   - Direct AleoScan links

3. **`aleo-data-service.js`** - Node.js backend service (optional)
   - Server-side caching
   - CORS-enabled API
   - Health endpoint

4. **`test-live-connection.html`** - Connection tester
   - Tests all endpoints
   - Shows API responses
   - Debugging tool

## 🔧 API Endpoints Used

### Primary Endpoints
```javascript
// Aleo official endpoints
https://api.explorer.provable.com/v1/testnet3
https://api.explorer.aleo.org/v1/testnet3

// API paths
/program/{contractId}           // Get program info
/program/{contractId}/transitions  // Get transactions
/transitions?program={contractId}  // Alternative format
```

### Data Flow
1. Dashboard loads → Connects to Aleo API
2. Fetches program data for each contract
3. Fetches recent transactions
4. Calculates health metrics
5. Updates UI with live data
6. Refreshes every 60 seconds

## 📈 Health Status Logic

```javascript
// Contract health calculation
if (no transactions) → "inactive"
else if (last activity > 48 hours) → "unhealthy"
else if (last activity > 24 hours) → "degraded"
else → "healthy"

// Success rate
successRate = (successful_transactions / total_transactions) * 100
```

## 🚨 Troubleshooting

### CORS Issues
If you see CORS errors:
1. Use the Python server: `python3 start-dashboard.py`
2. Or deploy to a web server
3. Or use the Node.js backend service

### SSL Certificate Errors
Some systems may have SSL issues with Aleo APIs:
1. Try opening dashboard in browser (browsers handle SSL better)
2. Or use a different endpoint
3. Or run behind a proxy

### No Data Showing
1. Check browser console for errors
2. Verify contracts exist on AleoScan
3. Try test-live-connection.html
4. API might be temporarily down

## 🔄 Updating the Dashboard

### To Add New Contracts
Edit `aleo-live-data.js`:
```javascript
this.contracts = [
    // ... existing contracts
    {
        id: 'new_contract.aleo',
        name: 'New Contract',
        deploymentTx: 'transaction_id'
    }
];
```

### To Change Refresh Interval
Edit `dashboard-live.html`:
```javascript
// Change from 60 seconds to 30 seconds
refreshInterval = setInterval(loadDashboard, 30000);
nextRefreshTime = Date.now() + 30000;
```

## 🌐 Deployment Options

### Deploy to ICP
```bash
# Copy live dashboard
cp dashboard-live.html dist/index.html
cp aleo-live-data.js dist/

# Deploy
./deploy-to-juno.sh
```

### Deploy to Vercel/Netlify
1. Copy `dashboard-live.html` and `aleo-live-data.js`
2. Push to GitHub
3. Connect to Vercel/Netlify
4. Deploy

### Self-Host
1. Copy files to web server
2. Ensure HTTPS is enabled
3. No backend required

## ✅ Verification

1. **Check Connection**: Open test-live-connection.html
2. **View Dashboard**: Open dashboard-live.html
3. **Verify Data**: Compare with AleoScan
4. **Monitor Updates**: Watch countdown timer

The dashboard is now connected to live Aleo blockchain data! 🎉