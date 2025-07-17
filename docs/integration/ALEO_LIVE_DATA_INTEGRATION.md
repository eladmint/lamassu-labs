# Connecting Dashboard to Live Aleo Blockchain Data

**Date**: June 23, 2025  
**Purpose**: Guide for integrating monitoring dashboard with live Aleo blockchain data  
**Network**: Aleo testnet3

## Overview

This guide explains how to connect the TrustWrapper monitoring dashboard to live Aleo blockchain data for real-time contract monitoring.

## 🔗 Deployed Contracts

### Live Contracts on Aleo Testnet3
1. **hallucination_verifier.aleo**
   - Address: `hallucination_verifier.aleo`
   - Explorer: https://testnet.aleoscan.io/program?id=hallucination_verifier.aleo
   - Purpose: ZK-verified AI hallucination detection

2. **agent_registry_v2.aleo**
   - Address: `agent_registry_v2.aleo`
   - Explorer: https://testnet.aleoscan.io/program?id=agent_registry_v2.aleo
   - Purpose: AI agent registration and performance tracking

3. **trust_verifier_v2.aleo**
   - Address: `trust_verifier_v2.aleo`
   - Explorer: https://testnet.aleoscan.io/program?id=trust_verifier_v2.aleo
   - Purpose: AI execution verification and trust scoring

## 🛠️ Integration Methods

### Method 1: Aleo API Integration (Recommended)

```javascript
// contract_monitor.js
const ALEO_API_ENDPOINTS = {
  primary: 'https://api.explorer.provable.com/v1',
  secondary: 'https://api.explorer.aleo.org/v1',
  testnet: 'https://api.explorer.aleo.org/v1/testnet3'
};

const CONTRACTS = [
  'hallucination_verifier.aleo',
  'agent_registry_v2.aleo', 
  'trust_verifier_v2.aleo'
];

async function fetchContractData(contractId) {
  const endpoint = `${ALEO_API_ENDPOINTS.primary}/testnet3/program/${contractId}`;
  
  try {
    const response = await fetch(endpoint);
    const data = await response.json();
    
    return {
      contractId,
      status: 'healthy',
      lastActivity: data.last_transaction_timestamp,
      transactionCount: data.transaction_count,
      executionTime: data.average_execution_time
    };
  } catch (error) {
    console.error(`Error fetching ${contractId}:`, error);
    return {
      contractId,
      status: 'error',
      error: error.message
    };
  }
}

// Fetch all contracts
async function fetchAllContracts() {
  const promises = CONTRACTS.map(fetchContractData);
  return await Promise.all(promises);
}
```

### Method 2: Direct RPC Integration

```javascript
// aleo_rpc_client.js
const AleoRPC = {
  endpoint: 'https://api.explorer.provable.com/v1/testnet3/rpc',
  
  async getProgram(programId) {
    const response = await fetch(this.endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        method: 'getProgram',
        params: [programId],
        id: 1
      })
    });
    
    return await response.json();
  },
  
  async getTransaction(txId) {
    const response = await fetch(this.endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        method: 'getTransaction',
        params: [txId],
        id: 1
      })
    });
    
    return await response.json();
  },
  
  async getProgramTransactions(programId, page = 1, limit = 10) {
    const response = await fetch(this.endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        method: 'getProgramTransactions',
        params: [programId, page, limit],
        id: 1
      })
    });
    
    return await response.json();
  }
};
```

### Method 3: WebSocket Real-time Updates

```javascript
// aleo_websocket.js
class AleoWebSocket {
  constructor() {
    this.ws = null;
    this.contracts = new Map();
  }
  
  connect() {
    this.ws = new WebSocket('wss://api.explorer.aleo.org/v1/testnet3/ws');
    
    this.ws.onopen = () => {
      console.log('Connected to Aleo WebSocket');
      this.subscribeToContracts();
    };
    
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleUpdate(data);
    };
  }
  
  subscribeToContracts() {
    const contracts = [
      'hallucination_verifier.aleo',
      'agent_registry_v2.aleo',
      'trust_verifier_v2.aleo'
    ];
    
    contracts.forEach(contract => {
      this.ws.send(JSON.stringify({
        action: 'subscribe',
        type: 'program',
        id: contract
      }));
    });
  }
  
  handleUpdate(data) {
    if (data.type === 'transaction' && data.program) {
      this.updateContractMetrics(data.program, data);
    }
  }
  
  updateContractMetrics(contractId, txData) {
    const metrics = this.contracts.get(contractId) || {
      transactionCount: 0,
      lastActivity: null,
      avgExecutionTime: 0
    };
    
    metrics.transactionCount++;
    metrics.lastActivity = new Date();
    metrics.avgExecutionTime = txData.execution_time;
    
    this.contracts.set(contractId, metrics);
    this.notifyDashboard(contractId, metrics);
  }
  
  notifyDashboard(contractId, metrics) {
    // Emit event or update UI
    window.dispatchEvent(new CustomEvent('contractUpdate', {
      detail: { contractId, metrics }
    }));
  }
}
```

