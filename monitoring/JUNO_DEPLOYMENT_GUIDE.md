# Juno Deployment Guide for Lamassu Labs Monitoring Dashboard

## Overview

This guide explains how to deploy the Lamassu Labs contract monitoring dashboard to a Juno satellite on the Internet Computer Protocol (ICP).

**Satellite ID**: `bvxuo-uaaaa-aaaal-asgua-cai`  
**Live URL**: https://bvxuo-uaaaa-aaaal-asgua-cai.icp0.io

## Prerequisites

1. **Node.js** (v16 or higher)
2. **npm** or **yarn**
3. **Juno CLI** - Install with:
   ```bash
   npm install -g @junobuild/cli
   ```

## Quick Deployment

For a quick deployment, simply run:

```bash
./deploy-to-juno.sh
```

This script will:
1. Build the dashboard for Juno
2. Deploy to your satellite
3. Configure datastore collections
4. Set up proper CORS headers

## Manual Deployment Steps

### 1. Build the Dashboard

```bash
# Make the build script executable
chmod +x build-juno.sh

# Build the project
./build-juno.sh
```

This creates a `dist/` directory with:
- `index.html` - The Juno-adapted dashboard
- `package.json` - Dependencies configuration
- `import-map.json` - ES module imports

### 2. Configure Juno

The `juno.json` file contains:

```json
{
  "satellite": {
    "satelliteId": "bvxuo-uaaaa-aaaal-asgua-cai",
    "source": "./dist"
  },
  "hosting": {
    "headers": [
      {
        "source": "**/*",
        "headers": [
          {
            "key": "Access-Control-Allow-Origin",
            "value": "*"
          }
        ]
      }
    ]
  },
  "datastore": {
    "collections": [
      {
        "collection": "monitoring_data",
        "read": "public",
        "write": "managed"
      },
      {
        "collection": "contract_metrics",
        "read": "public",
        "write": "managed"
      },
      {
        "collection": "alerts",
        "read": "public",
        "write": "managed"
      }
    ]
  }
}
```

### 3. Deploy to Juno

```bash
cd dist
juno deploy
```

## Datastore Collections

The deployment creates three collections:

### 1. `monitoring_data`
Stores the main monitoring summary:
```javascript
{
  key: "current",
  data: {
    timestamp: "2025-06-22T10:00:00Z",
    network: "ICP",
    summary: {
      total_contracts: 3,
      healthy_contracts: 2,
      degraded_contracts: 1,
      unhealthy_contracts: 0
    }
  }
}
```

### 2. `contract_metrics`
Stores individual contract metrics:
```javascript
{
  key: "lamassu_registry",
  data: {
    program_id: "lamassu_registry",
    total_transactions: 256,
    successful_transactions: 248,
    failed_transactions: 8,
    average_execution_time: 145,
    last_activity: "2025-06-22T08:00:00Z",
    health_status: "healthy"
  }
}
```

### 3. `alerts`
Stores active alerts:
```javascript
{
  key: "alert_001",
  data: {
    severity: "warning",
    contract: "trust_verifier",
    message: "No activity for 8.0 hours",
    timestamp: "2025-06-22T10:00:00Z"
  }
}
```

## Updating Monitoring Data

### Using Juno SDK (JavaScript/TypeScript)

```javascript
import { initJuno, setDoc } from '@junobuild/core';

// Initialize Juno
const juno = await initJuno({
  satelliteId: 'bvxuo-uaaaa-aaaal-asgua-cai'
});

// Update monitoring data
await setDoc({
  collection: 'monitoring_data',
  key: 'current',
  doc: {
    data: {
      timestamp: new Date().toISOString(),
      network: 'ICP',
      summary: {
        total_contracts: 3,
        healthy_contracts: 2,
        degraded_contracts: 1,
        unhealthy_contracts: 0
      }
    }
  }
});
```

### Using Juno CLI

```bash
# Set a document
juno doc set \
  --collection monitoring_data \
  --key current \
  --data '{"timestamp":"2025-06-22T10:00:00Z","network":"ICP"}'
```

## Features

### Real-time Updates
- Dashboard auto-refreshes every 60 seconds
- Fetches latest data from Juno datastore
- Falls back to mock data if no data exists

### ICP Integration
- Native integration with Internet Computer
- Decentralized data storage
- Public read access for transparency
- Managed write access for security

### CORS Configuration
- Proper CORS headers for API access
- Allows integration with external services
- Supports cross-origin requests

## Security Considerations

1. **Write Access**: Set to "managed" - requires authentication
2. **Read Access**: Set to "public" for transparency
3. **Data Validation**: Implement validation in your update scripts
4. **Rate Limiting**: Consider implementing rate limits for updates

## Troubleshooting

### Juno CLI Not Found
```bash
npm install -g @junobuild/cli
```

### Authentication Issues
```bash
juno login
```

### Deployment Fails
1. Check your internet connection
2. Verify satellite ID is correct
3. Ensure you have proper permissions

### Dashboard Not Loading
1. Check browser console for errors
2. Verify CORS headers are set correctly
3. Ensure Juno SDK is loading properly

## Next Steps

1. **Integrate with Backend**: Connect your monitoring backend to push data to Juno
2. **Set Up Automation**: Create cron jobs to update monitoring data
3. **Add Authentication**: Implement user authentication for write operations
4. **Enhance Visualizations**: Add charts and graphs for better insights

## Resources

- [Juno Documentation](https://juno.build/docs)
- [Internet Computer Documentation](https://internetcomputer.org/docs)
- [Juno SDK Reference](https://juno.build/docs/developers/sdk)

## Support

For issues specific to the monitoring dashboard:
- Check the deployment logs: `juno logs`
- Review the browser console for client-side errors
- Verify datastore collections are created correctly

---

**Note**: This dashboard is designed to work with the Lamassu Labs TrustWrapper infrastructure for monitoring AI agent contracts on various blockchains through ICP.