## 📊 Dashboard Integration

### Update `dashboard.html` to use live data:

```javascript
// dashboard.js
class AleoDashboard {
  constructor() {
    this.contracts = new Map();
    this.updateInterval = 30000; // 30 seconds
    this.init();
  }
  
  async init() {
    // Initial load
    await this.loadContractData();
    
    // Set up periodic updates
    setInterval(() => this.loadContractData(), this.updateInterval);
    
    // Optional: Set up WebSocket for real-time updates
    this.setupWebSocket();
  }
  
  async loadContractData() {
    const contracts = [
      'hallucination_verifier.aleo',
      'agent_registry_v2.aleo',
      'trust_verifier_v2.aleo'
    ];
    
    for (const contractId of contracts) {
      try {
        const data = await this.fetchContractMetrics(contractId);
        this.updateUI(contractId, data);
      } catch (error) {
        console.error(`Error loading ${contractId}:`, error);
        this.updateUI(contractId, { status: 'error' });
      }
    }
  }
  
  async fetchContractMetrics(contractId) {
    // Fetch from Aleo API
    const response = await fetch(
      `https://api.explorer.provable.com/v1/testnet3/program/${contractId}/metrics`
    );
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    // Calculate health status based on metrics
    const health = this.calculateHealth(data);
    
    return {
      status: health.status,
      transactions: data.transaction_count || 0,
      lastActivity: data.last_transaction_timestamp,
      avgExecutionTime: data.average_execution_time || 0,
      successRate: data.success_rate || 100
    };
  }
  
  calculateHealth(data) {
    // Health calculation logic
    if (!data.last_transaction_timestamp) {
      return { status: 'inactive', color: 'gray' };
    }
    
    const lastActivity = new Date(data.last_transaction_timestamp);
    const hoursSinceActivity = (Date.now() - lastActivity) / (1000 * 60 * 60);
    
    if (hoursSinceActivity > 24) {
      return { status: 'degraded', color: 'yellow' };
    }
    
    if (data.success_rate < 90) {
      return { status: 'unhealthy', color: 'red' };
    }
    
    return { status: 'healthy', color: 'green' };
  }
  
  updateUI(contractId, data) {
    // Update dashboard UI elements
    const element = document.getElementById(`contract-${contractId}`);
    if (element) {
      element.querySelector('.status').textContent = data.status;
      element.querySelector('.status').className = `status ${data.status}`;
      element.querySelector('.transactions').textContent = data.transactions || '0';
      element.querySelector('.last-activity').textContent = 
        data.lastActivity ? new Date(data.lastActivity).toLocaleString() : 'Never';
      element.querySelector('.execution-time').textContent = 
        data.avgExecutionTime ? `${data.avgExecutionTime}ms` : 'N/A';
    }
  }
  
  setupWebSocket() {
    const ws = new AleoWebSocket();
    ws.connect();
    
    // Listen for updates
    window.addEventListener('contractUpdate', (event) => {
      const { contractId, metrics } = event.detail;
      this.updateUI(contractId, metrics);
    });
  }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
  new AleoDashboard();
});
```

## 🔧 Implementation Steps

### 1. Update Contract Monitor Backend

```python
# contract_monitor.py
import aiohttp
import asyncio
from datetime import datetime

class AleoContractMonitor:
    def __init__(self):
        self.api_endpoint = "https://api.explorer.provable.com/v1/testnet3"
        self.contracts = [
            "hallucination_verifier.aleo",
            "agent_registry_v2.aleo",
            "trust_verifier_v2.aleo"
        ]
    
    async def fetch_contract_data(self, session, contract_id):
        """Fetch live data for a specific contract"""
        try:
            # Get program info
            async with session.get(f"{self.api_endpoint}/program/{contract_id}") as resp:
                program_data = await resp.json()
            
            # Get recent transactions
            async with session.get(
                f"{self.api_endpoint}/transactions?program={contract_id}&limit=10"
            ) as resp:
                tx_data = await resp.json()
            
            return {
                "contract_id": contract_id,
                "status": "healthy" if tx_data else "inactive",
                "transaction_count": len(tx_data.get("transactions", [])),
                "last_activity": tx_data.get("transactions", [{}])[0].get("timestamp"),
                "metrics": self.calculate_metrics(tx_data)
            }
        except Exception as e:
            return {
                "contract_id": contract_id,
                "status": "error",
                "error": str(e)
            }
    
    def calculate_metrics(self, tx_data):
        """Calculate performance metrics from transaction data"""
        transactions = tx_data.get("transactions", [])
        
        if not transactions:
            return {
                "avg_execution_time": 0,
                "success_rate": 0,
                "daily_volume": 0
            }
        
        # Calculate metrics
        execution_times = [tx.get("execution_time", 0) for tx in transactions]
        successful = sum(1 for tx in transactions if tx.get("status") == "success")
        
        return {
            "avg_execution_time": sum(execution_times) / len(execution_times),
            "success_rate": (successful / len(transactions)) * 100,
            "daily_volume": len([
                tx for tx in transactions 
                if datetime.fromtimestamp(tx.get("timestamp", 0)).date() == datetime.now().date()
            ])
        }
    
    async def monitor_all_contracts(self):
        """Monitor all contracts and return aggregated data"""
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch_contract_data(session, contract) 
                for contract in self.contracts
            ]
            results = await asyncio.gather(*tasks)
            
        return {
            "timestamp": datetime.now().isoformat(),
            "contracts": results,
            "summary": self.generate_summary(results)
        }
    
    def generate_summary(self, results):
        """Generate summary statistics"""
        healthy = sum(1 for r in results if r.get("status") == "healthy")
        total = len(results)
        
        return {
            "total_contracts": total,
            "healthy_contracts": healthy,
            "health_percentage": (healthy / total) * 100,
            "last_update": datetime.now().isoformat()
        }
```

### 2. Update Dashboard HTML

```html
<!-- dashboard.html -->
<div id="contract-dashboard">
  <div class="contract-card" id="contract-hallucination_verifier.aleo">
    <h3>Hallucination Verifier</h3>
    <div class="status">Loading...</div>
    <div class="metrics">
      <span class="transactions">0</span> transactions
      <span class="last-activity">Never</span>
      <span class="execution-time">N/A</span>
    </div>
  </div>
  
  <div class="contract-card" id="contract-agent_registry_v2.aleo">
    <h3>Agent Registry v2</h3>
    <div class="status">Loading...</div>
    <div class="metrics">
      <span class="transactions">0</span> transactions
      <span class="last-activity">Never</span>
      <span class="execution-time">N/A</span>
    </div>
  </div>
  
  <div class="contract-card" id="contract-trust_verifier_v2.aleo">
    <h3>Trust Verifier v2</h3>
    <div class="status">Loading...</div>
    <div class="metrics">
      <span class="transactions">0</span> transactions
      <span class="last-activity">Never</span>
      <span class="execution-time">N/A</span>
    </div>
  </div>
</div>

<script src="aleo-dashboard.js"></script>
```

## 🔐 Security Considerations

1. **API Key Management**: Store API keys securely, never in frontend code
2. **Rate Limiting**: Implement rate limiting to avoid API throttling
3. **Error Handling**: Graceful fallback for API failures
4. **Data Validation**: Validate all data from external APIs
5. **CORS**: Configure proper CORS headers for API access

## 🧪 Testing Live Integration

```javascript
// test_aleo_integration.js
async function testAleoIntegration() {
  console.log('Testing Aleo API integration...');
  
  const contracts = [
    'hallucination_verifier.aleo',
    'agent_registry_v2.aleo',
    'trust_verifier_v2.aleo'
  ];
  
  for (const contract of contracts) {
    try {
      const response = await fetch(
        `https://api.explorer.provable.com/v1/testnet3/program/${contract}`
      );
      
      if (response.ok) {
        const data = await response.json();
        console.log(`✅ ${contract}: Connected successfully`);
        console.log(`   Transactions: ${data.transaction_count || 0}`);
      } else {
        console.log(`❌ ${contract}: HTTP ${response.status}`);
      }
    } catch (error) {
      console.log(`❌ ${contract}: ${error.message}`);
    }
  }
}

// Run test
testAleoIntegration();
```

## 📊 Monitoring Best Practices

1. **Update Frequency**: Poll API every 30-60 seconds to avoid rate limits
2. **Caching**: Cache results for 30 seconds minimum
3. **Batch Requests**: Fetch multiple contracts in parallel
4. **Error Recovery**: Implement exponential backoff for failed requests
5. **Metrics Storage**: Store historical data for trend analysis

## 🚀 Deployment Checklist

- [ ] Update all dashboard files with correct contract names
- [ ] Configure API endpoints in environment variables
- [ ] Set up monitoring backend with Aleo API integration
- [ ] Test live data fetching for all contracts
- [ ] Implement error handling and fallbacks
- [ ] Set up alerts for contract health issues
- [ ] Deploy updated dashboard to production
- [ ] Monitor API usage and performance

## 📚 Resources

- **Aleo Explorer API**: https://api.explorer.provable.com/docs
- **AleoScan**: https://testnet.aleoscan.io/
- **Aleo Developer Docs**: https://developer.aleo.org/
- **Contract Addresses**: See deployed contracts section above

---

**Note**: This integration connects to live Aleo testnet3 data. Ensure proper error handling and rate limiting to maintain reliable dashboard operation.